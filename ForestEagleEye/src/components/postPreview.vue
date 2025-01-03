<template>
  <RouterLink :to="`/post/${id}`">
    <div>
      <div>
        <h2>{{ title }}</h2>
        <p>{{ time }}</p>
      </div>
      <div>
        <img v-if="image" :src="image ? `public/${image}` : '#'" alt="Post Image">
        <p>{{ content }}</p>
      </div>
    </div>
  </RouterLink>

  <div class="interact-buttons">
    <p :style="likedButton" @click="likePost">点赞👍<span>{{ _likeNum }}</span></p>
    <p @click="sharePost">分享🏑</p>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import axios from 'axios';
import { defineProps, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps<{
  id: number;
  title: string;
  time: string;
  content: string;
  image: string;
  likeNum: number;
}>();

//点赞
const _likeNum = ref(props.likeNum);
const likedButton = reactive({
  backgroundColor: 'azure'
});
const likePost = async () => {
  const response = await axios.post(`http://127.0.0.1:5000/post/${props.id}/like`);
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
//分享
const sharePost = () => {
  router.push(`/postshare/${props.id}`).then(() => {
    window.location.reload();
  });
};
</script>

<style scoped>
/*单个帖子*/
a {
  color: black;
  text-decoration: none;
}

a>div {
  border-top: 2px solid #ababab;
  padding-bottom: 10px;
}

a>div>div {
  display: flex;
  gap: 10px;
}

a>div>div:nth-of-type(2)>img {
  width: 10vw;
  height: 10vw;
  flex: 1;
  object-fit: cover;
}

a>div>div:nth-of-type(2)>p {
  flex: 3;
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
  gap: 10px;
  margin-top: 50px;
  align-items: center;
}

.interact-buttons>p {
  margin-top: 10px;
  border-radius: 5px;
  background-color: azure;
  width: 110px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>