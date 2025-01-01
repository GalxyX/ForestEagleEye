<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Nav from '../components/navbar.vue'
import postPreview from '../components/postPreview.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

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
if (!username.value || !user_id.value || !email.value) {
  router.push('/login');
}

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
  time: string;
}

const posts = ref<Post[]>([]);
onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/forum');
    if (response.status === 200) {
      posts.value = response.data;
    }
    else {
      console.error('Failed to fetch posts');
    }
  }
  catch (error) {
    console.error('Error fetching posts:', error);
  }
});
</script>
<template>
  <Nav />
  <main>
    <!-- 网页主体内容 -->
    <div>
      <!--左侧帖子-->
      <div class="posts-block">
        <h1>实时热帖</h1>
        <postPreview v-for="post in posts" :key="post.id" :id="post.id" :title="post.title" :time="post.time"
          :content="post.content_preview" :image="post.images.length ? post.images[0] : ''"
          :likeNum="post.like_count" />
      </div>
      <!--右侧信息-->
      <aside class="info-block">
        <img :src="avatar ?? '#'" alt="avatar" width="100" height="100" />
        <p>{{ username }}</p>
        <p>{{ signature }}</p>
        <div>
          <div>
            <p>今日阅读（播放）数</p>
            <p style="font-weight: bold; font-size: larger;">这里后端还没给出相应功能，等待后端以后写完了再添加</p>
            <p>昨日数据4</p>
          </div>
          <div>
            <p>今日新增赞同数</p>
            <p style="font-weight: bold; font-size: larger;">这里后端还没给出相应功能，等待后端以后写完了再添加</p>
            <p>昨日数据0</p>
          </div>
        </div>
        <RouterLink to="/postwrite">发点什么 ></RouterLink>
      </aside>
    </div>
  </main>
  <!--底部版权信息-->
  <footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</footer>
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
  margin: 20px 30px;
  text-align: center;
  background-color: #E7E6E6;

}

aside a {
  color: greenyellow;
  text-decoration: none;
  border-style: solid;
  border-radius: 10px;
  border-color: greenyellow;
  width: 80%;
  text-align: center;
}

aside a:hover {
  background-color: greenyellow;
  color: white;
}

aside a:active {
  background-color: greenyellow;
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
</style>
