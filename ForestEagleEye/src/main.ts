import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/index'
//引入echarts
import Echarts from 'vue-echarts'
import * as echarts from 'echarts'
//引入element-plus
import ElementPlus from 'element-plus'

const app = createApp(App)

app.use(createPinia())
//挂载echarts到全局
app.component('e-charts',Echarts)
app.config.globalProperties.$echarts = echarts
//挂载element-plus到全局
app.use(ElementPlus)

app.use(router)
app.mount('#app')

