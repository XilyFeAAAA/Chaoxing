<template>
    <div class="vben-login relative w-full h-full px-4">
        <div class="container relative h-full py-2 mx-auto sm:px-10">
            <div class="flex h-full">
                <div class="hidden min-h-full pl-4 mr-4 xl:flex xl:flex-col xl:w-6/12">
                    <div class="flex items-center absolute top-12">
                        <img src="@/assets/images/logo.png" class="w-14"/>
                        <div class="ml-2 truncate text-lg text-white font-bold">Chaoxing Admin</div>
                    </div>
                    <div class="my-auto">
                        <img alt="Vben Admin" src="@/assets/images/login-box-bg.svg" class="w-1/2 -mt-16 -enter-x"/>
                        <div class="mt-10 font-medium text-white -enter-x">
                            <span class="inline-block mt-4 text-3xl">超星刷课后台管理系统</span>
                        </div>
                    </div>
                </div>
                <div class="flex h-full py-5 w-6/12">
                    <div
                        class="vben-login-form relative w-full px-10 py-8 mx-auto my-auto rounded-md">
                        <h2 class="mb-3 text-2xl font-bold text-center xl:text-3xl enter-x xl:text-left enter-x">登录</h2>
                        <el-form ref="formRef" :model="form" :rules="rules" class="w-[400px] py-2">
                            <el-form-item prop="email">
                                <el-input type="email" v-model="form.email" size="large" placeholder="邮箱"/>
                            </el-form-item>
                            <el-form-item prop="password">
                                <el-input type="password" v-model="form.password" size="large" placeholder="密码" show-password/>
                            </el-form-item>
                            <el-form-item>
                                <div class="w-full flex items-center justify-between">
                                    <el-checkbox v-model="form.remember">记住我</el-checkbox>
                                    <el-link type="success">忘记密码?</el-link>
                                </div>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="primary" class="w-full" size="large" @click="handleLogin">
                                    登陆
                                </el-button>
                            </el-form-item>
                            <el-form-item>
                                <div class="w-full flex items-center">
                                    <el-button class="w-1/3">手机登陆</el-button>
                                    <el-button class="w-1/3 mx-3">二维码登陆</el-button>
                                    <el-button class="w-1/3">注册</el-button>
                                </div>
                            </el-form-item>
                        </el-form>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<script setup>
import {reactive, ref} from 'vue'
import {useRouter} from "vue-router";
import {useAuthStore} from "@/stores";
import {admin_login} from '@/requests/api'
import validator from "@/utils/validator";
import {ElNotification} from "element-plus";
const router = useRouter()
const authStore = useAuthStore()
// constants
const rules = reactive({
    email: [
        {required: true, message: '请输入邮箱', trigger: 'blur'},
        {
            validator: (rule, value, callback, source, options) => {
                let error = [];
                let checkRes = validator.checkEmail(value);
                if (!checkRes.data) {
                    error.push(checkRes.msg);
                }
                callback(error);
            },
            trigger: "blur",
        },
    ],
    password: [
        {required: true, message: '请输入密码', trigger: 'blur'}
    ]
})
// refs
const formRef = ref(null)
const form = ref({})
// functions
const handleLogin = () => {
    if (!formRef.value) return
    formRef.value.validate(valid => {
        if (valid) {
            admin_login(form.value).then(res=>{
                authStore.login(res.data.data)
                router.push('/admin')
                ElNotification({
                    title: 'Success',
                    message: '登陆成功',
                    type: 'success',
                })
            }).catch(err=>{
                console.log(err)
                ElNotification({
                    title: 'Error',
                    message: '用户名和密码不匹配',
                    type: 'error',
                })
            })
        }else{
            return false
        }
    })
}
</script>


<style scoped lang="scss">
.vben-login:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    margin-left: -48%;
    background-image: url('@/assets/images/login-bg.svg');
    background-repeat: no-repeat;
    background-position: 100%;
    background-size: auto 100%;
}
</style>