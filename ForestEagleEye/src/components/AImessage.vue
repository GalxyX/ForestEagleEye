<template>
  <main class="message-container" :class="{ 'left': name === '小林', 'right': name !== '小林' }">
    
    <div class="message-content">
      <div v-if="name==='小林'" class="message-header-left">
        <img :src="avatar_img" alt="对话头像" class="avatar" />
        <p class="name">{{ name }}</p>
      </div>
      <div v-else class="message-header-right">
        <p class="name">{{ name }}</p>
        <img :src="avatar_img" alt="对话头像" class="avatar" />
      </div>

      <div
        class="message-bubble"
        :style="{
          backgroundColor: name === '小林' ? 'white' : '#d4edda', /* 浅绿色背景 */
          color: '#333', 
          border: name !== '小林' ? '1px solid #28a745' : '1px solid #ccc' /* 边框颜色 */
        }"
      >
        <p>{{ message }}</p>
        
      </div>
      <p class="time">{{ time }}</p>
    </div>
  </main>
</template>

<script setup lang="ts">
const props = defineProps<{
  avatar_img: string;
  name: string;
  time: string;
  message: string;
}>();
</script>

<style scoped>
.message-container {
  display: flex;
  align-items: flex-start;
  margin: 10px 0;
}

/* AI 消息靠左 */
.message-container.left {
  flex-direction: row;
}

/* 用户消息靠右 */
.message-container.right {
  flex-direction: row-reverse;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 10px;
}

.message-content {
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  padding: 5px 10px;
  max-width: 70%;
}

.message-header-left {
  align-items: center;
  font-size: 12px;
  color: #888;
  display: flex;
  justify-content: left;
}

.message-header-right {
  align-items: center;
  font-size: 12px;
  color: #888;
  display: flex;
  justify-content: right;
}

.name {
  font-weight: bold;
  color: #333;
  font-size: 15px;
  /* 调大字体 */
}

.time {
  font-size: 12px;
  color: #aaa;
  margin-left: 20px;
  margin-right: 20px;
}

.message-bubble {
  border-radius: 10px;
  padding: 0px 20px;
  /* 调整上下和左右的文字空隙 */
  margin-top: 3px;
  /* 调小消息框与上一部分的间距 */
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
  margin-left: 20px;
  margin-right: 20px;
}
</style>
