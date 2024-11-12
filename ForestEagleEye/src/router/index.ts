import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: App,
    },
    {
      path:'/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path:'/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path:'/activities',
      name: 'activities',
      component: () => import('../views/activities.vue'),
    },
    {
      path:'/encyclopedia',
      name: 'encyclopedia',
      component: () => import('../views/encyclopedia.vue'),
    },
    {
      path:'/reflect',
      name: 'reflect',
      component: () => import('../views/reflect.vue'),
    },
    {
      path:'/forum',
      name: 'forum',
      component: () => import('../views/forum.vue'),
    },
    {
      path:'/game',
      name: 'game',
      component: () => import('../views/game.vue'),
    },
    {
      path:'/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
    },
    {
      path:'/message',
      name: 'message',
      component: () => import('../views/message.vue'),
    },
    {
      path:'/forest_detail/:id',
      name: 'forest_detail',
      component: () => import('../components/ForestDetailView.vue'),
      meta:{
        id: 1,
        title:'森林详情',
      }
    },
    {
      path: '/forests/:id/edit', // 使用动态路径参数 :id
      name: 'ForestEdit',
      component: () => import('../components/ForestEditView.vue'),
    },
  ]
});

export default router