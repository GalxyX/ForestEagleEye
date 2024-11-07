<template>
    <div class="container">
      <div class="page-header">
        <div class="header-left">
          <button class="btn-back" @click="goBack">
            <i class="icon-back"></i>
            返回
          </button>
          <span class="separator"></span>
          <div class="header-title">
            <span>活动报名</span>
          </div>
        </div>
      </div>
      <!-- 活动基本信息 -->
      <div class="event-info">
        <div class="info-left">
          <div class="little-title">活动名称</div>
          <div class="big-title">这里是活动名称（需要连后端）</div>
          <div class="little-title">活动简介</div>
          <div class="text">&nbsp;&nbsp;这里是活动介绍（需要连后端）这里是活动介绍（需要连后端）这里是活动介绍（需要连后端）这里是活动介绍（需要连后端）这里是活动介绍（需要连后端）这里是活动介绍（需要连后端）这里是活动介绍（需要连后端）这里是活动介绍（需要连后端）</div>
          <div class="little-title">活动信息</div>
          <div class="info-detail">
            <div class="group1">
              <div class="group2">
              <div class="combination">
              <div class="cover-text">
                <div class="info-little-title">活动地点：</div>
                <div class="info-text">（连后端）</div>
              </div>
            </div>
  
            <div class="combination">
              <div class="cover-text">
                <div class="info-little-title">活动名额：</div>
                <div class="info-text">（连后端）</div>
              </div>
            </div>
  
              </div>
              <div class="group2">
              <div class="combination">
              <div class="cover-text">
                <div class="info-little-title">活动类型：</div>
                <div class="info-text">（连后端）</div>
              </div>
            </div>
  
            <div class="combination">
              <div class="cover-text">
                <div class="info-little-title">剩余名额：</div>
                <div class="info-text">（连后端）</div>
              </div>
            </div>
  
              </div>
            </div>
          </div>
  
          <div class="little-title">报名信息</div>
          <div class="group3">
            <div style="color: #60a103;">报名人数</div>
            <div style="color: red;padding-right: 20px">*</div>
            <input type="text" class="input-field" v-model="inputValue" :placeholder="'请输入内容'"/>
          </div>
  
          <div class="group3">
            <div style="color: #60a103;">身份证号</div>
            <div style="color: red;padding-right: 20px">*</div>
            <input type="text" class="input-field" v-model="inputValue" :placeholder="'请输入内容'"/>
          </div>
  
          <div class="group3">
            <div style="color: #60a103;">报名备注</div>
            <div style="color: red;padding-right: 20px">*</div>
            <input type="text" class="input-field" v-model="inputValue" :placeholder="'请输入内容'"/>
          </div>
  
        </div>
        <div class="info-right">
          <img class="event-img" src="../assets/default-avatar.png">
        </div>
      </div>
  
      <!-- 报名按钮 -->
      <div class="button-group">
        <button class="btn-signup" @click="signUp">报名</button>
        <button class="btn-cancel" @click="cancel">取消</button>
      </div>
  </div>
  
  <footer>
        <p>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</p>
      </footer>
  </template>
  
  <script>
  // import axios from 'axios';
  
  // export default {
  //   name: 'EventDetails',
  //   data() {
  //     return {
  //       activity: {
  //         name: '', // 活动名称
  //         introduction: '', // 活动简介
  //         type: '', // 活动类型
  //         location: '', // 活动地点
  //         beginTime: '', // 活动开始时间
  //         endTime: '', // 活动结束时间
  //         participantNumber: 0, // 活动人数
  //         enrolledNumber: 0, // 已报名人数
  //         state: '', // 活动状态
  //         picPath: '', // 活动图片路径
  //       },
  //       activityStatus: '', // 活动状态，用于条件渲染
  //     };
  //   },
  //   mounted() {
  //     this.loadActivityFromSession(); // 尝试从 sessionStorage 加载活动详情
  
  //     // 如果 sessionStorage 中没有活动详情，则从后端获取
  //     if (!this.activity.name) {
  //       this.fetchActivityDetails();
  //     }
  //   },
  //   methods: {
  //     async fetchActivityDetails() {
  //       try {
  //         const response = await axios.get('http://127.0.0.1:5000/', {
  //           params: {
  //             a_id: this.$route.params.a_id, // 假设活动编号通过路由参数传递
  //           },
  //         });
  //         const activityData = response.data;
  //         this.activity = activityData;
  //         this.activityStatus = this.getActivityStatus(activityData.state);
  //         this.saveActivityToSession(); // 存储活动详情到 sessionStorage
  //       } catch (error) {
  //         console.error('Error fetching activity details:', error);
  //         // 这里可以添加错误处理逻辑，例如显示错误消息
  //       }
  //     },
  //     getActivityStatus(state) {
  //       switch (state) {
  //         case 'approving':
  //           return 'pending';
  //         case 'approved':
  //           return 'ongoing';
  //         case 'ongoing':
  //           return 'ongoing';
  //         case 'ended':
  //           return 'finished';
  //         default:
  //           return 'unknown';
  //       }
  //     },
  //     saveActivityToSession() {
  //       sessionStorage.setItem('activityName', this.activity.name);
  //       sessionStorage.setItem('activityIntroduction', this.activity.introduction);
  //       sessionStorage.setItem('activityType', this.activity.type);
  //       sessionStorage.setItem('activityLocation', this.activity.location);
  //       sessionStorage.setItem('activityBeginTime', this.activity.beginTime);
  //       sessionStorage.setItem('activityEndTime', this.activity.endTime);
  //       sessionStorage.setItem('activityParticipantNumber', this.activity.participantNumber.toString());
  //       sessionStorage.setItem('activityEnrolledNumber', this.activity.enrolledNumber.toString());
  //       sessionStorage.setItem('activityState', this.activity.state);
  //       sessionStorage.setItem('activityPicPath', this.activity.picPath);
  //       sessionStorage.setItem('activityStatus', this.activityStatus);
  //     },
  //     loadActivityFromSession() {
  //       this.activity.name = sessionStorage.getItem('activityName') || '';
  //       this.activity.introduction = sessionStorage.getItem('activityIntroduction') || '';
  //       this.activity.type = sessionStorage.getItem('activityType') || '';
  //       this.activity.location = sessionStorage.getItem('activityLocation') || '';
  //       this.activity.beginTime = sessionStorage.getItem('activityBeginTime') || '';
  //       this.activity.endTime = sessionStorage.getItem('activityEndTime') || '';
  //       this.activity.participantNumber = parseInt(sessionStorage.getItem('activityParticipantNumber') || '0', 10);
  //       this.activity.enrolledNumber = parseInt(sessionStorage.getItem('activityEnrolledNumber') || '0', 10);
  //       this.activity.state = sessionStorage.getItem('activityState') || '';
  //       this.activity.picPath = sessionStorage.getItem('activityPicPath') || '';
  //       this.activityStatus = sessionStorage.getItem('activityStatus') || '';
  //     },
  //   },
  // };
  </script>
  
  <style scoped>
  .container {
    background-color: white;
    width: 1200px;
    margin-bottom: 20px;
    padding: 10px 25px 25px 25px;
  }
  
  .page-header {
    display: flex;
    align-items: center;
    padding: 1rem;
    position: relative; /* For the horizontal line at the bottom */
  }
  
  .header-left {
    display: flex;
    align-items: center;
  }
  
  .btn-back {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    padding: 0.3rem;
    color: #333;
  }
  
  .icon-back::before {
    content: '\2190'; 
    margin-right: 0.5rem;
  }
  
  .separator {
    margin: 0 1rem;
    width: 1px;
    height: 1.5rem;
    background-color: #ccc; 
  }
  
  .header-title {
    font-size: 1.25rem;
    font-weight: bold;
    color: #333;
    margin-left: 10px; 
  }
  
  
  .page-header::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 1px;
    background-color: #ccc;
  }
  
  .event-info{
    display: flex;
    flex-direction: row;
    width:auto;
    padding: 20px 30px 0px 30px;
  }
  .info-left{
    display: flex;
    flex-direction: column;
    width:50%;
    padding: 0px 20px 0px 0px;
  }
  .info-right{
    width:50%;
    padding: 10px 20px 10px 20px;
  }
  .event-img {
    width: 100%; /* 设置图片宽度填满容器 */
    height: 100%; /* 设置图片高度填满容器 */
    object-fit: cover; /* 让图片完全覆盖容器，同时保持图片的宽高比 */
  }
  .little-title{
    color:#bdc2bf;
    padding: 20px 0px 20px 0px;
    font-size: 20px;
    font-family: "Microsoft YaHei";
  }
  .big-title{
    color:#333;
    padding: 10px 0px 10px 10px;
    font-size: 32px;
    font-family: "SimSun";
    font-weight: bold;
  }
  .text{
    color:#333;
    padding: 10px 25px 10px 10px;
    font-size: 20px;
    font-family: "SimSun";
    font-weight: bold;
    line-height: 1.5; /* 行距设置为字体大小的1.5倍 */
  }
  .combination{
    padding: 0px 15px 20px 0px;
  }
  .cover-text{
    display: flex;
    flex-direction: row;
    color:#333;
    padding: 7px 0px 7px 0px;
    border-radius: 20px;
    width:100%;
    background-color: #e0f2e0;
    font-size: 16px;
    font-weight: bold;
    font-family: "SimSun";
    line-height: 1.5; 
  }
  .info-little-title{
    padding: 2px 2px 2px 18px;
  }
  .info-text{
    padding: 2px 2px 2px 2px;
  }
  .group2{
    width:50%;
  }
  .group1{
    display:flex;
    flex-direction: row;
  }
  
  .event-process{
    display: flex;
    flex-direction: column;
  }
  .timeline {
      padding: 30px 0px 0px 0px;
      /* position: relative; */
      width: 1200px; /* 根据需要调整宽度 */
      /* margin: 20px auto; 居中容器，增加上下边距 */
      background-color: #f9fefb; /* 容器背景颜色 */
      display: flex; /* 使用 flex 布局 */
      justify-content: center; /* 水平居中 */
      align-items: center; /* 垂直居中 */
    }
  
    .vertical-line {
      position: absolute;
      left: 50%; /* 居中 */
      top: 0; /* 从顶部开始 */
      bottom: 0; /* 到达底部 */
      width: 2px; /* 直线的宽度 */
      background-color: #c8c7c7; /* 直线的颜色 */
      transform: translateX(-50%); /* 使直线完全居中 */
      height: 1000px; /* 确保直线充满整个容器高度 */
    }
  
  .group3{
    display: flex;
    flex-direction: row;
    align-items: center; /* 垂直居中 */
    padding: 10px 0px 10px 0px;
  }
  
  
  .input-field {
    background-color: #f3fcf3; /* 浅灰色背景 */
    border: 1px solid #f3fcf3; /* 边框颜色 */
    border-radius: 15px; /* 圆角 */
    padding: 10px; /* 内边距 */
    font-size: 16px; /* 字体大小 */
    width: 300px; /* 宽度 */
    transition: border-color 0.3s; /* 边框颜色变化动画 */
  }
  .input-field:focus {
    outline: none; /* 移除焦点时的轮廓 */
    border-color: #60a103; /* 聚焦时边框颜色变化 */
  }
  
  .button-group{
    gap:20px;
    display: flex;
    padding:10px 0px 5px 0px;
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
  }
  
  .btn-signup {
    background-color: #71b512; /* 绿色背景 */
    color: white; /* 白色字体 */
    border: none; /* 无边框 */
    border-radius: 10px; /* 圆角 */
    padding: 10px 20px; /* 内边距 */
    cursor: pointer; /* 鼠标手形 */
    transition: background-color 0.3s; /* 背景色变化动画 */
  }
  
  .btn-signup:hover {
    background-color: #60a103; /* 鼠标悬停时的背景色 */
  }
  
  .btn-cancel {
    background-color: #b9bcb9; /* 灰色背景 */
    color: white; /* 白色字体 */
    border: none; /* 无边框 */
    border-radius: 10px; /* 圆角 */
    padding: 10px 20px; /* 内边距 */
    cursor: pointer; /* 鼠标手形 */
    transition: background-color 0.3s; /* 背景色变化动画 */
  }
  
  .btn-cancel:hover {
    background-color: #8d908b; /* 鼠标悬停时的背景色 */
  }
  
  footer {
      background-color: transparent;
      color: #ababab;
      text-align: center;
      padding: 0; 
      bottom: 0;
      width: 100%;
      font-size:xx-small;
  }
  </style>