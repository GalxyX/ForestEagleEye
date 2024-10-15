<template>
    <NavigationBar />
    <div class="main">
      <!-- sidebar -->
      <div class="sidebar">
        个人信息展板
      </div>
      <!-- userinfo -->
      <div class="userinfo">
        <div class="container">
          <h1>Hi,{{username}}</h1>
          <text class="label">{{greeting}}</text>
        </div>
        <div class="container">
          <h2>个人信息</h2>
          
          <div class="user-info">
            <div class="info-row">
              <div class="info-label">昵称</div>
              <div class="info-value">{{username}}</div>
            </div>
            <div class="info-row">
              <div class="info-label">用户ID</div>
              <div class="info-value">{{user_id}}</div>
            </div>
            <div class="info-row">
              <div class="info-label">邮箱</div>
              <div class="info-value">{{email}}</div>
            </div>
            <div class="info-row">
              <div class="info-label">注册时间</div>
              <div class="info-value">{{signupTime}}</div>
            </div>
          </div>

          <div class="user-info">
            <div class="info-row">
              <div class="info-label">角色</div>
              <div class="info-value">{{role}}</div>
            </div>
            <div class="info-row">
              <div class="info-label">最近登录时间</div>
              <div class="info-value">{{newestTime}}</div>
            </div>
          </div>

        </div>
        <div class="container">
          <div class="subtitle"><h2>主页访问数据</h2><h3>(次)</h3></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import NavigationBar from '../components/navbar.vue'

  export default {
    name: 'activities',
    components: {
      NavigationBar
    },
    data() {
    return {
        greeting:'',

        username:'',
        avatar:'',
        user_id:'',
        email:'',
        role:'',
        signupTime:'',
        newestTime:'',
        days:'',
      };
    },
    mounted(){
      this.username=sessionStorage.getItem('username');
      this.avatar=sessionStorage.getItem('avatar');
      this.user_id=sessionStorage.getItem('user_id');
      this.email=sessionStorage.getItem('email');
      this.role=sessionStorage.getItem('role');
      this.signupTime=sessionStorage.getItem('signupTime');
      this.newestTime=sessionStorage.getItem('newestTime');
      this.days=sessionStorage.getItem('days');

      const hour= new Date().getHours;
      if (hour < 6) {
        this.greeting = '凌晨好，';
      } else if (hour < 9) {
        this.greeting = '早上好，';
      } else if (hour < 12) {
        this.greeting = '上午好，';
      } else if (hour === 12) {
        this.greeting = '中午好，';
      } else if (hour < 18) {
        this.greeting = '下午好，';
      } else {
        this.greeting = '晚上好，';
      }
      this.greeting+='今天是你来到林上鹰眼的第'+this.days+'天~';
    }
  }
  </script>
  
  <style scoped>
  .main{
    padding-top: 50px;
    background-color: #F0F2F5;
    display: flex;
    height: 100vh;
  }

  .userinfo{
    margin-top: 20px;
    margin-left:25px;
    justify-content: center;
  }

  .sidebar{
    background-color: #60a103;
    width:20%;
    height: 100vh;
  }
  .container{
    background-color: white;
    width:1200px;
    margin-bottom: 20px;
    padding:10px 25px 25px 25px;
  }
  .subtitle{
    display:flex;
    align-content: space-between;
    align-items: center;
    gap:5px;
  }
  h1{
    font-size: 16pt;
  }
  h2{
    font-size: 12pt;
    font-weight: normal;
  }
  h3{
    font-size:small;
    font-weight:normal;
    color:grey;
  }
  .label{
    color:#456E02;
    font-size: 11pt;
  }

  .user-info {
    padding: 10px;
    margin-top: 10px;
    display: flex;
  }
 
  .info-header {
    font-weight: bold;
    text-align: left;
    margin-bottom: 10px;
  }
  .info-row {
    flex: none;
    justify-content: space-between;
    width:300px;
    margin-bottom: 10px;
    
  }
  .info-label{
    text-align: left;
    font-size: small;
    margin-bottom:10px;
    color:grey;
  }
  .info-value{
    text-align: left;
    font-size: small;
  }
  </style>