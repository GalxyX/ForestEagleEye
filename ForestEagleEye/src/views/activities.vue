<template>
    <div class="main">
      <NavigationBar />
      <h1>林业活动</h1>
      <img src="../assets/register.png">
      <!-- 页面内容 -->
    </div>
  </template>
  
  <script>
  import NavigationBar from '../components/navbar.vue'
  
  export default {
    name: 'activities',
    components: {
      NavigationBar
    }
  }
  </script>
  
  <style scoped>
  .main{
    padding-top: 50px;
    background-color: #F0F2F5;
  }
  </style>