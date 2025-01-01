<template>
  <div class="apply-page">
     <!-- Tab 切换 -->
      <div class="tabs">
        <div class="tabs-header">
        <span
          v-for="(tab, index) in tabs"
          :key="index"
          :class="['tab', { 'active-tab': activeTab === tab.name }]"
          @click="activeTab = tab.name"
        >
          {{ tab.label }}
        </span>
      </div>
      <div class="tabs-content">
        <component :is="activeTabComponent"></component>
      </div>
    </div>

    <div class="activity-list">
      <el-table :data="filteredActivities" stripe style="width: 100%">
        <el-table-column prop="a_name" label="活动名称" width="240"></el-table-column>
        <el-table-column prop="a_id" label="活动编号" width="240"></el-table-column>
        <el-table-column prop="a_forest" label="审批单位" width="240"></el-table-column>
        <el-table-column label="审批人" width="240">
          <template v-slot="scope">
            {{ scope.row.a_approver_id || "未知" }}
          </template>
        </el-table-column>
        <el-table-column label="审批时间" width="240">
          <template v-slot="scope">
            {{ scope.row.a_approveTime || "暂无" }}
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" min-width="240">
          <template #default="scope">
              <el-button link type="success"  @click="viewDetails(scope.row.a_id)">
                Read more
              </el-button>
            </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- <div class="action-buttons">
      <el-button type="primary" @click="navigateToCreateActivity">创建新活动</el-button>
    </div> -->
    <el-button class="mt-4" type="success" plain style="width: 100%" @click="navigateToCreateActivity">+   创建新活动</el-button>
    
  </div>
  <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
</template>

<script>
import axios from "axios";

export default {
  name: "apply",
  data() {
    return {
      activeTab: "approving",
      approvingActivities: [],
      approvedActivities: [],
      dismissedActivities: [],
      tabs: [
        { name: 'approving', label: '申请中', component: 'ApprovingTab' },
        { name: 'approved', label: '已通过', component: 'ApprovedTab' },
        { name: 'dismissed', label: '已驳回', component: 'DismissedTab' }
      ]
    };
  },
  computed: {
    // 根据激活的 Tab 返回对应的活动数据
    filteredActivities() {
      let activities = [];
      if (this.activeTab === "approving") {
        activities = this.approvingActivities;
      } else if (this.activeTab === "approved") {
        activities = this.approvedActivities;
      } else {
        activities = this.dismissedActivities;
      }
      return activities;
    },
    activeTabComponent() {
      return this.tabs.find(tab => tab.name === this.activeTab)?.component;
    },
  },
  mounted() {
    this.fetchActivities();
  },
  methods: {
    async fetchActivities() {
      const user_id = sessionStorage.getItem("user_id"); // 从sessionStorage获取user_id
      if (user_id) {
        try {
          const params = new URLSearchParams();
          params.append("user_id", user_id);
          const response = await axios.post(
            "http://127.0.0.1:5000/apply",
            params
          );
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
    },
    navigateToCreateActivity() {
      this.$router.push("/create_activity"); // 跳转到 create_activity 页面
    },
    viewDetails(activityId) {
      this.$router.push(`/activity_detail/${activityId}`); // 跳转到详情页面
    },
  },
};
</script>

<style scoped>
.apply-page {
  padding: 20px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.activity-info {
  flex: 1;
}

.activity-info h2 {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.activity-info p {
  font-size: 14px;
  margin: 5px 0;
  color: #666;
}

.activity-actions {
  margin-left: 20px;
}

.activity-actions .el-button {
  color: #409eff;
  font-size: 14px;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
.tabs-header {
  display: flex;
}

.tab {
  padding: 10px 15px;
  cursor: pointer;
  color: rgb(115, 121, 115); /* 设置标签文字颜色为绿色 */
  border-bottom: 2px solid transparent; /* 下划线默认透明 */
}

.active-tab {
  color:#60a130;
  border-bottom: 2px solid #60a130; /* 激活状态的下划线颜色 */
}

.tabs-content {
  margin-top: 20px;
}
.tab:hover {
  color: #60a130; 
}
.el-footer{
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size:xx-small;
}
.mt-4{
  margin-top: 20px;
}
</style>
