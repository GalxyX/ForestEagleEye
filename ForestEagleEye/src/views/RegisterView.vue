<template>
  <!doctype html>
  <html lang="zh-CN">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>注册 - 林上鹰眼</title>
      <link rel="icon" href="/favicon.ico" />
      <link rel="stylesheet" href="styles/style.css" />
    </head>
    <body>
      <main>
        <div>
          <div class="image-box"></div>
          <div class="signup-box">
            <section>
              <div class="title-wrapper">
                <h1 style="text-align: center; font-weight: bold">创建你的账号</h1>
                <p style="text-align: center; color: grey; font-weight: 100">
                  注册成为林上鹰眼的一员
                </p>
              </div>
              <form @submit.prevent="register">
                <div class="input-wrapper">
                  <label for="username">用户名</label>
                  <input
                    type="text"
                    v-model="username"
                    id="username"
                    placeholder="请输入用户名"
                    required
                  />
                </div>
                <div class="input-wrapper">
                  <label for="email">邮箱</label>
                  <input
                    type="email"
                    v-model="email"
                    id="email"
                    placeholder="请输入账号的电子邮箱"
                    required
                  />
                </div>
                <div class="input-wrapper">
                  <label for="password">密码</label>
                  <input
                    type="password"
                    v-model="password"
                    id="password"
                    placeholder="请输入账号的密码"
                    required
                  />
                </div>
                <div class="input-wrapper">
                  <label for="verification">验证码</label>
                  <div>
                    <input type="text" v-model="code" id="verification"/>
                    <button type="button" class="sendcode" @click="send_verification_code">发送验证码</button>
                  </div>
                </div>
                <button class="submit">注册</button>
              </form>

              <p>已有账号？ <a href="/login">登录</a></p>
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
    };
  },
  methods: {
    async send_verification_code() {
      try {
        const params = new URLSearchParams();
        params.append('email', this.email);

        const response = await axios.post('http://127.0.0.1:5000/send_verification_code', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        // 处理响应
        alert(response.data.message);
      } catch (error) {
        // 处理错误
        console.error('Error sending verification code:', error);
        alert(response.data.message);
      }
    },
    async register() {
      try {
        const params = new URLSearchParams();
        params.append('username', this.username);
        params.append('email', this.email);
        params.append('password', this.password);
        params.append('code', this.code);

        const response = await axios.post('http://127.0.0.1:5000/register', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });

        // 处理响应
        alert(response.data.message);
        if (response.data.status === 'success') {
          //注册成功直接跳转到Login
          this.$router.push('/login');
        } 
      } catch (error) {
        window.location.reload(); // 刷新当前页面
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
  background-image: url(../assets/register.png);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: -50px;
}

.signup-box {
  width: 40%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

section {
  width: 85%;
  max-width: 500px;
  margin-top: 10px;
  margin-right:50px;
}

.title-wrapper {
  padding: 10px;
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
  margin-bottom: 10px;
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

.sendcode {
  width: 100%;
  padding: 10px;
  border: 1.5px solid #60a130;
  border-radius: 10px;
  background-color: white;
  color: #60a130;
  cursor: pointer;
  align-content: center;
  font-weight: bold;
}

.sendcode:hover {
  background-color: #60a130;
  color: white;
}

.submit {
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

.submit:hover {
  background-color: black;
  color: white;
}

form .input-wrapper div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
}
#verification {
  flex: 2 40px;
  margin-right: 10px;
  box-sizing: border-box;
  width: auto;
}
.input-wrapper div button {
  flex: 1 40px;
  width: auto;
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
