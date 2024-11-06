<template>
  <div class="common-layout">
      <el-container>
          <NavigationBar />
          <el-container>
              <el-aside width="250px">
                  <el-scrollbar>
                      <el-menu 
                        :default-active="activeIndex"
                        @select="handleSelect"
                        >
                          <el-menu-item index="1">
                              <template #title>
                              <el-icon><icon-message /></el-icon>概要
                              </template>
                          </el-menu-item>

                          <el-sub-menu index="2">
                              <template #title>
                              <el-icon><icon-menu /></el-icon>数据查询
                              </template>
                              <el-menu-item-group>
                                  <template #title>按国家和地区</template>
                                  <el-menu-item index="2-1">单国家和地区查询</el-menu-item>
                                  <el-menu-item index="2-2">多国家和地区比较</el-menu-item>
                              </el-menu-item-group>
                              <el-menu-item-group>
                                  <template #title>按森林</template>
                                  <el-menu-item index="2-3">单林区查询</el-menu-item>
                                  <el-menu-item index="2-4">多林区比较</el-menu-item>
                              </el-menu-item-group>
                          </el-sub-menu>

                          <el-menu-item index="3" v-if="role =='林业管理人员' || role == '林业监管人员'">
                              <template #title>
                              <el-icon><icon-menu /></el-icon>百科编辑
                              </template>
                          </el-menu-item>
                      </el-menu>
                  </el-scrollbar>
              </el-aside>
              <el-container>
                  <!--子页面内容-->
                  <el-main>
                    <!--概要-->
                    <div v-if="activeIndex === '1'">概要页面内容</div>
                    <!--单国家-->
                    <div v-if="activeIndex === '2-1'">单国家和地区查询页面内容</div>
                    <!--多国家-->
                    <div v-if="activeIndex === '2-2'">多国家和地区比较页面内容</div>
                    <!--单林区-->
                    <div v-if="activeIndex === '2-3'">单林区查询页面内容</div>
                    <!--多林区-->
                    <div v-if="activeIndex === '2-4'">多林区比较页面内容</div>
                    <!--子页面内容-->
                    <div v-if="activeIndex === '3'">百科编辑页面内容</div>
                  </el-main>
                  <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
              </el-container>
          </el-container>
    </el-container>
  </div>
</template>


<script>
import { ref } from 'vue';
import WorldJSON from '@/assets/json/world.json';
import axios from 'axios';
import NavigationBar from '../components/navbar.vue';


export default {
  name: 'encyclopedia',
  components: {
    NavigationBar,
  },
  data() {
    return {
      role: sessionStorage.getItem('role'),
      activeIndex: '1',
      defaultOpeneds: ['2'] // 默认展开的子菜单
    };
  },
  methods: {
    async handleSelect(index, indexPath) {
      this.activeIndex = index;
      // 根据选择的索引加载相应的数据或执行相应的操作
      switch (index) {
        case '1':
          // 概要
          break;
        case '2-1':
          // 单国家和地区
          break;
        case '2-2':
          // 多国家和地区
          break;
        case '2-3':
          // 单林区
          break;
        case '2-4':
          // 多林区
          break;
        default:
          // 其他情况
          break;
      }
    }
  }
};
</script>

<style scoped>
.common-layout{
  padding-top: 50px;
  background-color: #F0F2F5;
}
.el-scrollbar{
  background-color: white;
}
.el-menu-item:hover{
  background-color: rgba(149, 242, 4, 0.1); 
}
.el-menu-item.is-active{
  color:#60a103;
}
.el-footer{
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size:xx-small;
}
</style>