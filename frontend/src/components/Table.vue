<template>
    <div>
        <!-- 表格 -->
        <el-table
            ref="tableRef"
            :data="dataSource.items || []"
            :stripe="options.stripe"
            :border="options.border"
            :height="tableHeight + 'px'"
            highlight-current-row
            @row-click="handleRowClick"
            @selection-change="handleSelectionChange"
        >
            <!-- 选择框 -->
            <el-table-column
                v-if="options.selectType && options.selectType == 'checkbox'"
                type="selection"
                width="50"
                align="center"
            >
            </el-table-column>
            <!-- 序号 -->
            <el-table-column
                v-if="options.showIndex"
                label="序号"
                type="index"
                width="60"
                align="center"
            >
            </el-table-column>
            <!-- 数据 -->
            <template v-for="(column, index) in columns">
                <template v-if="column.scopedSlots">
                    <el-table-column
                        :key="index"
                        :prop="column.prop"
                        :label="column.label"
                        :align="column.align || 'center'"
                        :width="column.width"
                        :min-width="column.minWidth"
                    >
                        <template #default="scope">
                            <slot
                                :name="column.scopedSlots"
                                :index="scope.$index"
                                :row="scope.row"
                            ></slot>
                        </template>
                    </el-table-column>
                </template>
                <template v-else>
                    <el-table-column
                        :key="index"
                        :prop="column.prop"
                        :label="column.label"
                        :align="column.align || 'center'"
                        :width="column.width"
                        :fixex="column.fixed"
                    >
                    </el-table-column>
                </template>
            </template>
        </el-table>
        <!-- 分页 -->
        <div class="px-4 py-3 flex justify-end">
            <el-pagination
                background
                :total="dataSource.total"
                :page-sizes="[15, 30, 50, 100]"
                v-model:page-size="dataSource.limit"
                v-model:current-page="dataSource.cursor"
                layout="sizes, prev, pager, next"
                @size-change="handlePageSizeChange"
                @current-change="handlePageNoChange"
            ></el-pagination>
        </div>
    </div>
</template>
<script setup>
import { ref, onUnmounted, onMounted } from 'vue'
// props
const props = defineProps({
    dataSource: Object,
    showPagination: {
        type: Boolean,
        default: true,
    },
    options: {
        type: Object,
        default: {
            tableHeight: null,
            stripe: true,
            border: false,
            extHeight: 0,
            showIndex: false,
        },
    },
    columns: Array,
    fetch: Function,
    initFetch: {
        type: Boolean,
        default: true,
    },
})
// emits
const emits = defineEmits(['rowSelected', 'rowClick'])
// constant
const topHeight = 108
// refs
const tableRef = ref()
const tableHeight = ref(
    props.options.tableHeight
        ? props.options.tableHeight
        : window.innerHeight - topHeight - props.options.extHeight,
)
// functions
const clearSelection = () => {
    tableRef.value.clearSelection()
}
const init = () => {
    if (props.initFetch && props.fetch) {
        props.fetch()
    }
}
// 行点击
const handleRowClick = (row) => {
    emits('rowClick', row)
}
// 多选
const handleSelectionChange = (row) => {
    emits('rowSelected', row)
}
// 切换页大小
const handlePageSizeChange = (size) => {
    props.dataSource.limit = size
    props.dataSource.cursor = 1
    props.fetch()
}
// 切换页码
const handlePageNoChange = (pageNo) => {
    props.dataSource.cursor = pageNo
    props.fetch()
}
// 页面改变大小回调
const handleResize = () => {
    tableHeight.value = props.options.tableHeight
        ? props.options.tableHeight
        : window.innerHeight - topHeight - props.options.extHeight
}
// expose
defineExpose(['clearSelection'])
onMounted(() => {
    window.addEventListener('resize', handleResize, false)
    init()
})
onUnmounted(() => {
    window.removeEventListener('resize', handleResize, false)
})
</script>
