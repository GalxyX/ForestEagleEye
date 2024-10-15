<template>
    <div>
      <NavigationBar />
      <h1>森林百科</h1>
      <!-- 页面内容 -->
    </div>
  </template>
  
  <script>
  import NavigationBar from '../components/navbar.vue'
  
  export default {
    name: 'encyclopedia',
    components: {
      NavigationBar
    }
  }
  </script>
  
  <style scoped>
  </style>