<template>
  <main>
    <div>
      <span>
        <img :src="avatar_img" alt="对话头像" />
        <p class="name">{{ name }}</p>
      </span>
      <p class="time">{{ time }}</p>
    </div>
    <p>{{ message }}</p>
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
main {
  border: 0px solid grey;
  border-top: 1px;
  margin: 5px 10px;
}

img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

div {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.name {
  font-weight: bold;
  display: inline;
}

.time {
  color: grey;
}
</style>