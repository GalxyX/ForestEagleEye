<template>
  <!-- 页面内容 -->
  <NavigationBar />
  <div class="main">
    <aside class="sidebar">
      我是sidebar

    </aside>
    <main class="content">
      这里是主要内容
    </main>
    
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
.main{
  padding-top: 50px;
  background-color: #F0F2F5;
  display: flex;
}
.sidebar {
  width: 15vw;
  height:90vh;
  background-color: #456E02;
}
.content {
  flex: 1;
  height:90vh;
}
</style>