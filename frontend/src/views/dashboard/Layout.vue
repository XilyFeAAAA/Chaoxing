<template>
  <div>
    <!-- header -->
    <header class="flex items-center justify-between">
      <div class="flex items-center">
        <TriangleIcon class="cursor-pointer"/>
        <div class="mx-7 cursor-pointer">xilyfeaaaa</div>
      </div>
      <div class="flex items-center">
        <div class="btn border px-4 py-[6px] rounded-md text-sm">Feedback</div>
        <div class="mx-4 text-sm cursor-pointer">Changelog</div>
        <div class="mx-4 text-sm cursor-pointer">Help</div>
        <div class="mx-4 text-sm cursor-pointer">Docs</div>
        <div class="mx-4">
          <el-popover placement="bottom-end" :width="400" trigger="click">
            <template #reference>
              <button
                  class="flex items-center justify-center h-8 w-8 rounded-full border text-gray-500"
              >
                <svg-icon type="mdi" size="20" :path="mdiBellOutline"></svg-icon>
              </button>
            </template>
          </el-popover>
        </div>
        <div>
          <el-popover placement="bottom-end" :width="250" trigger="click">
            <template #reference>
              <button
                  class="flex items-center justify-center h-8 w-8 rounded-full border overflow-hidden"
              >
                <img
                    src="https://vercel.com/api/www/avatar/Zlsuf4ZskLFLoqcxw8KKHYAq?&s=60"
                    alt=""
                />
              </button>
            </template>
            <template #default>
              <div class="py-5">
                <div class="px-5 py-2">xilyfe@proton.me</div>
                <div class="text-[15px]">
                  <div class="pop-item">
                    <div>Dashboard</div>
                    <div>
                      <svg-icon type="mdi" size="20" :path="mdiBulletinBoard"></svg-icon>
                    </div>
                  </div>
                  <div class="pop-item">
                    <div>Settings</div>
                    <div>
                      <svg-icon type="mdi" size="20" :path="mdiCogOutline"></svg-icon>
                    </div>
                  </div>
                  <div class="pop-item">
                    <div>Create Team</div>
                    <div>
                      <svg-icon type="mdi" size="22" :path="mdiPlus "></svg-icon>
                    </div>
                  </div>
                </div>
                <div class="my-2 h-[1px] w-full bg-gray-200"></div>
                <div class="text-[15px]">
                  <div class="pop-item">
                    <div>Theme</div>
                    <div>
                      <el-switch v-model="value" active-text="Dark" inactive-text="Light" />
                    </div>
                  </div>
                  <div class="pop-item">
                    <div>Log Out</div>
                  </div>
                </div>
              </div>
            </template>
          </el-popover>
        </div>
      </div>
    </header>
    <!-- submenu -->
    <div class="submenu flex items-center mx-6">
      <a href="#" class="menu-item active">Overview</a>
      <a href="#" class="menu-item">Integrations</a>
      <a href="#" class="menu-item">Activity</a>
      <a href="#" class="menu-item">Domains</a>
      <a href="#" class="menu-item">Usage</a>
      <a href="#" class="menu-item">Monitor</a>
      <a href="#" class="menu-item">Setting</a>
    </div>
    <main class="h-[calc(100vh-112px)] bg-[#fafafa]">
      <div class="m-auto max-w-[1248px]">
        <div class="py-4">
          <div class="w-full my-3 flex items-stretch gap-2">
            <div class="w-full flex items-center border rounded-md bg-white">
                            <span class="flex items-center h-10 px-3 -mr-3">
                                <svg
                                    class="with-icon_icon__aLCKg"
                                    data-testid="geist-icon"
                                    fill="none"
                                    height="24"
                                    shape-rendering="geometricPrecision"
                                    stroke="currentColor"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="1.5"
                                    viewBox="0 0 24 24"
                                    width="24"
                                    style="color: currentcolor; width: 20px; height: 20px"
                                >
                                    <path
                                        d="M11 17.25a6.25 6.25 0 110-12.5 6.25 6.25 0 010 12.5z"
                                    ></path>
                                    <path d="M16 16l4.5 4.5"></path>
                                </svg>
                            </span>
              <input
                  type="text"
                  placeholder="Search"
                  class="w-full h-10 px-3 outline-none"
              />
            </div>
            <div class="switcher">
              <button :class="{ active: align === 'grid' }" @click="align = 'grid'">
                <svg-icon type="mdi" :path="mdiViewGridOutline"></svg-icon>
              </button>
              <button :class="{ active: align === 'row' }" @click="align = 'row'">
                <svg-icon type="mdi" :path="mdiViewList"></svg-icon>
              </button>
            </div>
          </div>
        </div>
        <div class="grid" v-show="align == 'grid'">
          <div class="course-card">
            <a href="#">
              <!-- img and base info -->
              <div class="flex">
                <div class="mr-3">
                  <img
                      src="https://p.ananas.chaoxing.com/star3/270_160c/601c40b268e10e7afcd6ececa7403884.jpg"
                      class="w-24 rounded-sm"
                  />
                </div>
                <div class="flex-1 flex flex-col justify-between">
                  <div>2021级形势与政策（五）</div>
                  <div class="text-sm text-gray-500">程平、李明等</div>
                </div>
              </div>
              <!-- teacher -->
              <div class="mt-6 text-xs text-[#666]">授课老师: 程平、李明等</div>
              <!-- time -->
              <div class="my-1 text-xs text-[#666]">开课时间: 2023年04月27日</div>
              <!-- progress -->
              <div class="mt-3 text-xs text-[#000]">Progress: 100%</div>
            </a>
          </div>
        </div>
        <div class="list" v-show="align === 'list'"></div>
      </div>
    </main>
  </div>
</template>
<script setup>
import {mdiBellOutline, mdiViewGridOutline, mdiViewList, mdiCogOutline, mdiBulletinBoard, mdiPlus} from '@mdi/js'
import {onMounted, ref} from 'vue'
import {getme} from '@/requests/api'
import {useAuthStore} from "@/stores/auth";
import TriangleIcon from '@/components/icons/triangle.vue'

const authStore = useAuthStore()
//refs
const align = ref('grid')
// onMounted
onMounted(() => {
  getme().then(res => {
    authStore.setInfo(res.data.data)
  }).catch(err => {
    console.log(err)
  })
})
</script>
<style lang="scss" scoped>
header {
  padding: 0 var(--dashboard-header-padding);
  height: var(--dashboard-header-height);

  .btn {
    transition: background-color 0.2s;
    cursor: pointer;

    &:hover {
      background-color: hsla(0, 0%, 95%);
    }
  }
}

.submenu {
  height: 48px;
  box-shadow: inset 0 -1px rgba(0, 0, 0, 0.08);

  .menu-item {
    position: relative;
    font-size: 14px;
    color: #666;
    border-radius: 5px;
    padding: 6px 12px;
    margin-right: 5px;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: hsla(0, 0%, 92%);
    }

    &.active {
      color: #000;

      &::before {
        content: '';
        display: block;
        position: absolute;
        height: 0;
        left: 9px;
        right: 9px;
        bottom: -7px;
        border-bottom: 2px solid;
      }
    }
  }
}

main {
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
}

.pop-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 20px;
  cursor: pointer;
  &:hover {
    background-color: rgba(0,0,0,.05);
  }

}
</style>
