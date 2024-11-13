<template>
    <nav class="navbar">
      <div class="navbar-container">
        <!--logo-->
        <router-link to="/" class="nav-link">
          <img class="homelogo" src="../assets/logo.png">
        </router-link>
        <!-- 中间页面导航 -->
        <ul class="nav-list">
          <div class="nav-item">
            <router-link to="/encyclopedia" class="nav-link">森林百科</router-link>
          </div>
          <div class="nav-item">
            <router-link to="/activities" class="nav-link">林业活动</router-link>
          </div>
          <div class="nav-item" router-link to="/reflect">
            <router-link to="/reflect" class="nav-link">举报建议</router-link>
          </div>
          <div class="nav-item">
            <router-link to="/forum" class="nav-link">林上论坛</router-link>
          </div>
          <div class="nav-item">
            <router-link to="/game" class="nav-link">林上游戏</router-link>
          </div>
        </ul>

        <!-- 右侧个人中心与消息中心 -->
        <div class="user-info">
            <img class="icon-message" src="../assets/icon-message-normal.png">
            <img class="icon-message" src="../assets/icon-profile-normal.png" @click="profile">
            <div class="vertical-divider"></div>
            <img class="user-avatar" src="../assets/default-avatar.png">
            <span class="user-nickname">{{username}}</span>
            <button class="btn-logout" @click="logout" v-if="username">退出登录</button>
            <button class="btn-logout" @click="login" v-else="">登录/注册</button>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
  name: 'NavigationBar',
  data() {
    return {
      username: sessionStorage.getItem('username'),
      avatar:sessionStorage.getItem('avatar')
    };
  },
  methods:{
    login(){
      this.$router.push('/login');
    },
    async logout() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/logout',{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        if(response.data.status==='success'){
          localStorage.clear();//清除缓存
          sessionStorage.clear();//清除会话
          this.$router.push('/login');
        }

      } catch (error) {
        console.error('Error logging out');
      }
    },
    async profile(){
      try{
        this.$router.push('/profile');
      }catch (error) {
        console.error('Error navigating to profile');
      }
    }
  }
};
  </script>
  
  <style scoped>
  .navbar {
    position:fixed;/* navbar吸顶 */
    top:0;
    color: black;
    justify-content: center;
    padding:10px 0;
    width: 100%;
    box-shadow: 0 5px 15px rgba(225, 225, 225, 0.4);
    background-color: white; 
    transition: background-color 0.3s ease;
    z-index:99;
  }

  .navbar-container {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
  
  .nav-list {
    list-style: none;
    display: flex;
    height:1vh;
    padding: 0;
    gap:50px;
    font-size: small;
    align-self: center;
  }
  
  .nav-item {
   align-items: center;
   align-self: center;
  }
  
  .nav-link {
    color: black;
    text-decoration: none;
    transition: color 0.3s ease;
  }
  
.nav-item:hover .nav-link{
  color: #60a103; /* 鼠标悬停时链接的颜色 */
  background-color: rgba(149, 242, 4, 0.1); 
}

.homelogo{
    height: 4vh;
    margin-left: 2vw;
    align-self: center;
}

.icon-message,.a{
    height: 2.5vh;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  color: black;
}

.user-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
}

.user-nickname {
  font-size: small;
  font-weight: bold;
}

.vertical-divider {
  width: 1px; 
  background-color: #cdcdcd; 
  height: 4vh;
  align-self: center;
}

.btn-logout{
    background: transparent;
    border:1px solid black;
    border-radius:30px;
    color: black;
    font-size: x-small;
    height:3.5vh;
    width:4vw;
    margin-right:30px;
}
.btn-logout:hover{
    border:1px solid #63a103;
    color: #63a103;
}
  </style>