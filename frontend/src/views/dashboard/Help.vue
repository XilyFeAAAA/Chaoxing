<template>
    <div>
        <header class="w-full border-b py-10">
            <div class="mx-auto h-full w-[1200px]">
                <h1 class="text-3xl">帮助</h1>
            </div>
        </header>
        <main>
            <!-- table -->
            <div class="mx-auto w-[1200px] py-6">
                <el-timeline>
                    <el-timeline-item hide-timestamp>
                        <div class="flex justify-between py-2">
                            <!-- description -->
                            <div class="flex-1 pr-3">
                                <div class="font-bold text-base">绑定超星学习通账号</div>
                                <div class="text-gray-600 mt-2">
                                    输入账号(手机号)、密码、图形验证码进行绑定。网站不会对密码进行保存,仅用于获取Cookie进行登陆,没有泄漏风险。
                                </div>
                            </div>
                            <!-- image -->
                            <div class="border rounded-xl overflow-hidden">
                                <img src="@/assets/images/guide-1.png" width="700" />
                            </div>
                        </div>
                    </el-timeline-item>
                    <el-timeline-item hide-timestamp>
                        <div class="flex justify-between py-2">
                            <!-- description -->
                            <div class="flex-1 pr-3">
                                <div class="font-bold text-base">管理已绑定的账户</div>
                                <div class="text-gray-600 mt-2">
                                    1. 网站支持绑定多个超星学习通账号,点击
                                    <strong>设置为活跃账号</strong> 进行切换。
                                    <br />
                                    2.
                                    由于Cookie具有时效性,账号失效后需要点击<strong>刷新账号</strong>重新校验。
                                    <br />
                                    3. 删除账号后无法撤回,请谨慎操作。
                                </div>
                            </div>
                            <!-- image -->
                            <div class="border rounded-xl overflow-hidden">
                                <img src="@/assets/images/guide-2.png" width="700" />
                            </div>
                        </div>
                    </el-timeline-item>
                    <el-timeline-item hide-timestamp>
                        <div class="flex justify-between py-2">
                            <!-- description -->
                            <div class="flex-1 pr-3">
                                <div class="font-bold text-base">选择课程并且提交</div>
                                <div class="text-gray-600 mt-2">
                                    在课程界面选择需要刷课的课程,单击卡片以提交订单。
                                </div>
                            </div>
                            <!-- image -->
                            <div class="border rounded-xl overflow-hidden">
                                <img src="@/assets/images/guide-3.png" width="700" />
                            </div>
                        </div>
                    </el-timeline-item>
                    <el-timeline-item hide-timestamp>
                        <div class="flex justify-between py-2">
                            <!-- description -->
                            <div class="flex-1 pr-3">
                                <div class="font-bold text-base">检查订单</div>
                                <div class="text-gray-600 mt-2">
                                    在订单界面你可以了解各个订单的完成情况,对于失败或是刷课不完全的订单可以点击<strong>批量补单</strong>进行重刷(多次补单可能造成异常记录)
                                </div>
                            </div>
                            <!-- image -->
                            <div class="border rounded-xl overflow-hidden">
                                <img src="@/assets/images/guide-4.png" width="700" />
                            </div>
                        </div>
                    </el-timeline-item>
                </el-timeline>
            </div>
        </main>
    </div>
</template>
