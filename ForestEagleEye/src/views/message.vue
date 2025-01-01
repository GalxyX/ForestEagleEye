<template>
  <el-carousel interval="2500" arrow="always">
    <el-carousel-item v-for="(image, index) in sfImages" :key="index">
      <img :src="image" style="width: 100%; height: 100%;" alt="Forest Image">
    </el-carousel-item>
  </el-carousel>
</template>

<script setup>
import { ref } from 'vue';

const sfImages = ref([
  "/uploads/周小新的森林_2024-12-01_204742.png",
  "/uploads/周小新的森林_2024-12-05_194410.png",
  "/uploads/周小新的森林_2024-12-08_130544.png"
]);

// 注意：请确保服务器正确配置了静态资源路径，以便这些图片可以被浏览器访问。
</script>