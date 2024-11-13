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

                <!--选择角色-->
                <div class="detail-wrapper">
                  <label for="role">角色</label>
                  <div style="display:flex;flex-direction:column;">
                    <div style="display:flex;">
                      <label class="radio"><input type="radio" value="普通用户" v-model="role">普通用户</label>
                      <label class="radio"><input type="radio" value="林业从业人员" v-model="role">林业从业人员</label>
                    </div>
                    <div style="display:flex;">
                      <label class="radio"><input type="radio" value="林业管理人员" v-model="role">林业管理人员</label>
                      <label class="radio"><input type="radio" value="林业监管人员" v-model="role">林业监管人员</label>
                    </div>
                  </div>
                </div>
                <!--选择森林和团队-->
                <div style="display: flex;" v-if="role!=='普通用户'">
                  <div class="detail-wrapper">
                    <label>森林</label>
                    <select id="forest" v-model="forest">
                      <option v-for="f in forests" :value="f.value">{{ f.label }}</option>
                    </select>
                  </div>
                  <div class="detail-wrapper">
                    <label>机构</label>
                    <select id="inst" v-model="inst">
                      <option v-for="i in insts" :value="i.value">{{ i.label }}</option>
                    </select>
                  </div>
                  
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
import { Position } from '@element-plus/icons';
import axios from 'axios';
import { ref } from 'vue';

export default {
  data() {
    return {
      email: '',
      code:'',
      username:'',
      password:'',
      role:'普通用户',
      forest:null,
      inst:null,
      forests:ref(),
      insts:ref(),
    };
  },
  watch:{
      role(newValue){
        // role变化则对应都清空
        this.forest=null;
        this.inst=null;
        if(newValue!=='普通用户'){
          this.fetchForest();
        }
      },
      forest(newValue){
        if(newValue)
          this.fetchInst();
        
      }
    },
  methods: {
    //获取全部森林
    async fetchForest(){
      try{
        const response =await axios.get('http://127.0.0.1:5000/get_all_forests');
        this.forests=response.data.forests;
      }catch(error){
        console.error('Error Fetching options:', error);
      }
    },

    //依据forest和role选择该森林下的机构
    async fetchInst(){
      try {
        const params=new URLSearchParams();
        params.append('role',this.role);

        const response = await axios.post('http://127.0.0.1:5000/get_relative_inst',params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        this.insts=response.data.insts;
      } catch (error) {
        console.error('Error Fetching options:', error);
        alert(error);
      }
    },
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
        return;
      }

    },
    async register() {
      try {
        const params = new URLSearchParams();
        params.append('username', this.username);
        params.append('email', this.email);
        params.append('password', this.password);
        params.append('code', this.code);
        params.append('role',this.role);
        // 若是除普通用户以外的角色，还需添加管辖森林和所属机构团队
        if(this.role!=='普通用户'){
          params.append('forest',this.forest);
          params.append('inst',this.inst);
        }

        const response = await axios.post('http://127.0.0.1:5000/register', params);

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
  width: 65%;

  display: flex;
  align-items: center;
  overflow: hidden;
}

.image-box {
  display: block;

  height: 80vh;
  width: 50%;
  background-image: url(../assets/register.png);
  background-repeat: no-repeat;
  background-size: cover;
  background-position: -50px;
}

.signup-box {
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

section {
  width: 60%;
  max-width: 500px;
  margin-top: 10px;
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
.detail-wrapper{
  width:100%;
  margin-bottom: 1%;
}
.detail-wrapper label {
  display: block;
  margin-bottom: 5px;
  font-size: smaller;
  width:40%;
}
select{
  width: 95%;
  box-sizing: border-box;
  padding: 5px;
  border: 1.5px solid #ddd;
  border-radius: 10px;
}
select:hover{
  border: 1.5px solid #60a130;
}
select:focus{
  border: 1.5px solid #60a130;
  background-color: #f6fdf3;
  outline: none;
}

select option{
  background-color: white;
  line-height: 2;
}
select option:hover{
  background-color: #f6fdf3;
  color:#60a130;
}
.radio{
  cursor: pointer;
  transition: color 0.3s;
}

.radio:hover {
  color: #60a130;
}

.radio input[type="radio"] {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  border: 2px solid grey;
  border-radius: 50%;
  outline: none;
  cursor: pointer;
}

  .radio input[type="radio"]:checked {
    border: 2px solid #60a130;
  }

  .radio input[type="radio"]:checked::before {
    content: "";
    display: block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #60a130;
    margin-top: 2px;
    margin-left: 2px;
  }



</style>
