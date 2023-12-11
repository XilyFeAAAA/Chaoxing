<template>
    <div>
        <header class="w-full border-b py-10">
            <div class="mx-auto h-full w-[1200px]">
                <h1 class="text-3xl">订单确认</h1>
            </div>
        </header>
        <main>
            <!-- table -->
            <div class="mx-auto w-[1200px] py-6">
                <div class="mx-auto w-[700px]">
                    <div>
                        <el-steps :active="activeStep" finish-status="success">
                            <el-step title="确认订单信息"/>
                            <el-step title="完成"/>
                        </el-steps>
                    </div>
                    <div v-if="activeStep === 0" class="flex flex-col items-center py-4">
                        <el-form
                            :model="form"
                            label-position="right"
                            label-width="80px"
                            style="width: 400px"
                        >
                            <el-form-item label="邮箱">
                                <el-input  v-model="form.email" disabled/>
                            </el-form-item>
                            <el-form-item label="平台">
                                <el-input v-model="form.platform" disabled/>
                            </el-form-item>
                            <el-form-item label="联系电话">
                                <el-input  v-model="form.phone" disabled/>
                            </el-form-item>
                            <el-form-item label="课程名称">
                                <el-input v-model="form.course_name" disabled/>
                            </el-form-item>
                        </el-form>
                        <el-button @click="handleSubmitOrder">提交</el-button>
                    </div>
                    <div v-else-if="!error">
                        <el-result
                            icon="success"
                            title="订单提交成功"
                        >
                            <template #extra>
                                <el-button type="primary" @click="router.push({name: 'courses'})">
                                    返回课程列表
                                </el-button>
                                <el-button @click="router.push({name: 'order'})">
                                    查看订单
                                </el-button>
                            </template>
                        </el-result>
                    </div>
                    <div v-else>
                        <el-result
                            icon="error"
                            title="订单提交失败"
                            :sub-title="error"
                        >
                            <template #extra>
                                <el-button type="primary" @click="router.push({name: 'courses'})">
                                    返回课程列表
                                </el-button>
                            </template>
                        </el-result>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>
<script setup>
import {onMounted, ref } from 'vue'
import {useAuthStore} from "@/stores";
import {useRoute, useRouter, onBeforeRouteLeave} from "vue-router";
import {ElNotification, ElMessage} from "element-plus";
import {get_confrim, cancel_order, sumbit_course_order} from '@/requests/api'
const route = useRoute()
const router = useRouter()
const form = ref({})
const error = ref('')
const authStore = useAuthStore()
// refs
const activeStep = ref(0)
const handleSubmitOrder = () => {
    if (!form.value.is_open) {
        return ElNotification({
            title: 'Warning',
            message: '课程已结束',
            type: 'warning',
        })
    }
    sumbit_course_order({
        order_id: route.params.order_id,
    })
        .then((res) => {
            authStore.user.userinfo = res.data.data
            activeStep.value = 2
        })
        .catch((err) => {
            activeStep.value = 2
            error.value = err.response.data.detail
        })
}
const handleGetOrder = () => {
    get_confrim(route.params.order_id).then(res=>{
        form.value = res.data.data
    }).catch(err=>{
        router.go(-1)
        ElMessage({
            type:'warning',
            message: '订单不存在'
        })
    })
}
onMounted(() => {
    if (!route.params.order_id) {
        router.go(-1)
    } else {
        console.log(route.params.order_id)
        handleGetOrder()
    }
})
onBeforeRouteLeave((to, from, next) => {
    cancel_order(route.params.order_id).then(res=>{
        next()
    }).catch(err=>{
        next()
    })
});
</script>
<style scoped>
.el-form-item {
    margin-bottom: 10px !important;
}

</style>