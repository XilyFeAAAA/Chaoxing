<template>
    <div>
        <header class="w-full border-b py-10">
            <div class="mx-auto h-full w-[1200px] flex items-center justify-between">
                <div>
                    <h1 class="text-3xl">通知</h1>
                </div>
                <div class="flex items-center">
                    <div>
                        <svg-icon type="mdi" size="30" :path="mdiCog" class="text-gray-600 cursor-pointer hover:text-gray-500"/>
                    </div>
                    <div class="ml-6" @click="handleMarkRead">
                        <svg-icon type="mdi" size="30" :path="mdiCheckCircle" class="text-gray-600 cursor-pointer hover:text-gray-500"/>
                    </div>
                    <div class="ml-6" @click="handleClearNotification">
                        <svg-icon type="mdi" size="30" :path="mdiDeleteSweep" class="text-gray-600 cursor-pointer hover:text-gray-500"/>
                    </div>
                </div>
            </div>
        </header>
        <main>
            <!-- table -->
            <div class="mx-auto w-[1200px]" v-if="notifications.length">
                <el-collapse v-model="activeCollapseName" accordion class="text-gray-600" @change="handleCollapseChange">
                    <el-collapse-item v-for="(notification, index) in notifications" :key="index" :name="notification.notification_id">
                        <template #title>
                            <div class="flex items-center justify-between w-full pr-2">
                                <div class="flex items-center">
                                    <svg-icon v-if="notification.read" type="mdi" size="17" :path="mdiMessage"/>
                                    <svg-icon v-else type="mdi" size="17" :path="mdiMessageBadge"/>
                                    <p class="ml-3 font-bold">{{ notification.title }}</p>
                                </div>
                                <div class="text-sm">
                                    {{ formatTimestamp(notification.created_time) }}
                                </div>
                            </div>
                        </template>
                        <div class="pb-6 whitespace-pre">
                            {{ notification.message }}
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </div>
        </main>
    </div>
</template>
<script setup>
import {onMounted, ref} from 'vue'
import {mdiCheckCircle, mdiCog, mdiDeleteSweep, mdiMessage, mdiMessageBadge} from '@mdi/js';
import {del_notificaion, get_notification, read_notification} from "@/requests/api";
import {ElNotification} from "element-plus";
import {formatTimestamp} from '@/utils/time'
// refs
const activeCollapseName = ref(null)
const not_read = ref()
const notifications = ref([])
// functions
const handleGetNotification = () => {
    get_notification().then((res) => {
        not_read.value = res.data.data.not_read
        notifications.value = res.data.data.notifications
    })
}
const handleClearNotification = () => {
    del_notificaion().then(res => {
        not_read.value = 0
        notifications.value = []
    }).catch(err => {
        ElNotification({
            type: 'error',
            message: '消息清空失败'
        })
    })
}
const handleMarkRead = (ids) => {
    read_notification(ids).then(res => {
        not_read.value = 0
        notifications.value = notifications.value.map(obj => {
            if (ids.includes(obj.notification_id)) {
                return {...obj, read: true};
            }
            return obj;
        });
    })
}
const handleCollapseChange = (activeName) => {
    handleMarkRead([activeName])
}
onMounted(() => {
    handleGetNotification()
})
</script>
<style>
.el-collapse-item__header {
    height: 80px !important;
}
</style>