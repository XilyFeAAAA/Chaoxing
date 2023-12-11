<template>
    <header class="w-full border-b py-10">
        <div class="mx-auto h-full w-[1200px]">
            <h1 class="text-3xl">账户</h1>
        </div>
    </header>
    <main>
        <div class="mx-auto w-[1200px] py-6">
            <!--add new account-->
            <div class="border rounded p-5 bg-[#fafafa]">
                <el-collapse v-model="active_method" accordion>
                    <el-collapse-item title="账号密码登陆" name="pwd">
                        <div class="pb-4 mb-4 border-b">
                            <form>
                                <div class="flex gap-2 items-center text-xs text-gray-600">
                                    <div class="flex-1">
                                        <div class="pb-2">PHONE NUMBER</div>
                                        <div>
                                            <el-input
                                                size="large"
                                                placeholder="phone"
                                                v-model="accountFormData.phone"
                                            ></el-input>
                                        </div>
                                    </div>
                                    <div class="flex-1">
                                        <div class="pb-2">PASSWORD</div>
                                        <div>
                                            <el-input
                                                size="large"
                                                type="password"
                                                placeholder="password"
                                                v-model="accountFormData.password"
                                            ></el-input>
                                        </div>
                                    </div>
                                    <div class="flex-1">
                                        <div class="pb-2">IMAGE CAPTCHA</div>
                                        <div class="flex items-center">
                                            <div class="mr-2">
                                                <el-input
                                                    size="large"
                                                    v-model="accountFormData.captcha"
                                                ></el-input>
                                            </div>
                                            <div class="border cursor-pointer">
                                                <img
                                                    :src="captcha_url"
                                                    @click="handleRefreshCaptcha"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="flex justify-between">
                            <div class="flex items-center">
                                <div class="text-sm mr-1">Learn more about</div>
                                <a href="#" class="flex items-center text-blue-600 hover:underline">
                                    Chaoxing Account
                                    <svg-icon type="mdi" size="15" :path="mdiOpenInNew"></svg-icon>
                                </a>
                            </div>
                            <div>
                                <el-button
                                    color="#000"
                                    :disabled="loading"
                                    @click="handlePwdBindAccount"
                                >
                                    {{ loading ? '绑定中...' : '绑定' }}
                                </el-button>
                            </div>
                        </div>
                    </el-collapse-item>
                    <el-collapse-item title="扫码登陆" name="code">
                        <div class="flex justify-evenly items-center">
                            <div>
                                <div class="flex justify-center">
                                    <img
                                        ref="qrcodeRef"
                                        class="w-32 h-32 m-3 p-1 border-gray-300 border-2 rounded cursor-pointer"
                                        @click="handleRefreshQrcode"
                                    />
                                </div>
                                <div class="flex justify-center">
                                    <button
                                        class="bg-[#171717] rounded-md h-10 w-52 border hover:bg-[#383838]"
                                        @click="handleQrcodeBindAccount"
                                    >
                                        <span class="text-white font-bold">绑 定</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </div>
            <div class="mt-10">
                <div
                    v-for="(account, idx) in accounts"
                    :key="idx"
                    class="flex border rounded p-4 mb-4"
                >
                    <!-- basic info -->
                    <div class="flex flex-1">
                        <div class="flex justify-center items-center">
                            <!-- avatar -->
                            <img
                                :src="`http://photo.chaoxing.com/p/${account.uid}_80?`"
                                class="w-5 h-5 rounded-full border"
                            />
                        </div>
                        <div class="ml-4">
                            <div>{{ account.username }}</div>
                            <div class="text-sm text-gray-500">{{ account.department }}</div>
                        </div>
                    </div>
                    <div v-if="account.active" class="flex items-center mr-4">
                        <svg-icon
                            type="mdi"
                            size="22"
                            :path="mdiStarBoxOutline"
                            class="text-yellow-500"
                        ></svg-icon>
                    </div>
                    <!-- valid status -->
                    <div class="flex items-center">
                        <div
                            class="rounded px-2 py-[2px] text-white"
                            :class="account.valid ? 'bg-green-300' : 'bg-red-400 '"
                        >
                            {{ account.valid ? 'valid' : 'invalid' }}
                        </div>
                    </div>
                    <!-- bind_time -->
                    <div class="flex items-center ml-4">
                        <div class="text-gray-500">
                            上次刷新时间 {{ calculateDaysFromTimestamp(account.bind_time) }}天前
                        </div>
                    </div>
                    <!-- more btn -->
                    <div class="flex items-center ml-4 cursor-pointer">
                        <el-popover
                            ref="popoverRefs"
                            placement="top-end"
                            :width="240"
                            trigger="click"
                        >
                            <template #reference>
                                <div class="hover:bg-[rgba(0,0,0,.08)] p-2 rounded transition-all">
                                    <svg-icon
                                        type="mdi"
                                        size="15"
                                        :path="mdiDotsHorizontal"
                                    ></svg-icon>
                                </div>
                            </template>
                            <template #default>
                                <div class="p-3">
                                    <div
                                        class="more-item"
                                        v-if="!account.active"
                                        @click="handleActiveAccount(idx)"
                                    >
                                        <div class="text-sm font-bold">设置为活动账户</div>
                                        <div>
                                            <svg-icon
                                                type="mdi"
                                                size="20"
                                                :path="mdiStarCircleOutline"
                                            ></svg-icon>
                                        </div>
                                    </div>
                                    <div class="more-item" @click="handleRefreshAccount(idx)">
                                        <div class="text-sm font-bold">刷新账户</div>
                                        <div>
                                            <svg-icon
                                                type="mdi"
                                                size="20"
                                                :path="mdiRefresh"
                                            ></svg-icon>
                                        </div>
                                    </div>
                                    <div
                                        v-if="!account.active"
                                        class="more-item"
                                        @click="handleDeleteAccount(idx)"
                                    >
                                        <div class="text-sm font-bold">删除账户</div>
                                        <div>
                                            <svg-icon
                                                type="mdi"
                                                size="20"
                                                :path="mdiDeleteOutline"
                                            ></svg-icon>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </el-popover>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>
<script setup>
import * as constants from '@/common/constant'
import { ref, onMounted } from 'vue'
import { ElNotification, ElMessageBox } from 'element-plus'
import {
    getaccounts,
    pwd_bind_account,
    qrcode_bind_account,
    del_account,
    active_account,
    refresh_account,
    get_qrcode,
} from '@/requests/api'
import {
    mdiOpenInNew,
    mdiDotsHorizontal,
    mdiStarCircleOutline,
    mdiDeleteOutline,
    mdiRefresh,
    mdiStarBoxOutline,
} from '@mdi/js'
import { calculateDaysFromTimestamp } from '@/utils/time'
// refs
const loading = ref(false)
const accounts = ref(null)
const active_method = ref('pwd')
const accountFormData = ref({
    phone: '',
    password: '',
    captcha: '',
})
const qrcodeRef = ref(null)
const popoverRefs = ref(null)
const expired = ref(false)
const captcha_url = ref(constants.BASEURL + 'auth/captcha')
// functions
const get_accounts = () => {
    getaccounts()
        .then((res) => {
            accounts.value = res.data.data || []
        })
        .catch((err) => {})
}
const handleRefreshCaptcha = () => {
    captcha_url.value = constants.BASEURL + 'auth/captcha?t=' + Date.now()
}
const handlePwdBindAccount = () => {
    loading.value = true
    const data = {
        account_info: {
            phone: accountFormData.value.phone,
            password: accountFormData.value.password,
        },
        captcha: accountFormData.value.captcha,
    }
    pwd_bind_account(data)
        .then((res) => {
            ElNotification({
                title: 'Success',
                message: '绑定成功',
                type: 'success',
            })
            accounts.value.push(res.data.data)
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: problem == err.response.data.msg,
                type: 'error',
            })
        })
    loading.value = false
}
const handleActiveAccount = (index) => {
    active_account({ account_id: accounts.value[index].account_id })
        .then((res) => {
            ElNotification({
                title: 'Success',
                message: '设置成功',
                type: 'success',
            })
            get_accounts()
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: '设置失败',
                type: 'error',
            })
        })
}
const handleDeleteAccount = (index) => {
    del_account({ account_id: accounts.value[index].account_id })
        .then((res) => {
            ElNotification({
                title: 'Success',
                message: '删除账户成功',
                type: 'success',
            })
            get_accounts()
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: '删除账户失败',
                type: 'error',
            })
        })
}
const handleRefreshAccount = (index) => {
    ElMessageBox.prompt(`请输入账号${accounts.value[index].phone}的密码`, '刷新账号', {
        confirmButtonText: '刷新',
        cancelButtonText: '取消',
    }).then(({ value }) => {
        refresh_account({
            account_id: accounts.value[index].account_id,
            password: value,
        })
            .then((res) => {
                accounts.value[index] = res.data.data
            })
            .catch((err) => {
                ElNotification({
                    title: 'Error',
                    message: err.response.data.msg,
                    type: 'error',
                })
            })
    })
}
const handleRefreshQrcode = () => {
    get_qrcode()
        .then((res) => {
            const reader = new FileReader()
            reader.onloadend = () => {
                qrcodeRef.value.src = reader.result
            }
            reader.readAsDataURL(res.data)
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: '获取二维码失败',
                type: 'error',
            })
        })
}
const handleQrcodeBindAccount = () => {
    loading.value = true
    qrcode_bind_account()
        .then((res) => {
            ElNotification({
                title: 'Success',
                message: '绑定成功',
                type: 'success',
            })
            accounts.value.push(res.data.data)
        })
        .catch((err) => {
            const data = err.response.data.msg
            let msg = null
            if (data === '1') {
                msg = '二维码验证码失败'
            } else if (data === '2') {
                msg = '二维码已失效'
                expired.value = true
            } else if (data === '3') {
                msg = '二维码未登录'
            } else if (data === '4') {
                msg = '二维码已扫描,请确认'
            }
            ElNotification({
                title: 'Warning',
                message: msg,
                type: 'warning',
            })
        })
    loading.value = false
}
// onMounted
onMounted(() => {
    handleRefreshQrcode()
    get_accounts()
})
</script>
<style lang="scss" scoped>
.more-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    cursor: pointer;
    border-radius: 6px;
    &:hover {
        background-color: #f0f0f0;
    }
}
</style>
<style>
.el-collapse {
    border: 0;
}
.el-collapse-item__wrap,
.el-collapse-item__header {
    border: 0;
    background-color: #fafafa;
}
</style>
