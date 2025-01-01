<template>
  <div class="container">
    <!-- 顶部导航栏 -->
    <NavigationBar />

    <div class="all-contents">
      <el-page-header @back="handleBack" content="活动详情" title="返回">
      </el-page-header>
      <el-divider></el-divider>

      <div v-if="activity">
        <!-- 审批流程展示 -->
        <div class="h1">申请流程</div>
        <div class="approval-steps">
          <el-steps :active="getApprovalStep()" finish-status="success" align-center>
            <el-step title="申请提交"></el-step>
            <el-step title="审批中"></el-step>
            <el-step title="申请通过"></el-step>
            <el-step title="活动完成"></el-step>
          </el-steps>
        </div>
        <!-- 活动信息 -->
        <div class="h1">活动信息</div>
        <div class="activity-info">
            <div class="info-grid">
              <div class="info-unit">
                <p class="h2">活动名称</p>
                <p class="h3">{{ activity.a_name }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动编号</p>
                <p class="h3">{{ activity.a_id }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动地点</p>
                <p class="h3">{{ activity.a_location }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动类型</p>
                <p class="h3">{{ activity.a_type || "未知" }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动开始时间</p>
                <p class="h3">{{ activity.a_beginTime }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动结束时间</p>
                <p class="h3">{{ activity.a_endTime }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动人数</p>
                <p class="h3">{{ activity.a_participantNumber }}</p>
              </div>
              <div v-if="activity.a_ableParticipate" class="info-unit">
                <p class="h2">已报名人数</p>
                <p class="h3">{{ activity.a_enrolledNumber }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动主办单位</p>
                <p class="h3">{{ activity.a_forest }}</p>
              </div>
              <div class="info-unit">
                <p class="h2">活动简介</p>
                <p class="h3">{{ activity.a_introduction }}</p>
              </div>

              <!-- 图片显示 -->
              <div v-if="activity.a_picPath">
                <h2 class="h2">活动封面</h2>
                <div class="images">
                  <img :src="activity.a_picPath" alt="活动封面" />
                </div>
              </div>

            </div>
        </div>

        <el-divider></el-divider>
        <!-- 审批信息 -->
        <div class="approval-info">
          <h2 class="h1">审批信息</h2>
          <div class="info-grid">
            <div class="info-unit">
                <p class="h2">审批状态</p>
                <p class="h3" :style="{ color: getStateColor(activity.a_state) }">
                  <span v-if="activity.a_state" :style="{ backgroundColor: getStateColor(activity.a_state) }" class="status-dot"></span>
                  {{ getStateText(activity.a_state) }}
                </p>

                <!-- <p class="h3">{{ activity.a_state === 'approving' ? '审批中' : activity.a_state === 'approved' ? '已通过' : '已驳回' }}</p> -->
            </div>
            <div class="info-unit">
                <p class="h2">申请人编号</p>
                <p class="h3">{{ activity.a_applicantId }}</p>
            </div>
            <div class="info-unit">
                <p class="h2">申请提交时间</p>
                <p class="h3">{{ activity.a_submitTime }}</p>
            </div>
          </div>
        </div>

        <div class="buttons">
          <div class="action-buttons">
            <form @click="deleteActivity">
              <el-button round type="danger">删除活动</el-button>
            </form>
          </div>

          <div class="action-buttons" v-if="isApprover && activity.a_state === 'approving'">
            <form @click="approveActivity">
              <el-button round type="success">同意</el-button>
            </form>
          </div>

          <div class="action-buttons" v-if="isApprover && activity.a_state === 'approving'">
            <form @click="dismissActivity">
              <el-button round type="warning">驳回</el-button>
            </form>
          </div>
          <div class="action-buttons" v-if="isApprover && activity.a_state === 'approving'">
          <el-input
                type="textarea"
                v-model="dismissReason"
                id="dismiss_reason"
                placeholder="请输入驳回理由"
                style="width: 300px;"
          ></el-input> 
          </div>
        </div>

      </div>
      <div v-else>
        <p>加载中...</p>
      </div>
    </div>
    <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
  </div>
</template>

<script>
import axios from "axios";
import NavigationBar from "../components/navbar.vue";
import { ArrowLeft } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      activity: null, // 活动数据
      isApprover: false, // 是否是审批人
      dismissReason: "", // 驳回理由
    };
  },
  setup() {
    const router = useRouter();

    // 返回方法
    const handleBack = () => {
      router.push("/activities");
    };

    return { handleBack };
  },
  mounted() {
    this.fetchActivityDetails();
  },
  methods: {
    async fetchActivityDetails() {
      const activityId = this.$route.params.activityId;
      const user_id = sessionStorage.getItem("user_id");
      try {
        const params = new URLSearchParams();
        params.append("user_id", user_id);
        const response = await axios.post(
          `http://127.0.0.1:5000/activity_detail/${activityId}`,
          params
        );
        const { activity, isApprover } = response.data;
        this.activity = activity;
        this.isApprover = isApprover;
      } catch (error) {
        console.error("活动数据获取失败", error);
      }
    },
    async deleteActivity() {
      const activityId = this.activity.a_id;
      try {
        await axios.post(`http://127.0.0.1:5000/delete_activity/${activityId}`);
        this.$router.push("/activities");
      } catch (error) {
        console.error("删除活动失败", error);
      }
    },
    async approveActivity() {
      console.log('你好吗你好吗在同意');
      const activityId = this.activity.a_id;
      try {
        await axios.post(`http://127.0.0.1:5000/approve_activity/${activityId}`);
        this.activity.a_state = "approved";
      } catch (error) {
        console.error("同意活动失败", error);
      }
    },
    async dismissActivity() {
      const activityId = this.activity.a_id;
      try {
        await axios.post(
          `http://127.0.0.1:5000/dismiss_activity/${activityId}`,
          { dismiss_reason: this.dismissReason }
        );
        this.activity.a_state = "dismissed";
      } catch (error) {
        console.error("驳回活动失败", error);
      }
    },
    getApprovalStep() {
      const state = this.activity.a_state;
      switch (state) {
        case "submitted":
          return 1;
        case "approving":
          return 2;
        case "approved":
          return 3;
        case "completed":
          return 4;
        default:
          return 1;
      }
    },
    getStateColor(state) {
    switch (state) {
      case 'approving':
        return '#db9d41'; // 审批中的颜色，例如：浅珊瑚色
      case 'approved':
        return '#60a130'; // 已通过的颜色，例如：亮绿色
      default:
        return '#8d2c2c'; // 已驳回的颜色，例如：红色
    }
    },
    getStateText(state) {
      switch (state) {
        case 'approving':
          return '审批中';
        case 'approved':
          return '已通过';
        default:
          return '已驳回';
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;       /* 使用Flexbox布局 */
  flex-direction: column; /* 设置主轴方向为垂直 */
  background-color: #f8f8f8;
}

.page-header {
  z-index: 10;
  position: sticky;
  top: 0;
  background-color: white;
}

.activity-details-container {
  margin: 20px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.approval-steps {
  margin-bottom: 20px;
}

.activity-info,
.approval-info {
  margin-bottom: 30px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #8d2c2c;
  margin-bottom: 10px;
}

.info-grid {
  margin-left:150px;
  margin-right:80px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px 20px;
}

.images img {
  width: 300px;
  height: auto;
  border-radius: 4px;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.dismiss-label {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}
.el-page-header {
  margin-top: 20px; /* 或者其他适当的值 */
  margin-left: 20px; /* 左边距 */
}
.all-contents{
  background-color: #ffffff;
  margin-left: 20px; /* 左边距 */
  margin-right: 20px; /* 右边距 */
  margin-top: 80px;
  display: flex;
  flex-direction: column; /* 设置子元素纵向排列 */
}
.h1{
  margin-left: 50px;
  margin-top:10px;
  margin-bottom:30px;
  font-size:20px;
  font-weight: lighter;
  color:grey;
}
.h2 {
  font-size: 20px;
  /* font-family: 'Source Han Serif', 'Noto Serif CJK SC', serif; */
  /* font-weight: bold;  */
  color:rgb(164, 162, 162);
  width:160px;
}
.h3{
  font-size: 20px;
  /* font-family: 'Source Han Serif', 'Noto Serif CJK SC', serif; */
  width:500px;
  /* font-weight:bolder; */
}
.info-unit{
  display: flex;
}
.status-dot {
  display: inline-block;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  margin-right: 5px;
}
.buttons {
  display: flex;          /* 启用 Flexbox 布局 */
  justify-content: center; /* 水平居中对齐子组件 */
  align-items: center;     /* 垂直居中对齐子组件（如果需要的话） */
  flex-wrap: wrap;        /* 允许子组件换行 */
  gap: 30px;              /* 设置子组件之间的间隔为 30px */
  margin-bottom: 30px;
}
.el-footer{
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size:xx-small;
  margin-top: 50px;
}
</style>
