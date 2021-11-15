from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.config import SSH_PORT
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, SSHException
from io import StringIO


class SSH(object):
    def __init__(self,hostname, port=SSH_PORT, username='root', pkey=None, password=None, connect_timeout=30):
        if pkey is None and password is None:
            raise SSHException('私钥或者密码必须有一个不为空')

        self.client = None

        self.arguments = {
            'hostname': hostname,
            'port'    : port,
            'username': username,
            'password': password,
            'pkey'    : RSAKey.from_private_key(StringIO(pkey)) if isinstance(pkey, str) else pkey,
            'timeout' : connect_timeout,
        }

        # print(self.arguments)

    @staticmethod
    def generate_key():
        # 生成公私钥键值对
        key_obj = StringIO()
        key = RSAKey.generate(2048) # 生成长度为2024的秘钥对
        key.write_private_key(key_obj)
        # 返回值是一个元祖，两个成员分别是私钥和公钥
        return key_obj.getvalue(), 'ssh-rsa ' + key.get_base64()

    # 将公钥上传到对应主机
    def add_public_key(self, public_key):
        # 700 是文档拥有可读可写可执行，同一组用户或者其他用户都不具有操作权限
        # 600 是文件拥有者可读可写，不可执行，同一组用户或者其他用户都不具有操作权限
        command = f'mkdir -p -m 700 ~/.ssh && \
        echo {public_key!r} >> ~/.ssh/authorized_keys && \
        chmod 600 ~/.ssh/authorized_keys'
        code, out = self.exec_command(command)
        if code != 0:
            raise Exception(f'添加公钥失败: {out}')

    def exec_command(self, command, timeout=1800, environment=None):
        # 设置执行指令过程，一旦遇到错误/异常，则直接退出操作，不再继续执行。
        command = 'set -e\n' + command
        with self as cli:
            chan = cli.get_transport().open_session()
            chan.settimeout(timeout)
            chan.set_combine_stderr(True)  # 正确和错误输出都在一个管道对象里面输出出来
            # if environment:
            #     str_env = ' '.join(f"{k}='{v}'" for k, v in environment.items())
            #     command = f'export {str_env} && {command}'
            chan.exec_command(command)
            stdout = chan.makefile("rb", -1)
            return chan.recv_exit_status(), self._decode(stdout.read())

    def _decode(self, out: bytes):
        # 解码方法[把bytes类型数据转换成普通字符]
        try:
            return out.decode()
        except UnicodeDecodeError:
            return out.decode('GBK')

    # 检测连接并获取连接
    def ping(self):
        """ping远程主机，连接成功则返回True"""
        with self: # self 实际上就是 self.get_client() 的 返回值
            return True

    def put_file_by_fl(self, fl, remote_path, callback=None):
        """
        上传文件到远程主机
        fl:文件对象(文件句柄或类文件句柄)
        remote_path: 远程主机中存储当前文件的路径
        callback: 上传文件以后的回调方法
        """
        with self as cli:
            sftp = cli.open_sftp()
            # 这里之所以上传的是文件对象的主要原因是我们api服务器上传到远程主机的文件，往往来自于客户端上传过来的。
            # 所以我们api服务器中得到的本来就是一个文件对象，因此没必要保存到api服务器，直接转发给远程主机即可
            sftp.putfo(fl, remote_path, callback=callback)

    # 从远程主机下载文件到本地
    def download_file(self, local_path, remote_path):
        """
        local_path: 指定保存下载文件的本地地址
        remote_path: 要下载文件在远程主机的路径
        """
        with self as cli:
            sftp = cli.open_sftp()
            sftp.get(remote_path, local_path)

    # 获取指定目录路径下的文件和文件夹列表详细信息,结果为列表，列表里面的每一项是from paramiko.sftp_attr import SFTPAttributes  类的对象，通过对象.属性可以获取对应的数据，比如获取修改时间用对象.st_mtime
    def list_dir_attr(self, remote_path):
        with self as cli:
            sftp = cli.open_sftp()
            return sftp.listdir_attr(remote_path)

    # 根据指定路径删除对应文件,没有对应文件会报错，有返回None
    def remove_file(self, remote_path):
        with self as cli:
            sftp = cli.open_sftp()
            sftp.remove(remote_path)

    # 删除远程主机上的目录
    def remove_dir(self, remote_path):
        with self as cli:
            sftp = cli.open_sftp()
            sftp.rmdir(remote_path)

    # 获取文件详情
    def file_stat(self, remote_path):
        with self as cli:
            sftp = cli.open_sftp()
            return sftp.stat(remote_path)

    # 直接获取连接
    def get_client(self):
        print(f"self.client={self.client}")
        if self.client is not None:
            return self.client
        try:
            # 创建客户端连接对象
            self.client = SSHClient()
            # 在本机第一次连接远程主机时记录指纹信息
            self.client.set_missing_host_key_policy(AutoAddPolicy)
            # 建立连接
            self.client.connect(**self.arguments)
        except AuthenticationException as e:
            return None

        return self.client

    # with self: 先执行__enter__方法
    def __enter__(self):
        print(f"self.client={self.client}")
        if self.client is not None:
            # 告知当前执行上下文，self.client已经实例化
            raise RuntimeError('已经建立连接了！！！')

        return self.get_client()
        # with self: 语句体内容结束后执行如下方法 先执行__enter__方法

    def __exit__(self, Type, value, traceback):
        self.client.close()