<template>
    <div class="login-container" >
      <div class="login-box" style="overflow: hidden;">
        <div class="image-container">
          <img src="@/assets/login.png" alt="" />
        </div>
        <div class="form-container">
          <h2 style="text-align: center; font-weight: bold;">Welcome back!</h2>
          <h5 style="text-align: center; color: grey; font-weight: 100;">登录开启你的林上之旅</h5>
          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="email">Email</label>
              <input type="email" id="email" v-model="email" placeholder="请输入账号的电子邮箱" required />
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input type="password" id="password" v-model="password" placeholder="请输入账号的密码" required />
            </div>
            <button type="submit">Sign in</button>
            <p>还没有账号？ <a href="/register">Create an Account</a></p>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    setup() {
      const email = ref('');
      const password = ref('');
  
      const handleLogin = () => {
        // 登录逻辑
        console.log('Logging in with:', email.value, password.value);
      };
  
  
      return {
        email,
        password,
        handleLogin,
      };
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #ddd;
  }
  
  .login-box {
    display: flex;
    background: white;
    border-radius: 30px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 1000px;
    align-items: center;
    margin-left: 10px;
    margin-right: 10px;
  }
  
  .image-container img {
    display: block;
    max-height: 70vh;
  }
  
  .form-container {
    flex: 1;
    padding: 10px;
  }
  
  .form-group {
    margin-bottom: 20px;
    margin-left: 10px;
    margin-right: 10px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-size: smaller;
  }
  
  .form-group input {
    width: 90%;
    padding: 10px;
    border: 1.5px solid #ddd;
    border-radius: 10px;
  }
  .form-group input:hover {
    border: 1.5px solid #60A130;
  }
  .form-group input:focus {
    border: 1.5px solid #60A130;
    background-color: #f6fdf3;
    outline: none;
  }
  
  button {
    width: 90%;
    padding: 10px;
    border:  1.5px solid black;
    border-radius: 10px;
    background-color: white;
    color: black;
    cursor: pointer;
    align-content: center;
    margin-left: 10px;
    margin-right: 10px;
    font-weight: bold;
  }
  
  button:hover {
    background-color: black;
    color: white;
  }
  
  p {
    margin-left: 10px;
    margin-right: 10px;
    font-size: smaller;
    text-align: center;
    color: gray;
  }
  
  a {
    color: #60A130;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>