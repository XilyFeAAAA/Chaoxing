import { ref } from 'vue'
import { defineStore } from 'pinia'
import * as storage from '@/common/storage'

export const useAuthStore = defineStore('auth', () => {
  const isAuth = ref(false)
  const userInfo = ref({})
  function login(access_token, refresh_token){
    isAuth.value = true
    storage.setAccessToken(access_token)
    storage.setRefreshToken(refresh_token)
  }

  function setInfo(info){
    isAuth.value = true
    userInfo.value = info
  }
  function logout(){
    isAuth.value = false
    userInfo.value = {}
    storage.removeAccessToken()
    storage.removeRefreshToken()
  }

  return { isAuth, userInfo, login, logout, setInfo}
})
