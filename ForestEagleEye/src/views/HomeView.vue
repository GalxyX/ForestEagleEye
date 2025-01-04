<script setup lang="ts">
import { ref,onMounted } from 'vue'
import Nav from '../components/navbar.vue'
import axios from "axios";

onMounted(async () => {
  choose_i_pic(0);
  slideShow();

   try{
    const resp = await axios.get('http://127.0.0.1:5000/get_top5_participation')
    const response = resp.data
    if (response.status === 'success') {
      topParticipationList.value = response.data
      console.log('已更新 topParticipationList')
    } else {
      console.error('接口返回异常: ', response.message || response)
    }
  } catch (err) {
    console.error('请求 http://127.0.0.1:5000/get_top5_participation 时出错: ', err)
  }
  console.log(topParticipationList.value);

})

function scrollToContent() {
window.scrollTo({
top: 950, // 指定滚动到的位置
 behavior: 'smooth' // 平滑滚动
 });
}
//图片自动轮播
function slideShow() {
  const waiting_time = 100000;
  let interval = setInterval(show_next_pic, waiting_time);
  let now = 0;
  let pic_box = document.querySelector('.slideshow-images-container');
  if (pic_box) {
    pic_box.addEventListener('mouseover', () => {
      clearInterval(interval);
    });
    pic_box.addEventListener('mouseout', () => {
      interval = setInterval(() => {
        show_next_pic(now);
        const image_number = document.querySelectorAll('.slideshow-images-container ul li').length;
        console.log(now);
        if (now >= image_number - 1)
          now = 0;
        else
          ++now;
      }, waiting_time);
    });
  }
  const image_number = document.querySelectorAll('.slideshow-images-container ul li').length;
  for (let i = 0; i < image_number; ++i) {
    let dot = document.querySelectorAll('.slideshow-images-container>ol li')[i];
    dot.addEventListener('click', () => {
      choose_i_pic(i);
      now = i;
    });
  }
}
function choose_i_pic(i: number) {
  const image_number = document.querySelectorAll('.slideshow-images-container ul li').length;
  let images = document.querySelectorAll('.slideshow-images-container>ul li');
  let dots = document.querySelectorAll('.slideshow-images-container>ol li');
  for (let j = 0; j < image_number; ++j) {
    (images[j] as HTMLElement).style.opacity = '0';
    (dots[j] as HTMLElement).style.backgroundColor = "#000000";
  }
  (images[i] as HTMLElement).style.opacity = '1';
  (dots[i] as HTMLElement).style.backgroundColor = "#ffffff";
}
function show_next_pic(i: number) {
  const image_number = document.querySelectorAll('.slideshow-images-container ul li').length;
  let images = document.querySelectorAll('.slideshow-images-container>ul li');
  let dots = document.querySelectorAll('.slideshow-images-container>ol li');
  (images[i] as HTMLElement).style.opacity = '0';
  (dots[i] as HTMLElement).style.backgroundColor = "#000000";
  if (i >= image_number - 1)
    i = 0;
  else
    ++i;
  (images[i] as HTMLElement).style.opacity = '1';
  (dots[i] as HTMLElement).style.backgroundColor = "#ffffff";
}
const postimages = ref([
  "src/assets/img1.jpg",
  "src/assets/img2.jpg",
  "src/assets/img3.jpg",
  "src/assets/img4.jpg",
  "src/assets/img5.jpg",
]);
const topParticipationList = ref([])

const sections = ref([
  {
    title: '森林百科',
    description: '探索森林知识的海洋，了解生态系统和物种保护的重要性。',
    image: 'src/assets/img1.jpg',
    link: '/encyclopedia',
  },
  {
    title: '林业活动',
    description: '参与森林保护活动，与自然和谐共处，共建绿色家园。',
    image: 'src/assets/img2.jpg',
    link: '/activities',
  },
  {
    title: '林上论坛',
    description: '加入讨论，与全球森林爱好者一起分享你的灵感和想法。',
    image: 'src/assets/img3.jpg',
    link: '/ForumView',
  },
  {
    title: '小林问答',
    description: '使用AI助手小林，解答您关于森林的一切问题。',
    image: 'src/assets/img4.jpg',
    link: '/AIfloating',
  },
]);

</script>

<template>
  <Nav />
  <main>
    <!--轮播图片-->
    <div class="slideshow-images-container">
      <ul>
        <li><img src="../assets/login.png" alt="" /></li>
        <li><img src="../assets/default-avatar.png" alt="" /></li>
        <li><img src="../assets/icon-pencil.png" alt="" /></li>
        <li><img src="../assets/icon-ready.png" alt="" /></li>
        <li><img src="../assets/icon-right.png" alt="" /></li>
      </ul>
      <ol>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
      </ol>
    </div>
   <div class="beginbutton"@click.prevent="scrollToContent">
<el-icon-arrow-down style="width: 120px;height: 120px;font-weight: bolder;"></el-icon-arrow-down>
</div>
    <article id="content-start-point">
      <!--介绍部分-->
      <section>
        <div>
          <div class="image-container">
          </div>
          <div class="text-container">
            <h2>Why Are Forests So Important?</h2>
            <h2>森林资源为什么如此重要？</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin gravida
              dolor sit amet lacus accumsan et viverra justo commodo. Proin sodales pulvinar sic tempor. Sociis natoque
              penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam fermentum, nulla luctus pharetra
              vulputate, felis tellus mollis orci, sed rhoncus pronin sapien nunc accuan eget.</p>
          </div>
        </div>
      </section>
      <section>
        <div>
          <div class="text-container">
            <h2>Why Are Forests So Important?</h2>
            <h2>森林资源为什么如此重要？</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin gravida
              dolor sit amet lacus accumsan et viverra justo commodo. Proin sodales pulvinar sic tempor. Sociis natoque
              penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam fermentum, nulla luctus pharetra
              vulputate, felis tellus mollis orci, sed rhoncus pronin sapien nunc accuan eget.</p>
          </div>
          <div class="image-container">
          </div>
        </div>
      </section>
      <!--能做什么部分-->
      <section>
        <h2 class="can-do-heading">
          在林上鹰眼，你可以...
        </h2>
        <div class="carousel-section">
  <el-carousel :interval="5000" arrow="always" type="card" :autoplay="true">
      <el-carousel-item v-for="(item, index) in sections" :key="index">
        <div class="carousel-item">
          <img :src="item.image" alt="板块图片" class="carousel-image" />
          <div class="carousel-text">
            <h2 class="section-title">{{ item.title }}</h2>
            <p class="section-description">{{ item.description }}</p>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</section>
      <!--林上资讯-->
<section>
  <div class="function-intro-topic">
    <p>Forest News·林上资讯</p>
    <h2>从林上鹰眼获得新闻</h2>
  </div>
  <div class="function-example-container">
    <div class="function-example-news">
      <a href="https://www.sciencedaily.com/news/earth_climate/forests/" target="_blank">气候变化导致北卡罗来纳州沿海湿地从森林转变为沼泽地 >></a><br />
      <a href="https://www.sciencedaily.com/news/earth_climate/forests/" target="_blank">澳大利亚土著的古老文化焚烧实践限制了燃料供应 >></a><br />
      <a href="https://globalforestcoalition.org/featured-news/" target="_blank">全球森林联盟在生物多样性公约第16次缔约方大会上呼吁采取实际行动 >></a><br />
      <a href="https://forestsnews.cifor.org/" target="_blank">2024年环境叙事：树木、气候和社区 >></a><br />
      <a href="https://www.wri.org/insights/global-trends-forest-fires" target="_blank">最新数据证实：森林火灾愈发严重 >></a><br />
      <a href="https://www.sciencedaily.com/news/earth_climate/forests/" target="_blank">全球热带地区有2.15亿公顷土地具有自然再生森林的潜力 >></a><br />
      <a href="https://globalforestcoalition.org/featured-news/" target="_blank">第29次缔约方大会上敦促立即停止为碳交易和抵消等虚假解决方案融资 >></a><br />
      <a href="https://forestsnews.cifor.org/" target="_blank">2024年森林的五个积极迹象 >></a><br />
      <a href="https://www.globalforestwatch.org/blog/insights/global-tree-cover-loss-data-2021/" target="_blank">2021年巴西亚马逊地区出现新的大规模森林砍伐前沿 >></a><br />
      <a href="https://www.wri.org/insights/global-trends-forest-fires" target="_blank">农业扩张和森林退化加剧了热带森林的火灾 >></a>
    </div>
    <div class="function-example-image">
      <img src="../assets/homenew.png" alt="新闻相关图片" />
    </div>
  </div>
</section>
  <!--林业活动-->

  <section>
  <div class="function-intro-topic">
    <p>Forest Events·林业活动</p>
    <h2>享受林上鹰眼的活动</h2>
    </div>
   <div class="forest-events-section">
    <div class="forest-events-container">
      <!-- 左侧轮播图 -->
      <div class="carousel-container">
        <el-carousel :interval="3000" arrow="always" height="300px">
          <el-carousel-item v-for="i in 5" :key="i">
            <img :src="`src/assets/img${i}.jpg`" alt="轮播图图片" class="carousel-image-activity" />
          </el-carousel-item>
        </el-carousel>
      </div>
      <!-- 右侧活动列表 -->
      <div class="activities-container">
        <h3>报名活动排行榜</h3>
        <div v-for="(item, index) in topParticipationList" :key="item.upa_id" class="activity-item">
          <p class="activity-name">
            {{ index + 1 }}. {{ item.activityName }}
          </p>
          <p class="participation-number">
            参与人数: {{ item.participateNumber }}
          </p>
        </div>
      </div>
    </div>
    </div>
  </section>
    </article>
  </main>

  <!--底部版权信息-->
  <footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</footer>
</template>


<style scoped>
html,
body {
  scroll-behavior: smooth;
}

main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/*轮播图片*/
main>div:nth-of-type(1) {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  background-color: #f5f5f5;
  margin-top: 7vh;
}

main>div:nth-of-type(1) ul {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 100%;
  height: 100%;
  list-style: none;
}

main>div:nth-of-type(1) ul>li img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

main>div:nth-of-type(1) ul>li {
  width: 100%;
  height: 100%;
  position: absolute;
  transition: 1s;
  opacity: 0;
}

main>div:nth-of-type(1) ol {
  display: grid;
  grid-template-columns: repeat(5, 75px);
  grid-template-rows: auto;
  grid-gap: 1px;
  gap: 1px;
  list-style: none;
  position: absolute;
  right: 0;
  bottom: 12vh;
}

main>div:nth-of-type(1) ol>li {
  width: 10px;
  height: 10px;
  font-size: 15px;
  line-height: 20px;
  float: left;
  text-align: center;
  border-radius: 2em;
  border: 4px solid #999999;
}

/*开始按钮*/
.beginbutton{
margin-top:0px;
font-size:28px;
color: #7da85f;
}

main>a:nth-of-type(1):hover {
  background-color: #000000;
  color: #ffffff;
}

main>a:nth-of-type(1):active {
  background-color: beige;
  color: #ffffff;
}

/*总体设计*/
main>article section {
  margin-top: 80px;
}

main>article h2 {
  font-family: "Georgia Negreta", "Georgia Normal", "Georgia", sans-serif;
  font-weight: 700;
  font-style: normal;
  font-size: 28px;
  color: #000000;
}

/*介绍部分*/
main>article {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 80%;
  margin-top: 5vh;
}

main>article>section>div {
  display: flex;
  gap: 80px;
  justify-content: center;
  align-items: stretch;
}

section>div>div {
  flex: 1;
}

.image-container {
  background-image: url("../assets/default-avatar.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* .text-container h2:nth-of-type(1) {
  font-family: "Georgia Negreta", "Georgia Normal", "Georgia", sans-serif;
} */
.text-container h2:nth-of-type(2) {
  font-family: 华文中宋, sans-serif;
}

.text-container p {
  font-family: "Georgia Normal", "Georgia", sans-serif;
  font-weight: 400;
  font-style: normal;
  font-size: 20px;
  color: #555555;
  line-height: 25px;
}

/*功能总览部分*/
/* 轮播部分的样式 */
.carousel-section {
  width: 700px;
  margin: 0 auto;
  padding-top: 0px;
}

.carousel-item {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  text-align: center;
  height: 300px;
  background-color: #66a833; /* 绿色背景 */
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.carousel-image {
  width: 100%;
  height: 70%;
  object-fit: cover;
}

.carousel-text {
  padding: 10px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 5px;
  width: 90%;
  margin-top: 10px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #105e21; /* 深绿色 */
}

.section-description {
  font-size: 14px;
  color: #333;
}
/*林上资讯*/
.function-intro-topic>p:nth-child(1):before {
  content: "";
  display: inline-block;
  width: 25px;
  height: 1.3em;
  background-image: url("../assets/leaf1.svg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.function-intro-topic>p:nth-child(1) {
  color: rgba(119, 190, 5, 0.99);
}

.function-intro-topic {
  width: 70vw;
  display: block;
  margin-bottom: 20px;
}

.function-example-container {
  display: flex;
  justify-content: space-between;
  gap: 20px; /* 左右框的间距 */
  align-items: flex-start;
  border-width: 1px;
  border-style: solid;
  border-color: #ababab;
  border-radius: 10px; /* 圆角边框 */
  padding: 15px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.function-example-news {
  flex: 2;
}

.function-example-news a {
  font-size: 20px;
  line-height: 1.8; /* 增加行距 */
  color: #0056b3; /* 链接为蓝色 */
  text-decoration: none; /* 去掉下划线 */
}

.function-example-news a:hover {
  text-decoration: underline; /* 鼠标悬停时显示下划线 */
  color: #003d99; /* 鼠标悬停时字体颜色加深 */
}

.function-example-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.function-example-image img {
  max-width: 100%;
  height:380px;
  border-radius: 10px; /* 图片圆角 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 添加图片阴影 */
}
/* 林业活动部分样式 */
.forest-events-section {
  margin: -28px;
  width: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.forest-events-header p {
  font-size: 18px;
  color: #77be05;
  font-weight: bold;
  margin: 0;
}

.forest-events-header h2 {
  font-size: 24px;
  color: #333;
  margin-top: 5px;
}

/* 主体容器 */
.forest-events-container {
  display: flex;
  gap: 20px;
  margin-top: 30px;
  justify-content: space-between;
  width: 100%;
}

/* 轮播图容器 */
.carousel-container {
  flex: 1.5;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: 300px; /* 确保容器有固定高度 */
}

.carousel-image-activity {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保证图片填满父容器 */
  border-radius: 10px;
}

/* 活动列表容器 */
.activities-container {
  flex: 1.5;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
  text-align: left;
  height: 300px; /* 确保与轮播图容器高度一致 */
  overflow-y: auto; /* 如果内容过多，则添加滚动条 */
}

.activities-container h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.activity-item {
  margin-bottom: 15px;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.activity-name {
  font-size: 14px;
  color: #0056b3;
  font-weight: bold;
}

.participation-number {
  font-size: 14px;
  color: #555;
}

/*林上论坛*/
.carousel-image-post {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

/*底部版权信息*/
footer {
  background-color: transparent;
  color: #ababab;
  text-align: center;
  padding: 10px 0;
  bottom: 0;
  width: 100%;
  font-size: xx-small;
  margin-top: 50px;
}
</style>
