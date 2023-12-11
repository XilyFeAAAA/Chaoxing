<template>
    <div>
        <!-- header -->
        <header class="flex items-center justify-between">
            <div class="flex items-center">
                <TriangleIcon class="cursor-pointer"/>
                <div class="mx-7 cursor-pointer" v-if="authStore.user.info">
                    {{ authStore.user.info.nickname }}
                </div>
            </div>
            <div class="flex items-center">
                <div class="border rounded">
                    <el-button  text>FeedBack</el-button>
                </div>
                <div class="mx-4 text-sm cursor-pointer">Help</div>
                <div class="mx-4 text-sm cursor-pointer">Docs</div>
                <div class="ml-4 mr-8">
                    <el-popover ref="InmailRef" placement="bottom-end" :width="400" trigger="click">
                        <template #reference>
                            <el-badge
                                :value="not_read"
                                :hidden="!not_read"
                                :max="99"
                                class="item"
                            >
                                <button
                                    class="flex items-center justify-center h-8 w-8 rounded-full border text-gray-500"
                                >
                                    <svg-icon
                                        type="mdi"
                                        size="20"
                                        :path="mdiBellOutline"
                                    ></svg-icon>
                                </button>
                            </el-badge>
                        </template>
                        <template #default>
                            <div class="w-[400px] h-[240px] p-4 flex flex-col">
                                <div class="flex justify-between item-center px-5 rounded-lg h-[44px] bg-gray-100">
                                    <div class="flex items-center ">
                                        <p class="font-bold text-2xl">
                                            {{ not_read }}
                                        </p>
                                        <p class="ml-4 font-bold">条新通知</p>
                                        <p class="ml-4 cursor-pointer">清除全部</p>
                                    </div>
                                    <div class="flex items-center cursor-pointer text-gray-400 hover:text-gray-500 transition-colors"
                                        @click="handleJumpInmail"
                                    >
                                        <p class="text-xs">查看更多</p>
                                        <svg-icon type="mdi" size="16" :path="mdiArrowRightThin"/>
                                    </div>
                                </div>
                                <div class="flex-1 pt-4">
                                    <div v-if="notifications.length">
                                        <ul class="h-[144px]">
                                            <li v-for="(notification, index) in notifications.slice(0, 2)" :key="index">
                                                <div class="h-[72px] px-5 text-xs">
                                                    <div class="flex">
                                                        <div class="w-6">
                                                            <svg-icon type="mdi" size="16" :path="mdiMessageBadge" />
                                                        </div>
                                                        <div class="text-[14px]  font-bold">
                                                            {{ notification.title }}
                                                        </div>
                                                    </div>
                                                    <div class="pl-6 my-1 truncate">
                                                        {{ notification.message }}
                                                    </div>
                                                    <div class="pl-6 font-bold">
                                                        {{ getTimeAgo(notification.created_time) }}
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                    <div v-else class="h-full flex justify-center items-center">
                                        <div class="flex flex-col items-center">
                                            <div
                                                class="flex justify-center items-center w-12 h-12 rounded-full bg-[#fafafa]"
                                            >
                                                <svg-icon type="mdi" :path="mdiMailboxUpOutline"/>
                                            </div>
                                            <div class="text-[#666] my-4">暂无新通知</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </el-popover>
                </div>
                <div>
                    <el-popover ref="UserCardRef" placement="bottom-end" :width="250" trigger="click">
                        <template #reference>
                            <button
                                class="flex items-center justify-center h-8 w-8 rounded-full border overflow-hidden"
                            >
                                <img
                                    src="@/assets/images/logo.png"
                                />
                            </button>
                        </template>
                        <template #default>
                            <div class="py-5" v-if="authStore.user.userinfo">
                                <div class="px-5 py-1 truncate">
                                    email: {{ authStore.user.email }}
                                </div>
                                <div class="px-5 py-1 truncate">
                                    coins: {{ authStore.user.userinfo.money }}
                                </div>
                                <div class="text-[15px] border-y my-2 py-2">
                                    <div class="pop-item">
                                        <div>Dashboard</div>
                                        <div>
                                            <svg-icon
                                                type="mdi"
                                                size="20"
                                                :path="mdiBulletinBoard"
                                            ></svg-icon>
                                        </div>
                                    </div>
                                    <div class="pop-item">
                                        <div>Settings</div>
                                        <div>
                                            <svg-icon
                                                type="mdi"
                                                size="20"
                                                :path="mdiCogOutline"
                                            ></svg-icon>
                                        </div>
                                    </div>
                                    <div class="pop-item">
                                        <div>Create Team</div>
                                        <div>
                                            <svg-icon
                                                type="mdi"
                                                size="22"
                                                :path="mdiPlus"
                                            ></svg-icon>
                                        </div>
                                    </div>
                                </div>
                                <div class="text-[15px]">
                                    <div class="pop-item">
                                        <div>Theme</div>
                                        <div>
                                            <el-switch
                                                v-model="value"
                                                active-text="Dark"
                                                inactive-text="Light"
                                            />
                                        </div>
                                    </div>
                                    <div class="pop-item" @click="handleLogout">
                                        <div>Log Out</div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </el-popover>
                </div>
            </div>
        </header>
        <!-- submenu -->
        <div class="submenu flex items-center px-6">
            <a
                v-for="(submenu, idx) in submenus"
                class="menu-item"
                :class="{ active: submenu.route_name === route.name }"
                @click="router.push({ name: submenu.route_name })"
            >
                {{ submenu.name }}
            </a>
        </div>
        <main class="h-[calc(100vh-112px)]">
            <router-view></router-view>
        </main>
    </div>
</template>
<script setup>
import {
    mdiArrowRightThin,
    mdiBellOutline,
    mdiBulletinBoard,
    mdiCogOutline,
    mdiMailboxUpOutline,
    mdiPlus,
    mdiMessageBadge
} from '@mdi/js'
import {useRoute, useRouter} from 'vue-router'
import {onMounted, ref} from 'vue'
import {get_notification} from '@/requests/api'
import {useAuthStore} from '@/stores/auth'
import TriangleIcon from '@/components/icons/triangle.vue'
import {getTimeAgo} from "../../utils/time";

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const not_read = ref(0)
const UserCardRef = ref(null)
const InmailRef = ref(null)
// constants
const submenus = [
    {name: '课程', route_name: 'courses'},
    {name: '账户', route_name: 'account'},
    {name: '订单', route_name: 'order'},
    {name: '帮助', route_name: 'help'},
    {name: '设置', route_name: 'accountsetting'},
]
//refs
const active_submenu = ref(null)
const notifications = ref([])
// functions
const handleLogout = () => {
    authStore.logout()
    router.push({name: 'login'})
}
const handleClosePopover = ( popover ) => {
    popover.hide()
}
const handleGetNotification = () => {
    get_notification().then((res) => {
        not_read.value = res.data.data.not_read
        notifications.value = res.data.data.notifications.filter(obj => obj.read === false);
    })
}

const handleJumpInmail = () => {
    handleClosePopover(InmailRef.value)
    router.push({name: 'inmail'})
}
// onMounted
onMounted(() => {
    handleGetNotification()
})
</script>
<style lang="scss" scoped>
header {
    font-family: ChaoXing-1;
    padding: 0 var(--dashboard-header-padding);
    height: var(--dashboard-header-height);
}

.submenu {
    height: 48px;
    box-shadow: inset 0 -1px rgba(0, 0, 0, 0.08);

    .menu-item {
        position: relative;
        font-size: 14px;
        color: #666;
        border-radius: 5px;
        padding: 6px 12px;
        margin-right: 5px;
        cursor: pointer;
        transition: background-color 0.2s;

        &:hover {
            background-color: hsla(0, 0%, 92%);
        }

        &.active {
            color: #000;

            &::before {
                content: '';
                display: block;
                position: absolute;
                height: 0;
                left: 9px;
                right: 9px;
                bottom: -7px;
                border-bottom: 2px solid;
            }
        }
    }
}

.pop-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 20px;
    cursor: pointer;

    &:hover {
        background-color: rgba(0, 0, 0, 0.05);
    }
}

/* 修改滚动条的样式 */
::-webkit-scrollbar {
    width: 5px; /* 滚动条宽度 */
}

/* 滚动条轨道 */
::-webkit-scrollbar-track {
    background-color: transparent; /* 轨道颜色 */
}

/* 滚动条滑块 */
::-webkit-scrollbar-thumb {
    background-color: #c1c1c1; /* 滑块颜色 */
    border-radius: 5px; /* 滑块圆角 */
}
</style>
