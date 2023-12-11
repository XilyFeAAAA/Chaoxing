<template>
    <div class="p-5">
        <div class="bg-white rounded-md shadow">
        <div ref="searchRef" class="px-6 pt-5">
            <el-form :model="searchFormData" label-width="100px">
                <el-row>
                    <div class="w-[300px]">
                        <el-form-item label="订单编号" prop="order_id__contains">
                            <el-input
                                placeholder="请输入编号"
                                v-model="searchFormData.order_id__contains"
                                clearable
                                @keyup.enter.native="fetch"
                            ></el-input>
                        </el-form-item>
                    </div>
                    <div class="w-[300px]">
                        <el-form-item label="用户名">
                            <el-input
                                placeholder="请输入昵称"
                                v-model="searchFormData['user.userinfo.nickname__contains']"
                                clearable
                                @keyup.enter.native="fetch"
                            ></el-input>
                        </el-form-item>
                    </div>

                    <div class="w-[300px]">
                        <el-form-item label="课程名称" prop="course_name__contains">
                            <el-input
                                placeholder="请输入编号"
                                v-model="searchFormData.course_name__contains"
                                clearable
                                @keyup.enter.native="fetch"
                            ></el-input>
                        </el-form-item>
                    </div>
                    <div class="pl-10">
                        <el-button @click="fetch">查询</el-button>
                        <el-button
                            @click="handleVerifyWarn"
                            :disabled="selectBatchList.length === 0"
                        >
                            批量补单
                        </el-button>
                        <el-button
                            @click="handleDeleteWarn"
                            :disabled="selectBatchList.length === 0"
                        >
                            批量删除
                        </el-button>
                    </div>
                </el-row>
                <el-row>
                    <div class="w-[300px]">
                        <el-form-item label="平台" prop="platform">
                            <el-select v-model="searchFormData.platform" placeholder="请选择平台">
                                <el-option label="超星学习通" :value="超星学习通" />
                            </el-select>
                        </el-form-item>
                    </div>
                    <div class="w-[300px]">
                        <el-form-item label="状态" prop="state">
                            <el-select
                                placeholder="请选择状态"
                                v-model="searchFormData.state"
                                clearable
                                style="width: 100%"
                            >
                                <el-option :value="true" label="已审核">已审核</el-option>
                                <el-option :value="false" label="未置顶"></el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-row>
            </el-form>
        </div>
        <Table
            :columns="columns"
            :dataSource="tableData"
            :options="options"
            :fetch="fetch"
            @rowSelected="setRowSelected"
        >
            <!-- 订单编号 -->
            <template #orderId="{ index, row }">
                {{ row.course_order.order_id }}
            </template>
            <!-- 用户编号 -->
            <template #userId="{ index, row }">
                {{ row.course_order.user_id }}
            </template>
            <!-- 用户名称 -->
            <template #nickname="{ index, row }">
                {{ row.user.nickname }}
            </template>
            <!-- 平台 -->
            <template #platform="{ index, row }">
                {{ row.course_order.platform }}
            </template>
            <!-- 手机号 -->
            <template #phone="{ index, row }">
                {{ row.account.phone }}
            </template>
            <!-- 课程名称 -->
            <template #courseName="{ index, row }">
                {{ row.course_order.course_name }}
            </template>
            <template #state="{ index, row }">
                {{ stateDict[row.course_order.state] }}
            </template>
            <!-- 下单时间 -->
            <template #orderTime="{ index, row }">
                {{ formatTimestamp(row.course_order.order_time) }}
            </template>
            <!-- 操作 -->
            <template #op="{ index, row }">
                <div class="flex justify-center items-center">
                    <div class="op ok" @click="router.push({name: '日志', query:{order_id: row.course_order.order_id}})">
                        日志
                    </div>
                    <div class="op ok">补单</div>
                    <div class="op error">删除</div>
                </div>
            </template>
        </Table>
    </div>
    </div>
</template>
<script setup>
import { ref } from 'vue'
import { get_admin_courseorder } from '@/requests/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatTimestamp } from '@/utils/time'
import {useRouter} from "vue-router";
import Table from '@/components/Table.vue'
const router = useRouter()
// constants
const stateDict = {
    0: '确认中',
    1: '正在完成',
    2: '完成',
    3: '失败',
    4: '取消订单',
    5: '补单'
}
const columns = [
    {
        label: '订单编号',
        width: 150,
        scopedSlots: 'orderId',
    },
    {
        label: '用户编号',
        width: 200,
        scopedSlots: 'userId',
    },
    {
        label: '用户名称',
        width: 150,
        scopedSlots: 'nickname',
    },
    {
        label: '平台',
        width: 150,
        scopedSlots: 'platform',
    },
    {
        label: '手机号',
        width: 150,
        scopedSlots: 'phone',
    },
    {
        label: '课程名称',
        scopedSlots: 'courseName',
    },
    {
        label: '订单状态',
        width: 100,
        scopedSlots: 'state',
    },
    {
        label: '下单时间',
        width: 150,
        scopedSlots: 'orderTime',
    },
    {
        label: '操作',
        prop: 'op',
        width: 180,
        scopedSlots: 'op',
    },
]
// refs
const searchRef = ref()
const options = ref({
    selectType: 'checkbox',
    extHeight: 209,
})
const searchFormData = ref({})
const selectBatchList = ref([])
const tableData = ref({
    items: [],
    limit: 15,
    cursor: 1,
    total: 0,
})
// functions
const fetch = () => {
    get_admin_courseorder({
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
                message: '订单数据获取失败',
            })
        })
}
// 选择行回调
const setRowSelected = (rows) => {
    selectBatchList.value = []
    rows.forEach((row) => {
        selectBatchList.value.push(row.article.id)
    })
}
// 删除文章
const handleDeleteArticle = (ids) => {
    adminDeleteArticle({ ids })
        .then((res) => {
            fetch()
        })
        .catch((err) => {
            ElMessage({
                type: 'error',
                message: '文章删除失败',
            })
        })
}
// 置顶文章
const handlePinArticle = (ids, pinned) => {
    adminUpdateArticle({ ids, update: { pinned } })
        .then((res) => {
            fetch()
        })
        .catch((err) => {
            ElMessage({
                type: 'error',
                message: `文章${pinned ? '置顶' : '取消置顶'}失败`,
            })
        })
}
// 审核文章
const handleVerifyArticle = (ids) => {
    adminUpdateArticle({ ids, update: { verify: 1 } })
        .then((res) => {
            fetch()
        })
        .catch((err) => {
            ElMessage({
                type: 'error',
                message: '文章审核失败',
            })
        })
}
// 批量审核提醒
const handleVerifyWarn = () => {
    ElMessageBox.confirm('此操作不可逆，是否继续?', '批量审核文章', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(() => {
        handleVerifyArticle(selectBatchList.value)
    })
}
// 批量删除提醒
const handleDeleteWarn = () => {
    ElMessageBox.confirm('此操作不可逆，是否继续?', '批量删除文章', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(() => {
        handleDeleteArticle(selectBatchList.value)
    })
}
</script>
<style lang="scss" scoped>
.op {
    margin: 0 4px;
    font-size: 13px;
    cursor: pointer;
    &.ok {
        color: rgb(9, 96, 189);
        &:hover {
            color: rgb(0, 68, 150);
            text-decoration: underline;
        }
    }
    &.error {
        color: rgb(237, 111, 111);
        &:hover {
            color: rgb(243, 156, 156);
            text-decoration: underline;
        }
    }
}
</style>
