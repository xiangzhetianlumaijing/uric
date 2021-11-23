import django, os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uric_api.uric_api.settings.dev')
django.setup()

import paramiko
import traceback
from paramiko.ssh_exception import AuthenticationException
from ...uric_api.apps.host.models import PkeyModel
from paramiko.rsakey import RSAKey
from io import StringIO


if __name__ == '__main__':

    # 通过parammiko创建一个ssh短连接客户端实例对象
    ssh = paramiko.SSHClient()
    # 自动在本机第一次连接远程服务器时，记录主机指纹
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 1. 直接密码远程连接的方式
        # ssh.connect(hostname='192.168.0.52', port=22, username='root', password='123', timeout=10)
        # 注意，如果你测试某个服务器的连接时，如果你本地已经配置了这个远程服务器的免密登录(公私钥模式)，那么就不能测试出密码是否正确了，因为首先会通过公私钥模式登录，不会使用你的密码的。

        # 2. 使用秘钥免密登录的方式
        pkey = PkeyModel.objects.get(name=settings.DEFAULT_KEY_NAME).private
        pkey = RSAKey.from_private_key(StringIO(pkey))
        ssh.connect(hostname='192.168.0.52', port=22, username='root', pkey=pkey, timeout=10)

        # 连接成功以后，就可以发送操作指令
        # stdin 输入[本机发送给远程主机的信息]
        # stdout 输出[远程主机返回给本机的信息]
        # stderr 错误
        stdin, stdout, stderr = ssh.exec_command('ls -la')
        # 读取stdout对象中返回的内容，返回结果bytes类型数据
        result = stdout.read()
        print(result.decode())
        # 关闭连接
        ssh.close()
    except AuthenticationException as e:
        print(e.message)
        print(traceback.format_exc())