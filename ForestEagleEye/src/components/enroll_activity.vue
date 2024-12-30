<template>
  <div>
    <h1 v-if="activity">报名活动 - {{ activity.name }}</h1>
    <div v-if="activity">
      //<img :src="`/static/${activity.picPath}`" alt="活动封面">
      <p><strong>活动地点:</strong> {{ activity.location }}</p>
      <p><strong>活动类型:</strong> {{ activity.type }}</p>
      <p><strong>活动简介:</strong> {{ activity.introduction }}</p>
      <p><strong>剩余名额:</strong> {{ activity.participantNumber - activity.enrolledNumber }}</p>
    </div>

    <form @submit.prevent="handleSubmit">
      <div>
        <label for="participantNumber">报名人数:</label>
        <input type="number" v-model="participantNumber" required :min="1" :max="remainingSlots" />
      </div>
      <div>
        <label for="remark">备注:</label>
        <textarea v-model="remark" rows="4" cols="50" placeholder="请输入备注（可选）"></textarea>
      </div>
      <button type="submit">提交报名</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
const user_id = sessionStorage.getItem('user_id');
export default {
  data() {
    return {
      activity: {},              // 存储活动详情
      participantNumber: 1,        // 默认报名人数
      remark: "",                 // 用户输入的备注
    };
  },
  computed: {
    remainingSlots() {
      if (this.activity) {
        return this.activity.participantNumber - this.activity.enrolledNumber;
      }
      return 0;
    }
  },
  mounted() {
    this.fetchActivity();
  },
  methods: {
    // 获取活动数据
    async fetchActivity() {
      const activityId = this.$route.params.activityId;  // 获取活动ID从路由参数中
      try {
        const response = await axios.get(`http://127.0.0.1:5000/activity_enroll/${activityId}`); // 假设你有一个接口返回活动详情
        this.activity = response.data.activity;
      } catch (error) {
        console.error('获取活动数据失败:', error);
      }
    },

    // 提交报名表单
    async handleSubmit() {
      const activityId = this.$route.params.activityId;  // 获取活动ID

      try {
          const params = new URLSearchParams();
          params.append('participantNumber',this.participantNumber);
          params.append('remark',this.remark);
          params.append('user_id',user_id);
          console.log(params);
          const response = await axios.post(`http://127.0.0.1:5000/enroll/${activityId}`, params);

        if (response.data.success) {
          this.$router.push('/activities');  // 跳转回活动列表页面
          alert('报名成功');
        } else {
          alert(response.data.message || '报名失败');
        }
      } catch (error) {
        console.error('报名失败:', error);
        alert('报名失败');
      }
    }
  }
};
</script>

<style scoped>
/* 添加活动页面样式 */
form {
  margin-top: 20px;
}

label {
  margin-right: 10px;
}

button {
  margin-top: 20px;
}
</style>
