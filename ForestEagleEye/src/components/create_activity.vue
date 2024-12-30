<template>
  <el-page-header :icon="ArrowLeft" @click="handleClick" style="margin-top: 5px;">
    <template #content>
      <span class="text-large font-600 mr-3"> 创建活动 </span>
    </template>
  </el-page-header>
  <el-divider></el-divider>

  <el-form
    ref="ruleFormRef"
    style="max-width: 600px"
    :model="ruleForm"
    label-width="auto"
    class="ruleForm"
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
      <el-input v-model="ruleForm.a_introduction" type="textarea" maxlength="1000" show-word-limit />
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
      <el-switch v-model="ruleForm.a_ableParticipate" active-text="是" inactive-text="否" />
    </el-form-item>


    <el-form-item>
      <el-button type="success" style="align-self: center;" @click="submitForm(ruleFormRef)">创建</el-button>
      <el-button type="info" plain style="align-self: center;" @click="resetForm(ruleFormRef)">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElNotification } from 'element-plus';
import axios from 'axios';
import { ArrowLeft } from '@element-plus/icons-vue';
import { ElUpload } from 'element-plus';


const forestList = ref([]); // 存储森林数据

onMounted(async () => {
  await fetchForests();
});

const fetchForests = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_all_forests');
    forestList.value = response.data.forests.map((forest: any) => ({
      value: forest.value,
      label: forest.label,
      location: forest.location,
    }));
  } catch (error) {
    console.error('获取森林数据失败:', error);
    ElNotification({
      title: '获取失败',
      message: '无法获取森林数据，请稍后重试',
      type: 'error',
    });
  }
};



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
 });

const router = useRouter();
const user_id = sessionStorage.getItem('user_id');

  const rules = reactive<FormRules<RuleForm>>({
    a_name: [
      { required: true, message: '请输入活动名称', trigger: 'blur' },
    ],
    a_location : [
      {
        required: true,
        message: '请选择活动所在区域',
        trigger: 'change',
      },
    ],
    a_beginTime: [
      {
        required: true,
        message: '请输入',
      },
    ],
    a_endTime: [
      {
        required: true,
        message: '请输入',
      },
    ],
    a_participantNumber: [
      {
        required: true,
        message: '请输入',
      },
    ],
    a_introduction: [
      {
        required: true,
        message: '请输入',
      },
    ],
    a_forest: [
      {
        required: true,
        message: '请输入',
      },
    ],
    a_type: [
      {
        type: 'array',
        required: true,
        message: '请选择一种类型类型',
        trigger: 'change',
      },
    ],
    a_ableParticipate:[
      {
        required:true,
        message:'请选择',
        trigger:'change',
      }
    ],
  })
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
  }
const resetForm = (formEl: any) => {
  if (!formEl) return;
  formEl.resetFields();
};

const handleClick = () => {
  router.push('/activity');
};
</script>

<style scoped>
.ruleForm {
  margin: 10px 30px 10px 30px;
}
.el-divider {
  margin-top: 10px;
}
.el-input__inner {
  color: black;
}
.el-textarea__inner {
  color: black;
  padding: 15px 15px 15px 15px !important;
  line-height: 20px;
  height: 200px;
}
</style>
