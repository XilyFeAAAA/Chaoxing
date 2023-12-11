<template>
    <div class="p-5">
        <div class="bg-white rounded-md shadow">
            <div ref="searchRef" class="px-6 pt-5">
                <el-form :model="searchFormData" label-width="100px">

                </el-form>
            </div>
            <Table
                :columns="columns"
                :dataSource="tableData"
                :options="options"
                :fetch="fetch"
            >
                <!-- 订单编号 -->
                <template #orderId="{ index, row }">
                    {{ row.order_id }}
                </template>
                <!-- 详情 -->
                <template #info="{ index, row }">
                    {{ row.info }}
                </template>
                <!-- 日志时间 -->
                <template #logTime="{ index, row }">
                    {{ formatTimestamp(row.log_time) }}
                </template>
            </Table>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import {useRoute, useRouter} from "vue-router";
import { get_admin_logger } from '@/requests/api'
import { ElMessage } from 'element-plus'
import { formatTimestamp } from '@/utils/time'
import Table from '@/components/Table.vue'
const route = useRoute()
const router = useRouter()
// constants
const columns = [
    {
        label: '订单编号',
        width: 150,
        scopedSlots: 'orderId',
    },

    {
        label: '详情',
        scopedSlots: 'info',
    },
    {
        label: '日志时间',
        width: 200,
        scopedSlots: 'logTime',
    }
]
// refs
const searchRef = ref()
const options = ref({
    showIndex: true,
    extHeight: 109,
})
const searchFormData = ref({
    order_id: route.query.order_id
})
const tableData = ref({
    items: [],
    limit: 15,
    cursor: 1,
    total: 0,
})
// functions
const fetch = () => {
    get_admin_logger({
        limit: tableData.value.limit,
        cursor: tableData.value.cursor - 1,
        keyword: searchFormData.value,
    })
        .then((res) => {
            tableData.value = Object.assign({}, tableData.value, res.data.data)
        })
        .catch((err) => {
            ElMessage({
                type: 'error',
                message: '日志数据获取失败',
            })
        })
}
onMounted(() => {

    console.log(route.query.order_id)
    if (!route.query.order_id){
        router.go(-1)
    }
})
</script>