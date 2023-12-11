<template>
    <main v-if="form">
        <section class="rounded-md border mb-8 overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">题库</h1>
                </div>
                <!-- 输入 -->
                <div class="w-[300px] mt-4">
                    <el-form :model="form.searcher" label-width="140px" label-position="left">
                        <el-form-item label="启用付费题库">
                            <el-switch v-model="form.searcher.use_paid" />
                        </el-form-item>
                    </el-form>
                </div>
            </div>
            <footer class="px-6 py-3 bg-[#fafafa]">
                <div class="min-h-[30px] flex justify-between items-center">
                    <div class="text-sm text-[#666]">题库有关配置。</div>
                </div>
            </footer>
        </section>
        <section class="rounded-md border mb-8 overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">章节</h1>
                </div>
                <!-- 输入 -->
                <div class="w-[300px] mt-4">
                    <el-form :model="form.task" label-width="140px" label-position="left">
                        <el-form-item label="启用">
                            <el-switch v-model="form.task.enable" />
                        </el-form-item>
                        <el-form-item label="完成视频任务点">
                            <el-switch v-model="form.task.video_enable" />
                        </el-form-item>
                        <el-form-item label="完成音频任务点">
                            <el-switch v-model="form.task.audio_enable" />
                        </el-form-item>
                        <el-form-item label="完成阅读任务点">
                            <el-switch v-model="form.task.read_enable" />
                        </el-form-item>
                        <el-form-item label="完成文档任务点">
                            <el-switch v-model="form.task.document_enable" />
                        </el-form-item>
                        <el-form-item label="完成直播任务点">
                            <el-switch v-model="form.task.live_enable" />
                        </el-form-item>
                        <el-form-item label="完成书籍任务点">
                            <el-switch v-model="form.task.book_enable" />
                        </el-form-item>
                        <el-form-item label="完成章节测试">
                            <el-switch v-model="form.task.quiz_enable" />
                        </el-form-item>
                        <el-form-item label="间隔时间(s)">
                            <el-input v-model="form.task.interval" />
                        </el-form-item>
                    </el-form>
                </div>
            </div>
            <footer class="px-6 py-3 bg-[#fafafa]">
                <div class="min-h-[30px] flex justify-between items-center">
                    <div class="text-sm text-[#666]">章节任务点有关配置</div>
                </div>
            </footer>
        </section>
        <section class="rounded-md border mb-8 overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">作业</h1>
                </div>
                <!-- 输入 -->
                <div class="w-[300px] mt-4">
                    <el-form :model="form.work" label-width="140px" label-position="left">
                        <el-form-item label="启用">
                            <el-switch v-model="form.work.enable" />
                        </el-form-item>
                        <el-form-item label="暂存不提交">
                            <el-switch v-model="form.work.save" />
                        </el-form-item>
                        <el-form-item label="没有答案时随机选择">
                            <el-switch v-model="form.work.random" />
                        </el-form-item>
                    </el-form>
                </div>
            </div>
            <footer class="px-6 py-3 bg-[#fafafa]">
                <div class="min-h-[30px] flex justify-between items-center">
                    <div class="text-sm text-[#666]">课程作业有关配置。</div>
                </div>
            </footer>
        </section>
        <section class="rounded-md border mb-8 overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">考试</h1>
                </div>
                <!-- 输入 -->
                <div class="w-[300px] mt-4">
                    <el-form :model="form.exam" label-width="140px" label-position="left">
                        <el-form-item label="启用">
                            <el-switch v-model="form.exam.enable" />
                        </el-form-item>
                    </el-form>
                </div>
            </div>
            <footer class="px-6 py-3 bg-[#fafafa]">
                <div class="min-h-[30px] flex justify-between items-center">
                    <div class="text-sm text-[#666]">课程考试有关配置。</div>
                </div>
            </footer>
        </section>
        <section class="rounded-md border overflow-hidden">
            <div class="p-6 border-b">
                <!-- 标题 -->
                <div>
                    <h1 class="text-xl font-bold">签到</h1>
                </div>
                <!-- 介绍 -->
                <div>
                    <p class="my-3 text-sm text-[#171717]">
                        从Chaoxing平台永久删除您的个人帐户及其所有内容。此操作是不可逆的，因此请谨慎继续。
                    </p>
                </div>
            </div>
            <footer class="px-6 py-3">
                <div class="min-h-[30px] flex justify-end items-center">
                    <el-button>删除个人账户</el-button>
                </div>
            </footer>
        </section>
    </main>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import { get_setting, set_setting } from '@/requests/api'
import { ElNotification } from 'element-plus'
const form = ref(null)
// functions
const handleGetSetting = () => {
    get_setting('course').then((res) => {
        form.value = res.data.data
    })
}
const handleSetSetting = () => {
    set_setting('course', form.value).catch((err) => {
        ElNotification({
            title: 'Error',
            message: '上传配置失败',
            type: 'error',
        })
    })
}
watch(
    form,
    (to, prev) => {
        if (prev != null) {
            handleSetSetting()
        }
    },
    { deep: true },
)
onMounted(() => {
    handleGetSetting()
})
</script>
