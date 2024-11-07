<template>
    <div class="container">
      <div class="tab-header">
        <button
          v-for="tab in tabs"
          :key="tab.name"
          :class="{ active: activeTab === tab.name }"
          @click="activeTab = tab.name"
        >
          {{ tab.label }}
        </button>
      </div>
      <div class="tab-content">
        <div v-if="activeTab === 'all'">
          <div class="event-list">
            <!-- 第一项 -->
            <div v-if="activities.length > 0" class="event-item">
              <img :src="activities[0].a_picPath" alt="Event Image">
              <div class="event-text">
                <div class="big-name">{{ activities[0].a_name }}</div>
                <hr class="line" />
                <div class="small-info">{{ activities[0].a_type }} - {{ activities[0].a_location }}</div>
                <div class="small-info">{{ formatDate(activities[0].a_beginTime) }} - {{ formatDate(activities[0].a_endTime) }}</div>
                <div class="read-more" @click="readMore(activities[0])">Read More >></div>
              </div>
            </div>
  
            <!-- 第二项 -->
            <div v-if="activities.length > 1" class="event-item">
              <div class="event-text">
                <div class="big-name">{{ activities[1].a_name }}</div>
                <hr class="line" />
                <div class="small-info">{{ activities[1].a_type }} - {{ activities[1].a_location }}</div>
                <div class="small-info">{{ formatDate(activities[1].a_beginTime) }} - {{ formatDate(activities[1].a_endTime) }}</div>
                <div class="read-more" @click="readMore(activities[1])">Read More >></div>
              </div>
              <img :src="activities[1].a_picPath" alt="Event Image">
            </div>
  
            <!-- 第三项 -->
            <div v-if="activities.length > 2" class="event-item">
              <img :src="activities[2].a_picPath" alt="Event Image">
              <div class="event-text">
                <div class="big-name">{{ activities[2].a_name }}</div>
                <hr class="line" />
                <div class="small-info">{{ activities[2].a_type }} - {{ activities[2].a_location }}</div>
                <div class="small-info">{{ formatDate(activities[2].a_beginTime) }} - {{ formatDate(activities[2].a_endTime) }}</div>
                <div class="read-more" @click="readMore(activities[2])">Read More >></div>
              </div>
            </div>
          </div>
          <div class="pagination-container">
            <button
              v-if="currentPage > 1"
              class="pagination-button"
              @click="goToPage(1)"
              style="width: 110px;"
            >
              &lt;&lt; 第一页
            </button>
            <button
              v-if="currentPage > 1"
              class="pagination-button"
              @click="goToPage(currentPage - 1)"
              style="width: 90px;"
            >
              &lt; 上一页
            </button>
            <span class="pagination-page-info">
              第 {{ currentPage }} 页 / 共 {{ totalPage }} 页
            </span>
            <button
              v-if="currentPage < totalPage"
              class="pagination-button"
              @click="goToPage(currentPage + 1)"
              style="width: 90px;"
            >
              下一页 &gt;
            </button>
            <button
              v-if="currentPage < totalPage"
              class="pagination-button"
              @click="goToPage(totalPage)"
              style="width: 110px;"
            >
              最后一页 &gt;&gt;
            </button>
          </div>
        </div>
        <div v-if="activeTab === 'available'">
          <p>可报名活动</p>
        </div>
      </div>
    </div>
    <footer>
      <p>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</p>
    </footer>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { defineEmits } from 'vue';
  
  const activeTab = ref('all');
  const tabs = ref([
    { label: '全部活动', name: 'all' },
    { label: '可报名活动', name: 'available' },
  ]);
  const currentPage = ref(1);
  const totalPage = ref(0);
  const activities = ref([]); // 存储当前页的活动数据
  const emit = defineEmits(['readMore']);
  
  const fetchActivities = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/activities', {
        params: {
          page: currentPage.value,
          size: 3 // 每页显示3项
        }
      });
      activities.value = response.data.activities; // 存储当前页的活动数据
      totalPage.value = response.data.totalPages;
    } catch (error) {
      console.error('Failed to fetch activities:', error);
    }
  };
  
  const goToPage = (page) => {
    if (page >= 1 && page <= totalPage.value) {
      currentPage.value = page;
      fetchActivities();
    }
  };
  
  const readMore = (activity) => {
    emit('readMore', activity);
  };
  
  const formatDate = (date) => {
    return new Date(date).toLocaleDateString();
  };
  
  onMounted(() => {
    fetchActivities();
  });
  </script>

<style scoped>
.container {
  background-color: white;
  width: 1200px;
  margin-bottom: 20px;
  padding: 10px 25px 25px 25px;
}
.event-list{
    position: relative;
    flex-direction: column;
    display: flex;
}
.tab-header {
  display: flex;
  border-bottom: 2px solid #eaeaea;
}

.tab-header button {
  padding: 10px 15px;
  margin-right: 5px;
  background-color: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-size: 16px;
}

.tab-header button.active {
  border-bottom: 2px solid #60a103;
  color: rgb(9, 126, 56);
}


.event-item {
  display: flex; 
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* 添加下方阴影 */
}

.event-item img {
  padding: 20px 0px 0px 0px;
  width: 50%; 
  height: 200px; 
  object-fit: cover; 
}


.event-text{
    position: relative;
    height:150px;
    padding: 20px 0px 20px 30px;
}

.big-name {
    padding: 10px 0px 0px 0px;
    font-size: 30px;
    font-weight: bold;
}
.line {
  height: 2px; 
  background-color: #d1d1d1; 
  border: none; 
  margin-top: 15px; 
  width: 571px; 
}
.small-info {
    padding: 10px 0px 0px 0px;
    font-size: 15px;
    color:  #858985;
}
.read-more {
  position: absolute; 
  bottom: 0px; 
  right: 20px; 
  padding: 10px 15px; 
  color:  rgb(9, 126, 56);
  text-decoration: none; 
  cursor: pointer;
  font-weight: bold;
}
.read-more:hover {
  color: #8cc9a6; /* 悬停时的文字颜色 */
}
footer {
    background-color: transparent;
    color: #ababab;
    text-align: center;
    padding: 0; 
    bottom: 0;
    width: 100%;
    font-size:xx-small;
}
.tab-content {
  position: relative; /* 设置定位参考 */
  padding: 10px 0px 0px 0px;
  min-height: 200px;
  border-top: none;
}

.pagination-container {
  padding: 20px 0px 0px 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  color:#858985;
  width:650px;
}

.pagination-button {
  margin: 0 5px;
  padding: 5px 10px;
  background-color: #eaeaea;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  text-align: center; /* 使文本居中 */
}

.pagination-button:hover {
  background-color: #60a103;
  color: white;
  font-weight:bold;
}

.pagination-page-info {
  margin: 0 10px;
  max-width: 200px;
  white-space: nowrap; /* 防止文本换行 */
}
<<<<<<< HEAD
</style>
=======
</style>
>>>>>>> 1312137d13c8f1507044bac004e8c25de30dfac7
