<template>
  <Nav />
  <div class="detail-page">
    <div class="all-contents">
      <el-page-header @back="$router.go(-1)" content="帖子详情" title="返回"></el-page-header>

      <el-divider></el-divider>

          <article>
            <div>
              <section class="poster-title">
                <div style="display: flex; align-items: center;">
                  <h1 class="titleh1">{{ post?.title }}</h1>
                  <p style="margin-left:30px;">{{ post?.time ? formatDateTime(post.time) : '' }}</p>
                </div>
                  <section class="poster-info">
                    <p style="font-weight: bold;">{{ post?.author.username }}</p>
                    <img class="avatar" :src="post?.author.avatar ? `${post?.author.avatar}` : '#'" alt="avatar" />
                  </section>
              </section>
            </div>

            <el-divider border-style="dashed" />
            <div style="display: flex;justify-content: space-between;margin-left: 30px;margin-right: 30px;gap:50px;">
              <section>
                <h2 class="h2title">原文</h2>
                <p class="pcontext">{{ post?.content }}</p>
                <h2 v-if="post?.original_post" style="color:grey;margin-top: 30px; font-size: 20px;">被引原贴</h2>
                <div v-if="post?.original_post" class="oriPost-container" @click="toOriPost">
                  <div>
                    <h2 class="oriposttitle">{{ post?.original_post?.title }}</h2>
                    <span style="display: flex; justify-content: space-between; align-items: center; width:100%;">
                      <div style="display: flex; align-items: center;">
                        <img :src="post?.original_post?.avatar ? `${post?.original_post?.avatar}` : '#'" alt="avatar" />
                        <p style="margin-left: 10px;">{{ post?.original_post?.author }}</p>
                      </div>
                      <div>
                        <p style="padding-top:0px;margin-right: 20px;text-decoration: underline;">点击查看更多</p>
                      </div>
                    </span>
                  </div>
                </div>
              </section>
              <div class="postimage-container">
                  <ImageViewer v-for="image in post?.images" :key="image" :alt="image"
                    :src="image ? `/public/${image}` : '#'" height="200px" width="200px" />
              </div>
            </div>

            <el-divider border-style="dashed" />

            <div class="upload">
              <div style="display: flex; justify-content: space-between;margin-right: 20px;margin-left: 20px;">
                <section class="postComment-container">
                <div>
                  <textarea placeholder="留下你想说的话~~ 理性发言，友善互动" v-model="comment" rows="99999" style="resize: none;"></textarea>
                  <!-- @keyup.enter="submitComment" -->
                  <!-- <input type="file" accept="image/*" multiple @change="handleFileUpload" ref="fileInput" /> -->

                  <div class="btn-box">
                    <button class="btn">上传图片</button>
                    <!-- <input type="file" id="file" accept="image/*" @change="handleFileUpload" class="file-ipt" > -->
                    <input type="file" accept="image/*" @change="handleFileUpload" ref="fileInput" class="file-ipt" />
                  </div>

                  <p @click="submitComment">发布评论✍</p>
                </div>

              </section>

              <section class="interact-buttons">
                <p :style="likedButton" @click="likePost">点赞👍<span>{{ likeNum }}</span></p>
                <p @click="sharePost">分享🏑</p>
              </section>
              </div>

           <!--上传图片的预览-->
              <ul>
              </ul>
            </div>


            <p id="wrongWarning" v-if="warningSentence">{{ warningSentence }}</p>

            <el-divider border-style="dashed" />

            <section>
              <h2 style="font-size: 30px; margin-left: 20px; margin-top: 0px; margin-bottom: 20px;color:#60a130;">{{ comments.length }}条评论</h2>
              <div class="comment-container" v-for="comment in comments" :key="comment.content">
                <span style="align-items: center;">
                  <img class="avatar" :src="comment.author.avatar ? `${comment.author.avatar}` : '#'" alt="avatar" />
                  <p>{{ comment.author.username }}</p>
                </span>
                <p style="margin-left:20px ;">{{ comment.content }}</p>
                <div class="commentImage-container">
                  <!-- <img v-for="image in comment.images" :key="image" :src="image ? `/public/static/${image}` : '#'"
                    alt="image" @click="previewImage(image)" /> -->
                  <ImageViewer v-for="image in comment.images" :key="image" :alt="image"
                    :src="image ? `/public/${image}` : '#'" height="100px" width="100px" />
                </div>
              </div>
            </section>
          </article>
    </div>
    <footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</footer>
  </div>
  <!--底部版权信息-->
  
</template>

<script setup lang="ts">
import router from '@/router';
import Nav from '../components/navbar.vue'
import axios from 'axios';
import { createApp, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import ImageViewer from '@/components/imageViewer.vue';
import { formatDateTime } from '@/components/fotmatTime';
interface Post {
  id: number;
  title: string;
  content: string;
  images: string[];
  time: Date;
  author: {
    username: string;
    avatar: string;
  };
  original_post?: {
    id: number;
    title: string;
    author: string;
    avatar: string;
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
const likeNum = ref(999);
const username = sessionStorage.getItem('username');

//获取post信息
const route = useRoute();
const likedButton = reactive({
  backgroundColor: 'azure'
});
const fetchPostDetails = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/post/${route.params.id}`, { params: { username: username } });
    if (response.status === 200) {
      post.value = response.data.posts;
      console.log('Post details:', post.value);
      if (post.value) {
        post.value.time = new Date(response.data.posts.time); // 将时间字符串转换为 Date 对象
      }
      comments.value = response.data.comments;
      comments.value.reverse();
      likeNum.value = response.data.like_count;
      if (response.data.is_liked) {
        likedButton.backgroundColor = 'green';
      }
      else {
        likedButton.backgroundColor = 'azure';
      }
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
const likePost = async () => {
  const params = new FormData();
  params.append('username', username as string);
  const response = await axios.post(`http://127.0.0.1:5000/post/${route.params.id}/like`, params, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
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
  }
  else {
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
    params.append('username', username as string);
    const response = await axios.post(`http://127.0.0.1:5000/post/${route.params.id}/comment`, params, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.status === 200) {
      console.log('Comment submitted:', comment.value);
      comment.value = '';
      images.value = [];
      const imagesList = document.querySelector('.upload ul');
      if (imagesList) {
        imagesList.innerHTML = '';
      }
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

  //上传图片的预览
  const imagesList = document.querySelector('.upload ul');
  if (images.value.length && imagesList) {
    imagesList.innerHTML = '';
    for (let i = 0; i < images.value.length; i++) {
      const li = document.createElement('li');
      imagesList.appendChild(li);
      const app = createApp(ImageViewer, {
        src: URL.createObjectURL(images.value[i]),
        alt: images.value[i].name,
        height: '100px',
        width: '100px'
      });
      app.mount(li);
    }
  }
  else {
    warningSentence.value = "显示图片预览失败";
    console.error('No images selected or container not found');
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
  router.push(`/postshare/${post.value?.id}`).then(() => {
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
.poster-title {
  display: flex;
  justify-content: space-between; /* 子元素横向排布，两端对齐 */
  align-items: center; /* 子元素在垂直方向上居中对齐 */
  margin-right: 20px;
  height: 100%; /* 确保容器的高度占满其父容器的高度 */
}

.poster-title p {
  color: grey;
}

/* 头像 */
/* 用户名 */
.poster-info {
  margin-left: 50px;
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

/* 
.postimage-container img {
  height: 200px;
  max-width: 200px;
  object-fit: cover;
} */

/* 转发 */
.oriPost-container {
  margin-top: 10px;
  width: 800px;
  padding-left: 20px;
  padding-top: 12px;
  padding-bottom: 12px;
  padding-right: 10px;
  border-radius: 14px;
  border: 2px solid #60a130; /* 设置边框为2px宽的实线，颜色为#60a130 */
  line-height: 0.5;
  box-shadow: 0 13px 20px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  display: flex;
  justify-content: space-between;
}

.oriPost-container:hover {
  border: 2px solid #60a130; /* 设置边框为2px宽的实线，颜色为#60a130 */
  background-color: #60a130;
  color:#ffffff;
}

.oriPost-container p {
  color: grey;
}

.oriPost-container span {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
}

.oriPost-container span img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

/* 互动按钮 */
.interact-buttons {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
  align-items: center;
}

.interact-buttons>p,
.postComment-container p {
  border-radius: 15px;
  background-color: rgb(230, 245, 235);
  border: 2px solid #60a103;
  width: 110px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.interact-buttons>p:hover{
  background-color: #60a103;
}
.postComment-container p :focus{
  background-color: #60a103;
}
/* 评论 */
.postComment-container>div {
  display: flex;
  justify-content: stretch;
  gap: 10px;
  margin-top: 10px;
  align-items: center;
}

.postComment-container textarea {
  width: 500px;
  height: 80px;
  border-radius: 4px;
  padding-left: 10px;
  padding-top: 10px;
}

.postComment-container input {
  width: 160px;
  border-radius: 5px;
  margin: 20px;
  color: #60a103;
  margin-left: 20px;
}
.postComment-container textarea:focus {
  border-color: green; /*设置选中时的边框颜色为绿色 */
  outline:none;/*移除默认的选中样式*/
}
.upload ul {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  margin-left: 0px;
  flex-wrap: wrap;
  list-style-type: none;
}

.comment-container {
  border-top: 1px solid #60a130;
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

/* .commentImage-container img {
  height: 100px;
  width: 100px;
  object-fit: cover;
} */

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
.detail-page {
  display: flex;       /* 使用Flexbox布局 */
  flex-direction: column; /* 设置主轴方向为垂直 */
  background-color: #f0f2f5;
}
.all-contents{
  background-color: #ffffff;
  margin-left: 20px; /* 左边距 */
  margin-right: 20px; /* 右边距 */
  margin-top: 70px;
  display: flex;
  flex-direction: column; /* 设置子元素纵向排列 */
  padding-bottom: 30px;
}
.el-page-header {
  margin-top: 20px; /* 或者其他适当的值 */
  margin-left: 20px; /* 左边距 */
}
.try-btn{
  color:#60a103;
  border: 1px solid#60a103;
  border-radius: 10px;
  margin: 0;
}
.try-btn:hover{
  color:#ffffff;
  border: 1px solid#60a103;
}
.oriPost-container:hover p {
  color: white;
}

.h2title{
  color:grey;
  margin-top: 5px;
   font-size: 20px;
}
.pcontext{
  font-size:16px;
  color:rgb(93, 95, 94);
  width:800px;
  flex: 3;
  word-wrap: break-word;
  /* 使长单词换行 */
  word-break: break-all;
  /* 强制长单词换行 */
}
.oriposttitle{
  padding-right: 20px;
  padding-left: 0px;
  line-height: 26px;
  flex: 3;
  word-wrap: break-word;
  /* 使长单词换行 */
  word-break: break-all;
  /* 强制长单词换行 */
}








.img {
    width: 80px;
    height: 80px;
    border: 1px solid rgb(143, 59, 59);
    }

.btn-box {
    position: relative;
    }

.file-ipt {
    position: absolute;
    left: 0;
    top: 0;
    opacity: 0; 
    }

.btn {
    width: 100px;
    height: 30px;
    background-color: #60a130;
    color: white;
    margin-right: 10px;
    border: none;
    border-radius: 10px;
}
.titleh1{
  width:1400px;
  font-size: 30px; 
  margin-left: 20px; 
  margin-top: 0px; 
  margin-bottom: 0px;
  color:#60a130;
  flex: 3;
  word-wrap: break-word;
  /* 使长单词换行 */
  word-break: break-all;
  /* 强制长单词换行 */
}
</style>