<template>
     <el-page-header :icon="ArrowLeft" @click="handleClick" style="margin-top: 5px;">
        <template #content>
        <span class="text-large font-600 mr-3"> 创建森林 </span>
        </template>
    </el-page-header>
    <el-divider></el-divider>
    
    <el-form
      ref="ruleFormRef"
      style="max-width: 600px"
      :model="ruleForm"
      :rules="rules"
      label-width="auto"
      class="ruleForm"
      :size="formSize"
      status-icon
    >
      <el-form-item label="森林名称" prop="f_name">
        <el-input v-model="ruleForm.f_name" placeholder="请填写名称"/>
      </el-form-item>
      <el-form-item label="森林所在区域" prop="f_location">
        <el-cascader
        ref="cascaderRef"
        :options="options"
        v-model="selectedValue"
        placeholder="请选择地址"
        @change="onCascadarChange"
      ></el-cascader>
      
      </el-form-item>
      <el-form-item label="森林占地面积" prop="f_area">
        <el-input v-model="ruleForm.f_area"/>
      </el-form-item>

      <el-form-item label="森林土壤类型" prop="f_soilType">
        <el-checkbox-group v-model="ruleForm.f_soilType">
          <el-checkbox value="砂土" name="type">
            砂土
          </el-checkbox>
          <el-checkbox value="壤土" name="type">
            壤土
          </el-checkbox>
          <el-checkbox value="粘土" name="type">
            粘土
          </el-checkbox>
          <el-checkbox value="粉砂土" name="type">
            粉砂土
          </el-checkbox>
          <el-checkbox value="黑土" name="type">
            黑土
          </el-checkbox>
          <el-checkbox value="红土" name="type">
            红土
          </el-checkbox>
          <el-checkbox value="黄土" name="type">
            黄土
          </el-checkbox>
          <el-checkbox value="白土" name="type">
            白土
          </el-checkbox>
          <el-checkbox value="盐碱土" name="type">
            盐碱土
          </el-checkbox>
          <el-checkbox value="水稻土" name="type">
            水稻土
          </el-checkbox>
          <el-checkbox value="泥炭土" name="type">
            泥炭土
          </el-checkbox>
          <el-checkbox value="火山土" name="type">
            火山土
          </el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      
      <el-form-item label="森林管理机构" prop="f_manager">
        <el-select v-model="ruleForm.f_manager" placeholder="请选择管理机构">
          <!--这里的标红不用管-->
          <el-option
            v-for="item in instsOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
      </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="森林简介" prop="f_intro">
        <el-input v-model="ruleForm.f_intro" type="textarea" maxlength="1000" show-word-limit />
      </el-form-item>
      <el-form-item>
        <el-button type="success" style="align-self: center;" @click="submitForm(ruleFormRef)">创建</el-button>
        <el-button type="info" plain style="align-self: center;" @click="resetForm(ruleFormRef)">重置</el-button>
      </el-form-item>
    </el-form>
  </template>
  
  <script lang="ts" setup>
  import { onMounted,reactive, ref } from 'vue'
  import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
  import { ArrowLeft } from '@element-plus/icons-vue'
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import { regionData } from 'element-china-area-data';


  interface RuleForm {
    f_name: string
    f_location: string
    f_area: number
    f_soilType: string[]
    f_manager:string
    f_intro: string
  }
  
  const formSize = ref<ComponentSize>('default')
  const ruleFormRef = ref<FormInstance>()
  const ruleForm = reactive<RuleForm>({
    f_name: '',
    f_location: '',
    f_area: 0,
    f_manager:'',
    f_soilType: [],
    f_intro: '',
  })
  
  const router = useRouter();
  // 省市区级联选择器响应式数据
  const options = ref(regionData);
  var selectedValue = ref([]);
  const cascaderRef = ref(null);
  //这里的标红不是因为报错，是因为全局导入的el-ui这里无需再写，编译器的问题，不用管可以直接跑
  const onCascadarChange = (value) =>{
    if (cascaderRef.value && value.length > 0) {
      const labelArray = cascaderRef.value.getCheckedNodes()[0].pathLabels;      
      ruleForm.f_location = labelArray.join('/');
    }
  }

  //选择管理机构响应式数据
  const instsOptions = ref([]);

  // 获取机构数据的方法
  const fetchInstitutions = async () => {
    const params = new URLSearchParams();
    params.append('role','林业管理人员');
    try {
      const response = await axios.post('http://127.0.0.1:5000/get_relative_inst', params,{
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
      });
      if (response.data.insts) {
        instsOptions.value = response.data.insts;
        console.log(response.data.insts);
        console.log(instsOptions.value);
      } else {
        // 处理错误情况
        console.error(response.data.error);
      }
    } catch (error) {
      console.error('请求错误:', error);
    }
  };
  onMounted(() => {
    fetchInstitutions();
  });
 
  const rules = reactive<FormRules<RuleForm>>({
    f_name: [
      { required: true, message: '请输入森林名称', trigger: 'blur' },
      { min: 1, max: 100, message: '森林名称长度应介于1~100之间', trigger: 'blur' },
    ],
    f_location: [
      {
        required: true,
        message: '请选择森林所在区域',
        trigger: 'change',
      },
    ],
    f_area: [
      {
        required: true,
        message: '请输入森林占地面积',
        trigger: 'change',
      },
    ],
    f_soilType: [
      {
        type: 'array',
        required: true,
        message: '请至少选择一种土壤类型',
        trigger: 'change',
      },
    ],
    f_manager:[
      {
        required:true,
        message:'请选择森林的管理机构',
        trigger:'change',
      }
    ],
    f_intro: [
      { required: true, message: '请填写森林简介', trigger: 'blur' },
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
      params.append('f_name',ruleForm.f_name);
      params.append('f_location',ruleForm.f_location);
      params.append('f_area',ruleForm.f_area.toString());
      params.append('f_soilType',ruleForm.f_soilType.toString());
      params.append('f_manager',ruleForm.f_manager);
      params.append('f_intro',ruleForm.f_intro);
      
      const response = await axios.post('http://127.0.0.1:5000/add_forest', params,
      );

      //这里的ElNotification标红不是因为报错，是因为全局导入的el-ui这里无需再写，编译器的问题，不用管可以直接跑
      ElNotification({
        title: '创建成功',
        message: '森林已成功添加到林上鹰眼数据库~',
        type: 'success',
      });
      formEl.resetFields();
      selectedValue.value=[];
    }
    catch(error){
      //这里的ElNotification标红不是因为报错，是因为全局导入的el-ui这里无需再写，编译器的问题，不用管可以直接跑
      ElNotification({
          title: '操作失败',
          message: '操作失败，请重新尝试',
          type: 'error',
      })
      console.log('error to post!')
    }
  }
  
  const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
  }
  
  // 定义可以触发的事件
  const emit = defineEmits(['back']);

  const handleClick= (event:MouseEvent) =>{
    if((event.target as HTMLElement).classList.contains('text-large'))
      return;//点击“创建森林”没有反应
    else{
      emit('back');
      //router.back();
    }
  }
</script>
  
<style>
.ruleForm{
  margin: 10px 30px 10px 30px;
}
.el-checkbox__input.is-checked .el-checkbox__inner {
  background-color: #60a130 !important;
  border-color: #60a130 !important;
}
.el-checkbox__input.is-checked + .el-checkbox__label {
  color: #60a130 !important;
}
.el-checkbox__input .el-checkbox__inner {
  border-color: #dcdfe6; /* 未选中时的边框颜色 */
}
.el-divider{
  margin-top: 10px;
}
.el-input__inner{
  color: black;
}
.el-textarea__inner{
  color: black;
  padding: 15px 15px 15px 15px !important;
  line-height: 20px;
  height: 200px;
}
</style>