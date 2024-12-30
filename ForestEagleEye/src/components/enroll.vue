<template>
  <div>
    <h1>我的报名活动</h1>
    <div v-if="participations.length > 0">
      <div v-for="participation in participations" :key="participation.a_id">
        <h2>{{ participation.a_name }}</h2>
        <p><strong>活动编号:</strong> {{ participation.a_id }}</p>
        <p><strong>活动地点:</strong> {{ participation.a_location }}</p>
        <p><strong>活动类型:</strong> {{ participation.a_type }}</p>
        <p><strong>活动开始时间:</strong> {{ participation.a_beginTime }}</p>
        <button @click="cancelEnrollment(participation.a_id)">取消报名</button>
      </div>
    </div>
    <div v-else>
      <p>您没有报名任何活动。</p>
    </div>
    <router-link to="/activities">返回</router-link>
  </div>
</template>

<script>
import axios from 'axios';
const user_id = sessionStorage.getItem('user_id');
export default {
  data() {
    return {
      participations: []  // 存储用户报名的活动列表
    };
  },
  mounted() {
    this.fetchMyEnrollments();  // 组件挂载后获取用户报名的活动
  },
  methods: {
    // 获取用户报名的活动
    async fetchMyEnrollments() {
      try {
         const params = new URLSearchParams();
          params.append('user_id',user_id);
          const response = await axios.post('http://127.0.0.1:5000/myenrolled', params);
          this.participations = response.data.participations;
      } catch (error) {
        console.error('获取报名活动失败:', error);
      }
    },

    // 取消报名
    async cancelEnrollment(activityId) {
      try {
        const params = new URLSearchParams();
        params.append('user_id',user_id);
        const response = await axios.post(`http://127.0.0.1:5000/cancel_enrollment/${activityId}`,params);
        if (response.data.success) {
          this.fetchMyEnrollments();  // 取消报名后重新加载活动列表
          alert('取消报名成功');
        } else {
          alert(response.data.message || '取消报名失败');
        }
      } catch (error) {
        console.error('取消报名失败:', error);
        alert('取消报名失败');
      }
    }
  }
};
</script>

<style scoped>
/* 添加样式 */
h1 {
  font-size: 24px;
}

button {
  margin-top: 10px;
  padding: 10px;
  background-color: #ff5555;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #e03e3e;
}
</style>
