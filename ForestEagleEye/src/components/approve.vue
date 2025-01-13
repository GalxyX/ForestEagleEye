<template>
  <div class="container">
    <!-- Tab 切换 -->
    <div class="tabs">
      <div class="tabs-header">
        <span v-for="(tab, index) in tabs" :key="index" :class="['tab', { 'active-tab': activeTab === tab.name }]"
          @click="activeTab = tab.name">
          {{ tab.label }}
        </span>
      </div>
      <div class="tabs-content">
        <component :is="activeTabComponent"></component>
      </div>
    </div>

    <!-- 活动列表 -->
    <div class="activity-list">
      <el-table :data="filteredActivities" stripe style="width: 100%">
      <el-table-column prop="a_name" label="活动名称" width="300"></el-table-column>
      <el-table-column prop="a_id" label="活动编号" width="300"></el-table-column>
      <el-table-column prop="applicant" label="申请人" width="200"></el-table-column>
      <el-table-column prop="startTime" label="开始时间" width="350"></el-table-column>
      <el-table-column fixed="right" label="更多" min-width="200">
        <template #default="scope">
            <el-button link type="success"  @click="viewDetails(scope.row.a_id)">
              操作
            </el-button>
          </template>
      </el-table-column>
    </el-table>
    </div>

  </div>
  <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
</template>

<script>
import axios from "axios";
import { formatDateTime } from "../components/formatTime";

export default {
  name: "Approve",
  data() {
    return {
      activeTab: "all", // 当前激活的标签
      approvingActivities: [],
      approvedActivities: [],
      dismissedActivities: [],
      currentPage: 1, // 当前页码
      pageSize: 5, // 每页显示数量

      activeTab: 'all', // 默认激活的标签
      tabs: [
        { name: 'all', label: '全部', component: 'AllTab' },
        { name: 'approving', label: '待审批', component: 'ApprovingTab' },
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
      } else if (this.activeTab === "dismissed") {
        activities = this.dismissedActivities;
      } else {
        activities = [
          ...this.approvingActivities,
          ...this.approvedActivities,
          ...this.dismissedActivities,
        ];
      }
      // 分页处理
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return activities.slice(start, end);
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
      const user_id = sessionStorage.getItem("user_id"); // 从 sessionStorage 获取 user_id
      if (user_id) {
        try {
          const params = new URLSearchParams();
          params.append("user_id", user_id);
          const response = await axios.post("http://127.0.0.1:5000/approve", params);
          this.approvingActivities = response.data.approving_activities;
          this.approvedActivities = response.data.approved_activities;
          this.dismissedActivities = response.data.dismissed_activities;

          // 时间格式化
          if(this.approvingActivities){
            this.approvingActivities.forEach(activity => {
              let tmp_time = activity.startTime;
              activity.startTime = formatDateTime(new Date(tmp_time));
            });
          }
          if(this.approvedActivities){
            this.approvedActivities.forEach(activity => {
              let tmp_time = activity.startTime;
              activity.startTime = formatDateTime(new Date(tmp_time));
            });
          }
          if(this.dismissedActivities){
            this.dismissedActivities.forEach(activity => {
              let tmp_time = activity.startTime;
              activity.startTime = formatDateTime(new Date(tmp_time));
            });
          }

        } catch (error) {
          console.error("获取审批活动失败:", error);
        }
      } else {
        console.error("未找到 user_id，请先登录");
      }
    },
    viewDetails(activityId) {
      this.$router.push(`/activity_detail/${activityId}`);
    },
    onPageChange(page) {
      this.currentPage = page;
    },
    getProgressStatus(status) {
      switch (status) {
        case "approved":
          return "success";
        case "rejected":
          return "exception";
        default:
          return "active";
      }
    },
  },
};
</script>

<style scoped>
.container {
  background-color: white;
  width:95%;
  margin-bottom: 20px;
  padding:10px 40px 30px 40px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.activity-item {
  display: flex;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  align-items: center;
}

.activity-image img {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  object-fit: cover;
}

.activity-info {
  flex: 1;
  margin-left: 20px;
}

.activity-info h2 {
  font-size: 16px;
  font-weight: bold;
  margin: 0 0 10px 0;
}

.activity-info p {
  font-size: 14px;
  color: #666;
  margin: 5px 0;
}

.activity-actions {
  margin-left: 20px;
}

.activity-actions .el-button {
  color: #60a130;
}

.tabs-header {
  display: flex;
}

.tab {
  padding: 10px 15px;
  cursor: pointer;
  color: rgb(115, 121, 115);
  /* 设置标签文字颜色为绿色 */
  border-bottom: 2px solid transparent;
  /* 下划线默认透明 */
}

.active-tab {
  color: #60a130;
  border-bottom: 2px solid #60a130;
  /* 激活状态的下划线颜色 */
}

.tabs-content {
  margin-top: 20px;
}

.tab:hover {
  color: #60a130;
}

.el-footer {
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size: xx-small;
}
</style>
