<template>
  <div class="container">
    <el-carousel :interval="5000" arrow="always">
      <el-carousel-item v-for="item in 4" :key="item">
        <img :src="`image-${item}.jpg`" alt="carousel image" class="carousel-image">
        <h3>{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>


<script>
export default {
  // 您的脚本逻辑
};
</script>

<style scoped>
.container {
  padding-top: 20px;
  padding-left: 20px;
}
.el-carousel {
  height: 700px;
}
.el-carousel__item {
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
}
.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  margin: 0;
}
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}
.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}
.carousel-image {
  width: 100%;
  height: auto;
  object-fit: cover; /* 确保图片覆盖整个容器 */
}
</style>