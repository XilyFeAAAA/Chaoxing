<template>
    <div class="h-full w-full">
        <header class="border-b h-16">
            <div class="m-auto max-w-7xl h-full flex items-center justify-between">
                <div class="flex items-center h-full cursor-pointer">
                    <TriangleIcon />
                    <div class="font-bold text-2xl">Chaoxing</div>
                </div>

                <div class="flex items-center">
                    <div class="mx-4 text-sm cursor-pointer">Contact</div>
                    <div
                        class="btn border px-4 py-[6px] rounded-md text-sm cursor-pointer select-none transition-all hover:bg-gray-100"
                        @click="status = !status"
                    >
                        {{ status ? 'Sign Up' : 'Log In' }}
                    </div>
                </div>
            </div>
        </header>

        <main class="h-[calc(100%-64px)]">
            <Transition name="fade" mode="out-in">
                <div v-if="status" class="h-full w-full flex justify-center items-center">
                    <div class="w-[320px] text-center">
                        <div class="mb-5">
                            <h1 class="font-bold text-3xl">Log in to Chaoxing</h1>
                        </div>
                        <form>
                            <div class="flex border h-12 py-2 px-4 rounded-lg">
                                <input
                                    type="text"
                                    v-model="loginFormData.email"
                                    class="flex-1 outline-none"
                                    placeholder="Email Address"
                                />
                            </div>
                            <div class="my-3 flex border h-12 py-2 px-4 rounded-lg">
                                <input
                                    type="password"
                                    v-model="loginFormData.password"
                                    class="flex-1 outline-none"
                                    placeholder="Password"
                                    @keyup.enter="handleLogin"
                                />
                            </div>
                        </form>
                        <div>
                            <button
                                class="flex justify-center items-center px-3 h-12 w-full bg-black rounded text-white transition-all hover:bg-[rgba(0,0,0,.8)]"
                                @click="handleLogin"
                            >
                                <svg-icon type="mdi" :path="mdiLogin"></svg-icon>
                                <span class="font-bold ml-4">Login</span>
                            </button>
                        </div>
                    </div>
                </div>
                <div v-else class="h-full w-full flex justify-center items-center">
                    <div class="w-[320px] text-center">
                        <div class="mb-5">
                            <h1 class="font-bold text-3xl">Create Your Chaoxing Account</h1>
                        </div>
                        <form>
                            <div class="flex border h-12 py-2 px-4 rounded-lg">
                                <input
                                    type="text"
                                    v-model="registerFormData.nickname"
                                    class="flex-1 outline-none"
                                    placeholder="Username"
                                />
                            </div>
                            <div class="my-3 flex border h-12 py-2 px-4 rounded-lg">
                                <input
                                    type="text"
                                    v-model="registerFormData.email"
                                    class="flex-1 outline-none"
                                    placeholder="Email Address"
                                />
                            </div>
                            <div class="my-3 flex border h-12 py-2 px-4 rounded-lg">
                                <input
                                    type="password"
                                    v-model="registerFormData.password"
                                    class="flex-1 outline-none"
                                    placeholder="Password"
                                />
                            </div>
                        </form>
                        <div>
                            <button
                                class="flex justify-center items-center px-3 h-12 w-full bg-black rounded text-white transition-all hover:bg-[rgba(0,0,0,.8)]"
                                @click="handleRegister"
                            >
                                <span class="font-bold ml-4">SignUp</span>
                            </button>
                        </div>
                    </div>
                </div>
            </Transition>
        </main>
    </div>
</template>
<script setup>
import { mdiLogin } from '@mdi/js'
import { ElNotification } from 'element-plus'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, register } from '@/requests/api'
import { useAuthStore } from '@/stores/auth'
import TriangleIcon from '@/components/icons/triangle.vue'

const router = useRouter()
const authStore = useAuthStore()
// refs
const loginFormData = ref({
    email: '',
    password: '',
})
const registerFormData = ref({
    email: '',
    nickname: '',
    password: '',
})
const status = ref(true) // true: login false: register
// functions
const handleLogin = () => {
    if (!loginFormData.value.email.trim().length || !loginFormData.value.password.trim().length) {
        return ElNotification({
            title: 'Warning',
            message: '用户名或密码不得为空',
            type: 'warning',
        })
    }
    const data = new FormData()
    data.append('email', loginFormData.value.email)
    data.append('password', loginFormData.value.password)
    login(loginFormData.value)
        .then((res) => {
            authStore.login(res.data.data)
            router.push({name:'dashboard'})
            ElNotification({
                title: 'Success',
                message: '登陆成功',
                type: 'success',
            })
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: '用户名和密码不匹配',
                type: 'error',
            })
        })
}
const handleRegister = () => {
    if (
        !registerFormData.value.email.trim() ||
        !registerFormData.value.password.trim() ||
        !registerFormData.value.nickname.trim()
    ) {
        return ElNotification({
            title: 'Warning',
            message: '字段不得为空',
            type: 'warning',
        })
    }
    register(registerFormData.value)
        .then((res) => {
            status.value = true
            loginFormData.value.email = registerFormData.value.email
            ElNotification({
                title: 'Success',
                message: '注册成功',
                type: 'success',
            })
        })
        .catch((err) => {})
}
</script>
<style lang="scss">
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
