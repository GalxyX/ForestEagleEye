<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Nav from '../components/navbar.vue'
import postPreview from '../components/postPreview.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { formatDateTime } from '@/components/formatTime';

const username = ref(sessionStorage.getItem('username'));
const avatar = ref(sessionStorage.getItem('avatar'));
const user_id = ref(sessionStorage.getItem('user_id'));
const email = ref(sessionStorage.getItem('email'));
const role = ref(sessionStorage.getItem('role'));
const signupTime = ref(sessionStorage.getItem('signupTime'));
const newestTime = ref(sessionStorage.getItem('newestTime'));
const days = ref(sessionStorage.getItem('days'));
const signature = ref(sessionStorage.getItem('signature'));
const inst = ref(sessionStorage.getItem('inst'));
const forest = ref(sessionStorage.getItem('forest'));

const router = useRouter();

interface Post {
  id: number;
  title: string;
  content_preview: string;
  images: string[];
  like_count: number;
  is_liked: boolean;
  author: {
    username: string;
    avatar: string;
  };
  original_post?: {
    id: number;
    title: string;
  } | null;
  time: Date;
}
const total_likes = ref<number>(0);
const total_writes = ref<number>(0);

const posts = ref<Post[]>([]);
onMounted(async () => {
  try {
    if (!username.value || !user_id.value || !email.value) {
      router.push('/login');
    }
    else {
      const response = await axios.get('http://127.0.0.1:5000/forum', { params: { username: username.value } });
      if (response.status === 200) {
        posts.value = response.data.posts.map((item: any) => ({
          ...item,
          time: new Date(item.time)
        }));
        total_likes.value = response.data.total_likes
        total_writes.value = response.data.total_writes
        console.log(total_likes.value);
        console.log(total_writes.value);
      }
      else {
        console.error('Failed to fetch posts');
      }
    }
  }
  catch (error) {
    console.error('Error fetching posts:', error);
  }
});
</script>
<template>
  <Nav />
  <main style="background-color:#f0f2f5;">
    <!-- 网页主体内容 -->
    <div class="all-contents">
      <div class="posts-block">
        <!--顶部论坛介绍-->
        <div style="display: block; margin-bottom: 30px;">
          <h1 style="font-size: x-large; margin-bottom: 10px; margin-top:30px; color: #60a130;">Forest Forum</h1>
          <h2 style="font-size: xx-large; margin-top: 10px; margin-bottom: 10px;">实时热帖</h2>
          <el-alert
            title="🔈论坛公告：欢迎来到林上论坛！在这里与森林爱好者一起分享知识、活动打卡、探讨热点话题，携手构建一个充满活力的森林交流平台。您在论坛中的所有行为都应遵守法律法规，发布内容真实、尊重他人、原创保护！"
            type="warning"
            :closable="false"
            style="font-size: small;">
          </el-alert>
        </div>
        <!--左侧帖子-->
        <postPreview v-for="post in posts" :key="post.id" :id="post.id" :title="post.title"
          :time="formatDateTime(post.time)" :content="post.content_preview"
          :image="post.images.length ? post.images[0] : ''" :likeNum="post.like_count" :liked="post.is_liked" />
        <!-- <div v-for="post in posts" :key="post.id" class="post">
          <el-divider border-style="dashed" />
          <h1>{{ post.title }}</h1>
          <p class="time">{{ post.time }}</p>
          <p class="content">{{ post.content_preview }}</p>
          <img v-if="post.images.length" :src="post.images[0]" alt="Post Image" class="post-image">
          <p class="like-num">点赞数: {{ post.like_count }}</p>
        </div> -->
      </div>
      <!--右侧信息-->
      <div class="right">
        <aside class="info-block">
          <img :src="avatar ?? '#'" alt="avatar" width="100" height="100" />
          <p style="font-size: 20px;margin-top: 20px;margin-bottom: 10px;font-weight:bold;">{{ username }}</p>
          <div class="signature">
            <el-icon-location style="width:20px;height: 20px;color:#60a130;font-weight: bolder;"></el-icon-location>
            <p>{{ signature }}</p>
          </div>
          <div class="unit3">
            <div class="unit2">
              <div class="unit">
                <p class="h2">发布数</p>
                <p class="text">{{ total_writes }}</p>
              </div>
              <el-divider style="width: 100px;"></el-divider>
              <div class="unit">
                <p class="h2">昨日点赞数据</p>
                <p class="text">13</p>
              </div>
            </div>
            <el-divider direction="vertical" style="height: 150px;"></el-divider>
            <div class="unit2">
              <div class="unit">
                <p class="h2">赞同数</p>
                <p class="text">{{ total_likes }}</p>
              </div>
              <el-divider style="width: 100px;"></el-divider>
              <div class="unit">
                <p class="h2">昨日发布数据</p>
                <p class="text">8</p>
              </div>
            </div>
          </div>


          <RouterLink to="/postwrite" class="sendbottom">
            <el-icon-edit style="width: 25px;height: 25px;margin-right: 10px;"></el-icon-edit>
            发点什么
          </RouterLink>
        </aside>
        
        <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
      </div>

    </div>
    <!--底部版权信息-->
  <footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</footer>
  </main>
</template>


<style scoped>
main {
  padding-left: 200px;
  padding-right: 200px;
  background-color: #E7E6E6;
}

main>div {
  padding-top: 10px;
  margin-top: 9vh;
  display: flex;
  gap: 10px;
  background-color: #E7E6E6;
}

.posts-block {
  padding-left: 40px;
  padding-right: 40px;
  flex: 5;
  background-color: white;
}

.info-block {
  flex: 2;
  background-color: white;
  padding-top: 30px;
}

/*个人信息*/
aside {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 600px;
}

aside>div {
  display: flex;
  gap: 20px;
  margin: 20px 40px;
  text-align: center;
  background-color: rgba(219, 219, 219, 0.167);
  border-radius: 30px;
}

aside a {
  color: #60a130;
  text-decoration: none;
  border-style: solid;
  border-radius: 40px;
  border-color: #60a130;
  width: 80%;
  text-align: center;
  font-size: 20px;
  width: 200px;
  height: 60px;
  display: flex;
  align-items: center;
  /* 垂直居中 */
  justify-content: center;
  /* 水平居中（如果需要） */
  font-weight: bold;
  margin-top: 10px;
}

aside a:hover {
  background-color: #60a130;
  color: white;
}

aside a:active {
  background-color: #60a130;
  color: white;
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

.all-contents {
  background-color: #f0f2f5;
  margin-left: 20px;
  /* 左边距 */
  margin-right: 20px;
  /* 右边距 */
  margin-top: 60px;
  display: flex;
}

.posts-block h1 {
  color: #60a130;
  font-size: 20px;
  margin-top: 20px;
}

.signature {
  display: flex;
  background-color: white;
  align-items: center;
  margin-top: 0px;
  margin-bottom: 0px;
  gap: 10px;
}

.signature p {
  color: #858383;
}

.unit {
  display: flex;
  flex-direction: column;
  /* 设置子元素垂直排列 */
}

.h2 {
  font-size: 20px;
  margin-top: 0px;
  margin-bottom: 0px;
  font-size: 16px;
  color: #4b4b4b;
}

.text {
  font-weight: bold;
  font-size: larger;
  margin-top: 10px;
  margin-bottom: 0px;
  color: #4b4b4b;
}

.unit2 {
  display: flex;
  flex-direction: column;
}

.unit3 {
  padding-left: 40px;
  padding-right: 40px;
  padding-top: 30px;
  padding-bottom: 30px;
  margin-top: 10px;
  margin-bottom: 30px;
}

/* .right{
  position: fixed;
  top: 40px; 
  left: 1300px; 
} */
.sendbottom {
  border: 1px solid #60a130;
  border-radius: 10px;
  font-weight: normal;
  font-size: 12pt;
  height: 40px;
  width: 200px;
}
</style>
