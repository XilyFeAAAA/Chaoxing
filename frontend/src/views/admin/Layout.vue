<template>
    <div class="w-screen h-screen flex">
        <nav class="h-full bg-[#001529] overflow-auto">
            <div class="h-12 px-4 flex items-center">
                <img src="@/assets/images/logo.png" class="h-7" />
                <span v-if="!isCollapse" class="text-base font-bold text-white ml-2">
                  Chaoxing
                </span>
            </div>
            <div>
                <el-menu :collapse="isCollapse" :default-openeds="openeds" :default-active="route.path" collapse-transition router>
                    <template v-for="(menu, index) in menus" :key="index">
                        <el-sub-menu v-if="menu.children" :index="menu.index">
                            <template #title>
                                <svg-icon
                                    type="mdi"
                                    :path="menu.icon"
                                    size="18"
                                    class="mr-2"
                                ></svg-icon>
                                <span>{{ menu.text }}</span>
                            </template>
                            <el-menu-item
                                v-for="(sub, sub_index) in menu.children"
                                :key="sub_index"
                                :index="sub.index"
                                class=""
                            >
                                <div class="pl-2">{{ sub.text }}</div>
                            </el-menu-item>
                        </el-sub-menu>
                        <el-menu-item v-else :index="menu.index" class="w-[210px]">
                            <svg-icon
                                type="mdi"
                                :path="menu.icon"
                                size="18"
                                class="mr-2"
                            ></svg-icon>
                            <span>{{ menu.text }}</span>
                        </el-menu-item>
                    </template>
                </el-menu>
            </div>
        </nav>
        <main class="h-full flex-1 overflow-hidden">
            <div class="w-full h-12 bg-white shadow-lg z-10">
                <div class="h-full flex justify-between items-center">
                    <div class="flex items-center">
                        <div class="mr-2 header-btn" @click="isCollapse = !isCollapse">
                            <svg-icon type="mdi" size="18" :path="mdiBackburger" />
                        </div>
                        <div>
                        <el-breadcrumb separator="/">
                            <template v-for="item in menuBreadCrumbList">
                                <el-breadcrumb-item v-if="item.name">
                                    {{ item.name }}
                                </el-breadcrumb-item>
                            </template>
                        </el-breadcrumb>
                    </div>
                    </div>
                    <div class="flex flex-row-reverse items-center">
                        <div class="header-btn">
                            <svg-icon type="mdi" size="18" :path="mdiCogOutline" />
                        </div>
                        <div class="header-btn">
                            <svg-icon type="mdi" size="20" :path="mdiFullscreen" />
                        </div>
                        <div class="header-btn">
                            <svg-icon type="mdi" size="20" :path="mdiIdeogramCjkVariant" />
                        </div>
                        <div class="header-btn">
                            <svg-icon type="mdi" size="20" :path="mdiMagnify" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex flex-col w-full h-[calc(100%-48px)]">
                <el-tabs
                    type="border-card"
                    v-model="activeTab"
                    @tab-click="handleTabChange"
                    @edit="handleTabClose"
                >
                    <el-tab-pane
                        v-for="tab in tabs"
                        :name="tab.path"
                        :label="tab.menuName"
                        :closable="tabs.length > 1"
                    ></el-tab-pane>
                </el-tabs>
                <div class="flex-1 bg-[#f5f5f5]">
                    <router-view></router-view>
                </div>
            </div>
        </main>
    </div>
</template>
<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
    mdiCalendarCheckOutline,
    mdiAccountBoxOutline,
    mdiBackburger,
    mdiPoll,
    mdiCogOutline,
    mdiFullscreen,
    mdiIdeogramCjkVariant,
    mdiMagnify
} from '@mdi/js'
// router
const route = useRoute()
const router = useRouter()
// constant
const menus = [
    {
        icon: mdiPoll,
        text: '仪表盘',
        index: '/admin/dashboard',
        children: [
            { text: '工作台', index: '/admin/dashboard/workbench' },
            { text: '分析页', index: '/admin/dashboard/analysis' },
        ]
    },
    {
        icon: mdiCalendarCheckOutline,
        text: '订单管理',
        index: '/admin/order',
        children: [
            { text: '刷课订单', index: '/admin/order/course' },
            { text: '硬币订单', index: '/admin/order/coin' },
        ],
    },
    {
        icon: mdiAccountBoxOutline,
        text: '用户管理',
        index: '/admin/user',
        children: [
            { text: '用户列表', index: '/admin/user/member' },
            { text: '管理员列表', index: '/admin/user/admin' }
        ],
    },
    {
        icon: mdiAccountBoxOutline,
        text: '权限管理',
        index: '/admin/rbac',
        children: [
            { text: '权限列表', index: '/admin/rbac/permission' },
            { text: '角色列表', index: '/admin/rbac/role' }
        ],
    },
    {
        icon: mdiCogOutline,
        text: '设置',
        index: '/admin/setting',
    },
]
// refs
const activeTab = ref()
const isCollapse = ref(false)
const tabs = ref([])
const menuBreadCrumbList = ref([])
// computed
const openeds = computed(() => {
    let temp = []
    for (let menu of menus) {
        temp.push(menu.index)
    }
    return temp
})
// functions
const handleTabChange = (e) => {
    const tab = tabs.value.find(item => item.path === e.props.name)
    router.push({path: tab.path, query: tab.query})
}
const handleTabClose = (targetKey, action) => {
    if (action !== 'remove') {
        return
    }
    let cntPath = activeTab.value
    let temp = tabs.value
    if (targetKey === cntPath) {
        temp.forEach((tab, index) => {
            if (tab.path === targetKey) {
                let nextTab = temp[index + 1] || temp[index - 1]
                if (nextTab) {
                    cntPath = nextTab.path
                }
            }
        })
    }
    tabs.value = temp.filter((tab) => {
        return tab.path !== targetKey
    })
    if (cntPath !== route.path) {
        router.push(cntPath)
    }
}
watch(
    () => route,
    (to, prev) => {
        activeTab.value = route.path
        menuBreadCrumbList.value = route.matched
        let cnt = tabs.value.findIndex((item) => {
            return item.path === route.path
        })
        if (cnt === -1) {
            tabs.value.push({
                path: route.path,
                menuName: route.name,
                query: route.query
            })
        }else if (tabs.value[cnt].query !== route.query){
            tabs.value[cnt].query = route.query
        }
    },
    { immediate: true, deep: true },
)
</script>
<style lang="scss">
.header-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 48px;
    width: 48px;
    cursor: pointer;
    transition: background-color  cubic-bezier(0.4, 0, 0.2, 1) 150ms;
    &:hover {
        background-color: #f5f5f5;
    }

}
</style>
