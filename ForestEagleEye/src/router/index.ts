import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/activities',
      name: 'activities',
      component: () => import('../views/activities.vue')
    },
    {
      path: '/encyclopedia',
      name: 'encyclopedia',
      component: () => import('../views/EncyclopediaView.vue')
    },
    {
      path: '/forum',
      name: 'forum',
      component: () => import('../views/ForumView.vue')
    },
    {
      path: '/post/:id',
      name: 'post',
      component: () => import('../views/postDetailView.vue')
    },
    {
      path: '/postshare/:id',
      name: 'sharepost',
      component: () => import('../views/postWriteView.vue')
    },
    {
      path: '/postwrite',
      name: 'writepost',
      component: () => import('../views/postWriteView.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue')
    },
    {
      path: '/forests/:id/edit', // 使用动态路径参数 :id
      name: 'ForestEdit',
      component: () => import('../components/ForestEditView.vue'),
    },
    {
      path: '/create_activity',
      name: 'create_activity',
      component: () => import('../components/create_activity.vue'),
    },
    {
      path: '/approve',
      name: 'approve',
      component: () => import('../components/approve.vue'),
    },
    {
      path: '/apply',
      name: 'apply',
      component: () => import('../components/apply.vue'),
    },
    {
      path: '/enroll',
      name: 'enroll',
      component: () => import('../components/enroll.vue'),
    },
    {
        path: '/activity_detail/:activityId',  // 这里的 activityId 是动态参数
        name: 'activity_detail',
        component: () => import('../components/activity_detail.vue'),  // Vue 组件路径
        meta: {
            title: '活动详情'
        }
    },
    {
        path: '/enroll_activity/:activityId',  // 这里的 activityId 是动态参数
        name: 'enroll_activity',
        component: () => import('../components/enroll_activity.vue'),  // Vue 组件路径
        meta: {
            title: '活动详情'
        }
    },
  ]
})

export default router
