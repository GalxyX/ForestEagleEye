<template>
  <div>
  <!-- 导航栏 -->
    <nav>
      <ul>
        <li v-if="user_role === '林业从业人员'">
          <router-link to="/apply">我的申请</router-link>
        </li>
        <li v-if="user_role === '林业管理人员'">
          <router-link to="/approve">我的审批</router-link>
        </li>
        <li><router-link to="/enroll">我的报名</router-link></li>
      </ul>
    </nav>

    <h1>可报名活动</h1>
    <div v-if="activities.length">
      <div v-for="activity in activities" :key="activity.id">
        <h2>{{ activity.name }}</h2>
        //<img :src="`/static/${activity.picPath}`" alt="活动封面">
        <p><strong>活动地点:</strong> {{ activity.location }}</p>
        <p><strong>活动类型:</strong> {{ activity.type }}</p>
        <p><strong>活动简介:</strong> {{ activity.introduction }}</p>
        <p><strong>剩余名额:</strong> {{ activity.participantNumber - activity.enrolledNumber }}</p>
        <router-link :to="`/enroll_activity/${activity.id}`">报名</router-link>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
const user_role = sessionStorage.getItem('user_role');
export default {
  data() {
    return {
      activities: []  // 存储活动数据
    };
  },
  mounted() {
    // 组件创建时调用 API 获取活动数据
    this.fetchActivities();
  },
  methods: {
    async fetchActivities() {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/activities`);
        this.activities = response.data.activities;
      } catch (error) {
        console.error('获取活动数据失败:', error);
      }
    }
  }
};
</script>


<style scoped>
/* 添加导航栏样式 */
nav {
  background-color: #f8f8f8;
  padding: 10px;
  margin-bottom: 20px;
}

nav ul {
  list-style: none;
  display: flex;
  justify-content: space-around;
}

nav li {
  font-size: 16px;
}

nav a {
  text-decoration: none;
  color: #333;
  padding: 10px 20px;
}

nav a:hover {
  background-color: #ddd;
  border-radius: 4px;
}

/* 你可以在这里添加其他页面的样式 */
</style>
