<template>
  <div class="common-layout">
    <!-- 顶部导航栏 -->
    <NavigationBar />

    <div class="container">
      <el-page-header @back="handleBack" content="活动详情" title="返回">
      </el-page-header>
      
      <el-divider></el-divider>

      <div v-if="activity" style="margin-left: 60px;margin-right: 60px;">
        <!-- 审批流 -->
        <div style="margin-top: 20px;">
          <el-descriptions
            title="申请流程"
            direction="vertical"
            :column="1"
          >
        </el-descriptions>
          <div class="approval-steps">
            <el-steps :active="getApprovalStep()" finish-status="success" align-center>
              <el-step title="申请提交"></el-step>
              <el-step title="审批中"></el-step>
              <el-step title="申请通过"></el-step>
              <el-step title="活动完成"></el-step>
            </el-steps>
          </div>
        </div>
        <!-- 活动信息表单 -->
        <div style="margin-top: 20px;">
          <el-descriptions 
            title="活动信息"
            :column="3">
            <el-descriptions-item label="活动编号">ACT{{activity.a_id}}</el-descriptions-item>
            <el-descriptions-item label="活动名称">{{activity.a_name}}</el-descriptions-item>
            <el-descriptions-item label="活动地点">{{activity.a_location}}</el-descriptions-item>
            <el-descriptions-item label="活动类型">
              <el-tag size="normal" type="success">{{activity.a_type || "未知"}}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="活动开始时间">{{activity.a_beginTime}}</el-descriptions-item>
            <el-descriptions-item label="活动结束时间">{{activity.a_endTime}}</el-descriptions-item>
            <el-descriptions-item label="计划人数">{{activity.a_participantNumber}}</el-descriptions-item>
            <el-descriptions-item label="已报名人数">{{activity.a_enrolledNumber}}</el-descriptions-item>
            <el-descriptions-item label="主办单位">{{activity.a_inst}}</el-descriptions-item>        
          </el-descriptions>
        </div>
        
        <!--活动简介-->
        <div style="margin-top: 20px;"> 
          <el-descriptions
          title="活动简介"
          direction="vertical"
          :column="1"
          >
            <el-descriptions-item>{{activity.a_introduction}}</el-descriptions-item>        
          </el-descriptions>
        </div>

        <!-- 图片显示 -->
        <div v-if="activity.a_picPath" style="margin-top: 20px;">
          <el-descriptions
            title="活动封面"
            direction="vertical"
            :column="1"
          ></el-descriptions>
          <div class="images">
            <img :src="activity.a_picPath" alt="活动封面" />
          </div>
        </div>
        
        <!-- 审批信息 -->
        <div style="margin-top: 20px;">
          <el-descriptions
            title="审批信息"
            :column="3"
          >
          <el-descriptions-item label="审批状态">
            <el-tag v-if="activity.a_state === 'approving'" size="normal" type="warning">审批中</el-tag>
            <el-tag v-if="activity.a_state === 'approved'" size="normal" type="success">已通过</el-tag>
            <el-tag v-if="activity.a_state === 'dismissed'" size="normal" type="error">已驳回</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="申请人编号">U{{activity.a_applicantId}}</el-descriptions-item>
          <el-descriptions-item label="申请提交时间">{{activity.a_submitTime}}</el-descriptions-item>
          <el-descriptions-item label="驳回原因" v-if="activity.a_state === 'dismissed'">{{activity.a_dismissReason}}</el-descriptions-item>
        </el-descriptions>
        </div>
        

        <div class="buttons">
          <div class="action-buttons" v-if="user_role ==='林业从业人员'">
            <el-button plain type="danger" @click="deleteDialogVisible=true">撤销申请</el-button>
            <!--确认撤销申请弹窗-->
            <el-dialog
              v-model="deleteDialogVisible"
              title="提示"
              width="500"
              :before-close="handleClose"
            >
              <span>您确认撤销此次活动申请吗？</span>
              <template #footer>
                <div class="dialog-footer">
                  <el-button plain type="info" @click="deleteDialogVisible = false">取消</el-button>
                  <el-button type="success" @click="deleteActivity">
                    确认
                  </el-button>
                </div>
              </template>
            </el-dialog>
          </div>
          

          <div class="action-buttons" v-if="isApprover && activity.a_state === 'approving'">
            <form @click="approveActivity">
              <el-button plain type="success">同意申请</el-button>
            </form>
          </div>

          <div class="action-buttons" v-if="isApprover && activity.a_state === 'approving'">
            <el-button plain type="warning" @click="dismissDialogVisible = true">驳回申请</el-button>
            <!--驳回理由弹窗-->
            <el-dialog
              v-model="dismissDialogVisible"
              title="驳回理由"
              width="500"
              :before-close="handleClose"
            >
              
              <el-input
                type="textarea"
                v-model="dismissReason"
                id="dismiss_reason"
                placeholder="请输入驳回理由"
                style="width: 470px;"
              ></el-input> 
              
              <template #footer>
                <div class="dialog-footer">
                  <el-button plain type="info" @click="dismissDialogVisible = false">取消</el-button>
                  <el-button type="success" @click="dismissActivity">
                    驳回
                  </el-button>
                </div>
              </template>
            </el-dialog>

          </div>
         
        </div>

      </div>
      <div v-else>
        <el-empty description="来到了没有森林的荒原..." />
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
import { ElMessage } from "element-plus";
import { formatDateTime } from "../components/formatTime";

const user_id = sessionStorage.getItem("user_id");

export default {
  components: {
    NavigationBar,
  },
  data() {
    return {
      activity: null, // 活动数据
      isApprover: false, // 是否是审批人
      dismissReason: "", // 驳回理由
      user_role: sessionStorage.getItem('role'),
      deleteDialogVisible: false,
      dismissDialogVisible: false,
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

      try {
        const params = new URLSearchParams();
        params.append("user_id", user_id);
        const response = await axios.post(
          `http://127.0.0.1:5000/activity_detail/${activityId}`,
          params
        );
        const { activity, isApprover } = response.data;
        this.activity = activity;
        if(this.activity){
          //将所有时间标准化
          this.activity.a_beginTime = formatDateTime(new Date(this.activity.a_beginTime));
          this.activity.a_endTime = formatDateTime(new Date(this.activity.a_endTime));
          this.activity.a_submitTime = formatDateTime(new Date(this.activity.a_submitTime));
        }
        this.isApprover = isApprover;
      } catch (error) {
        console.error("活动数据获取失败", error);
      }
    },
  async deleteActivity() {
    const activityId = this.activity.a_id;
    try {
      const response = await axios.post(`http://127.0.0.1:5000/delete_activity/${activityId}`);

      if (response.data.status === "success") {
        this.deleteDialogVisible = false;
        // 删除成功的提示
        ElNotification({
          title: '撤销成功',
          message: '本次活动申请已成功撤销~',
          type: 'success',
        });
        // 跳转到活动列表页面
        this.$router.push("/activities");
      } else {
        throw new Error(response.data.message || "删除失败");
      }
    } catch (error) {
      console.error("删除活动失败", error);
      // 删除失败的提示
      ElNotification({
        title: '撤销失败',
        message: error.message || "请稍后再试",
        type: 'error',
      });
    }
  },
    async approveActivity() {
      const activityId = this.activity.a_id;
      try {
        const params = new URLSearchParams();
        params.append("user_id", user_id);
        await axios.post(`http://127.0.0.1:5000/approve_activity/${activityId}`,params);
        this.activity.a_state = "approved";
      } catch (error) {
        console.error("同意活动失败", error);
      }
    },
    async dismissActivity() {
      const activityId = this.activity.a_id;
      try {
         const params = new URLSearchParams();
         params.append("user_id", user_id);
         params.append("dismiss_reason", this.dismissReason);
        await axios.post(
          `http://127.0.0.1:5000/dismiss_activity/${activityId}`,params
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
    
  },
};
</script>

<style scoped>
.common-layout{
  padding-top: 50px;
  background-color: #F0F2F5;
}

.container{
  background-color: white;
  padding: 1px 20px 10px 20px; /* 上 右 下 左 */
  margin: 20px 40px 20px 40px; /* 上 右 下 左 */
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
  grid-template-columns: repeat(3, 1fr);
  gap: 10px 10px;
}

.images img {
  width: 500px;
  height: auto;
  border-radius: 4px;
}

.action-buttons {
  margin-top: 20px;
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
  font-size:normal;
  font-weight: bold;
  color:grey;
}
.h2 {
  font-size: 15px;
  /* font-family: 'Source Han Serif', 'Noto Serif CJK SC', serif; */
  /* font-weight: bold;  */
  color:rgb(164, 162, 162);
  width:160px;
}
.h3{
  font-size: 15px;
  /* font-family: 'Source Han Serif', 'Noto Serif CJK SC', serif; */
  width:300px;
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
