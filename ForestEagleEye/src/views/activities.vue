<template>
  <NavigationBar />
  <div class="common-layout">
    <el-container>
      <el-aside width="250px">
        <el-scrollbar>
          <el-menu :default-active="activeIndex" @select="handleSelect">
            <el-menu-item index="1">
              <template #title>
                <el-icon><icon-message /></el-icon>活动风采
              </template>
            </el-menu-item>

            <el-menu-item index="2">
              <template #title>
                <el-icon><icon-message /></el-icon>我的报名
              </template>
            </el-menu-item>

            <el-menu-item index="3" v-if="role === '林业管理人员' || role === '林业监管人员'">
              <template #title>
                <el-icon><icon-menu /></el-icon>我的审批
              </template>
            </el-menu-item>
            <el-menu-item index="4" v-if="role === '林业从业人员' || role === '林业监管人员'">
              <template #title>
                <el-icon><icon-menu /></el-icon>我的申请
              </template>
            </el-menu-item>
          </el-menu>
        </el-scrollbar>
      </el-aside>

      <el-container>
        <el-main>
          <div v-if="activeIndex === '1'">
            <ActivityBox />
          </div>

          <div v-if="activeIndex === '2'">
            <EnrollBox />
          </div>
          <div v-if="activeIndex === '3'">
            <ApproveBox />
          </div>
          <div v-if="activeIndex === '4'">
            <ApplyBox />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import NavigationBar from '../components/navbar.vue';
import ApproveBox from '../components/approve.vue';
import ApplyBox from '../components/apply.vue';
import EnrollBox from '../components/enroll.vue';
import ActivityBox from '../components/activity.vue';

export default {
  components: {
    NavigationBar,
    ApproveBox,
    ApplyBox,
    EnrollBox,
    ActivityBox
  },
  data() {
    return {
      role: sessionStorage.getItem('role'),
      activities: [], // 存储活动数据
      activeIndex: '1',
    };
  },
  mounted() {
    this.fetchActivities();
  },
  methods: {
    async fetchActivities() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/activities');
        this.activities = response.data.activities;
      } catch (error) {
        console.error('获取活动数据失败:', error);
      }
    },
    async handleSelect(index) {
      this.activeIndex = index;
    }
  }
};
</script>

<style scoped>
.common-layout {
  padding-top: 50px;
  background-color: #f0f2f5;
}
.el-scrollbar {
  background-color: white;
  position: fixed;
  width: 250px;
}
.el-menu-item:hover {
  background-color: rgba(149, 242, 4, 0.1);
}
.el-menu-item.is-active {
  color: #60a103;
}

.container {
  background-color: white;
  width: 95%;
  margin: 20px auto;
  padding: 20px 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 24px;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.carousel-section {
  margin-bottom: 30px;
}

.el-carousel {
  height: 400px;
}

.el-carousel__item {
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  margin: 0;
}

.carousel-image {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.activity-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr)); /* 自动调整列数 */
  gap: 20px; /* 卡片之间的间距 */
}

.activity-card {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  padding: 15px;
}

.activity-image {
  width: 100%;
  height: auto;
  border-radius: 4px;
  margin-bottom: 10px;
}

.activity-details {
  flex: 1;
  margin-bottom: 10px;
}

.activity-details h2 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.activity-details p {
  font-size: 14px;
  margin: 5px 0;
  color: #666;
}

.activity-actions {
  text-align: center;
}

.enroll-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #5cb85c;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.enroll-button:hover {
  background-color: #4cae4c;
}
</style>
