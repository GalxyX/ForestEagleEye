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
            <!-- 右侧内容 -->
            <!-- <div class="container">
              <h1>可报名活动</h1>
              <div v-if="activities.length" class="activity-list">
                <div v-for="activity in activities" :key="activity.id" class="activity-card">
                  <img :src="activity.picPath" alt="活动封面" class="activity-image">
                  <div class="activity-details">
                    <h2>{{ activity.name }}</h2>
                    <p><strong>活动地点:</strong> {{ activity.location }}</p>
                    <p><strong>活动类型:</strong> {{ activity.type }}</p>
                    <p><strong>活动简介:</strong> {{ activity.introduction }}</p>
                    <p><strong>剩余名额:</strong> {{ activity.participantNumber - activity.enrolledNumber }}</p>
                  </div>
                  <div class="activity-actions">
                    <router-link :to="`/enroll_activity/${activity.id}`" class="enroll-button">报名</router-link>
                  </div>
                </div>
              </div>
            </div> -->
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
import ActivityBox from '../components/activity.vue'

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
.activity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.activity-card {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  width: calc(33.333% - 20px); /* 三列布局 */
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
