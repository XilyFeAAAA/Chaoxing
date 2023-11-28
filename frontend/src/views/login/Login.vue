<template>
  <div class="h-full w-full">
    <header class="border-b h-16">
      <div class="m-auto max-w-7xl h-full flex items-center justify-between">
        <div class="flex items-center h-full cursor-pointer">
          <TriangleIcon/>
          <div class="font-bold text-2xl">Chaoxing</div>
        </div>

        <div class="flex items-center">
          <div class="mx-4 text-sm cursor-pointer">Contact</div>
          <div class="btn border px-4 py-[6px] rounded-md text-sm cursor-pointer">Sign Up</div>
        </div>
      </div>
    </header>

    <main class="flex justify-center items-center h-[calc(100%-64px)]">
      <div class="w-[320px] text-center">
        <div class="mb-5">
          <h1 class="font-bold text-3xl">Log in to Chaoxing</h1>
        </div>
        <form>
          <div class="flex border h-12 py-2 px-4 rounded-lg">
            <input
                type="text"
                v-model="formData.email"
                class="flex-1 outline-none"
                placeholder="Email Address"
            />
          </div>
          <div class="my-3 flex border h-12 py-2 px-4 rounded-lg">
            <input type="password" v-model="formData.password" class="flex-1 outline-none" placeholder="Password"/>
          </div>
        </form>
        <div>
          <button
              class="flex justify-center items-center px-3 h-12 w-full bg-black rounded text-white"
              @click="handleLogin"
          >
            <svg-icon type="mdi" :path="mdiLogin"></svg-icon>
            <span class="font-bold ml-4">Login</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>
<script setup>
import { mdiLogin } from '@mdi/js'
import { ElNotification } from "element-plus";
import { ref } from 'vue'
import { useRouter } from "vue-router";
import { login } from '@/requests/api'
import { useAuthStore } from "@/stores/auth";
import TriangleIcon from '@/components/icons/triangle.vue'

const router = useRouter()
const authStore = useAuthStore()
// refs
const formData = ref({
  email: '',
  password: ''
})
// functions
const handleLogin = () => {
  if (!formData.value.email.trim().length || !formData.value.password.trim().length) {
    return ElNotification({
      title: 'Warning',
      message: '用户名或密码不得为空',
      type: 'warning',
    })
  }
  const data = new FormData
  data.append("username", formData.value.email)
  data.append("password", formData.value.password)
  login(data).then(res => {
    ElNotification({
      title: 'Success',
      message: '登陆成功',
      type: 'success',
    })
    authStore.login(res.data.data.access_token, res.data.data.refresh_token)
    router.push('dashboard')
  }).catch(err => {
    ElNotification({
      title: 'Error',
      message: '用户名和密码不匹配',
      type: 'error',
    })
  })
}
</script>
