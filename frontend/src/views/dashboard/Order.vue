<template>
    <div>
        <header class="w-full border-b py-10">
            <div class="mx-auto h-full w-[1200px]">
                <h1 class="text-3xl">订单</h1>
            </div>
        </header>
        <main>
            <!-- table -->
            <div class="mx-auto w-[1200px] py-6">
                <div>
                    <el-table
                        :data="orders"
                        style="width: 100%"
                        :header-cell-style="{ 'text-align': 'center' }"
                        :cell-style="{ 'text-align': 'center' }"
                        @selection-change="handleSelectionChange"
                    >
                        <el-table-column type="selection" width="50" />
                        <el-table-column property="order_id" label="订单编号" width="120" />
                        <el-table-column property="platform" label="平台" width="120" />
                        <el-table-column property="account_phone" label="账号" width="130" />
                        <el-table-column property="course_name" label="课程名称" width="270" />
                        <el-table-column property="cost" label="硬币" width="60" />
                        <el-table-column label="进度" width="200">
                            <template #default="scope">
                                <el-progress
                                    :percentage="scope.row.progress"
                                    :color="customColorMethod"
                                />
                            </template>
                        </el-table-column>
                        <el-table-column label="下单时间" width="150">
                            <template #default="scope">
                                {{ formatTimestamp(scope.row.order_time) }}
                            </template>
                        </el-table-column>
                        <el-table-column label="状态" width="100">
                            <template #default="scope"> {{ states[scope.row.state] }}</template>
                        </el-table-column>
                    </el-table>
                </div>
                <div class="flex justify-between my-6">
                    <div class="flex items-center">
                        <div class="btn border text-sm">批量删除</div>
                        <div class="btn border text-sm mx-3">批量补单</div>
                    </div>
                    <div>
                        <el-pagination
                            v-model:current-page="currentPage"
                            v-model:page-size="pageSize"
                            :page-sizes="[10, 20, 40]"
                            layout="total, sizes, prev, pager, next, jumper"
                            :total="totalSize"
                            @size-change="handleGetOrders"
                            @current-change="handleGetOrders"
                        />
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { ElNotification } from 'element-plus'
import { formatTimestamp } from '@/utils/time'
import { get_course_orders } from '@/requests/api'
// constants
const states = {
    0: '提交中',
    1: '正在进行',
    2: '已完成',
    3: '失败',
    4: '取消',
    5: '补单中'
}
// refs
const pageSize = ref(10)
const currentPage = ref(1)
const totalSize = ref(0)
const orders = ref([])
const seletions = ref([])
// functions
const handleSelectionChange = (val) => {
    seletions.value = val
}
const handleGetOrders = () => {
    get_course_orders({
        cursor: currentPage.value - 1,
        limit: pageSize.value,
    })
        .then((res) => {
            orders.value = res.data.data.items
            totalSize.value = res.data.data.total
        })
        .catch((err) => {
            ElNotification({
                title: 'Error',
                message: `获取订单失败:${err.response.data.msg}`,
                type: 'error',
            })
        })
}
onMounted(() => {
    handleGetOrders()
})
</script>
