<template>
    <div>
        <header class="w-full border-b py-10">
            <div class="mx-auto h-full w-[1200px]">
                <h1 class="text-3xl">设置</h1>
            </div>
        </header>
        <main>
            <div class="mx-auto w-[1200px] py-10 flex">
                <div class="flex flex-col justify-start items-stretch">
                    <div class="w-[240px] mr-6">
                        <a
                            v-for="(sidemenu, index) in sidemenus"
                            :class="{ active: route.name == sidemenu.name }"
                            class="sidemenu-item"
                            @click="router.push({ name: sidemenu.name })"
                        >
                            {{ sidemenu.title }}
                        </a>
                    </div>
                </div>
                <div class="flex-1 ml-6">
                    <router-view></router-view>
                </div>
            </div>
        </main>
    </div>
</template>
<script setup>
import { useRouter, useRoute } from 'vue-router'
const route = useRoute()
const router = useRouter()
const sidemenus = [
    {
        title: '账号',
        name: 'accountsetting',
    },
    {
        title: '课程',
        name: 'coursesetting',
    },
    {
        title: '签到',
        name: 'sign',
    },
    {
        title: '消息推送',
        name: 'msg',
    },
]
</script>
<style lang="scss" scoped>
.sidemenu-item {
    text-decoration: none;
    display: block;
    padding: 8px 12px;
    margin-left: -12px;
    font-size: 15px;
    color: #444;
    transition: color 0.2s ease, background-color 0.2s ease;
    border-radius: 6px;
    cursor: pointer;
    &.active {
        font-weight: bold;
        color: #000;
    }
    &:hover {
        background-color: #eaeaea;
    }
}
</style>
