<template>
  <Nav />
  <main>
    <div>
      <RouterLink to="/forum">
        < 返回 </RouterLink>
          <article>
            <h1>{{ post?.title }}</h1>
            <section class="poster-info">
              <img class="avatar" :src="post?.author.avatar ? `${post?.author.avatar}` : '#'" alt="avatar" />
              <p>{{ post?.author.username }}</p>
            </section>

            <section>
              <p>{{ post?.content }}</p>
              <div class="postimage-container">
                <img v-for="image in post?.images" :key="image" :src="image ? `/public/static/${image}` : '#'"
                  alt="image" />
              </div>
              <div v-if="post?.original_post" class="oriPost-container" @click="toOriPost">
                <h2>{{ post?.original_post?.title }}</h2>
                <p>{{ post?.original_post?.author }}</p>
              </div>
            </section>

            <section class="interact-buttons">
              <p :style="likedButton" @click="likePost">点赞👍<span>{{ likeNum }}</span></p>
              <p @click="sharePost">分享🏑</p>
            </section>

            <section class="postComment-container">
              <textarea placeholder="理性发言，友善互动" v-model="comment" rows="99999" style="resize: none;"></textarea>
              <!-- @keyup.enter="submitComment" -->
              <input type="file" accept="image/*" multiple @change="handleFileUpload" ref="fileInput" />
              <p @click="submitComment">评论✍</p>
            </section>
            <p id="wrongWarning" v-if="warningSentence">{{ warningSentence }}</p>

            <section>
              <h2>{{ comments.length }}条评论</h2>
              <div class="comment-container" v-for="comment in comments" :key="comment.content">
                <span>
                  <img class="avatar" :src="comment.author.avatar ? `${comment.author.avatar}` : '#'" alt="avatar" />
                  <p>{{ comment.author.username }}</p>
                </span>
                <p>{{ comment.content }}</p>
                <div class="commentImage-container">
                  <img v-for="image in comment.images" :key="image" :src="image ? `/public/static/${image}` : '#'"
                    alt="image" />
                </div>
              </div>
            </section>
          </article>
    </div>
  </main>
  <!--底部版权信息-->
  <footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</footer>
</template>

<script setup lang="ts">
import router from '@/router';
import Nav from '../components/navbar.vue'
import axios from 'axios';
import { onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
interface Post {
  id: number;
  title: string;
  content: string;
  images: string[];
  author: {
    username: string;
    avatar: string;
  };
  original_post?: {
    id: number;
    title: string;
    author: string;
  } | null;
}

interface Comment {
  content: string;
  author: {
    username: string;
    avatar: string;
  };
  images: string[];
}

const post = ref<Post>();
const comments = ref<Comment[]>([]);

//获取post信息
const route = useRoute();
const fetchPostDetails = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/post/${route.params.id}`);
    if (response.status === 200) {
      post.value = response.data.posts;
      comments.value = response.data.comments;
      comments.value.reverse();
    }
    else {
      console.error('Failed to fetch post details');
    }
  }
  catch (error) {
    console.error('Error fetching post details:', error);
  }
};
onMounted(fetchPostDetails);
//点赞
const likedButton = reactive({
  backgroundColor: 'azure'
});
const likeNum = ref("本部分后端还未给出返回数据功能，后端完成后可参考添加");
const likePost = async () => {
  const response = await axios.post(`http://127.0.0.1:5000/post/${route.params.id}/like`);
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
    likeNum.value = response.data.like_count;
  } else {
    console.error(`ERROR: ${response.data.error}`);
  }
};
//评论
const comment = ref('');
const images = ref<File[]>([]);
const warningSentence = ref('');
const fileInput = ref<HTMLInputElement | null>(null);
const submitComment = async () => {
  if (comment.value) {
    warningSentence.value = '';
    const params = new FormData();
    params.append('content', comment.value);
    images.value.forEach((image, index) => {
      params.append('images', image);
    });
    const response = await axios.post(`http://127.0.0.1:5000/post/${route.params.id}/comment`, params, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.status === 200) {
      console.log('Comment submitted:', comment.value);
      comment.value = '';
      images.value = [];
      if (fileInput.value) {
        fileInput.value.value = '';
      }
      fetchPostDetails();
    }
    else {
      console.error('Failed to submit comment');
      warningSentence.value = '评论失败';
    }
  }
  else {
    warningSentence.value = '评论不能为空';
  }
};
const handleFileUpload = (e: Event) => {
  warningSentence.value = '';
  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (!files)
    return;
  else if (files.length > 3) {
    warningSentence.value = '最多上传3张图片';
    target.value = '';
  }
  else {
    images.value = Array.from(files);
  }
};
//跳转原帖
const toOriPost = () => {
  router.push(`/post/${post.value?.original_post?.id}`).then(() => {
    window.location.reload();
  });
};
//分享
const sharePost = () => {
  router.push(`/post/${post.value?.id}/share`).then(() => {
    window.location.reload();
  });
};
</script>

<style scoped>
main {
  padding-left: 200px;
  padding-right: 200px;
  background-color: #E7E6E6;
  margin-top: 9vh;
}

main>div {
  padding-top: 20px;
  background-color: white;
  padding-left: 20px;
  padding-right: 20px;
}

#wrongWarning {
  color: red;
  background-color: transparent;
}

/* 返回 */
a {
  text-decoration: none;
  color: grey;
}

/* 帖子内容 */
article {
  padding-left: 20px;
  padding-right: 20px;
  background-color: white;
  padding-bottom: 20px;
}

/* 标题 */
/* 头像 */
/* 用户名 */
.poster-info {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 2px;
}


/* 正文 */
.postimage-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.postimage-container img {
  height: 200px;
  max-width: 200px;
  object-fit: cover;
}

/* 转发 */
.oriPost-container {
  margin-top: 10px;
  margin-left: 20px;
  width: 30%;
  padding-left: 10px;
  padding-right: 10px;
  border-radius: 3px;
  border-style: solid;
  line-height: 0.5;
}

.oriPost-container p {
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

.interact-buttons>p,
.postComment-container>p {
  margin-top: 10px;
  border-radius: 5px;
  background-color: azure;
  width: 110px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 评论 */
.postComment-container {
  display: flex;
  justify-content: stretch;
  gap: 10px;
  margin-top: 10px;
  align-items: center;
}

.postComment-container>textarea {
  width: 60%;
  height: 80px;
  border-radius: 4px;
  padding-left: 10px;
}

.postComment-container>input {
  width: 160px;
  height: 40px;
  border-radius: 4px;
  padding-left: 10px;
}

.comment-container {
  border-top: 2px solid #ababab;
  padding-top: 10px;
  padding-left: 40px;
  margin-bottom: 10px;
}

.comment-container>span {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.comment-container>span img {
  width: 30px;
  height: 30px;
}

.comment-container>span p {
  font-size: small;
}

.commentImage-container {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.commentImage-container img {
  height: 100px;
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