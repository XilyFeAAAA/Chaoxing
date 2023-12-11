import { ref } from 'vue'
import { defineStore } from 'pinia'
import {getme} from '@/requests/api'


export const useAuthStore = defineStore('auth', () => {
    const isAuth = ref(false)
    const user = ref({})
    function login(info) {
        isAuth.value = true
        user.value = info
    }

    function logout() {
        isAuth.value = false
        user.value = {}
    }

    function handleGetMe() {
        getme().then((res) => {
            user.value = res.data.data
        })
    }

    return { isAuth, user, login, logout, handleGetMe }
},{
  persist: true
})
