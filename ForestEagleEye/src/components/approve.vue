<template>
  <div>
    <h1>审批活动</h1>
    <div>
      <h2>待审批</h2>
      <ul>
        <li v-for="activity in approvingActivities" :key="activity.a_id">
          <a :href="'/activity_detail/' + activity.a_id">{{ activity.a_name }}</a>
        </li>
      </ul>
    </div>
    <div>
      <h2>已通过</h2>
      <ul>
        <li v-for="activity in approvedActivities" :key="activity.a_id">
          <a :href="'/activity_detail/' + activity.a_id">{{ activity.a_name }}</a>
        </li>
      </ul>
    </div>
    <div>
      <h2>已驳回</h2>
      <ul>
        <li v-for="activity in dismissedActivities" :key="activity.a_id">
          <a :href="'/activity_detail/' + activity.a_id">{{ activity.a_name }}</a>
        </li>
      </ul>
    </div>
    <a href="/activities">返回</a>
  </div>
</template>

<script>
import axios from 'axios';

export default {
name: 'approve',
  data() {
    return {
      approvingActivities: [],
      approvedActivities: [],
      dismissedActivities: [],
    };
  },
  mounted() {
    this.fetchActivities();
  },
  methods: {
    async fetchActivities() {
      const user_id = sessionStorage.getItem('user_id'); // 从sessionStorage获取user_id
      if (user_id) {
        try {
          const params = new URLSearchParams();
          params.append('user_id',user_id);
          const response = await axios.post('http://127.0.0.1:5000/approve', params);
          this.approvingActivities = response.data.approving_activities;
          this.approvedActivities = response.data.approved_activities;
          this.dismissedActivities = response.data.dismissed_activities;

          console.log(response.data);
        } catch (error) {
          console.error("获取审批活动失败:", error);
        }
      } else {
        console.error("未找到user_id，请先登录");
      }
    }
  }
};
</script>

<style scoped>
/* 可以在这里添加自定义样式 */
</style>
