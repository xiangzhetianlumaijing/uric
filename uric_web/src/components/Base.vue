<template>
  <a-layout id="components-layout-demo-custom-trigger">
    <a-layout-sider v-model="collapsed" :trigger="null" collapsible :style="{ overflow: 'auto', height: '100vh'}">
      <div class="logo"/>
      <a-menu theme="dark" mode="inline" :default-selected-keys="['1']">

        <template v-for="(menu,index) in menu_list">
          <a-menu-item v-if="menu.children.length===0" :key="menu.id">
            <router-link :to="menu.menu_url">
              <a-icon type="mail"/>
              <span>{{menu.title}}</span>
            </router-link>
          </a-menu-item>
          <a-sub-menu v-else :key="menu.id">
              <span slot="title">
                <a-icon :type="menu.icon"/>
                <span>{{menu.title}}</span>
              </span>
            <a-menu-item v-for="(child_menu,child_index) in menu.children" :key="child_menu.id">
              <router-link :to="child_menu.menu_url">{{child_menu.title}}</router-link>
            </a-menu-item>

          </a-sub-menu>
        </template>

      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0">
        <a-icon
            class="trigger"
            :type="collapsed ? 'menu-unfold' : 'menu-fold'"
            @click="() => (collapsed = !collapsed)"
        />
      </a-layout-header>
      <a-layout-content
          :style="{ margin: '24px 16px', padding: '24px', background: '#fff', minHeight: '280px' }"
      >
        <router-view></router-view>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script>
export default {
  name: "Base",
  data() {
    return {
      collapsed: false,
      menu_list: [
        {id: 1, icon: 'mail', title: '展示中心', tube: '', 'menu_url': '/uric/workbench', children: []},
        {id: 2, icon: 'mail', title: '资产管理', 'menu_url': '/uric/host', children: []},
        {
          id: 3, icon: 'bold', title: '批量任务', tube: '', 'menu_url': '/uric/workbench', children: [
            {id: 10, icon: 'mail', title: '执行任务', 'menu_url': '/uric/multi_exec'},
            {id: 11, icon: 'mail', title: '命令管理', 'menu_url': '/uric/template_manage'},
          ]
        },
        {
          id: 4, icon: 'highlight', title: '代码发布', tube: '', 'menu_url': '/uric/workbench', children: [
            {id: 12, title: '应用管理', 'menu_url': '/uric/release'},
            {id: 13, title: '发布申请', 'menu_url': '/uric/release'},
          ]
        },
        {id: 5, icon: 'mail', title: '定时计划', tube: '', 'menu_url': '/uric/workbench', children: []},
        {
          id: 6, icon: 'mail', title: '配置管理', tube: '', 'menu_url': '/uric/workbench', children: [
            {id: 14, title: '环境管理', 'menu_url': '/uric/environment'},
            {id: 15, title: '服务配置', 'menu_url': '/uric/workbench'},
            {id: 16, title: '应用配置', 'menu_url': '/uric/workbench'},
          ]
        },
        {id: 7, icon: 'mail', title: '监控', tube: '', 'menu_url': '/uric/workbench', children: []},
        {
          id: 8, icon: 'mail', title: '报警', tube: '', 'menu_url': '/uric/workbench', children: [
            {id: 17, title: '报警历史', 'menu_url': '/uric/workbench'},
            {id: 18, title: '报警联系人', 'menu_url': '/uric/workbench'},
            {id: 19, title: '报警联系组', 'menu_url': '/uric/workbench'},
          ]
        },
        {
          id: 9, icon: 'mail', title: '用户管理', tube: '', 'menu_url': '/uric/workbench', children: [
            {id: 20, title: '账户管理', tube: '', 'menu_url': '/uric/workbench'},
            {id: 21, title: '角色管理', tube: '', 'menu_url': '/uric/workbench'},
            {id: 22, title: '系统设置', tube: '', 'menu_url': '/uric/workbench'},
          ]
        },
      ]
    };
  },
  methods: {
    selectedHandler(item, key, selectedKeys) {
      console.log('>>>>>', item, key, selectedKeys);
    }
  },
}
</script>

<style scoped>
#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}
</style>