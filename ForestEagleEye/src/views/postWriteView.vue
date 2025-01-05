<script setup lang="ts">
import { onMounted, ref } from 'vue';
import axios from 'axios';
import Nav from '../components/navbar.vue'
import { Plus } from '@element-plus/icons-vue'
import { useRoute } from 'vue-router';
import router from '@/router';
//////////////////////////////////////////////////区别写帖与分享的不同跳转//////////////////////////////////////////////////
const route = useRoute();
const id = route.params.id;
const username = sessionStorage.getItem('username');

onMounted(() => {
  if (id) {
    console.log(`通过分享链接跳转，ID: ${id}`);
    fetchPostDetails();
  }
  else {
    console.log('通过写帖子链接跳转');
  }
});
//////////////////////////////////////////////////分享处理//////////////////////////////////////////////////
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
// 原帖内容
const ori_post = ref<Post>();
const fetchPostDetails = async () => {
  try {
    console.log('Fetching post details...');
    const response = await axios.get(`http://127.0.0.1:5000/post/${route.params.id}`, {
      params: {
        username: username
      }
    });
    if (response.status === 200) {
      ori_post.value = response.data.posts;
      console.log('Post details:', ori_post.value);
    }
    else {
      console.error('Failed to fetch post details');
    }
  }
  catch (error) {
    console.error('Error fetching post details:', error);
  }
};
//跳转原帖
const toOriPost = () => {
  router.push(`/post/${ori_post.value?.original_post?.id}`).then(() => {
    window.location.reload();
  });
};
//////////////////////////////////////////////////提交帖子//////////////////////////////////////////////////
const title = ref('');
const warningSentence = ref('');
const comment = ref('');
const imageList = ref<File[]>([]);
const submitPost = async () => {
  const formData = new FormData();
  // 获取标题和内容
  if (username)
    formData.append('username', username);
  formData.append('title', title.value);
  formData.append('content', comment.value);
  // 检测标题和内容是否为空
  if (title.value === '' || comment.value === '') {
    warningSentence.value = '标题或内容不能为空';
    ElMessage({
      showClose: true,
      message: warningSentence.value,
      type: 'warning'
    });
    return;
  }
  // 获取上传图片
  imageList.value.forEach((file, index) => {
    formData.append(`images`, file.raw);
  });
  // 提交帖子（区分纯发和分享）
  if (id) { // 分享
    const response = await axios.post(`http://127.0.0.1:5000/post/${id}/share`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.status === 200) {
      console.log('Post shared successfully:', response.data);
      window.location.href = '/forum';
    }
    else {
      console.error('Failed to share post');
      warningSentence.value = '分享失败';
      ElMessage({
        showClose: true,
        message: warningSentence.value,
        type: 'warning'
      });
    }
  }
  else { // 写帖
    const response = await axios.post(`http://127.0.0.1:5000/forum/post`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    if (response.status === 200) {
      console.log('Post submitted successfully:', response.data);
      window.location.href = '/forum';
    }
    else {
      console.error('Failed to submit comment');
      warningSentence.value = '评论失败';
      ElMessage({
        showClose: true,
        message: warningSentence.value,
        type: 'warning'
      });
    }
  }
  return;
};
//////////////////////////////////////////////////上传图片//////////////////////////////////////////////////
const dialogImageUrl = ref('');
const dialogVisible = ref(false);

const uploadDisabled = ref(false);
const handleExceed = () => {
  warningSentence.value = '最多上传9张图片';
  ElMessage({
    showClose: true,
    message: warningSentence.value,
    type: 'warning'
  });
  if (imageList.value.length >= 9) {
    uploadDisabled.value = true;
  }
};
const handleRemove = (file: File, fileList: File[]) => {
  imageList.value = fileList;
  if (imageList.value.length < 9) {
    uploadDisabled.value = false;
  }
};
const handlePictureCardPreview = (file: File) => {
  dialogImageUrl.value = URL.createObjectURL(file);
  dialogVisible.value = true;
};
const handleUpload = (file: File, fileList: File[]) => {
  imageList.value = fileList;
  console.log('file:', file);
  console.log('imageList:', imageList.value);
  if (imageList.value.length >= 9) {
    uploadDisabled.value = true;
  }
  ElMessage({
    showClose: true,
    message: `${imageList.value.length} 张图片已上传`,
    type: 'warning'
  });
};
</script>
<template>
  <Nav />
  <div class="write-page">
    <div class="all-contents">
      
      <el-page-header v-if="ori_post" @back="$router.go(-1)" content="分享帖子" title="返回">
        </el-page-header>
      
      <el-page-header v-else @back="$router.go(-1)" content="发帖子" title="返回">
        </el-page-header>

      <el-divider></el-divider>

      <!-- 转发显示 -->
      <h2 v-if="ori_post"style="color:grey;margin-left: 32px; font-size: 20px;">被引原贴</h2>
      <section v-if="ori_post" class="oriPost-container" @click="toOriPost">
      <div style="width:100%; ">
        <h2 class="title">{{ ori_post?.title }}</h2>
        <span style="display: flex; justify-content: space-between; align-items: center; width:100%;">
            <div style="display: flex;">
              <img :src="ori_post?.author.avatar" alt="avatar" />
              <p style="margin-left: 10px;">{{ ori_post?.author.username }}</p>
            </div>
            <div>
              <p style="padding-top:0px;margin-right: 20px;text-decoration: underline;width:100px;">点击查看更多</p>
            </div>
        </span>
      </div>

      </section>

      <div class="mycontent">
        <div class="left">
          <h2>创建你的标题</h2>
          <input type="text" v-model="title" placeholder="请输入标题" />

          <h2>上传图片</h2>
          <div style="margin-left: 50px;margin-top: 20px;margin-bottom: 20px;">
            <el-upload :multiple="true" accept="image/*" :limit="9" list-type="picture-card" :disabled="uploadDisabled"
              :on-preview="handlePictureCardPreview" :on-remove="handleRemove" :on-exceed="handleExceed" :auto-upload="false"
              :on-change="handleUpload">
              <el-icon>
                <Plus />
              </el-icon>
            </el-upload>
          </div>

        </div>
        <div class="right">
          <h2>创建你的内容</h2>
          <textarea placeholder="请输入内容" v-model="comment" rows="1" style="resize: none;"></textarea>
        </div>
      </div>
      <div style="  display: flex; /* 使用 Flexbox 布局 */
            justify-content: center; /* 水平居中 */
            align-items: center; /* 垂直居中 */">
          <button @click="submitPost">✍ 一键发布
          </button>
      </div>
    
    <!-- 上传图片 -->
    <!-- :file-list="imageList" -->
<!-- 
    <el-dialog v-model:visible="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog> -->
    
    </div>
    <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
  </div>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 9vh;
}

input {
  width: 90%;
  height: 5vh;
  margin-bottom: 1vh;
  border: 1.5px solid #cdcfcf;
  border-radius: 12px;
  padding-left: 10px;
  margin-left:40px;
  margin-top:10px;
}

textarea {
  width: 90%;
  height: 75%;
  margin-bottom: 1vh;
  border: 1.5px solid #cdcfcf;
  border-radius: 12px;
  padding-left: 10px;
  padding-top: 10px;
  margin-left:40px;
  margin-top:10px;
}
input:focus, textarea:focus {
  border: 1.5px solid #60a130;
  outline:none;
}
el-upload {
  width: 80%;
  margin-bottom: 1vh;
}

button {
  width:160px;
  height: 5vh;
  background-color: #60a130;
  color: white;
  border: none;
  border-radius: 18px;
  margin: 1vh;
  font-size: 15px;
}

/* 转发 */
.oriPost-container {
  margin: 10px;
  margin-left: 50px;
  width: 30%;
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
.write-page {
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
.left h2, .right h2 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #60a130;
  font-weight: light;
  margin-left: 30px;
}

.left, .right {
  width: 50%;
}
.mycontent{
  display: flex;
  flex-direction: row;
  padding-right: 20px;
}
.el-upload{
  margin-left: 89px;
}
.el-footer{
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size:xx-small;
  margin-top: 20px;
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
.oriPost-container:hover p {
  color: white;
}
.title{
  flex: 3;
  word-wrap: break-word;
  /* 使长单词换行 */
  word-break: break-all;
  /* 强制长单词换行 */
  line-height: 26px;
}
</style>
