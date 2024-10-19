import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/index'


const app = createApp(App)

// 将 Axios 实例挂载到 Vue 原型上
app.use(createPinia())
app.use(router)


app.mount('#app')

