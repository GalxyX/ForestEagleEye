<!-- 图片预览与点击查看 -->
<template>
    <img :key="key" :src="src ? src : '#'" :alt="alt" :style="{ height: props.height, width: props.width }"
        @click="previewImage(src)" />
</template>
<script setup lang="ts">
import { defineProps, ref } from 'vue';

const props = defineProps<{
    key: string;
    src: string;
    alt: string;
    height: string;
    width: string;
}>();
//预览图片
const previewImage = (image: string) => {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.background = 'rgba(0, 0, 0, 0.8)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.cursor = 'zoom-out';
    overlay.style.zIndex = '1000';

    const img = document.createElement('img');
    img.src = image;
    img.style.maxWidth = '90%';
    img.style.maxHeight = '90%';

    overlay.appendChild(img);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', () => {
        document.body.removeChild(overlay);
    });
};
</script>
<style scoped>
img {
    object-fit: cover;
}
</style>