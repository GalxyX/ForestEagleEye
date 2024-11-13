<script setup lang="ts">
import { onMounted } from 'vue'
import Nav from '../components/navbar.vue'

onMounted(() => {
  choose_i_pic(0);
  slideShow();
})
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
    <a href="#content-start-point">开始</a>
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
        <el-carousel :interval="60000" arrow="always" style="width: 70vw;height: 500px;">
          <el-carousel-item style="height:500px;">
            <div class="after-el-carousel-item">
              <div class="can-do-cards-container">
                <div class="can-do-card">
                  <img src="../assets/default-avatar.png" alt="" />
                  <router-link to="/encyclopedia">
                    <h3>森林百科</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin
                    </p>
                  </router-link>
                </div>
                <div class="can-do-card">
                  <img src="../assets/default-avatar.png" alt="" />
                  <router-link to="/activities">
                    <h3>林业活动</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin
                    </p>
                  </router-link>
                </div>
                <div class="can-do-card">
                  <img src="../assets/default-avatar.png" alt="" />
                  <router-link to="/reflect">
                    <h3>举报建议</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin
                    </p>
                  </router-link>
                </div>
              </div>
            </div>
          </el-carousel-item>
          <el-carousel-item style="height:500px;">
            <div class="after-el-carousel-item">
              <div class="can-do-cards-container">
                <div class="can-do-card">
                  <img src="../assets/default-avatar.png" alt="" />
                  <router-link to="/forum">
                    <h3>林上论坛</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin
                    </p>
                  </router-link>
                </div>
                <div class="can-do-card">
                  <img src="../assets/default-avatar.png" alt="" />
                  <h3>小林问答</h3>
                  <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin</p>
                </div>
                <div class="can-do-card">
                  <img src="../assets/default-avatar.png" alt="" />
                  <router-link to="/game">
                    <h3>林上游戏</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin
                    </p>
                  </router-link>
                </div>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>
      </section>
      <!--林上资讯-->
      <section>
        <div class="function-intro-topic">
          <p> Forest News·林上资讯</p>
          <h2>从林上鹰眼获得新闻</h2>
        </div>
        <div>
          <div class="function-example-left">
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
          </div>
          <div class="function-example-right">
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
          </div>
        </div>
      </section>
      <!--林业活动-->
      <section>
        <div class="function-intro-topic">
          <p> Forest Events·林业活动</p>
          <h2>享受林上鹰眼的活动</h2>
        </div>
        <div>
          <div class="function-example-left">
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
          </div>
          <div class="function-example-right">
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
            <p>i dont know</p>
          </div>
        </div>
      </section>
      <!--林上论坛-->
      <section>
        <div class="function-intro-topic">
          <p> Forest Forumn·林上论坛</p>
          <h2>在林上鹰眼碰撞灵感</h2>
        </div>
        <el-carousel :interval="500000" arrow="always" style="width: 70vw;height: 500px;">
          <!------------------------------------------------等待论坛完成后修改------------------------------------------------>
          <!------------------------------------------------等待论坛完成后修改------------------------------------------------>
          <!------------------------------------------------等待论坛完成后修改------------------------------------------------>
          <el-carousel-item style="height:500px;">
            <div class="after-el-carousel-item">
              <div class="forum-cards-container">
                <div class="forum-card">
                  <div>
                    <img src="../assets/default-avatar.png" alt="" />
                  </div>
                  <div>
                    <h3>帖子标题</h3>
                    <!---tag-->
                    <!---头像，名称-->
                    <p>正文</p>
                  </div>
                </div>
                <div class="forum-card">
                  <div>
                    <img src="../assets/default-avatar.png" alt="" />
                  </div>
                  <div>
                    <h3>帖子标题</h3>
                    <!---tag-->
                    <!---头像，名称-->
                    <p>正文</p>
                  </div>
                </div>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>
      </section>
    </article>
    <a href="#">想了解更多？</a>
  </main>
  <!--底部版权信息-->
  <footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</footer>
</template>

<style>
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
  height: 60vh;
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
  bottom: 34vh;
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
main>a:nth-of-type(1) {
  border-radius: 30px;
  border-style: solid;
  border-width: 2px;
  background-color: azure;
  color: #000000;
  width: 150px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-decoration: none;
  margin-top: 50px;
  margin-bottom: -50px;
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
.after-el-carousel-item {
  display: flex;
  justify-content: center;
  align-content: center;
  height: 100%;
}

/* .el-carousel__item h3 {
  
}
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
} */
.can-do-cards-container {
  /* flex-wrap: nowrap; */
  gap: 2%;
  width: 93%;
  height: 100%;
  display: flex;
  justify-content: center;
  /* overflow: hidden; */
  /* height: 80px; */
}

.can-do-heading {
  text-align: center;
}

.can-do-card {
  width: 29%;
  background-color: green;
}

.can-do-card p,
.can-do-card h3 {
  padding-left: 6px;
  padding-right: 6px;
}

.after-el-carousel-item img {
  width: 100%;
}

/*林上资讯与林业活动*/
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
  color: rgba(119, 190, 5, 0.9921568627450981);
}

.function-intro-topic {
  width: 70vw;
  display: block;
}

.function-example-left {
  flex: 3;
  border-width: 1px;
  border-style: solid;
  border-color: #ababab;
}

.function-example-right {
  flex: 2;
  border-width: 1px;
  border-style: solid;
  border-color: #ababab;
}

/*林上论坛*/
.forum-cards-container {
  gap: 20px;
  width: 80%;
  height: 100%;
  display: flex;
  justify-content: center;
}

.forum-card {
  border-radius: 30px;
  overflow: hidden;
  display: flex;
  gap: 20px;
}

.forum-card>div {
  flex: 1;
}

main>a:nth-last-of-type(1) {
  margin-top: 50px;
}

main>a:hover {
  color: azure;
}

main>a:active {
  color: aquamarine;
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
