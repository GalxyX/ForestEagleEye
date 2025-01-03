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

onMounted(() => {
  if (id) {
    console.log(`通过分享链接跳转，ID: ${id}`);
    fetchPostDetails(); // 正确调用 fetchPostDetails 函数
    // 根据 ID 执行相应的逻辑，例如加载已有的帖子内容
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
    const response = await axios.get(`http://127.0.0.1:5000/post/${route.params.id}`);
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
  <main>
    <input type="text" v-model="title" placeholder="创建你的标题" />
    <!-- 转发显示 -->
    <section v-if="ori_post" class="oriPost-container" @click="toOriPost">
      <h2>{{ ori_post?.title }}</h2>
      <p>{{ ori_post?.author }}</p>
    </section>

    <textarea placeholder="创建你的内容" v-model="comment" rows="1" style="resize: none;"></textarea>
    <!-- 上传图片 -->
    <!-- :file-list="imageList" -->
    <el-upload :multiple="true" accept="image/*" :limit="9" list-type="picture-card" :disabled="uploadDisabled"
      :on-preview="handlePictureCardPreview" :on-remove="handleRemove" :on-exceed="handleExceed" :auto-upload="false"
      :on-change="handleUpload">
      <el-icon>
        <Plus />
      </el-icon>
    </el-upload>
    <el-dialog v-model:visible="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>

    <button @click="submitPost">发布✍</button>
  </main>
</template>
<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 9vh;
}

input {
  width: 80%;
  height: 5vh;
  margin-bottom: 1vh;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding-left: 1vh;
}

textarea {
  width: 80%;
  height: 20vh;
  margin-bottom: 1vh;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding-left: 1vh;
}

el-upload {
  width: 80%;
  margin-bottom: 1vh;
}

button {
  width: 80%;
  height: 5vh;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 5px;
  margin: 1vh;
}

/* 转发 */
.oriPost-container {
  margin: 10px;
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
</style>
