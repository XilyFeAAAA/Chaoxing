import axios from 'axios'
import router from "@/router";
import * as constants from '@/common/constant'
import * as storage from '@/common/storage'
import {ElLoading, ElNotification} from 'element-plus'

let authStore = null
let loading = null

const startLoading = () => {
    loading = ElLoading.service({
        lock: true,
        text: '加载中....',
        background: 'rgba(0,0,0,0.5)',
    })
}

const endLoading = () => {
    if (loading !== null) {
        loading.close()
        loading = null
    }
}

const instace = axios.create({
    withCredentials: true,
    baseURL: constants.BASEURL, //请求根路径
    timeout: constants.TIMEOUT, //请求超时时间
})

// 请求拦截器
instace.interceptors.request.use(
    (config) => {
        if (config.showLoading) {
            startLoading()
        }
        let access_token = storage.getAccessToken()
        if (access_token !== null) config.headers[constants.AUTH] = "Bearer " + access_token
        return config
    },
    (err) => {
        endLoading()
        return Promise.reject(err) //返回错误
    },
)

// 响应拦截器
instace.interceptors.response.use(
    async (response) => {
        let res = response.data
        endLoading()
        return response
    },
    (err) => {
        endLoading()
        if (err.response) {
            switch (err.response.status) {
                case 401:
                    ElNotification({
                        title: 'Warning',
                        message: '身份验证失败',
                        type: 'warning',
                    })
                    router.push('login')
                    break
                case 403:
                    // 双token
                    ElNotification({
                        title: 'Warning',
                        message: '登陆过期',
                        type: 'warning',
                    })
                    break
            }
        }
        return Promise.reject(err) //返回错误
    },
)

export default instace
