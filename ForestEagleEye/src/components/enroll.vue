<template>
  <div class="enrollment-container">
    <div v-if="participations.length > 0" class="activity-list">
      <el-table :data="participations" stripe style="width: 100%">
        <el-table-column prop="a_name" label="活动名称" width="200"></el-table-column>
        <el-table-column prop="a_id" label="活动编号" width="200"></el-table-column>
        <el-table-column prop="a_location" label="活动地点" width="250"></el-table-column>
        <el-table-column prop="a_type" label="活动类型" width="200"></el-table-column>
        <el-table-column prop="a_beginTime" label="活动开始时间" width="300"></el-table-column>
        <el-table-column fixed="right" label="操作" min-width="120">
          <template #default="scope">
            <el-button round type="danger" size="small" @click="cancelEnrollment(scope.row.a_id)" class="cancel-button">
              取消报名
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div v-else class="no-activity">
      <el-empty description="来到了没有森林的荒原...">
      </el-empty>
    </div>

  </div>
  <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
</template>

<script>
import axios from "axios";
const user_id = sessionStorage.getItem("user_id");
export default {
  data() {
    return {
      participations: [], // 存储用户报名的活动列表
    };
  },
  mounted() {
    this.fetchMyEnrollments(); // 组件挂载后获取用户报名的活动
  },
  methods: {
    // 获取用户报名的活动
    async fetchMyEnrollments() {
      try {
        const params = new URLSearchParams();
        params.append("user_id", user_id);
        const response = await axios.post(
          "http://127.0.0.1:5000/myenrolled",
          params
        );
        this.participations = response.data.participations;
      } catch (error) {
        console.error("获取报名活动失败:", error);
      }
    },

    // 取消报名
    async cancelEnrollment(activityId) {
      try {
        const params = new URLSearchParams();
        params.append("user_id", user_id);
        const response = await axios.post(
          `http://127.0.0.1:5000/cancel_enrollment/${activityId}`,
          params
        );
        if (response.data.success) {
          this.fetchMyEnrollments(); // 取消报名后重新加载活动列表
          ElMessage({
            showClose: true,
            message: '取消报名成功',
            type: 'success',
          })
        } else {
          ElMessage({
            showClose: true,
            message: response.data.message || "取消报名失败",
            type: 'error',
          })
        }
      } catch (error) {
        ElMessage({
          showClose: true,
          message: "取消报名失败",
          type: 'error',
        })
      }
    },
    setactiveIndex() {
      this.activeIndex = 1;
    },
  },
};
</script>

<style scoped>
/* 整体容器样式 */
.enrollment-container {
  padding: 20px;
}

h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

/* 活动列表样式 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 单个活动卡片样式 */
.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 活动信息样式 */
.activity-info h2 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.activity-info p {
  font-size: 14px;
  margin: 5px 0;
  color: #666;
}

/* 取消报名按钮样式 */
.cancel-button {
  background-color: #ff5555;
  color: white;
  border: none;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #e03e3e;
}

/* 没有活动时的提示 */
.no-activity {
  text-align: center;
  color: #888;
  font-size: 16px;
  margin-top: 50px;
}

/* 返回按钮样式 */
.back-link {
  display: block;
  margin-top: 30px;
  text-align: center;
  font-size: 16px;
  color: #409eff;
  text-decoration: none;
}

.back-link:hover {
  color: #66b1ff;
}

.el-footer {
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size: xx-small;
}
</style>
