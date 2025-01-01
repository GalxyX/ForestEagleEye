<template>
  <div class="container">
    <!-- 顶部导航栏 -->
    <NavigationBar />
    
    <div class="all-contents">
      <!-- 页头部分 -->
      <el-page-header @back="handleClick" content="创建活动" title="返回">
      </el-page-header>
      
      <el-divider></el-divider>

      <el-alert
        title="温馨提示：在创建森林活动时，请确保您的行为符合当地法律法规，尊重自然环境和当地文化。提前规划，明确活动目的，评估所需资源，并制定详细的安全计划和风险管理策略。与所有相关方保持良好沟通，合理安排时间，确保活动顺利进行。同时，制定有效的宣传推广计划，提高活动知名度。活动结束后，收集反馈以评估效果并改进未来活动。最重要的是，采取可持续的做法，减少对森林环境的影响，确保活动安全、环保且富有成效。"
        type="warning"
        :closable="false"
        style="font-size: small;margin-left:20px;max-width: 1750px;">
      </el-alert>

      <div class="approval-steps">
        <div class="h1">申请流程</div>
          <el-steps :active="0" finish-status="success" align-center>
            <el-step title="申请提交"></el-step>
            <el-step title="审批中"></el-step>
            <el-step title="申请通过"></el-step>
            <el-step title="活动完成"></el-step>
          </el-steps>

        <div class="h1">活动信息</div>
          <el-form
            ref="ruleFormRef"
            style="max-width: 900px;padding-left: 50px;"
            :model="ruleForm"
            :rules="rules"
            label-width="auto"
            lass="ruleForm"
            :size="formSize"
            status-icon
          >

          <el-form-item label="活动名称" prop="a_name">
            <el-input v-model="ruleForm.a_name" placeholder="请输入活动名称" />
          </el-form-item>

          <el-form-item label="活动地点" prop="a_location">
            <el-input v-model="ruleForm.a_location" placeholder="请输入活动地点" />
          </el-form-item>

          <el-form-item label="活动开始时间" prop="a_beginTime">
            <el-input type="datetime-local" v-model="ruleForm.a_beginTime" />
          </el-form-item>

          <el-form-item label="活动结束时间" prop="a_endTime">
            <el-input type="datetime-local" v-model="ruleForm.a_endTime" />
          </el-form-item>

          <el-form-item label="活动人数" prop="a_participantNumber">
            <el-input type="number" v-model="ruleForm.a_participantNumber" />
          </el-form-item>

          <el-form-item label="活动简介" prop="a_introduction">
            <el-input
              v-model="ruleForm.a_introduction"
              type="textarea"
              maxlength="1000"
              show-word-limit
            />
          </el-form-item>

          <el-form-item label="活动森林" prop="a_forest">
            <el-select v-model="ruleForm.a_forest" placeholder="请选择活动森林">
              <el-option
                v-for="forest in forestList"
                :key="forest.value"
                :label="`${forest.label} (${forest.location})`"
                :value="forest.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="活动类型" prop="a_type">
            <el-select v-model="ruleForm.a_type" placeholder="请选择活动类型">
              <el-option label="伐木" value="伐木" />
              <el-option label="采摘" value="采摘" />
              <el-option label="旅游参观" value="旅游参观" />
              <el-option label="野营" value="野营" />
              <el-option label="捕猎" value="捕猎" />
            </el-select>
          </el-form-item>

          <el-form-item label="是否面向大众" prop="a_ableParticipate">
            <el-switch  v-model="ruleForm.a_ableParticipate" active-color="#13ce66" inactive-color="#ff4949" active-text="是" inactive-text="否"></el-switch>
          </el-form-item>

          <!-- 上传活动图片 -->
          <el-form-item label="活动封面图片" prop="a_picPath">
            <el-upload
              action="http://127.0.0.1:5000/upload_activity_image"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :show-file-list="false"
            >
            <el-button type="success" round plain>上传图片</el-button>
            </el-upload>
            <img
              v-if="ruleForm.a_picPath"
              :src="ruleForm.a_picPath"
              alt="活动图片"
              style="margin-top: 10px; max-width: 100%;"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="success" style="align-self: center;" @click="submitForm(ruleFormRef)">创建</el-button>
            <el-button type="info" plain style="align-self: center;" @click="resetForm(ruleFormRef)">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

    </div>
    <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue';
import NavigationBar from '../components/navbar.vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ArrowLeft } from '@element-plus/icons-vue';

// 数据
const forestList = ref([]);
const user_id = sessionStorage.getItem('user_id') || '';
const router = useRouter();

// 表单规则
interface RuleForm {
  a_name: string;
  a_location: string;
  a_beginTime: string;
  a_endTime: string;
  a_participantNumber: number;
  a_introduction: string;
  a_forest: string;
  a_type: string;
  a_ableParticipate: boolean;
  a_picPath: string;
}

const formSize = ref('default');
const ruleFormRef = ref();
const ruleForm = reactive<RuleForm>({
  a_name: '',
  a_location: '',
  a_beginTime: '',
  a_endTime: '',
  a_participantNumber: 0,
  a_introduction: '',
  a_forest: '',
  a_type: '伐木',
  a_ableParticipate: false,
  a_picPath: '',
});

// 加载森林数据
const fetchForests = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_all_forests');
    forestList.value = response.data.forests.map((forest: any) => ({
      value: forest.value,
      label: forest.label,
      location: forest.location,
    }));
  } catch (error) {
    ElNotification({
      title: '获取失败',
      message: '无法获取森林数据，请稍后重试',
      type: 'error',
    });
  }
};

onMounted(() => {
  fetchForests();
});

const rules = reactive<FromRules<RuleForm>>({
  a_name: [
    {required: true, message: '请输入活动名称', trigger: 'blur' },
    {min:1,max :100,message:'活动名称长度应介于1~100之间',trigger: 'blur'},
  ],
  a_location: [
    {
      required:true,
      message:'请选择活动地点',
      trigger:'change',
    }
  ],
  a_beginTime:[
    {
      required:true,
      message:'请选择活动开始时间',
      trigger:'blur'
    }
  ],
  a_endTime: [
  {
      required:true,
      message:'请选择活动结束时间',
      trigger:'blur'
    }
  ],
  a_participantNumber: [
    {required: true, message: '请输入活动人数', trigger: 'blur' },
  ],
  a_introduction: [
    { required: true, message: '请填写活动简介', trigger: 'blur' },
  ],
  a_forest: [
    { required: true, message: '请填写活动所在森林', trigger: 'blur' },
  ],
  a_type: [
    {
      required:true,message:'请选择活动类型',trigger:'change'
    }
  ],
  a_ableParticipate: [
    {
      required: true, message: '请选择是否向公众开放', trigger: 'blur' 
    }
  ],
  a_picPath: '',
})


// 上传图片
const handleUploadSuccess = (response: any) => {
  ruleForm.a_picPath = response.filePath;
  //ElNotification({ title: '上传成功', message: '图片上传成功！', type: 'success' });
};

const handleUploadError = () => {
  ElNotification({ title: '上传失败', message: '图片上传失败，请重试。', type: 'error' });
};

// 返回
const handleClick = () => {
  router.push('/activities'); // 跳转到活动页面
};

const resetForm = (formEl: any) => {
  if (!formEl) return;
  formEl.resetFields();
};
const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        console.log('submit!')
        console.log(ruleForm)
      } else {
        //这里的ElNotification标红不是因为报错，是因为全局导入的el-ui这里无需再写，编译器的问题，不用管可以直接跑
        ElNotification({
          title: '创建失败',
          message: '操作失败，请重新尝试',
          type: 'error',
        })
        console.log('error submit!', fields)
      }
    })
    //向后端提交请求
    try{
      const params = new URLSearchParams();
      params.append('user_id',user_id);
      params.append('a_name',ruleForm.a_name.toString());
      params.append('a_location',ruleForm.a_location.toString());
      params.append('a_beginTime',ruleForm.a_beginTime);
      params.append('a_endTime',ruleForm.a_endTime);
      params.append('a_participantNumber',ruleForm.a_participantNumber);
      params.append('a_introduction',ruleForm.a_introduction.toString());
      params.append('a_forest',ruleForm.a_forest.toString());
      params.append('a_type',ruleForm.a_type);
      params.append('a_ableParticipate',ruleForm.a_ableParticipate);
      params.append('a_picPath',ruleForm.a_picPath);

       console.log(params);

      const response = await axios.post('http://127.0.0.1:5000/create_activity', params,{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
      }
      );
            //这里的ElNotification标红不是因为报错，是因为全局导入的el-ui这里无需再写，编译器的问题，不用管可以直接跑
      if (response.data.status === "success") {
      ElNotification({
        title: '创建成功',
        message: '已成功创建活动~',
        type: 'success',
      });
      formEl.resetFields();
      }else {
      throw new Error(response.data.message || "创建失败");
    }
    }

    catch(error){
      ElNotification({
          title: '操作失败',
           message: error.response?.data?.message || error.message || '操作失败，请重新尝试',
          type: 'error',
      })
      console.log('error to post!')
    }
  };





</script>

<style scoped>
.container {
  display: flex;       /* 使用Flexbox布局 */
  flex-direction: column; /* 设置主轴方向为垂直 */
  background-color: #f8f8f8;
}
.all-contents{
  background-color: #ffffff;
  margin-left: 20px; /* 左边距 */
  margin-right: 20px; /* 右边距 */
  margin-top: 80px;
  display: flex;
  flex-direction: column; /* 设置子元素纵向排列 */
}
.page-header {
  z-index: 10; /* 保证在最上层 */
  background-color: white;
  padding: 10px;
  position: sticky;
  top: 0; /* 固定在页面顶部 */
}

.ruleForm {
  margin: 10px 30px;
}

.el-divider {
  margin-top: 10px;
}

.el-input__inner,
.el-textarea__inner {
  color: black;
}
.all-contents{
  background-color: #ffffff;
  margin-left: 20px; /* 左边距 */
  margin-right: 20px; /* 右边距 */
  margin-top: 80px;
  display: flex;
  flex-direction: column; /* 设置子元素纵向排列 */
}
.el-page-header {
  margin-top: 20px; /* 或者其他适当的值 */
  margin-left: 20px; /* 左边距 */
}
.h1{
  margin-left: 30px;
  margin-top:30px;
  margin-bottom:30px;
  font-size:20px;
  font-weight: lighter;
  color:grey;
}
.el-footer{
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size:xx-small;
  margin-top: 30px;
}
</style>
