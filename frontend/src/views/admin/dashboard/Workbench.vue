<template>
    <div class="h-full flex flex-col">
        <div class="px-6 py-5 bg-white shadow-sm">
            <div class="pt-3">
                <div class="flex items-center">
                    <div class="h-[72px] w-[72px] ">
                        <img src="https://vben.vvbin.cn/assets/header-1b5fa5f8.jpg" class="rounded-full">
                    </div>
                    <div class="flex flex-col justify-center ml-5">
                        <p class="text-lg mb-2">早安, Vben Admin, 开始您一天的工作吧！</p>
                        <span class="text-[#00000073] text-sm">今日晴，20℃ - 32℃！</span>
                    </div>
                    <div class="flex-1 flex justify-end items-center">
                        <el-statistic title="待办" :value="268500" class="text-end"/>
                        <el-statistic title="项目" :value="268500" class="ml-5 text-end"/>
                        <el-statistic title="团队" :value="268500" class="ml-5 text-end"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex-1 flex p-4 ">
            <div class="w-[70%] mr-3">
                <el-card class="mb-5">
                    <template #header>
                        <div class="flex justify-between items-center">
                            <span>项目</span>
                            <el-button  text>更多</el-button>
                        </div>
                    </template>
                    <div class="p-5">
                        dd
                    </div>
                </el-card>
                <el-card >
                    <template #header>
                        <div class="flex justify-between items-center">
                            <span>动态</span>
                            <el-button  text>更多</el-button>
                        </div>
                    </template>
                    <div class="p-5">
                        dd
                    </div>
                </el-card>
            </div>
            <div class="w-[30%]">
                <el-card class="mb-5">
                    <template #header>
                        <div class="flex justify-between items-center">
                            <span>快捷导航</span>
                        </div>
                    </template>
                    <div class="flex flex-wrap">
                        <div v-for="(navigation, index) in navigations"
                             :key="index"
                             class="w-1/3 p-6 cursor-pointer flex flex-col items-center card-shadow">
                            <svg-icon type="mdi" size="20" :path="navigation.icon"></svg-icon>
                            <span class="text-sm mt-2">{{ navigation.name}}</span>

                        </div>

                    </div>
                </el-card>
                <el-card class="px-4 py-8">
                    <img src="@/assets/images/illustration.svg">
                </el-card>
            </div>
        </div>
    </div>
</template>


<script setup>
import { mdiChartBellCurve } from '@mdi/js'
//constants
const navigations = [
    {
        name: '分析页',
        icon: mdiChartBellCurve ,
    },{
        name: '分析页',
        icon: mdiChartBellCurve ,
    },{
        name: '分析页',
        icon: mdiChartBellCurve ,
    },{
        name: '分析页',
        icon: mdiChartBellCurve ,
    },{
        name: '分析页',
        icon: mdiChartBellCurve ,
    },{
        name: '分析页',
        icon: mdiChartBellCurve ,
    }
]
</script>


<style scoped lang="scss">
    .card-shadow{
        box-shadow: 1px 0 0 0 #f0f0f0, 0 1px 0 0 #f0f0f0, 1px 1px 0 0 #f0f0f0, 1px 0 0 0 #f0f0f0 inset;
    }
</style>