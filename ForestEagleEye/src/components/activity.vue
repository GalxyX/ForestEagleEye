<template>
  <div class="container">
    <div style="margin-left: 50px; margin-top: 50px;">
      <h1 style="font-size: x-large; margin-bottom: 10px; color: #60a130;">Forest Activities</h1>
      <h2 style="font-size: xx-large; margin-top: 10px;">林上活动</h2>
    </div>
    <div style="display: flex;  gap: 50px; margin-bottom: 50px;">
      <!-- 图片滑动展示 -->
      <div class="carousel-section">
        <div class="carousel-inner" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
          <div class="carousel-item" v-for="item in 4" :key="item">
            <img :src="`src/assets/Activity${item}.png`" alt="carousel image" class="carousel-image">
          </div>
        </div>
        <button class="prev" @click="prevSlide"></button>
        <button class="next" @click="nextSlide"></button>
      </div>
      <!--林上活动简介-->
      <div style="display: flex; flex-direction: column; width: 380px; margin-top: 20px;">
        <h2 style="font-size: x-large;margin-top: 10px;">您可以在林业活动做什么？</h2>
        <h2 style="font-size: large; margin-top: 5px;">What can you do in Forest Activities?</h2>
        <text style="margin-bottom: 10px;line-height: 1.5;">
          在林上鹰眼的林业活动板块申请、审批、报名您的林业活动，一站式管理您的林业活动生命周期。
        </text>
        <text style="color: grey;line-height: 1.5; font-family: Georgia, 'Times New Roman', Times, serif;">
          Apply, approve, and register for forestry activities in ForestEagleEye, managing the entire lifecycle of your forestry activities in one stop.
        </text>
        <el-button class="try-btn" type="success" plain style="margin-top: 20px;"@click="scroll">立即体验</el-button>
      </div>
    </div>

    <el-divider>· ForestEagleEye · Forest Activities ·</el-divider>

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

      
      <!-- 展示可报名的活动 -->
      <div class="activity-list">
        <div v-for="activity in filteredActivities" :key="activity.id" class="activity-card">
          <div style="display: flex; gap: 10px; align-items: center;">
            <h2>{{ activity.name }}</h2>
            <el-tag size="normal" type="warning" style="margin-top: 5px;">{{ activity.type }}</el-tag>
          </div>
          <div>
            <img :src="activity.picPath" alt="活动封面" class="activity-image">
          </div>
          <div>
            <div class="activity-details">
              <h3>活动地点</h3> 
              <p>📍{{ activity.location }}</p>              
              <h3>活动简介</h3> 
              <p>{{ activity.introduction.length > 50 ? activity.introduction.slice(0, 50) + '...' : activity.introduction }}</p>
              <h3>剩余名额</h3> 
              <p>{{ activity.participantNumber - activity.enrolledNumber }}</p>
            </div>
            <div v-if="activeTab === 'enrollable'" class="activity-actions">
              <el-button style="width: 100%; justify-content: center;" plain type="success" @click="$router.push(`/enroll_activity/${activity.id}`)">报名</el-button>
            </div>
          </div>
        </div>
      </div>
  </div>
  <!--底部版权信息-->
  <footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</footer>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      activities: [], // 存储活动数据
      due_activities: [],
      overdue_activities: [],
      activeTab: 'enrollable', // 默认激活的标签
      tabs: [
        { name: 'all', label: '往期风采', component: 'AllTab' },
        { name: 'enrollable', label: '可报名活动', component: 'EnrollableTab' },
      ],
      currentIndex: 0,
      interval: 5000, // 轮播间隔时间，单位为毫秒
      timer: null,
    };
  },
  computed: {
    // 根据激活的 Tab 返回对应的活动数据
    filteredActivities() {
      let activities = [];
      if (this.activeTab === "enrollable") {
        activities = this.due_activities;
      } else {
        activities = this.overdue_activities;
      }
      return activities;
    },
    activeTabComponent() {
      return this.tabs.find(tab => tab.name === this.activeTab)?.component;
    },
  },
  mounted() {
    this.fetch_Due_Activities();
    this.startAutoPlay();
  },
  beforeDestroy() {
    this.stopAutoPlay();
  },
  methods: {
    async fetch_Due_Activities() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/activities'); 
        this.due_activities = response.data.due_activities;
        this.overdue_activities = response.data.overdue_activities;
      } catch (error) {
        console.error('获取活动数据失败:', error);
      }
    },
    startAutoPlay() {
      this.timer = setInterval(this.nextSlide, this.interval);
    },
    stopAutoPlay() {
      clearInterval(this.timer);
    },
    nextSlide() {
      if (this.currentIndex < 3) {
        this.currentIndex++;
      } else {
        this.currentIndex = 0;
      }
    },
    prevSlide() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      } else {
        this.currentIndex = 3;
      }
    },
    scroll() {
      // 滚动到页面顶部
      window.scrollTo({
        top: 600,
        behavior: 'smooth'
      });
    },
  }
};
</script>

<style scoped>
.container{
  background-color: white;
  width:95%;
  margin-bottom: 20px;
  padding:10px 40px 30px 40px;
}

.el-carousel {
  height: 700px;
}

.el-carousel__item {
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
}

.el-carousel__item h3 {
  color: #47695b;
  font-size: 18px;
  opacity: 0.75;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

.carousel-image {
width: 800px;
height: 400px;
object-fit: cover; /* 确保图片覆盖整个容器 */
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

.carousel-section {
  position: relative;
  overflow: hidden;
  padding-bottom: 20px;
  width: 800px;
  height: 400px;
  margin-left: 50px;
}

.carousel-inner {
  display: flex;
  transition: transform 0.5s ease;
}

.carousel-item {
  min-width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-image {
  width: 100%;
  display: block;
}

.prev,
.next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  padding: 5px;
  z-index: 100;
  background: transparent;
  border: none;
  outline: none;
}

.prev::after {
  content: '《';
  display: block;
  padding: 5px;
  color: white;
  border-radius: 50%;
  font-size: 40px;
}

.next::after {
  content: '》';
  display: block;
  padding: 5px;
  color: white;
  border-radius: 50%;
  font-size: 40px;
}

.prev:hover::after,
.next:hover::after {
  color: #60a130;
  /* 鼠标悬停时的颜色，这里使用了金色作为示例 */
}

.prev {
  left: 7px;
}

.next {
  right: 7px;
}

.el-icon-arrow-down {
  font-size: 24px;
  /* 图标大小 */
}

.activity-card {
  background-color:  rgb(255, 255, 255);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  box-shadow: 0 15px 15px rgba(0, 0, 0, 0.1);
  flex-direction: row;
  padding: 20px 20px;
  justify-content: space-between; /* 子元素靠两侧排放 */
}

.activity-card:hover {
  background-color:  rgb(247, 253, 249); /* 鼠标悬停时的背景颜色 */
  border: 1px solid #60a130;
}

.activity-card>div:nth-of-type(1) {
  flex: 2;
}

.activity-card>div:nth-of-type(2) {
  flex: 1;
}

.activity-list {
  margin-left: 20px;
  margin-right: 40px;
  margin-bottom: 20px;
  display: grid;
  grid-template-columns: repeat(4,1fr); /* 自动调整列数 */
  gap: 10px 10px; /* 卡片之间的间距 */
}
.activity-card h2{
  font-size: 18px;
  font-weight: bold;
  color: black;
  margin-bottom: 10px;
}

.activity-details {
  margin-bottom: 10px;
  flex-direction: column; /* 子元素垂直排列 */
}


.activity-details h3 {
  font-size: 15px;
  font-weight: bold;
  color: #666;
  margin-bottom: 10px;
}


.activity-details p {
  font-size: 14px;
  margin: 5px 0;
  color: #666;
  justify-content: flex-end;
}

.activity-actions {
  align-items: center;
}

.activity-image {
  height: 200px;
  border-radius: 4px;
  object-fit: cover;
  width: 100%;
}

.el-icon-d-arrow-right {
  width: 10px;
}

.button {
  width: 100px;
  font-size: 25px;
  color: #60a130;
}

.button:hover {
  color: #3e634a; /* 鼠标悬停时的颜色 */
}
/*底部版权信息*/
footer {
  background-color: transparent;
  color: #ababab;
  text-align: center;
  padding: 10px 0;
  bottom: 0;
  width: 100%;
  font-size: xx-small;
  margin-top: 50px;
}
</style>
