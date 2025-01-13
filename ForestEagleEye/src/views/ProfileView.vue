<template>
  <NavigationBar />
  <div class="main">
    <!-- sidebar -->
    <div class="sidebar">
      <div style="background-color: #60a103;height:40vh;">
        <div style="display: flex;">
          <img class="avatar" :src="avatar || '../assets/default-avatar.png'" @click="openAvatarUploadDialog">
          <div style="margin-left: 15px; margin-top:50px;">
            <text class="side-username">{{ username }}</text>
            <text v-if="role === '普通用户'"
              style="color:white; font-size: small; display:block; text-align: left;">您还没有所属团队~</text>
            <text v-else style="color:white; font-size: small;">{{ inst }}</text>
          </div>
        </div>

        <div class="side-container">
          <div class="side-header">
            <text class="side-label">我的角色</text>
          </div>
          <h4>{{ role }}</h4>
        </div>
        <div class="side-container">
          <div class="side-header">
            <text class="side-label">个性签名</text>
            <img @click="toggleEdit" src="../assets/icon-pencil.png"
              style="height:18px; margin-left:5px;margin-bottom: -5px;">
          </div>
          <div v-if="isEditing">
            <textarea v-model="editedSignature" :maxlength="99" @input="updateInputInfo">
              </textarea>
            <span class="input-info">{{ editedSignature.length }}/99</span>
            <button @click="saveSignature">保存</button>
          </div>
          <h4 v-if="!isEditing">{{ signature }}</h4>
        </div>
      </div>
    </div>
    <div v-if="showAvatarDialog" class="avatar-upload-dialog">
      <input type="file" @change="handleFileChange" accept="image/*" />
      <button @click="uploadAvatar">上传头像</button>
      <button @click="closeAvatarUploadDialog">取消</button>
    </div>
    <!-- userinfo -->
    <div class="userinfo">
      <div class="container">
        <div style="display: flex;">
          <h1 v-if="!isEditingName">Hi，{{ username }}</h1>
          <img v-if="!isEditingName" @click="toggleEditname" src="../assets/icon-pencil2.png"
            style="height:18px; margin-left:5px;margin-top: 20px;">
          <input v-model="editedName" class="input-name" v-if="isEditingName" placeholder="输入修改后的昵称" maxlength="10">
          <button v-if="isEditingName" style="height:25px; margin-top: 11px; margin-left: 10px;"
            @click="saveName">保存</button>
        </div>
        <text class="label">{{ greeting }}</text>
      </div>
      <div class="container">
        <h2>个人信息</h2>

        <div class="user-info">
          <div class="info-row">
            <div class="info-label">昵称</div>
            <div class="info-value">{{ username }}</div>
          </div>
          <div class="info-row">
            <div class="info-label">用户ID</div>
            <div class="info-value">{{ user_id }}</div>
          </div>
          <div class="info-row">
            <div class="info-label">邮箱</div>
            <div class="info-value">{{ email }}</div>
          </div>
          <div class="info-row">
            <div class="info-label">注册时间</div>
            <div class="info-value">{{ signupTime }}</div>
          </div>
        </div>

        <div class="user-info">
          <div class="info-row">
            <div class="info-label">角色</div>
            <div class="info-value">{{ role }}</div>
          </div>
          <div class="info-row" v-if="role !== '普通用户'">
            <div class="info-label">所属森林</div>
            <div class="info-value">{{ forest }}</div>
          </div>
          <div class="info-row" v-if="role !== '普通用户'">
            <div class="info-label">所属机构</div>
            <div class="info-value">{{ inst }}</div>
          </div>

          <div class="info-row">
            <div class="info-label">最近登录时间</div>
            <div class="info-value">{{ newestTime }}</div>
          </div>
        </div>

      </div>

      <footer>
        <p>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</p>
      </footer>
    </div>
  </div>

</template>

<script>
import axios from 'axios';
import NavigationBar from '../components/navbar.vue'

export default {
  name: 'profile',
  components: {
    NavigationBar
  },
  data() {
    return {
      greeting: '',

      username: '',
      avatar: '',
      user_id: '',
      email: '',
      role: '',
      forest: '',
      inst: '',
      signupTime: '',
      newestTime: '',
      days: '',
      showAvatarDialog: false, // 控制头像上传对话框的显示
      selectedFile: null, // 保存用户选择的文件
      signature: '',
      isEditing: false,
      isEditingName: false,
      editedSignature: '',
      inputLength: 0
    };
  },
  mounted() {
    this.username = sessionStorage.getItem('username');
    this.avatar = sessionStorage.getItem('avatar');
    this.user_id = sessionStorage.getItem('user_id');
    this.email = sessionStorage.getItem('email');
    this.role = sessionStorage.getItem('role');
    this.signupTime = sessionStorage.getItem('signupTime');
    this.newestTime = sessionStorage.getItem('newestTime');
    this.days = sessionStorage.getItem('days');
    this.signature = sessionStorage.getItem('signature');
    this.inst = sessionStorage.getItem('inst');
    this.forest = sessionStorage.getItem('forest');

    const hour = new Date().getHours();
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
    this.greeting += '今天是你来到林上鹰眼的第' + this.days + '天~';

  },
  methods: {
    // 打开头像上传对话框
    openAvatarUploadDialog() {
      this.showAvatarDialog = true;
    },
    // 关闭头像上传对话框
    closeAvatarUploadDialog() {
      this.showAvatarDialog = false;
    },
    // 处理文件选择
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadAvatar() {
      if (!this.selectedFile) {
        ElMessage({
          showClose: true,
          message: '请先选择一个文件',
          type: 'warning'
        });
        return;
      }

      const formData = new FormData();
      formData.append('avatar', this.selectedFile);
      formData.append('user_id', this.user_id);

      try {
        const response = await axios.post('http://127.0.0.1:5000/uploadAvatar', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        // 更新头像
        if (response.data.status === 'success') {
          this.avatar = response.data.avatar_url;
          sessionStorage.setItem('avatar', this.avatar); // 保存到 sessionStorage
          this.closeAvatarUploadDialog(); // 关闭对话框
          window.location.reload();
        } else {
          alert('上传失败: ' + response.data.message);
        }
      } catch (error) {
        console.error('上传失败:', error);
        alert('上传失败，请稍后再试');
      }
    },
    async toggleEdit() {
      this.isEditing = true;
      this.editedSignature = this.signature;
    },
    async toggleEditname() {
      this.isEditingName = true;
    },
    async saveSignature() {

      if (this.editedSignature !== this.signature) {
        if (!this.editedSignature)
          this.editedSignature = "这个人很懒，什么都没有留下...";
        if (this.editedSignature.length > 99)
          this.editedSignature = this.editedSignature.substring(0, 98);
        try {
          const params = new URLSearchParams();
          params.append('target', 'signature');
          params.append('data', this.editedSignature);
          params.append('user_id', this.user_id);

          const response = await axios.post('http://127.0.0.1:5000/setUserInfo', params, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          });
          this.signature = this.editedSignature;
          sessionStorage.setItem('signature', this.signature);
          ElNotification({
            title: '修改成功',
            message: '个性签名已成功修改~',
            type: 'success',
          });
        }
        catch (error) {
          alert(response.data.message);
        }
      }
      this.isEditing = false;
    },
    async saveName() {
      if (this.editedName) {
        //向后端发送请求更改内容
        try {
          const params = new URLSearchParams();
          params.append('target', 'username');
          params.append('data', this.editedName);
          params.append('user_id', this.user_id);

          const response = await axios.post('http://127.0.0.1:5000/setUserInfo', params, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          });
          ElNotification({
            title: '修改成功',
            message: '用户名已成功修改~',
            type: 'success',
          });
        }
        catch (error) {
          alert(response.data.message);
        }
        this.username = this.editedName;
        // 更新会话中的存储
        sessionStorage.setItem('username', this.username);
        //location.reload();
      }
      this.isEditingName = false;
    },
    async updateInputInfo() {
      this.inputLength = this.editedSignature.length;
    }
  },
  computed: {
    inputLength() {
      return this.editedSignature.length;
    }
  }
}
</script>

<style scoped>
.avatar-upload-dialog {
  position: fixed;
  top: 20%;
  left: 15%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.avatar-upload-dialog input {
  width: 80%;
  margin-left: 30%;
}

.avatar-upload-dialog button {
  margin-top: 10px;
}

.main {
  padding-top: 50px;
  background-color: #F0F2F5;
  display: flex;
  height: 100vh;
}

.userinfo {
  margin-top: 20px;
  margin-left: 25px;
  justify-content: center;
}

.input-name {
  margin-top: 10px;
  border: 1px solid #456E02;
  border-radius: 10px;
  font-size: x-small;
  height: 25px;
  padding-left: 10px;
}

.input-name:focus {
  outline: none;
  background-color: rgb(245, 252, 232);
}

textarea {
  margin-top: 10px;
  border: 1px solid #456E02;
  padding: 5px;
  border-radius: 10px;
  font-size: xx-small;
  width: 90%;
  height: 6vh;
  color: grey;
  font-family: Arial, sans-serif;
}

textarea:focus {
  outline: none;
  background-color: rgb(251, 255, 243);
  color: black;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.input-info {
  position: absolute;
  font-size: small;
  color: #999;
  margin-top: 50px;
  margin-left: -40px;
}

button {
  display: block;
  background-color: white;
  border: 1px solid #456E02;
  color: #456E02;
  padding: 4px 12px;
  border-radius: 12px;
  cursor: pointer;
  font-size: xx-small;
  font-weight: bold;
  justify-content: center;
}

button:hover {
  background-color: rgb(239, 255, 213);
}

.sidebar {
  background-color: white;
  width: 20%;
  height: 100vh;
}

.avatar {
  height: 80px;
  width: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
  margin-left: 20px;
  margin-top: 40px;
  ;
}

.side-username {
  font-size: xx-large;
  font-weight: bold;
  color: white;
  display: block;
  text-align: left;
  margin-bottom: 5px;
  width: 200px;
  white-space: nowrap;
  /* 保持文本在一行显示 */
  overflow: hidden;
  /* 隐藏超出部分 */
  text-overflow: ellipsis;
  /* 超出部分显示省略号 */
}

.side-label {
  border: 1px solid white;
  border-radius: 15px;
  background-color: #456E02;
  padding-left: 15px;
  padding-right: 15px;
  padding-top: 3px;
  padding-bottom: 3px;
  font-size: small;
  color: white;

}

.side-container {
  margin-top: 10px;
  margin-left: 20px;
}

.container {
  background-color: white;
  width: 1200px;
  margin-bottom: 20px;
  padding: 10px 25px 25px 25px;
}

.subtitle {
  display: flex;
  align-content: space-between;
  align-items: center;
  gap: 5px;
}

h1 {
  font-size: 16pt;
}

h2 {
  font-size: 12pt;
  font-weight: normal;
}

h3 {
  font-size: small;
  font-weight: normal;
  color: grey;
}

h4 {
  margin-top: 10px;
  margin-left: 5px;
  font-size: small;
  color: white;
  font-weight: normal;
  width: 90%;
}

.label {
  color: #456E02;
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
  width: 300px;
  margin-bottom: 10px;

}

.info-label {
  text-align: left;
  font-size: small;
  margin-bottom: 10px;
  color: grey;
}

.info-value {
  text-align: left;
  font-size: small;
}

footer {
  background-color: transparent;
  color: #ababab;
  text-align: center;
  padding: 10px 0;
  bottom: 0;
  width: 100%;
  font-size: xx-small;
}
</style>