<template>
    <RouterLink :to="`/post/${id}`">
        <div>
            <div>
                <h2>{{ title }}</h2>
                <p>{{ time }}</p>
            </div>
            <div>
                <img v-if="image" :src="image ? `public/static/${image}` : '#'" alt="Post Image">
                <p>{{ content }}</p>
            </div>
        </div>
    </RouterLink>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';

const props = defineProps<{
    id: number;
    title: string;
    time: string;
    content: string;
    image: string;
}>();
</script>

<style scoped>
/*单个帖子*/
a {
    color: black;
    text-decoration: none;
}

a>div {
    border-top: 2px solid #ababab;
    padding-bottom: 10px;
}

a>div>div {
    display: flex;
    gap: 10px;
}

a>div>div:nth-of-type(2)>img {
    width: 10vw;
    height: 10vw;
    flex: 1;
    object-fit: cover;
}

a>div>div:nth-of-type(2)>p {
    flex: 3;
}

a>div>div:nth-of-type(1) {
    justify-content: space-between;
}

a>div>div>p {
    color: grey;
}
</style>