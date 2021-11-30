<template>
  <div class="template_manager">
    <div>
      <a-row>
        <a-col :span="10">
          <a-form-item
              label="模板类别："
              :label-col="formItemLayout.labelCol"
              :wrapper-col="formItemLayout.wrapperCol"
          >
            <a-select style="width: 160px;"
                      placeholder="请选择"
                      @change="handleSelectChange"
                      v-model="template_category.form.category_id"
            >
              <a-select-option :value="value.id" v-for="(value, index) in tem_categorys" :key="value.id">
                {{value.name}}
              </a-select-option>
            </a-select>
          </a-form-item>
        </a-col>
        <a-col :span="10">
          <a-form-item
              :label-col="formItemLayout.labelCol"
              :wrapper-col="formItemLayout.wrapperCol"
              label="模板名称："
          >
            <a-input placeholder="请输入" />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <!-- <router-link> -->
          <a-button type="primary" icon="sync" style="margin-top: 3px;" @click="refresh_data">刷新</a-button>
          <!-- </router-link> -->
        </a-col>
      </a-row>
    </div>
    <div style="margin-top: 20px;">
      <a-button type="primary" @click="showModal" icon="plus"> 新建 </a-button>
      <a-modal v-model="visible" title="新建模板" @ok="handleSubmit" width="960px">
        <div>
          <div>
            <a-form :form="form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }" @submit="handleSubmit">
              <a-row>
                <a-form-item label="模板类别">
                  <a-col :span="18">
                    <a-select
                        v-decorator="[ 'category',
              { rules: [{ required: true, message: 'Please select your gender!' }] }, ]"
                        placeholder=""
                        @change="handleSelectChange" >
                      <a-select-option :value="value.id" v-for="(value, index) in tem_categorys" :key="value.id">
                        {{value.name}}
                      </a-select-option>
                    </a-select>
                  </a-col>
                  <a-col :span="6"><a-button type="link">添加类别</a-button></a-col>
                </a-form-item>
              </a-row>
              <a-form-item label="模板名称">
                <a-input
                    v-decorator="['name', { rules: [{ required: true, message: 'Please input your note!' }] }]"
                />
              </a-form-item>
              <a-form-item label="模板内容">
                <div>
                  <editor v-model="cmd" @init="editorInit" lang="html" theme="chrome" width="500" height="300">
                  </editor>
                </div>
              </a-form-item>

              <a-form-item label="备注信息">
                <a-textarea v-decorator="['desc', { rules: [{ required: false, message: 'Please input your note!' }] }]"
                            placeholder="Basic usage" :rows="4"/>
              </a-form-item>


            </a-form>

          </div>

        </div>


      </a-modal>

    </div>

    <div style="margin-top: 10px;">
      <a-table :columns="columns" :data-source="data" :rowKey="record => record.id">

      <span slot="action" slot-scope="record">
        <a href="javascript:;">编辑</a> |
        <a href="javascript:;">删除</a>

      </span>
      </a-table>
    </div>
  </div>
</template>

<script>
const formItemLayout = {
  labelCol: {span: 6},
  wrapperCol: {span: 14},
};

const columns = [
  {
    title: '模板名称',
    dataIndex: 'name',
    key: 'name',

  },
  {
    title: '模板类型',
    dataIndex: 'category_name',
    key: 'category_name',

  },
  {
    title: '模板内容',
    dataIndex: 'cmd',
    key: 'cmd',
    width: 200,
  },
  {
    title: '描述信息',
    dataIndex: 'description',
    key: 'description',

  },
  {
    title: '操作',
    key: 'action',
    width: 200,
    scopedSlots: {customRender: 'action'},
  },
];
export default {
  name: "TemplateManage",
  data() {
    return {
      formItemLayout,
      visible: false,
      formLayout: 'horizontal',
      form: this.$form.createForm(this, {name: 'coordinated'}),
      tem_categorys: [],
      data: [],
      columns,
      cmd: '',  // 添加指令模板时的cmd指令
      template_category: {
        form: {
          category_id: 1,
          name: '',
          cmd: '',
          desc: '',
        }
      }
    }
  },
  components: {
    editor: require('vue2-ace-editor'),
  },
  created() {
    this.get_templates_list();
    this.get_templates_category_list();
  },

  methods: {
    editorInit: function () {
      require('brace/ext/language_tools') //language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/javascript')    //language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') //snippet
    },
    handleSubmit(e) {  // handleSubmit必须声明并使用这个方法，名字不能改
      e.preventDefault();
      this.form.validateFields((err, values) => {
        let token = sessionStorage.token || localStorage.token;
        if (!err) {
          values.cmd = this.cmd;
          // 拿到验证成功之后的数据
          console.log('Received values of form: ', values);
          // 发送添加模板的请求
          this.$axios.post(`${this.$settings.host}/mtask/templates`, values,{
            headers:{
              Authorization: "jwt " + token
            }
          })
              .then(response => {
                console.log(response);
                this.visible = false;
                this.get_templates_list();
              })

        }

      });
      // this.visible = false;
    },
    showModal() {
      this.visible = true;
    },
    // handleOk(e) {
    //
    //   this.visible = false;
    // },

    handleSelectChange(value) {
      // 切换模板分类
      this.get_templates_list(value)
    },
    refresh_data() {
      this.get_templates_list();
    },
    get_templates_list(category = null) {
      let token = sessionStorage.token || localStorage.token;
      let params = {}
      if(category !== null){
        params.category = category
      }
      this.$axios.get(`${this.$settings.host}/mtask/templates`,{
        params:params,
        headers:{
          Authorization: "jwt " + token
        }
      }).then(response => {
        this.data = response.data;
      })
    },
    get_templates_category_list() {
      let token = sessionStorage.token || localStorage.token;
      this.$axios.get(`${this.$settings.host}/mtask/templates/categorys`,{
        headers:{
          Authorization: "jwt " + token
        }
      })
          .then(response => {
            this.tem_categorys = response.data;
          })
    }
  }

}
</script>

<style scoped>

</style>