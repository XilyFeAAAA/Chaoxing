<template>
    <div class="w-hull min-h-full bg-[#fafafa]">
        <div class="m-auto max-w-[1200px]">
            <!--搜索框+按钮-->
            <div class="py-4">
                <div class="w-full my-3 flex items-stretch gap-2">
                    <div class="w-full flex items-center border rounded-md bg-white">
                        <span class="flex items-center h-10 px-3 -mr-3">
                            <svg-icon type="mdi" size="20" :path="mdiMagnify"></svg-icon>
                        </span>
                        <input
                            type="text"
                            placeholder="Search"
                            class="w-full h-10 px-3 outline-none"
                        />
                    </div>
                    <div class="switcher">
                        <button :class="{active: align==='grid'}" @click="align='grid'">
                            <svg-icon type="mdi" :path="mdiViewGridOutline"></svg-icon>
                        </button>
                        <button :class="{active: align==='list'}" @click="align='list'">
                            <svg-icon type="mdi" :path="mdiFormatListBulleted"></svg-icon>
                        </button>
                    </div>
                </div>
            </div>
            <div v-if="courses.length > 0" class="pb-5">
                <div v-if="align==='grid'" class="grid">
                    <div
                        v-for="(course, index) in courses"
                        :key="index"
                        class="course-card"
                        @click="handleQuery(course.course_id)"
                    >
                        <!-- img and base info -->
                        <div class="flex">
                            <div class="mr-3">
                                <img :src="course.img_url" class="w-24 rounded-sm"/>
                            </div>
                            <div class="flex-1 flex flex-col justify-between">
                                <div>{{ course.course_name }}</div>
                                <div class="text-sm text-gray-500">{{ course.course_teacher }}</div>
                            </div>
                        </div>
                        <!-- teacher -->
                        <div class="mt-6 text-xs text-[#666]">班级: {{ course.classroom }}</div>
                        <!-- time -->
                        <div class="my-1 text-xs text-[#666]">开课时间: {{ course.start_time }}</div>
                        <!-- progress -->
                        <div class="mt-3 text-xs text-[#000]">
                            状态: {{ course.is_open ? '开课' : '结课' }}
                        </div>
                    </div>
                </div>
                <div v-else class="list">
                    <div
                        v-for="(course, index) in courses"
                        :key="index"
                        class="course-list"
                        @click="handleQuery(course.course_id)"
                    >
                        <div class="flex items-stretch">
                            <div class="flex w-1/3">
                                <div class="mr-4">
                                    <img :src="course.img_url" class="w-10 h-10 rounded-full"/>
                                </div>
                                <div class="flex flex-col justify-between">
                                    <div class="text-sm hover:underline">
                                        {{ course.course_name }}
                                    </div>
                                    <div class="text-xs text-gray-500">
                                        {{ course.course_teacher }}
                                    </div>
                                </div>
                            </div>
                            <div class="flex-1 flex flex-col justify-between text-xs">
                                <div>班级: {{ course.classroom }}</div>
                                <div>开课时间: {{ course.start_time }}</div>
                            </div>
                            <div class="flex items-center">
                                <button class="flex justify-center items-center w-8 rounded h-8 hover:bg-[#e8e8e8] transition-all">
                                    <svg-icon type="mdi" size="18" :path="mdiDotsHorizontal"/>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <el-empty description="暂无课程" />
            </div>
        </div>
    </div>
</template>
<script setup>
import {onMounted, ref} from 'vue'
import {useRouter} from "vue-router";
import {useAuthStore} from '@/stores'
import {ElMessageBox, ElNotification} from 'element-plus'
import {mdiDotsHorizontal, mdiFormatListBulleted, mdiMagnify, mdiViewGridOutline} from '@mdi/js'
import {get_courses, pre_confirm, refresh_course} from '@/requests/api'

const router = useRouter()
const authStore = useAuthStore()
// refs
const align = ref('grid')
const courses = ref([])
// function
const handleGetCourse = () => {
    get_courses()
        .then((res) => {
            courses.value = res.data.data || []
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: '获取课程信息失败',
                type: 'error',
            })
        })
}
const handleQuery = (course_id) => {
    ElMessageBox.confirm(
        '是否选择该课程?',
        {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
        }
    )
        .then(() => {
            handleJumpConfirm(course_id)
        })
}

const handleJumpConfirm = (course_id) => {
    pre_confirm({course_id: course_id}).then(res => {
        router.push({
            name: 'confirm', params: {order_id: res.data.data}
        })
    }).catch(err => {
        ElNotification({
            type: 'error',
            message: '获取订单失败.'
        })
    })
}
const handleRefreshCourse = () => {
    refresh_course()
        .then((res) => {
            courses.value = res.data.data || []
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: err.response.data.msg,
                type: 'error',
            })
        })
}
onMounted(() => {
    handleGetCourse()
})

</script>
<style lang="scss" scoped>
.switcher {
    position: relative;
    display: flex;
    align-items: center;
    padding: 3px;
    background: #fff;
    border: 1px solid #eaeaea;
    border-radius: 5px;
    max-width: 100%;
    height: 40px;
    font-size: 0.875rem;
    -webkit-user-select: none;
    user-select: none;

    button {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 40px;
        height: 32px;
        color: #888;
        border-radius: 5px;
        background-color: #fff;

        &:hover {
            color: #000;
        }

        &.active {
            color: #000;
            background-color: #eaeaea;
        }
    }
}

.menu-btn {
    padding: 0 12px;
    height: 40px;
    min-width: 128px;
    max-width: 128px;
    font-size: 0.875rem;
    font-weight: 500;
    border: 1px solid #000;
    border-radius: 5px;
    color: #fff;
    background-color: #000;
    transition: all 0.15s;

    &:hover {
        color: #000;
        background-color: #fff;
    }
}

.grid {
    display: grid;
    grid-gap: 24px;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));

    .course-card {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        padding: 24px;
        background: #fff;
        border-radius: 8px;
        min-width: 350px;
        height: 100%;
        border: 1px solid #eaeaea;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
        cursor: pointer;
        user-select: none;
        transition: box-shadow 0.15s ease;

        &:hover {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
    }
}

.list {
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 0 0 1px rgba(0, 0, 0, .08), 0 4px 6px rgba(0, 0, 0, .04);

    .course-list {
        height: 78px;
        padding: 16px;
        cursor: pointer;
        border-bottom: 1px solid rgb(235, 235, 235);
    }
}
</style>
