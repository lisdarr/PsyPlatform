import Vue from 'vue'
import Router from 'vue-router'
/* Layout */
import Layout from '@/layout'

Vue.use(Router)

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  }

  // {
  //   path: '/404',
  //   component: () => import('@/views/404'),
  //   hidden: true
  // },

  // {
  //   path: '/',
  //   name: 'userManage',
  //   component: Layout,
  //   children: [{
  //     path: 'usermanage',
  //     name: 'userManage',
  //     component: () => import('@/views/userManage/index'),
  //     meta: { title: '用户管理', icon: 'el-icon-s-custom' }
  //   }]
  // }

  // 404 page must be placed at the end !!!
  // { path: '*', redirect: '/404', hidden: true }
]

// 异步挂载的路由
// 动态需要根据权限加载的路由表
export const asyncRoutes = [
  // 心理咨询师动态路由
  {
    path: '/',
    component: Layout,
    // redirect: '/dashboard',
    meta: { roles: ['Consultant'] },
    children: [{
      path: 'DashboardConsult',
      name: 'DashboardConsult',
      component: () => import('@/views/DashboardConsult/index'),
      // title设置sidebar标题
      meta: { roles: ['Consultant'], title: '首页', icon: 'el-icon-s-home' }
    }]
  },

  {
    path: '/',
    component: Layout,
    meta: { roles: ['Consultant'] },
    children: [{
      path: 'RecordConsult',
      component: () => import('@/views/RecordConsult/index'),
      name: 'RecordConsult',
      // title设置sidebar标题
      meta: { roles: ['Consultant'], title: '咨询记录', icon: 'el-icon-document' }
    }]
  },

  {
    path: '/ChatConsult',
    component: Layout,
    meta: { roles: ['Consultant'] },
    children: [
      {
        path: '/ChatConsult',
        component: () => import('@/views/ChatConsult/index'),
        name: 'ChatConsult',
        meta: { roles: ['Consultant'], title: '会话列表', icon: 'el-icon-chat-dot-square' }
      }
      // {
      //   path: '/ChatConsult/:id',
      //   component: () => import('@/views/ChatConsult/Chat'),
      //   // hidden: true,
      //   name: 'Chat',
      //   meta: { roles: ['Consultant'], title: '聊天' }
      // }
    ]
  },
  // 督导动态路由
  {
    path: '/',
    component: Layout,
    meta: { roles: ['Director'] },
    children: [{
      path: 'DashboardDirector',
      component: () => import('@/views/DashboardDirector/index'),
      name: 'DashboardDirector',
      meta: { roles: ['Director'], title: '首页', icon: 'el-icon-s-home' }
    }]
  },
  {
    path: '/',
    component: Layout,
    meta: { roles: ['Director'] },
    children: [{
      path: 'RecordDirector',
      component: () => import('@/views/RecordDirector/index'),
      name: 'RecordDirector',
      // title设置sidebar标题
      meta: { roles: ['Director'], title: '咨询记录', icon: 'el-icon-document' }
    }]
  },

  {
    path: '/',
    component: Layout,
    meta: { roles: ['Director'] },
    children: [{
      path: 'ChatDirector',
      component: () => import('@/views/ChatDirector/index'),
      name: 'ChatDirector',
      meta: { roles: ['Director'], title: '会话', icon: 'el-icon-chat-dot-square' }
    }]
  },
  // 管理员动态路由
  {
    path: '/',
    component: Layout,
    meta: { roles: ['Admin'] },
    children: [{
      path: 'DashboardAdmin',
      component: () => import('@/views/DashboardAdmin/index'),
      name: 'DashboardAdmin',
      meta: { roles: ['Admin'], title: '首页', icon: 'el-icon-s-home' }
    }]
  },
  {
    path: '/',
    name: 'RecordAdmin',
    component: Layout,
    meta: { roles: ['Admin'] },
    children: [{
      path: 'RecordAdmin',
      name: 'RecordAdmin',
      component: () => import('@/views/RecordAdmin/index'),
      meta: { roles: ['Admin'], title: '咨询记录', icon: 'el-icon-document' }
    }]
  },
  {
    path: '/',
    name: 'ScheduleAdmin',
    meta: { roles: ['Admin'] },
    component: Layout,
    children: [{
      path: 'ScheduleAdmin',
      name: 'ScheduleAdmin',
      component: () => import('@/views/ScheduleAdmin/index'),
      meta: { roles: ['Admin'], title: '排班表', icon: 'el-icon-date' }
    }]
  },

  {
    path: '/',
    name: 'consultantManage',
    meta: { roles: ['Admin'] },
    component: Layout,
    children: [{
      path: 'consultantmanage',
      name: 'consultantManage',
      component: () => import('@/views/consultantManage/index'),
      meta: { roles: ['Admin'], title: '咨询师管理', icon: 'el-icon-service' }
    }]
  },

  {
    path: '/',
    name: 'monitorManage',
    meta: { roles: ['Admin'] },
    component: Layout,
    children: [{
      path: 'monitormanage',
      name: 'monitorManage',
      component: () => import('@/views/monitorManage/index'),
      meta: { roles: ['Admin'], title: '督导管理', icon: 'el-icon-s-platform' }
    }]
  },
  {
    path: '/',
    name: 'userManage',
    component: Layout,
    meta: { roles: ['Admin'] },
    children: [{
      path: 'usermanage',
      name: 'userManage',
      component: () => import('@/views/userManage/index'),
      meta: { roles: ['Admin'], title: '访客管理', icon: 'el-icon-s-custom' }
    }]
  },
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router

