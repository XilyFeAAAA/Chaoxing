<template>
    <div class="p-5">
        <div class="bg-white rounded-md shadow">
            <div ref="searchRef" class="px-6 py-5">
                <el-form :model="searchFormData" label-width="100px">
                    <el-row>
                        <div class="w-[300px]">
                            <el-form-item label="接口编号" prop="code__contains">
                                <el-input
                                    placeholder="请输入编号"
                                    v-model="searchFormData.code__contains"
                                    clearable
                                    @keyup.enter.native="fetch"
                                ></el-input>
                            </el-form-item>
                        </div>
                        <div class="w-[300px]">
                            <el-form-item label="接口名称" prop="name__contains">
                                <el-input
                                    placeholder="请输入名称"
                                    v-model="searchFormData.name__contains"
                                    clearable
                                    @keyup.enter.native="fetch"
                                ></el-input>
                            </el-form-item>
                        </div>
                        <div class="w-[300px]">
                            <el-form-item label="接口方法" prop="method">
                                <el-select v-model="searchFormData.method" placeholder="请选择方法" @change="fetch" clearable>
                                    <el-option label="GET" value="GET"/>
                                    <el-option label="POST" value="POST"/>
                                </el-select>
                            </el-form-item>
                        </div>
                        <div class="w-[300px]">
                            <el-form-item label="状态" prop="disabled">
                                <el-select  placeholder="请选择状态" v-model="searchFormData.disabled" @change="fetch" clearable>
                                    <el-option :value="true" label="禁用"/>
                                    <el-option :value="false" label="开放"/>
                                </el-select>
                            </el-form-item>
                        </div>
                    </el-row>
                    <el-row>
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
                </el-form>
            </div>
            <Table
                :columns="columns"
                :dataSource="tableData"
                :options="options"
                :fetch="fetch"
                @rowSelected="setRowSelected"
            >
                <!-- 接口编号 -->
                <template #pCode="{ index, row }">
                    {{ row.code }}
                </template>
                <!-- 接口方法 -->
                <template #pMethod="{ index, row }">
                    {{ row.method }}
                </template>
                <!-- 接口路径 -->
                <template #pResource="{ index, row }">
                    {{ row.resource }}
                </template>
                <!-- 接口名称 -->
                <template #pName="{ index, row }">
                    {{ row.name }}
                </template>
                <!-- 注释 -->
                <template #description="{ index, row }">
                    <div class="truncate">
                        {{ row.description }}
                    </div>
                </template>
                <!--状态-->
                <template #state="{ index, row }">
                    {{ row.disabled ? '禁用' : '开放' }}
                </template>
                <!-- 操作 -->
                <template #op="{ index, row }">
                    <div class="flex justify-center items-center">
                        <div class="op ok">编辑</div>
                        <div class="op ok">补单</div>
                        <div class="op error">删除</div>
                    </div>
                </template>
            </Table>
        </div>
    </div>

</template>
<script setup>
import {ref} from 'vue'
import {get_admin_permission} from '@/requests/api'
import {ElMessage} from 'element-plus'
import Table from '@/components/Table.vue'
// constants
const columns = [
    {
        label: '接口编号',
        width: 150,
        scopedSlots: 'pCode',
    },
    {
        label: '接口方法',
        width: 150,
        scopedSlots: 'pMethod',
    },
    {
        label: '接口路径',
        minWidth: 200,
        scopedSlots: 'pResource',
    },
    {
        label: '接口名称',
        width: 250,
        scopedSlots: 'pName',
    },
    {
        label: '注释',
        minWidth: 300,
        scopedSlots: 'description',
    },
    {
        label: '状态',
        width: 100,
        scopedSlots: 'state',
    },
    {
        label: '操作',
        prop: 'op',
        minWidth: 180,
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
    get_admin_permission({
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
                message: '权限列表获取失败',
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
