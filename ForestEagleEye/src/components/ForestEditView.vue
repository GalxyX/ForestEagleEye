<template>
     <el-page-header :icon="ArrowLeft" @click="handleClick" style="margin-top: 5px;">
        <template #content>
        <span class="text-large font-600 mr-3"> 编辑详情 </span>
        </template>
    </el-page-header>
    <el-divider></el-divider>

    <div style="margin-left: 30px;margin-right: 30px;">
      <!-- 基本信息表单 -->
      <el-descriptions title="基本信息">
        <el-descriptions-item label="森林序号">{{f_id}}</el-descriptions-item>
        <el-descriptions-item label="森林名称">{{f_name}}</el-descriptions-item>
        <el-descriptions-item label="森林面积">{{f_area}}</el-descriptions-item>
        <el-descriptions-item label="管理机构">
          <el-tag size="normal" type="success">{{f_manager}}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="地理位置">
          {{f_location}}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <div style="margin-top:20px; margin-left: 30px;margin-right: 30px;">
      <!-- 变量信息表单 -->
      <el-descriptions
        title="变量信息"
        direction="vertical"
        :column="1"
      ></el-descriptions>
        <div>
          <div>
            <h1>编辑气候概况</h1>
            <div style="display: flex; align-items: center; gap: 10px;">
              <h2>
                <el-alert
                title="温馨提示：点击按钮获取本林区的最新气象数据，并更新到林上鹰眼数据库"
                type="warning"
                :closable="false"
                style="font-size: small;">
              </el-alert>
              </h2>
              
              <el-button type="success" plain style="width: 80px;" v-if="!showLoading" @click="fetchWeatherData">获取数据</el-button>
              <el-button  type="success" plain loading style="width: 80px;" v-else disabled>Loading</el-button>
            </div>
            <el-descriptions
              direction="vertical"
              :column="5"
              border
              v-if="showWeatherDataBox"
            >
              <el-descriptions-item label="温度(单位:°C)">{{w_temperature}}</el-descriptions-item>
              <el-descriptions-item label="风向">{{w_winddirection}}</el-descriptions-item>
              <el-descriptions-item label="风力(单位:级)">
                <el-tag size="small" type="success">{{w_windpower}}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="空气湿度">{{w_humidity}}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{w_time}}</el-descriptions-item>
            </el-descriptions>
            <h3 v-if="showWeatherDataBox" >*气象数据来源：高德开放平台-Web服务API</h3>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <div style="display: flex; align-items: center; margin-top: 10px;">
              <h1>编辑森林简介</h1>
              <img v-if="!isEditIntro" @click="toggleEditIntro" src="../assets/icon-pencil2.png" style="height:18px; margin-left:5px;margin-top: 20px;">
            </div>
            <div v-if="isEditIntro===false" style="color:grey; font-size: 10.5pt; margin-top: 15px;">{{intro}}</div>
            <div v-else disabled>
              <el-input  v-model="editedIntro"  placeholder="输入修改后的森林简介"  type="textarea" maxlength="1000" show-word-limit />
              <el-button class="ml-3" type="success" @click="submitIntro" style="margin-top: 10px;">
                上传至林上鹰眼
              </el-button>
            </div>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <h1>编辑资源分布</h1>
            <h2>
              <el-alert
              title="温馨提示：按照参考格式上传数据文件，林上鹰眼会自动帮您保存到数据库中"
              type="warning"
              :closable="false"
              style="font-size: small;">
            </el-alert>
            </h2>
            
            <el-descriptions
              direction="vertical"
              style="margin-bottom: 10px;"
              :column="5"
              border
            >
              <el-descriptions-item label="资源名称">野猪</el-descriptions-item>
              <el-descriptions-item label="资源类型">动物</el-descriptions-item>
              <el-descriptions-item label="分布中心经度">123.123</el-descriptions-item>
              <el-descriptions-item label="分布中心纬度">45.45</el-descriptions-item>
              <el-descriptions-item label="分布范围半径(公里)">5</el-descriptions-item>
            </el-descriptions>

            <el-upload
              ref="uploadResource"
              action="http://127.0.0.1:5000/uploadResourceFile"
              :limit="1"
              :on-exceed="handleExceedResource"
              :auto-upload="false"
              :data="uploadForest"
            >
              <template #trigger>
                <el-button type="success" plain>选择文件</el-button>
                <h3 style="margin-left: 10px; ">
                  您只能上传1个.xlsx格式的文件,多余的文件将被覆盖
                </h3>
              </template>
              
            </el-upload>
            <el-button class="ml-3" type="success" @click="submitUploadResource">
                上传至林上鹰眼
            </el-button>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <h1>灾害情况</h1>
            <h2>
              <el-alert
                title="温馨提示：按照参考格式上传数据文件，林上鹰眼会自动帮您保存到数据库中"
                type="warning"
                :closable="false"
                style="font-size: small;">
              </el-alert>
            </h2>
            <el-descriptions
              direction="vertical"
              style="margin-bottom: 10px;"
              :column="5"
              border
            >
              <el-descriptions-item label="日期">2024-11-18</el-descriptions-item>
              <el-descriptions-item label="灾害类型">火灾</el-descriptions-item>
              <el-descriptions-item label="受损森林面积(公顷)">2.00</el-descriptions-item>
              <el-descriptions-item label="灾情概述">本林区东北角处发生了森林火灾，灾情较为严重。</el-descriptions-item>
            </el-descriptions>
            <el-upload
              ref="uploadDisaster"
              action="http://127.0.0.1:5000/uploadDisasterFile"
              :limit="1"
              :on-exceed="handleExceedDisaster"
              :auto-upload="false"
              :data="uploadForest"
            >
              <template #trigger>
                <el-button type="success" plain>选择文件</el-button>
                <h3 style="margin-left: 10px;">
                  您只能上传1个.xlsx格式的文件,多余的文件将被覆盖
                </h3>
              </template>
            </el-upload>
            <el-button class="ml-3" type="success" @click="submitUploadDisaster">
                上传至林上鹰眼
            </el-button>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <h1>森林相册</h1>
            <h2>
              <el-alert
                title="温馨提示：为本林区上传资料图片，单次上传不得超过9张"
                type="warning"
                :closable="false"
                style="font-size: small;">
              </el-alert>
            </h2>
            
            
            <el-upload
              ref="upload"
              v-model:file-list="fileList"
              :action="'http://127.0.0.1:5000/uploadForestImage'"
              list-type="picture-card"
              :on-preview="handlePictureCardPreview"
              :on-remove="handleRemove"
              :limit="9"
              :on-exceed="handleExceed"
              :on-success="handleSuccess"
              :on-error="handleError"
              :before-upload="beforeUpload"
              :auto-upload="false"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
        
            <el-button class="ml-3" type="success" @click="submitUploadForestImage" :loading="uploading" style="margin-top: 10px;">上传至林上鹰眼</el-button>
        
            <el-dialog v-model="dialogVisible">
              <img :src="dialogImageUrl" alt="Preview Image" />
            </el-dialog>
          
          </div>
      
        </div>
     
    </div>

  </template>
  
  <script lang="ts" setup>
  import { ref, reactive, defineProps, defineEmits } from 'vue';
  import { ArrowLeft } from '@element-plus/icons-vue'
  import { normalize } from 'echarts/types/src/scale/helper.js';
  import axios from 'axios';
  import { genFileId } from 'element-plus'
  import type { UploadInstance, UploadProps, UploadRawFile, UploadUserFile } from 'element-plus';
  import { Plus } from '@element-plus/icons-vue';

  // 定义森林属性的接口
  interface ForestProps {
    value: string;
    label: string;
    location: string;
    area: number;
    manager: string;
    intro: string;
  }

  // 定义 props，并使用 ForestProps 接口作为类型注解
  const props = defineProps({
    forestProps: {
      type: Object as PropType<ForestProps | undefined>,
      default: () => ({})
    }
  });

  // 检查 props.forestProps 是否存在，然后解构赋值
  const { value: f_id, label: f_name, location: f_location, area: f_area, manager: f_manager, intro: f_intro } =
  props.forestProps || [];

  // 返回触发事件
  const emit = defineEmits(['back']);
  const handleClick = (event: MouseEvent) => {
    if ((event.target as HTMLElement).classList.contains('text-large')) 
    {
        return; //点击title没有反应
    } else 
    {
        emit('back');
    }
  };

  // 获取气象数据
  const showLoading = ref(false);
  const showWeatherDataBox = ref(false);
  // 声明响应式气象数据
  const w_temperature = ref(null);
  const w_winddirection = ref(null);
  const w_windpower = ref(null);
  const w_humidity = ref(null);
  const w_time = ref(null);

  const fetchWeatherData = async() => {
    showLoading.value = true;
    showWeatherDataBox.value=false;
    //处理地理位置并发送给后端
    const parts = f_location.split('/');
    const loc_last=parts.slice(2).join('/');//一般取最后一个地理区的数据
    const loc_mid=parts[1];//防止最后一个区的数据不存在
    const params = new URLSearchParams();
    params.append('city',loc_last);
    params.append('altcity',loc_mid);
    params.append('f_name',f_name);
    try{
      const response = await axios.post('http://127.0.0.1:5000/get_weather', params,{
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
      });
      if(response.data.status==='success'){
        const weatherData = response.data.weather[0];
        w_temperature.value=weatherData.temperature;
        w_winddirection.value=weatherData.winddirection;
        w_windpower.value=weatherData.windpower;
        w_humidity.value=weatherData.humidity;
        w_time.value = weatherData.time;

        ElNotification({
          title: '更新成功',
          message: '获取气象数据成功，记录已成功添加到林上鹰眼数据库~',
          type: 'success',
        })
      
        showWeatherDataBox.value = true;
      }
    }
    catch(error){
      ElNotification({
          title: '操作失败',
          message: '获取气象数据失败，请稍后再试',
          type: 'error',
      })
    }
    showLoading.value=false;

  }
  // 编辑简介
  const editedIntro =ref('');
  const isEditIntro = ref(false);
  var intro = f_intro;
  const toggleEditIntro = () =>{
    isEditIntro.value = true;
  }
  const submitIntro= async() => {
    
    if(editedIntro.value!=f_intro){
      if(!editedIntro){
        editedIntro="森林管理员尚未添加简介...";
      }
      // 向后端发送更改请求
      try{
        const params = new URLSearchParams();
        params.append('intro',editedIntro.value);
        params.append('id',f_id);

        const response = await axios.post('http://127.0.0.1:5000/setForestInfo',params,{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });     
        if(response.data.status==='success'){
          intro=editedIntro.value;
          ElNotification({
            title: '更新成功',
            message: '修改已成功添加到林上鹰眼数据库中~',
            type: 'success',
          });
        }
      }
      catch(error){      
      }
    }
    isEditIntro.value=false;

        
  }

  const uploadForest=ref({ f_id: f_id , f_name: f_name});
  // 资源数据
  const uploadResource = ref<UploadInstance>()
  const handleExceedResource: UploadProps['onExceed'] = (files) => {
    uploadResource.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    uploadResource.value!.handleStart(file)
  }
  const submitUploadResource = () => {
    uploadResource.value!.submit()
    ElNotification({
      title: '更新成功',
      message: '资源数据成功添加到林上鹰眼数据库~',
      type: 'success',
    });
  }

  // 灾害数据
  const uploadDisaster = ref<UploadInstance>()
  const handleExceedDisaster: UploadProps['onExceed'] = (files) => {
    uploadDisaster.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    uploadDisaster.value!.handleStart(file)
  }
  const submitUploadDisaster = () => {
    uploadDisaster.value!.submit()
    ElNotification({
      title: '更新成功',
      message: '灾害数据成功添加到林上鹰眼数据库~',
      type: 'success',
    });
  }

  //上传森林相册图片
  const fileList = ref<UploadFile[]>([]);
  const dialogImageUrl = ref('');
  const dialogVisible = ref(false);
  const uploading = ref(false);
  
  const handleRemove = (file: UploadFile, files: UploadFile[]) => {
    console.log(file, files);
  };
  
  // 使用 window.URL.createObjectURL 生成预览URL
  const handlePictureCardPreview = (file: UploadFile) => {
    if (!file.url && file.raw) {
      file.url = URL.createObjectURL(file.raw);
    }
    dialogImageUrl.value = file.url;
    dialogVisible.value = true;
  };
  
  const handleExceed = (files: UploadFile[], filesList: UploadFile[]) => {
    ElNotification({
      title: '超出限制',
      message: `限制选择 9 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + filesList.length} 个文件`,
      type: 'warning',
    });
  };
  
  const handleSuccess = (response: any, file: UploadFile) => {
    alert('文件上传成功');
    ElNotification({
      title: '上传成功',
      message: '图片成功添加到林上鹰眼数据库~',
      type: 'success',
    });
  };
  
  const handleError = (err: any, file: UploadFile) => {
    ElNotification({
      title: '上传失败',
      message: '图片添加失败，请稍后重试',
      type: 'error',
    });
  };
  
  const beforeUpload = (file: File) => {
    return true; 
  };
  
  const submitUploadForestImage = async () => {
    if (fileList.value.length === 0) {
      ElNotification({
      title: '上传失败',
      message: '请先选择图片',
      type: 'warning',
    });
      return;
    }
  
    uploading.value = true;
    try {
      for (let file of fileList.value) {
        const formData = new FormData();
        formData.append('files', file.raw);
        //添加森林名称
        formData.append('f_name', f_name);
  
        await axios.post('http://127.0.0.1:5000/uploadForestImage', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      }
      ElNotification({
      title: '上传成功',
      message: '图片成功添加到林上鹰眼数据库~',
      type: 'success',
    });
    } catch (error) {
      ElNotification({
      title: '上传失败',
      message: '上传失败，请稍后重试',
      type: 'error',
    });
      console.error(error);
    } finally {
      uploading.value = false;
      // 无论成功或失败，都清空文件列表
        fileList.value = [];
    }
  };
</script>

<style scoped>
h1{
  font-size: normal;
  font-weight: normal;
  color:black;
  margin-bottom: 5px;
}
h2{
  font-size: small;
  font-weight: normal;
  color:#60a103;
}
h3{
  font-size: xx-small;
  font-weight: normal;
  color:grey;
  margin-top: 10px;
}

</style>