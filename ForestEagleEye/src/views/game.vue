<template>
    <div>
      <h1>森林相册</h1>
      <h2>为本林区上传资料图片，单次上传不得超过9张</h2>
      <el-upload
        v-model="fileList"
        action="/upload"
        list-type="picture-card"
        :on-preview="handlePictureCardPreview"
        :on-remove="handleRemove"
        :before-upload="beforeUpload"
        :limit="9"
        :on-exceed="handleExceed"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
  
      <el-dialog v-model="dialogVisible">
        <img width="100%" :src="dialogImageUrl" alt="Preview Image" />
      </el-dialog>

      <el-button class="ml-3" type="success" style="margin-top: 10px;" @click="submitUploadImage">
                上传至林上鹰眼
            </el-button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { Plus } from '@element-plus/icons-vue';
  import { ElUpload, ElIcon, ElDialog } from 'element-plus';
  
  const fileList = ref([]);
  const dialogImageUrl = ref('');
  const dialogVisible = ref(false);
  
  const handleRemove = (file, fileList) => {
    console.log(file, fileList);
  };
  
  const handlePictureCardPreview = (file) => {
    dialogImageUrl.value = file.url;
    dialogVisible.value = true;
  };
  
  const beforeUpload = (file) => {
    // 可以在这里添加文件类型检查等逻辑
    return true;
  };
  
  const handleExceed = (files, fileList) => {
    ElNotification({
        title: '上传失败',
        message: '单次上传不得超过9张图片！',
        type: 'error',
    });
  };
  </script>
  
  <style>
  /* 你的样式 */
  </style>