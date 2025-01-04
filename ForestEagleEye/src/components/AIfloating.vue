<template>
  <div v-if="isShowIcon" class="floating-icon" :style="{ top: y + 'px', left: x + 'px', opacity: isActive ? 1 : 0.4 }"
    @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" @mousedown="handleMouseDown" @mouseup="handleMouseUp">
  </div>
  <div class="chat-window" v-if="isChatWindowOpen">
    <div>
      <h1>小林问答</h1>
      <span>
        <el-icon @click="deleteChatHistory" style="cursor: pointer;">
          <DeleteFilled />
        </el-icon>
        <el-icon @click="showChatWindow(false)" style="cursor: pointer;">
          <Close />
        </el-icon>
      </span>
    </div>
    <div class="messages-container">
      <AImessage v-for="(msg, index) in messages" :key="index"
        :avatar_img="AI_NAME === msg.name ? 'src/assets/leaf1.svg' : user_avatar" :name="msg.name"
        :time="formatDateTime(msg.time)" :message="msg.message" />
      <AImessage v-if="messages.length === 0" :avatar_img="'src/assets/leaf1.svg'" :name="AI_NAME"
        :time="formatDateTime(new Date())" message="你好，我是小林，有什么问题可以问我哦~" />
    </div>
    <div>
      <input v-model="inputAttrs" type="text" placeholder="请输入问题" @keyup.enter="fetchNewMessage" />
      <button @click="fetchNewMessage()">发送</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import { Close, DeleteFilled } from '@element-plus/icons-vue';
import AImessage from './AImessage.vue';
import { formatDateTime } from '@/components/fotmatTime';
//////////////////////////////////////////////////获取历史聊天信息//////////////////////////////////////////////////
const AI_NAME = '小林';
const username = sessionStorage.getItem('username') || '';
const user_avatar = sessionStorage.getItem('avatar') || '../assets/default-avatar.svg';
interface Message {
  // id: number;
  name: string;
  time: Date;
  message: string;
}
const messages = ref<Message[]>([]);
const fetchHistory = async () => {
  messages.value = [];
  const response = await axios.get(`http://127.0.0.1:5000/fetchChatHistory`, {
    params: {
      username: username
    }
  });
  if (response.status === 200) {
    console.log('SUCCESS: Post liked successfully');
    response.data.forEach((msg: any) => {
      messages.value.push({
        name: username,
        time: new Date(msg.q_time),
        message: msg.question
      });
      messages.value.push({
        name: AI_NAME,
        time: new Date(msg.a_time),
        message: msg.answer
      });
    });
  }
  else {
    console.error(`ERROR: ${response.data.error}`);
  }
};
//////////////////////////////////////////////////发送并获取新消息//////////////////////////////////////////////////
const inputAttrs = ref('');
const fetchNewMessage = async () => {
  if (inputAttrs.value === '') {
    return;
  }

  const newMessage: Message = {
    name: sessionStorage.getItem('username') || '未登录用户',
    time: new Date(),
    message: inputAttrs.value
  };
  messages.value.push(newMessage);
  // 滚动条滚动到底部
  nextTick(() => {
    const container = document.querySelector('.messages-container') as HTMLElement;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });

  const formData = new FormData();
  formData.append('question', inputAttrs.value);
  formData.append('username', sessionStorage.getItem('username') || '');
  inputAttrs.value = '';

  const response = await axios.post(
    `http://127.0.0.1:5000/ask_model`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );

  if (response.status === 200) {
    const responseMessage: Message = {
      name: AI_NAME,
      time: new Date(),
      message: response.data.text
    };
    messages.value.push(responseMessage);
  }
  else {
    const responseMessage: Message = {
      name: AI_NAME,
      time: new Date(),
      message: '抱歉，小林出现了一些问题，无法回答您的问题。' + response.data.error
    };
    messages.value.push(responseMessage);
  }
  // 滚动条滚动到底部
  nextTick(() => {
    const container = document.querySelector('.messages-container') as HTMLElement;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
};
//////////////////////////////////////////////////删除AI聊天记录//////////////////////////////////////////////////
const deleteChatHistory = async () => {
  const formData = new FormData();
  formData.append('username', username);

  const response = await axios.post(
    `http://127.0.0.1:5000/deleteChatHistory`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  if (response.status === 200) {
    messages.value = [];
    console.log('SUCCESS: Chat history deleted successfully');
  }
  else {
    console.error(`ERROR: ${response.data.error}`);
  }
};
//////////////////////////////////////////////////图标的点击与拖动//////////////////////////////////////////////////
const x = ref(window.innerWidth - 100);
const y = ref(window.innerHeight - 100);
const isActive = ref(false);
const isDragging = ref(true);
const isChatWindowOpen = ref(false);
const isShowIcon = ref(true);

const handleMouseEnter = () => {
  isActive.value = true;
};

const handleMouseLeave = () => {
  isActive.value = false;
};

const handleMouseDown = () => {
  isDragging.value = false;
  document.addEventListener('mousemove', handleMouseMove);
  document.body.style.userSelect = 'none'; // 禁用选择
};

const handleMouseUp = () => {
  // 如果正在拖拽，则关闭拖拽状态，否则执行点击逻辑
  if (!isDragging.value) {
    isDragging.value = true;
    showChatWindow(!isChatWindowOpen.value);
    console.log('Icon clicked');
  }
  document.removeEventListener('mousemove', handleMouseMove);
  document.body.style.userSelect = ''; // 重新启用选择
};

const handleMouseMove = (event: MouseEvent) => {
  isDragging.value = true;
  if (isDragging.value) {
    x.value = event.clientX - 25;
    y.value = event.clientY - 25;
  }
};

const showChatWindow = (isShow: boolean) => {
  isChatWindowOpen.value = isShow;
  fetchHistory();
  console.log('Chat window opened');
};

</script>
<style scoped>
.floating-icon {
  position: fixed;
  /* 绝对定位 */
  width: 50px;
  /* 宽度50px */
  height: 50px;
  /* 高度50px */
  border-radius: 50%;
  /* 边框圆角50% */
  cursor: pointer;
  /* 鼠标指针为移动 */
  transition: opacity 0.5s;
  /* 透明度过渡时间0.5秒 */
  background-image: url("../assets/icon-AI.svg");
  background-size: 100%;
  background-repeat: no-repeat;
  z-index: 100;
}

.chat-window {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 39%;
  height: 62%;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 3%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  /* 添加滚动条 */
}

.chat-window div {
  box-sizing: border-box;
  width: 100%;
  border: 0px;
  border-bottom: 1px;
  border-style: solid;
  padding: 10px 0px 10px 0px;
  background-color: white;
}

.chat-window>div:nth-of-type(1) {
  padding-right: 20px;
  padding-left: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-window>div:nth-of-type(1) span {
  gap: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-window>div:nth-of-type(2) {
  height: 80%;
  overflow-y: auto;
}

.chat-window h1 {
  margin: 0px;
}

el-icon {
  cursor: pointer;
}
</style>