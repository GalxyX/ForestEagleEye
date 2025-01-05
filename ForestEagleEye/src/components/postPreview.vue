<template>
  <RouterLink :to="`/post/${id}`">
    <div >
      <div class="title-time" >
        <h2 class="title">{{ title }}</h2>
        <p style="font-size: small;">{{ time }}</p>
      </div>
      <div style="margin-left:20px; ">
        <p style="font-size: normal; margin-right: 10px; line-height: 1.5;">{{ content }}</p>
        <img v-if="image" :src="image ? `public/${image}` : '#'" alt="Post Image">
      </div>
    </div>
  </RouterLink>
  <div  style="display:flex; justify-content: space-between;  align-items: center; margin-bottom: 15px; margin-bottom: 10px;">
    <div class="interact-buttons" style="margin-left:20px;">
      <div v-if="liked">
        <el-button type="success" @click="likePost">点赞👍<span>{{ _likeNum }}</span></el-button>
      </div>
      <div v-else>
        <el-button plain type="success" @click="likePost">点赞👍<span>{{ _likeNum }}</span></el-button>
      </div>
      <el-button plain type="success" @click="sharePost">分享🏑</el-button>
    </div>

    <div class="read" @click="routerToPost">
      <p style="width: 55px; font-size: small;">阅读全文</p>
      <el-icon-d-arrow-right style="width: 20px;height: 20px;"></el-icon-d-arrow-right>
    </div>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import axios from 'axios';
import { defineProps, reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps<{
  id: number;
  title: string;
  time: string;
  content: string;
  image: string;
  likeNum: number;
  liked: boolean;
}>();

//点赞
const _likeNum = ref(props.likeNum);
const likedButton = reactive({
  backgroundColor: 'azure'
});
const likePost = async () => {
  const formData = new FormData();
  formData.append('username', sessionStorage.getItem('username') as string);
  const response = await axios.post(`http://127.0.0.1:5000/post/${props.id}/like`, formData);
  if (response.status === 200) {
    console.log('SUCCESS: Post liked successfully');
    if (response.data.is_liked) {
      console.log('Post is liked');
      likedButton.backgroundColor = 'green';
    }
    else {
      console.log('Post is not liked');
      likedButton.backgroundColor = 'azure';
    }
    _likeNum.value = response.data.like_count;
  } else {
    console.error(`ERROR: ${response.data.error}`);
  }
};
const router1 = useRouter(); // 使用useRouter钩子获取router对象
const routerToPost = () => {
  router1.push(`/post/${props.id}`); // 使用router.push进行路由跳转
};
//分享
const sharePost = () => {
  router.push(`/postshare/${props.id}`).then(() => {
    window.location.reload();
  });
};
onMounted(() => {
  if (props.liked) {
    likedButton.backgroundColor = 'green';
  }
  else {
    likedButton.backgroundColor = 'azure';
  }
});
</script>

<style scoped>
/*单个帖子*/
a {
  color: black;
  text-decoration: none;
}

a>div {
  border-top: 1px solid #d6d6d6;
  padding-bottom: 10px;
}

a>div>div {
  display: flex;
  gap: 10px;
}

a>div>div:nth-of-type(2)>img {
  width: 10vw;
  height: 8vw;
  flex: 1;
  object-fit: cover;
}
.title {
  flex: 3;
  word-wrap: break-word;
  /* 使长单词换行 */
  word-break: break-all;
  /* 强制长单词换行 */
}


a>div>div:nth-of-type(2)>p {
  flex: 3;
  word-wrap: break-word;
  /* 使长单词换行 */
  word-break: break-all;
  /* 强制长单词换行 */
}

a>div>div:nth-of-type(1) {
  justify-content: space-between;
}

a>div>div>p {
  color: grey;
}

/* 互动按钮 */
.interact-buttons {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
  align-items: center;
  margin-bottom: 5px;
}


.interact-buttons>p:hover {
  background-color: #60a130;
  color:white;
}

.interact-buttons>p {
  margin-top: 10px;
  border-radius: 15px;
  background-color: rgba(149, 242, 4, 0.1); 
  width: 110px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  color:#3c5c26;
  font-weight: bold;
}


.title-time{
  margin-top:10px;
  margin-left:20px;
  align-items: center; /* 垂直居中 */
  
}
.read{
  display:flex;
  align-items: center;
  color:#8e918d;
}
.read:hover{
  color:#60a130;
}
</style>