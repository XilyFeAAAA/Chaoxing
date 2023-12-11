import axios from 'axios'
import router from '@/router'
import * as constants from '@/common/constant'
import { ElLoading } from 'element-plus'
import {useAuthStore} from "@/stores";

let loading = null
let authStore = null

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
        endLoading()
        return response
    },
    (err) => {
        if (authStore === null) {
            authStore = useAuthStore()
        }
        endLoading()
        if (err.response) {
            switch (err.response.status) {
                case 401:
                    if (err.response.data.detail === 'invalid_token') {
                        authStore.logout()
                        router.push({ name: 'login' })
                    }
                    break
            }
        }
        return Promise.reject(err) //返回错误
    },
)

export default instace
