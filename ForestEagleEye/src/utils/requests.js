//进行axios二次封装:使用请求与响应拦截器
import axios from 'axios'
 
//第一步:利用axios对象的create方法,去创建axios实例(其他的配置:基础路径、超时的时间)
const request = axios.create({
    //基础路径
    baseURL: 'http://localhost:5000', //基础路径
    timeout: 15000, //超时的时间的设置
})
//第二步:request实例添加请求与响应拦截器
request.interceptors.request.use((config) => {
    //config配置对象,headers属性请求头,经常给服务器端携带公共参数
    config.headers.Authorization = 'authorization'
    //返回配置对象
    return config
})
 
//第三步:响应拦截器
request.interceptors.response.use(
    (response) => {
        if (response.headers['content-type'] !== 'application/json') {
            // 返回的不是json则由调用方处理
            return response
        }
        if (response.data.status == 200) {
            // 请求成功
            return response.data
        } else if (response.data.status == 401) {
            // 未登录
            // todo 重新登录
            return Promise.reject(response.data)
        } else {
            // 弹出错误提示
            console.error(response.data.message)
            return Promise.reject(response.data)
        }
    },
    (error) => {
        //失败回调:处理http网络错误的
        //定义一个变量:存储网络错误信息
        let message = ''
        if (error.message.includes('timeout')) {
            message = '请求接口服务超时'
        } else if (error.message.includes('Network Error')) {
            message = '网络错误'
        }
        //http状态码
        if (error.response) {
            const status = error.response.status
            switch (status) {
                case 401:
                    message = 'TOKEN过期'
                    break
                case 403:
                    message = '无权访问'
                    break
                case 404:
                    message = '请求地址错误'
                    break
                case 500:
                    message = '服务器出现问题'
                    break
                default:
                    message = '网络出现问题'
                    break
            }
        }
        if (!message) message = '未知错误'
        //提示错误信息
        console.log(message)
        return Promise.reject(error)
    },
)
 
//对外暴露
export default request