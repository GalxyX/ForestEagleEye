<template>
  <NavigationBar />
  <div class="main">
    <!-- 左边菜单栏 -->
    <div class="sidebar">
      <nav>
        <ul>
          <li v-for="item in menuItems" :key="item">
            <a
              href="#"
              class="sidebar-link"
              :class="{ active: currentMenuItem === item }"
              @click="currentMenuItem = item"
            >
              {{ item }}
            </a>
          </li>
        </ul>
      </nav>
    </div>
    
    <!-- 右侧内容部分 -->
    <div class="content">
      <!-- 暂时没有设置跳转逻辑 想看页面暂时这样修改吧 -->
      <!-- <Detail v-if="currentMenuItem === '活动风采'"/> -->
      <!-- <Event v-if="currentMenuItem === '活动风采'"/> -->
      <SignUp v-if="currentMenuItem === '活动风采'"/>
      <MySignUp v-if="currentMenuItem === '我的报名'"/>
      <!-- 这里可以添加其他的条件渲染，以显示不同的内容 -->
    </div>
  </div>
</template>

<!-- <script setup>
import { ref } from 'vue';
import NavigationBar from '../components/navbar.vue';
import Event from '../components/event.vue';
import Detail from '../components/event_detail.vue';

const currentMenuItem = ref('活动风采');
const menuItems = ref([
  '活动风采', '我的报名', '我的申请', '我的审批', '数据管理'
]);
const showDetail = ref(false);
const selectedEvent = ref(null);
const showEventList = ref(true);

const handleReadMore = (event) => {
  console.log("Received event:", event);
  selectedEvent.value = event;
  showDetail.value = true;
  showEventList.value = false;
};

const closeDetail = () => {
  showDetail.value = false;
  showEventList.value = true;
};
</script> -->

<script>
import { ref } from 'vue';
import NavigationBar from '../components/navbar.vue';
import Event from '../components/activity.vue';
import Detail from '../components/activity_detail.vue';
import SignUp from '../components/activity_signup.vue';
import MySignUp from '../components/my_signup.vue';

export default {
  name: 'activities',
  components: {
    NavigationBar,
    Event,
    Detail,
    SignUp,
    MySignUp
  },
  setup() {
    const currentMenuItem = ref('活动风采');
    const menuItems = ref([
      '活动风采', '我的报名', '我的申请', '我的审批', '数据管理'
    ]);
    const showDetail = ref(false);
    const selectedEvent = ref(null);
    const showEventList = ref(true);

    const handleReadMore = (event) => {
      console.log("Received event:", event);
      selectedEvent.value = event;
      showDetail.value = true;
      showEventList.value = false;
    };

    const closeDetail = () => {
      showDetail.value = false;
      showEventList.value = true;
    };

    return {
      currentMenuItem,
      menuItems,
      showDetail,
      selectedEvent,
      showEventList,
      handleReadMore,
      closeDetail
    };
  }
};
</script>





<style scoped>
.main {
  display: flex;
  padding-top: 50px;
  background-color: #F0F2F5;
  flex-direction: row;
}
.sidebar {
  width: 200px;
  background-color: #60a103;
  color: white;
  padding: 0px;
  box-sizing: border-box;
  height: 100vh;
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar-link,
.submenu-link {
  color: white;
  text-decoration: none;
  padding: 20px 20px; 
  text-align: center; 
  display: block;
  font-size: 16px;
}
.submenu-link {
  padding-left: 30px;
}
.sidebar-link:hover {
  background-color: white;
  color: rgb(9, 126, 56);
  font-weight: bold; 
}
.sidebar-link.active {
  background-color: #eaf9ed; 
  color: rgb(9, 126, 56);
  font-weight: bold; 
}
.content {
  margin-top: 20px;
  margin-left: 25px;
  justify-content: center;
}
</style>