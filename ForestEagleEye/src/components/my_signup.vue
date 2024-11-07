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
        <div class="spacer"></div> <!-- 用于填充空间，将 mt-4 推到右侧 -->
        <div class="mt-4 right-side">
          <el-input
            v-model="input3"
            style="width: 500px"
            placeholder="请输入内容"
            class="input-with-select"
          >
          <template #prepend>
            <el-select v-model="select" placeholder="查询类型" style="width: 100px">
            <el-option label="活动名称" value="1" />
            <el-option label="报名人" value="2" />
            </el-select>
          </template>
         <template #append>
            <el-button :icon="Search" />
        </template>
        </el-input>
        </div>
      </div>

      <div class="tab-content">
        <div v-if="activeTab === 'all'">
          <div class="table">

          
          <el-table :data="tableData" style="width: 100%" max-height="640" height="640">
          <el-table-column fixed prop="name" label="活动名称" sortable  width="240" />
          <el-table-column prop="id" label="活动编号" sortable width="200" />
          <el-table-column prop="organization" label="主办单位" width="240" />
          <el-table-column prop="type" label="活动类型" width="200" />
          <el-table-column prop="date" label="活动开始日期" width="240" />
          <el-table-column prop="introduction" label="活动简介" width="400" />
          <el-table-column fixed="right" label="操作" min-width="240">
          <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="detail(scope.$index)"
          >
          活动详情
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="unregister(scope.$index)"
          >
          取消报名
          </el-button>
          </template>
         </el-table-column>
         </el-table>
        </div>
        <div class="count">
          共 5 项数据
        </div>
       </div>
       
       <div v-if="activeTab === 'started'">
        <div class="a_list">

          <!-- <div class="a_item" v-for="item in items" :key="item.id"> 此处连后端--> 
          <div class="a_item">
            <div class="text_info">
            <img class="event-img" src="../assets/default-avatar.png">
            <div class="group1">
              <div style="font-size: 16px; font-weight:bold;color:darkgray;padding:10px 0px 10px 20px">{{活动名称}}活动名称</div>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 10px 20px">{{活动编号}}活动编号|{{ 活动地点 }}活动地点|{{活动类型}}活动类型</div>
            </div>
            <div class="group2">
              <div style="font-size: 14px; color:darkgray;padding:10px 0px 10px 20px">报名人</div>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 10px 20px">{{报名人}}raracai</div>
            </div>
            <div class="group3">
              <div style="font-size: 14px; color:darkgray;padding:10px 0px 10px 20px">开始时间</div>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 10px 20px">{{开始时间}}2016.1.1 12:00</div>
            </div>
            <div class="group4">
              <img src="../assets/icon-right.png" alt="Check Icon" style="width: 20px; height: 20px;"/>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 0px 10px">已开始</div>
            </div>
            <div class="group5">
            <button class="text-button" @click="readMore">Read More >> </button>
            </div>
          </div>
          <el-divider class="custom-divider" style="margin: 10px;"/>
          </div>

        </div>


        <div class="pagination-container"><el-pagination background layout="prev, pager, next" :total="1000" /></div>
       </div>
       <div v-if="activeTab === 'ready'">
        <div class="a_list">

          <!-- <div class="a_item" v-for="item in items" :key="item.id"> 此处连后端--> 
          <div class="a_item">
            <div class="text_info">
            <img class="event-img" src="../assets/default-avatar.png">
            <div class="group1">
              <div style="font-size: 16px; font-weight:bold;color:darkgray;padding:10px 0px 10px 20px">{{活动名称}}活动名称</div>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 10px 20px">{{活动编号}}活动编号|{{ 活动地点 }}活动地点|{{活动类型}}活动类型</div>
            </div>
            <div class="group2">
              <div style="font-size: 14px; color:darkgray;padding:10px 0px 10px 20px">报名人</div>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 10px 20px">{{报名人}}raracai</div>
            </div>
            <div class="group3">
              <div style="font-size: 14px; color:darkgray;padding:10px 0px 10px 20px">开始时间</div>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 10px 20px">{{开始时间}}2016.1.1 12:00</div>
            </div>
            <div class="group4">
              <img src="../assets/icon-ready.png" alt="Check Icon" style="width: 20px; height: 20px;"/>
              <div style="font-size: 14px; color:darkgray;padding:0px 0px 0px 10px">待开始</div>
            </div>
            <div class="group5">
            <button class="text-button" @click="readMore">Read More >> </button>
            </div>
          </div>
          <el-divider class="custom-divider" style="margin: 10px;"/>
          </div>

        </div>


        <div class="pagination-container"><el-pagination background layout="prev, pager, next" :total="1000" /></div>
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
  // import { defineEmits } from 'vue';
  import { Search } from '@element-plus/icons-vue'
  const input3 = ref('')
  const select = ref('')
  
  const activeTab = ref('all');
  const tabs = ref([
    { label: '全部', name: 'all' },
    { label: '已开始', name: 'started' },
    { label: '待开始', name: 'ready' },
  ]);
  // const currentPage = ref(1);
  // const totalPage = ref(0);
  // const activities = ref([]); // 存储当前页的活动数据
  // const emit = defineEmits(['readMore']);
  
  // const fetchActivities = async () => {
  //   try {
  //     const response = await axios.get('http://127.0.0.1:5000/activities', {
  //       params: {
  //         page: currentPage.value,
  //         size: 3 // 每页显示3项
  //       }
  //     });
  //     activities.value = response.data.activities; // 存储当前页的活动数据
  //     totalPage.value = response.data.totalPages;
  //   } catch (error) {
  //     console.error('Failed to fetch activities:', error);
  //   }
  // };
  
  // const goToPage = (page) => {
  //   if (page >= 1 && page <= totalPage.value) {
  //     currentPage.value = page;
  //     fetchActivities();
  //   }
  // };
  
  // const readMore = (activity) => {
  //   emit('readMore', activity);
  // };
  
  // const formatDate = (date) => {
  //   return new Date(date).toLocaleDateString();
  // };
  
  // onMounted(() => {
  //   fetchActivities();
  // });



const now = new Date()

const tableData = ref([
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
  {
    name: '大砍树',
    date: '2016-05-01',
    id: '11111111111111',
    organization: '砍砍砍俱乐部',
    type: '伐木类',
    introduction: '砍树不好我爱砍树',
  },
])
</script>

<style scoped>
.container {
  background-color: white;
  width: 1200px;
  margin-bottom: 20px;
  padding: 10px 25px 25px 25px;
}
.tab-header {
  display: flex;
  border-bottom: 2px solid #eaeaea;
  align-items: center; /* 垂直居中 */
  justify-content: space-between; /* 两端对齐 */

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

.input-with-select .el-input-group__prepend {
  background-color: var(--el-fill-color-blank);
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
.spacer {
  flex-grow: 1; /* 填充剩余空间 */
}

.right-side {
  display: flex;
  align-items: center; /* 垂直居中 */
}
.count{
  font-size: small;
  color: #c7c7c7;
  padding: 10px;
}

.a_list{
  padding: 30px;
}
.event-img {
  width: 70px; /* 设置图片宽度为100px */
  height: 70px; /* 设置图片高度为100px */
}
.text_info{
  display: flex; /* 使用 flex 布局 */
  align-items: center; /* 垂直居中 */
}
.group1{
  display: flex;
  flex-direction: column;
  width: 320px; /* 设置图片宽度为100px */
}
.group2{
  display: flex;
  flex-direction: column;
  width: 120px; /* 设置图片宽度为100px */
}
.group3{
  display: flex;
  flex-direction: column;
  width: 180px; /* 设置图片宽度为100px */
}
.group4{
  display: flex;
  flex-direction: row;
  width: 300px; /* 设置图片宽度为100px */
}
.text-button {
  color: #ababab; /* 文字颜色 */
  background: none; /* 无背景 */
  border: none; /* 无边框 */
  padding: 0; /* 无内边距 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
  font-size: 16px; /* 文字大小 */
  text-decoration: none; /* 无下划线 */
  transition: text-decoration 0.3s; /* 平滑过渡效果 */
}

.text-button:hover {
  color:#60a103;
}
.pagination-container {
  display: flex; /* 启用 Flexbox */
  justify-content: flex-end; /* 将内容推向右侧 */
  padding: 10px; /* 根据需要调整内边距 */
  color:green;
}
</style>