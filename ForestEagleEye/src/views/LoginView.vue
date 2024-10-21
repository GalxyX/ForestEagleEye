<template>
  <!doctype html>
  <html lang="zh-CN">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>登录 - 林上鹰眼</title>
    </head>
    <body>
      <main>
        <div>
          <div class="image-box"></div>
          <div class="login-box">
            <section>
              <div class="title-wrapper">
                <h1>欢迎回来</h1>
                <p>登录开启你的林上之旅</p>
              </div>
              <form @submit.prevent="login" >
                <div class="input-wrapper">
                  <label for="email">邮箱</label>
                  <input
                    type="email"
                    name="email"
                    v-model="email"
                    id="email"
                    placeholder="请输入账号的电子邮箱"
                    required
                    autofocus
                  />
                </div>
                <div class="input-wrapper">
                  <label for="password">密码</label>
                  <input
                    type="password"
                    name="password"
                    v-model="password"
                    id="password"
                    placeholder="请输入账号的密码"
                    required
                  />
                </div>
                <button type="submit">登录</button>
              </form>
              <p>还没有账号？ <a href="/register" title="林上鹰眼-注册">注册</a></p>
            </section>
          </div>
        </div>
      </main>
    </body>
  </html>
</template>

<script>
import axios from 'axios';


export default {
  data() {
    return {
      email: '',
      password: '',
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const params = new URLSearchParams();
        params.append('email', this.email);
        params.append('password', this.password);

        const response = await axios.post('http://127.0.0.1:5000/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });

        // 处理响应
        alert(response.data.message);
        if (response.data.status === 'success') {
          // 会话状态存储当前用户信息
          sessionStorage.setItem('username',response.data.username);
          sessionStorage.setItem('email',response.data.email);
          sessionStorage.setItem('avatar',response.data.avatar);
          sessionStorage.setItem('user_id',response.data.user_id);
          sessionStorage.setItem('role',response.data.role);
          sessionStorage.setItem('newestTime',response.data.newestTime);
          sessionStorage.setItem('signupTime',response.data.signupTime);
          sessionStorage.setItem('days',response.data.days);
          sessionStorage.setItem('signature',response.data.signature);

          if(response.data.role!=='普通用户'){
            sessionStorage.setItem('forest',response.data.forest);
            sessionStorage.setItem('inst',response.data.inst);
          }

          // 暂时转到活动页面
          this.$router.push('/encyclopedia');
        } 
      } catch (error) {
        if(response.data.message=="请求错误")
          window.location.reload(); // 请求错误刷新当前页面
      }
    },
  },
};
</script>


<style scoped>
main {
  display: flex;
  align-items: center;
  height: 100vh;
  justify-content: center;
  background-color: #ddd;
}

main > div {
  background: white;
  border-radius: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 60%;

  display: flex;
  align-items: center;
  overflow: hidden;
}

.image-box {
  display: block;

  height: 70vh;
  width: 60%;
  background-image: url(../assets/login.png);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: -50px;
}

.login-box {
  width: 40%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 50px;
}

section {
  width: 85%;
  max-width: 500px;
  margin-right: 50px;
  margin-top: 10px;
}

.title-wrapper {
  padding: 10px;
  padding-bottom: 20px;
}

.title-wrapper h1 {
  text-align: center;
  font-weight: bold;
}

.title-wrapper p {
  text-align: center;
  color: grey;
  font-weight: 100;
}

.input-wrapper {
  width: 100%;
  margin-bottom: 20px;
}

.input-wrapper label {
  display: block;
  margin-bottom: 5px;
  font-size: smaller;
}

.input-wrapper input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: 1.5px solid #ddd;
  border-radius: 10px;
}

.input-wrapper input:hover {
  border: 1.5px solid #60a130;
}

.input-wrapper input:focus {
  border: 1.5px solid #60a130;
  background-color: #f6fdf3;
  outline: none;
}

button {
  width: 100%;
  padding: 10px;
  border: 1.5px solid black;
  border-radius: 10px;
  background-color: white;
  color: black;
  cursor: pointer;
  align-content: center;
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
  color: #60a130;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

</style>