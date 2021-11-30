<template>
  <div class="host">
    <a-card size="small" :bordered="false">
      <a-row>
        <a-col :span="6">
          <a-form-item label="主机类别：" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
            <a-select style="width: 120px;" placeholder="请选择" @change="handleSelectChange" v-model="host_form.form.category">
              <a-select-option :value="value.id" v-for="(value, index) in categorys" :key="value.id">
                {{value.name}}
              </a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="主机别名：">
            <a-input placeholder="请输入"/>
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="连接地址：" >
            <a-input v-decorator="['nickname', { rules: [{ required: checkHost, message: 'Please input your nickname' }] }, ]" placeholder="请输入"/>
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <router-link to="/workbench">
            <a-button type="primary" icon="sync" style="margin-top: 3px;">
              刷新页面
            </a-button>
          </router-link>
        </a-col>
      </a-row>

      <div class="add_host" style="margin-bottom: 15px;">
        <a-button type="primary" icon="plus" @click="showModal">
          新建
        </a-button>
        <a-button type="primary" icon="import" @click="showExcelModal" style="margin-left: 20px;">
          批量导入
        </a-button>
      </div>
      <!-- 新增主机 -->
      <a-modal
          :width="800"
          title="新建主机"
          :visible="visible"
          :confirm-loading="confirmLoading"

          @cancel="handleCancel"
      >
        <template slot="footer">
          <a-button key="back" @click="handleCancel">取消</a-button>
          <a-button key="submit" type="primary" :loading="loading" @click="onSubmit">验证</a-button>
        </template>
        <a-form-model ref="ruleForm" :model="host_form.form" :rules="host_form.rules" :label-col="host_form.labelCol" :wrapper-col="host_form.wrapperCol">

          <a-form-model-item label="主机类别" prop="zone">
            <a-row>
              <a-col :span="12">
                <a-select v-model="host_form.form.category" placeholder="请选择主机类别/区域/分组">
                  <a-select-option :value="value.id" v-for="(value, index) in categorys" :key="value.id">
                    {{value.name}}
                  </a-select-option>
                </a-select>
              </a-col>
              <a-col :span="5" :offset="2">
                <button type="button" class="ant-btn ant-btn-link"><span>添加类别</span></button>
              </a-col>
              <a-col :span="5">
                <button type="button" class="ant-btn ant-btn-link"><span>编辑类别</span></button>
              </a-col>
            </a-row>
          </a-form-model-item>
          <a-form-model-item ref="name" label="主机名称" prop="name">
            <a-row>
              <a-col :span="24">
                <a-input placeholder="请输入主机名称" v-model="host_form.form.name"/>
              </a-col>
            </a-row>
          </a-form-model-item>

          <a-form-model-item ref="ip_addr" label="连接地址" prop="ip_addr">
            <a-row>
              <a-col :span="8">
                <a-input placeholder="用户名" addon-before="ssh" v-model="host_form.form.username"/>
              </a-col>
              <a-col :span="8">
                <a-input placeholder="ip地址" addon-before="@" v-model="host_form.form.ip_addr"/>
              </a-col>
              <a-col :span="8">
                <a-input placeholder="端口号" addon-before="-p" v-model="host_form.form.port"/>
              </a-col>
            </a-row>
          </a-form-model-item>

          <a-form-model-item ref="password" label="连接密码" prop="password">
            <a-row>
              <a-col :span="24">
                <a-input placeholder="请输入连接密码" v-model="host_form.form.password" type="password"/>
              </a-col>
            </a-row>
          </a-form-model-item>

          <a-form-model-item extra="默认使用全局密钥，如果上传了独立密钥则优先使用该密钥。" ref="name" label="独立秘钥" prop="pkey">
            <a-row>
              <a-col :span="24">
                <a-upload name="file" :multiple="true" action="上传文件的地址" :headers="upload_pkey_headers" @change="handleFileChange">
                  <a-button>
                    <a-icon type="upload"/>
                    点击上传
                  </a-button>
                </a-upload>
              </a-col>
            </a-row>
          </a-form-model-item>
          <a-form-model-item ref="description" label="备注信息" prop="description">
            <a-row>
              <a-col :span="24">
                <a-textarea v-model="host_form.form.description" placeholder="请输入主机备注信息" :auto-size="{ minRows: 3, maxRows: 5 }"/>
              </a-col>
            </a-row>
          </a-form-model-item>

          <a-form-model-item>
            <a-row>
              <a-col :span="24" :offset="10">
                  <span>
                    <a-icon type="warning" style="color:yellow;"/>
                    首次验证时需要输入登录用户名对应的密码，但不会存储该密码。
                  </span>
              </a-col>
            </a-row>
          </a-form-model-item>
        </a-form-model>
      </a-modal>
      <!-- 批量导入主机 -->
      <div class="excel_push_modal">
        <a-modal v-model="excel_model_visible" title="批量导入主机信息" on-ok="handleUploadExcel" width="800px">
          <template slot="footer">
            <a-button key="back" @click="handleUploadExcelCancel">取消</a-button>
            <a-button type="primary" :disabled="excel_fileList.length === 0" :loading="excel_uploading" style="margin-top: 16px" @click="handleExcelUpload">{{ excel_uploading ? '上传处理中...' : '开始上传' }}</a-button>
          </template>
          <div>
            <a-alert type="info" message="导入或输入的密码仅作首次验证使用，并不会存储密码。" banner closable/><br/>
            <a-form :form="upload_excel_form">
              <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="模板下载" help="请下载使用该模板填充数据后导入">
                <a :href="`${$settings.host}/static/主机导入模板.xls`" download="主机导入模板.xls">主机导入模板.xls</a>
              </a-form-item>
              <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="默认密码" help="如果Excel中密码为空则使用该密码">
                <a-input v-model="default_password" placeholder="请输入默认主机密码"/></a-form-item>
              <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="导入数据">
                <div class="clearfix">
                  <a-upload :file-list="excel_fileList" :remove="handleExcelRemove" :before-upload="beforeExcelUpload" v-decorator="[ 'host_excel', { rules: [{ required: true, message: '请上传文件' }] }, ]">
                    <a-button><a-icon type="upload"/>选择上传的文件</a-button>
                  </a-upload>
                </div>
              </a-form-item>
            </a-form>
          </div>
        </a-modal>
      </div>
      <!-- 主机列表 -->
      <a-table :columns="columns" :data-source="data" rowKey="id">
        <a slot="name" slot-scope="text">{{ text }}</a>
        <template v-slot:action>
          <a href="javascript:;">编辑</a> |
          <a href="javascript:;">删除</a> |
          <a href="javascript:;">Console</a>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script>
const formItemLayout = {
  labelCol: {span: 8},
  wrapperCol: {span: 12},
};

const columns = [
  {
    title: '类别',
    dataIndex: 'category_name',
    key: 'category_name',
  },
  {
    title: '主机名称',
    dataIndex: 'name',
    key: 'name',
    sorter: true,

  },
  {
    title: '连接地址',
    dataIndex: 'ip_addr',
    key: 'ip_addr',
    ellipsis: true,
    sorter: true,
    width: 200,
  },
  {
    title: '端口',
    dataIndex: 'port',
    key: 'port',
    ellipsis: true,
  },
  {
    title: '备注信息',
    dataIndex: 'description',
    key: 'description',
    ellipsis: true,
  },

  {
    title: '操作',
    key: 'action',
    width: 200,
    scopedSlots: {customRender: 'action'},
  },
];

export default {
  name: "Host",
  data(){
    return {
      loading: false,
      formItemLayout,   // formItemLayout: formItemLayout,
      checkHost: false, // 是否验证信息
      visible: false,   // 是否显示添加主机的弹窗
      confirmLoading: false,
      categorys: [     // 主机类别

      ],
      data: [
        // {"id":1, "category_name":"数据库服务器","name":"iZbp1b1jw4l12ho53ivhkkZ","ip_addr":"47.98.130.212","port":22,"description":""},
        // {"id":2, "category_name":"数据库服务器","name":"iZbp1b1jw4l12ho53ivhkkZ","ip_addr":"47.98.130.212","port":22,"description":""},
        // {"id":3, "category_name":"数据库服务器","name":"iZbp1b1jw4l12ho53ivhkkZ","ip_addr":"47.98.130.212","port":22,"description":""},
        // {"id":4, "category_name":"数据库服务器","name":"iZbp1b1jw4l12ho53ivhkkZ","ip_addr":"47.98.130.212","port":22,"description":""},
      ],
      columns:columns, // 表格的表头信息
      // 上传文件的配置参数
      upload_pkey_headers: {
        authorization: 'authorization-text',
      },
      // 添加主机需要的数据属性
      host_form: {
        labelCol: {span: 6},
        wrapperCol: {span: 14},
        other: '',
        form: {
          name: '',
          category: '',
          ip_addr: '',
          username: '',
          port: '',
          description: '',
          password:'',
        },
        rules: {
          name: [
            {required: true, message: '请输入主机名称', trigger: 'blur'},
            {min: 3, message: '长度在3-20位之间', trigger: 'blur'},
          ],
          password: [
            {required: true, message: '请输入连接密码', trigger: 'blur'},
            {min: 3, max: 20, message: '长度在3-10位之间', trigger: 'blur'},
          ],
          category: [{required: true, message: '请选择类别', trigger: 'change'}],
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
            {min: 3, max: 20, message: '长度在3-10位', trigger: 'blur'},
          ],

          ip_addr: [
            {required: true, message: '请输入连接地址', trigger: 'blur'},
            {max: 50, message: '长度最大15位', trigger: 'blur'},
          ],

          port: [
            {required: true, message: '请输入端口号', trigger: 'blur'},
            {max: 5, message: '长度最大5位', trigger: 'blur'},
          ],
        },
      },
      excel_model_visible: false, // 批量导入主机的窗口显示和隐藏
      excel_fileList: [],  // 等待上传的xls文件列表
      excel_uploading: false, // 显示当前上传文件组件是否属于上传文件过程中的状态
      default_password: "",   // 默认上传的主机列表的通用登录密码
      upload_excel_form: this.$form.createForm(this, {name: 'coordinated'}),
    }
  },
  created(){
    // ajax获取数据
    this.get_categorys()
    this.get_host_list()
  },
  methods:{
    showExcelModal(){
      // 显示批量上传主机的窗口
      this.excel_model_visible = true
    },
    handleUploadExcelCancel() {
      // 关闭批量上传主机的窗口
      this.excel_model_visible = false;
    },
    beforeExcelUpload(file){
      // 当用户选择上传文件以后，需要手动把当前文件添加到待上传文件列表this.excel_fileList中
      this.excel_fileList = [...this.excel_fileList, file];
      return false;
    },
    handleExcelRemove(file){
      // 当用户要删除待上传文件列表中指定的文件时
      const index = this.excel_fileList.indexOf(file);
      const newFileList = this.excel_fileList.slice();
      newFileList.splice(index, 1);
      this.excel_fileList = newFileList;
    },
    handleExcelUpload(e){
      // 上传execl文件的处理函数
      console.log("excel_fileList =", this.excel_fileList)
      // 整理要上传到服务端的数据对象[上传文件列表和默认密码]
      const formData = new FormData();
      this.excel_fileList.forEach(file => {
        formData.append('host[]', file);
      });
      formData.append("default_password", this.default_password)
      this.excel_uploading = true;
      // ajax提交
      let token = sessionStorage.token || localStorage.token;
      this.$axios.post(`/host/host_excel`,formData,{
        headers:{
          Authorization: "jwt "+token
        }
      }).then(response=>{
        // 把本地的主机列表数组和服务端返回的数组列表进行合并产生一个新的主机列表数组
        this.data = this.data.concat(response.data.data);
        this.excel_uploading = false; // 退出登录处理状态
        this.$message.success('上传成功');
        if (response.data.error.length > 0){
          this.$message.error('上传的数据有存在错误！');
        }else{
          this.excel_model_visible = false;
        }
      }).catch(error=>{
        this.excel_uploading = false;
        this.$message.error('上传文件处理失败！');
      })
    },
    get_host_list(){
      let token = sessionStorage.token || localStorage.token || "";
      // 获取主机列表
      this.$axios.get(`/host/list`,{
        headers:{
          Authorization: "jwt " + token,
        }
      }).then(response=>{
        this.data = response.data
      }).catch(error=>{
        this.$message.error("主机列表获取失败！")
      })
    },
    get_categorys(){
      // 获取主机类别
      let token = sessionStorage.token || localStorage.token || "";
      this.$axios.get(`/host/categorys`,{
        headers:{
          Authorization: "jwt " + token,
        }
      }).then(response=>{
        this.categorys = response.data
      }).catch(error=>{
        this.$message.error("主机类别获取失败！")
      })
    },
    handleSelectChange(value) {
      console.log(value);
    },
    showModal() {
      // 显示添加主机的表单窗口
      this.visible = true;
    },
    handleCancel(e) {
      // 表单取消
      this.resetForm(); //清空表单内容

      this.visible = false; // 关闭对话框
    },
    onSubmit(){
      this.$refs.ruleForm.validate(valid => {
        // 验证通过则发送请求
        if (valid) {
          let token = sessionStorage.token || localStorage.token || "";
          // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
          this.$axios.post(`${this.$settings.host}/host/list/`,{
            "name":this.host_form.form.name,
            "category":this.host_form.form.category,
            "ip_addr":this.host_form.form.ip_addr,
            "description":this.host_form.form.description,
            "port":this.host_form.form.port,
            "username":this.host_form.form.username,
            "password":this.host_form.form.password,
          },{
            headers:{
              Authorization: "jwt " + token,
            }
          }).then(response=>{
            // 在现有的主机列表，追加新增的主机列表
            this.data.unshift(response.data);
            this.handleCancel();
          }).catch(error=>{
            this.$message.error("添加主机失败！");
          })

        } else {
          // 验证失败！
          return false;
        }
      });
    },
    handleFileChange(info){
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        this.$message.success(`${info.file.name} 上传成功`);
      } else if (info.file.status === 'error') {
        this.$message.error(`${info.file.name} 上传失败`);
      }
    },
    resetForm(){
      // 重置添加主机的表单信息
      this.$refs.ruleForm.resetFields();
    }
  }
}
</script>

<style scoped>

</style>