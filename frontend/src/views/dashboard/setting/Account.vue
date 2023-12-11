<template>
    <main v-if="user !== null">
        <section class="rounded-md border mb-8 overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">用户名</h1>
                </div>
                <!-- 介绍 -->
                <div>
                    <p class="my-3 text-sm text-[#171717]">
                        请输入您的全名或您认为合适的显示名称。
                    </p>
                </div>
                <!-- 输入 -->
                <div class="w-[300px]">
                    <el-input type="text" v-model="user.userinfo.nickname" />
                </div>
            </div>
            <footer class="px-6 py-3 bg-[#fafafa]">
                <div class="min-h-[30px] flex justify-between items-center">
                    <div class="text-sm text-[#666]">请最多使用48个字符。</div>
                    <div>
                        <el-button>保存</el-button>
                    </div>
                </div>
            </footer>
        </section>
        <section class="rounded-md border mb-8 overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">邮箱</h1>
                </div>
                <!-- 介绍 -->
                <div>
                    <p class="my-3 text-sm text-[#171717]">
                        请输入您想要使用Chaoxing登录的电子邮件地址。
                    </p>
                </div>
                <!-- 输入 -->
                <div class="w-[300px]">
                    <el-input type="text" v-model="user.email" />
                </div>
            </div>
            <footer class="px-6 py-3 bg-[#fafafa]">
                <div class="min-h-[30px] flex justify-between items-center">
                    <div class="text-sm text-[#666]">我们会发邮件给您确认更改。</div>
                    <div>
                        <el-button>保存</el-button>
                    </div>
                </div>
            </footer>
        </section>
        <section class="rounded-md border mb-8 overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">Chaoxing ID</h1>
                </div>
                <!-- 介绍 -->
                <div>
                    <p class="my-3 text-sm text-[#171717]">这是您在Chaoxing中的用户ID。</p>
                </div>
                <!-- 输入 -->
                <div class="w-[300px]">
                    <el-input type="text" disabled v-model="user.userId" />
                </div>
            </div>
            <footer class="px-6 py-3 bg-[#fafafa]">
                <div class="min-h-[30px] flex justify-between items-center">
                    <div class="text-sm text-[#666]">与Chaoxing API交互时使用。</div>
                </div>
            </footer>
        </section>
        <section class="rounded-md border border-red-100 mb-8 overflow-hidden">
            <div class="p-6 border-b border-red-100">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">删除账户</h1>
                </div>
                <!-- 介绍 -->
                <div>
                    <p class="my-3 text-sm text-[#171717]">
                        从Chaoxing平台永久删除您的个人帐户及其所有内容。此操作是不可逆的，因此请谨慎继续。
                    </p>
                </div>
            </div>
            <footer class="px-6 py-3 bg-red-100">
                <div class="min-h-[30px] flex justify-end items-center">
                    <el-button>删除个人账户</el-button>
                </div>
            </footer>
        </section>
    </main>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores'
const authStore = useAuthStore()
// refs
const user = ref(null)

onMounted(() => {
    if (authStore.isAuth) {
        user.value = authStore.user
    }
})
</script>
