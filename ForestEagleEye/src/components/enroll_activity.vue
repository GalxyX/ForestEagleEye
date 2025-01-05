<template>
  <div class="enroll-page">
    <!-- 顶部导航栏 -->
    <NavigationBar />

    <!-- 页头部分 -->
    <!-- <el-page-header
      class="page-header"
      :icon="ArrowLeft"
      @back="$router.go(-1)"
      content="活动报名"
    >
    </el-page-header> -->
    <div class="all-contents">
        <el-page-header @back="$router.go(-1)" content="活动报名" title="返回">
        </el-page-header>

    <el-divider></el-divider>

    <!-- 活动详情和报名部分 -->
    <div class="activity-container">
      <!-- 左侧活动信息 -->
      <div class="activity-details">
        <h1>{{ activity.name }}</h1>
        <h2>活动简介</h2>
        <p class="activity-description">{{ activity.introduction }}</p>
        <h2>活动信息</h2>
        <div class="activity-info-grid">
          <div class="info-item">
            <span class="info-label">活动地点:</span>
            <span class="info-value">{{ activity.location }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">活动类型:</span>
            <span class="info-value">{{ activity.type }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">活动名称:</span>
            <span class="info-value">{{ activity.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">剩余名额:</span>
            <span class="info-value">{{ remainingSlots }}</span>
          </div>
        </div>
        <h2>报名信息</h2>
        <form  @submit.prevent="handleSubmit" class="enroll-form">
          <div class="form-item1">
            <label for="participantNumber" class="participant-label">
              <div style="color: red;">*</div>
              <div>报名人数:</div>
            </label>
            <el-input-number
              v-model="participantNumber"
              :min="1"
              :max="remainingSlots"
              placeholder="请输入报名人数"
            />
          </div>
          <div class="form-item">
            <label for="remark" class="remark-label">备注:</label>
            <el-input
              type="textarea"
              v-model="remark"
              rows="4"
              placeholder="请输入备注（可选）"
            />
          </div>
          <div  class="form-actions">
            <el-button type="success" native-type="submit">提交</el-button>
            <el-button @click="$router.go(-1)">取消</el-button>
          </div>
        </form>
      </div>
      <!-- 右侧活动图片 -->
      <div class="activity-image">
        <img :src="activity.picPath" alt="活动封面" />
      </div>
    </div>
  </div>
  <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
  </div>
</template>

<script>
import axios from "axios";
import NavigationBar from "../components/navbar.vue";
import { ArrowLeft } from "@element-plus/icons-vue";
const user_id = sessionStorage.getItem("user_id");

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      activity: {}, // 存储活动详情
      participantNumber: 1, // 默认报名人数
      remark: "", // 用户输入的备注
    };
  },
  computed: {
    remainingSlots() {
      if (this.activity) {
        return this.activity.participantNumber - this.activity.enrolledNumber;
      }
      return 0;
    },
  },
  mounted() {
    this.fetchActivity();
  },
  methods: {
    async fetchActivity() {
      const activityId = this.$route.params.activityId;
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/activity_enroll/${activityId}`
        );
        this.activity = response.data.activity;
      } catch (error) {
        console.error("获取活动数据失败:", error);
      }
    },
    async handleSubmit() {
      const activityId = this.$route.params.activityId;
      try {
        const params = new URLSearchParams();
        params.append("participantNumber", this.participantNumber);
        params.append("remark", this.remark);
        params.append("user_id", user_id);
        const response = await axios.post(
          `http://127.0.0.1:5000/enroll/${activityId}`,
          params
        );
        if (response.data.success) {
          this.$router.push("/activities");
          alert("报名成功");
        } else {
          alert(response.data.message || "报名失败");
        }
      } catch (error) {
        console.error("报名失败:", error);
        alert("报名失败");
      }
    },
  },
};
</script>

<style scoped>
.enroll-page {
  display: flex;       /* 使用Flexbox布局 */
  flex-direction: column; /* 设置主轴方向为垂直 */
  background-color: #f8f8f8;

}
.all-contents{
  background-color: #ffffff;
  margin-left: 20px; /* 左边距 */
  margin-right: 20px; /* 右边距 */
  margin-top: 80px;
  display: flex;
  flex-direction: column; /* 设置子元素纵向排列 */
}
.el-page-header {
  margin-top: 20px; /* 或者其他适当的值 */
  margin-left: 20px; /* 左边距 */
}


.page-header {
  background-color: white;
  margin-bottom: 20px;
}

.activity-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.activity-details {
  flex: 1.5;
  margin-left: 40px;
  margin-bottom:40px;
}

.activity-details h1 {
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 20px;
  font-family: "SimSun";
}

.activity-details h2 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #a8aba8;
  font-weight: light;
  margin-left:5px;
}

.activity-description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 20px;
  margin-left:5px;
}

.activity-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  background-color: rgb(244, 251, 246);
  border-radius: 15px; /* 设置圆角大小为10px */
  height: 4dvh;
  margin-left:10px;
  margin-right: 10px;
  margin-top:5px;
  margin-bottom: 5px;
  align-items: center; /* 垂直居中子元素 */
}

.info-label {
  font-weight: lighter;
  color: #475e53;
  margin-left:20px;
}

.info-value {
  color: #666;
  margin-right:20px;
}

.enroll-form {
  background-color: rgb(244, 251, 246);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display:flex;
  justify-content: center; /* 水平居中 */
  flex-direction: column; /* 设置子元素纵向排列 */
}

.form-item {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.el-input,
.el-input-number {
  width: 100%;
}

.form-actions {
  display: flex;
  padding-left: 400px;
  padding-right:200px;
}

.activity-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* 设置高度为100%，使其与父元素等高 */
  padding-top:90px;
}

.activity-image img {
  border-radius: 10px;
  object-fit: cover;
  border: 1px solid #ddd;
  margin-left:20px;
  margin-right:10px;
  max-width:800px;
}

.participant-label {
  font-size: 16px; /* 字体大小 */
  color: #3b693d; /* 字体颜色 */
  font-weight: lighter;
  margin-right: 10px; /* 与输入框之间的距离 */
  width: 200px; /* 最大宽度为200px */
  align-items: center; /* 垂直居中子元素 */
  display: flex; /* 使用Flexbox布局 */
}

.remark-label{
  font-size: 16px; /* 字体大小 */
  font-weight: lighter;
  color: #3b693d; /* 字体颜色 */
  margin-right: 10px; /* 与输入框之间的距离 */
}

.form-item1{
  margin-bottom: 20px;
  display: flex; /* 使用Flexbox布局 */
  justify-content: space-between; /* 子元素靠至左右两侧排布 */
}
.el-footer{
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size:xx-small;
  margin-top: 20px;
}
</style>
