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
              <h2>点击按钮获取本林区的最新气象数据，并更新到林上鹰眼数据库</h2>
              <el-button type="success" style="width: 80px;" v-if="!showLoading" @click="fetchWeatherData">获取数据</el-button>
              <el-button  type="success" loading style="width: 80px;" v-else disabled>Loading</el-button>
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
            <h3 v-if="showWeatherDataBox">*气象数据来源：高德开放平台-Web服务API</h3>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <h1>编辑森林简介</h1>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <h1>编辑资源分布</h1>
            <h2>按照参考格式上传数据文件，林上鹰眼会自动帮您保存到数据库中</h2>
            <el-descriptions
              direction="vertical"
              style="margin-bottom: 10px;"
              :column="5"
              border
            >
              <el-descriptions-item label="资源名称">野猪</el-descriptions-item>
              <el-descriptions-item label="资源类型(植物/动物)">动物</el-descriptions-item>
              <el-descriptions-item label="分布中心经度">123.123</el-descriptions-item>
              <el-descriptions-item label="分布中心纬度">45.45</el-descriptions-item>
              <el-descriptions-item label="分布范围">5</el-descriptions-item>
            </el-descriptions>

            <el-upload
              ref="upload"
              class="upload-demo"
              action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
              :limit="1"
              :on-exceed="handleExceed"
              :auto-upload="false"
            >
              <template #trigger>
                <el-button type="success" plain>选择文件</el-button>
                <h3 style="margin-left: 10px;">
                  您只能上传1个.xlsx格式的文件,多余的文件将被覆盖
                </h3>
              </template>
              
            </el-upload>
            <el-button class="ml-3" type="success" @click="submitUpload">
                上传至林上鹰眼
            </el-button>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <h1>灾害情况</h1>
          </div>
          <el-divider border-style="dashed" />
          <div>
            <h1>森林相册</h1>
            <h2>为本林区上传资料图片,单次上传不得超过9张</h2>
            <el-upload
              v-model:file-list="fileList"
              action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
              list-type="picture-card"
              :on-preview="handlePictureCardPreview"
              :on-remove="handleRemove"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>

            <el-dialog v-model="dialogVisible">
              <img w-full :src="dialogImageUrl" alt="Preview Image" />
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
  import { ElNotification } from 'element-plus';
  import { genFileId } from 'element-plus'
  import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
  import { Plus } from '@element-plus/icons-vue'

  // 定义森林属性的接口
  interface ForestProps {
    value: string;
    label: string;
    location: string;
    area: number;
    manager: string;
  }

  // 定义 props，并使用 ForestProps 接口作为类型注解
  const props = defineProps({
    forestProps: {
      type: Object as PropType<ForestProps | undefined>,
      default: () => ({})
    }
  });

  // 检查 props.forestProps 是否存在，然后解构赋值
  const { value: f_id, label: f_name, location: f_location, area: f_area, manager: f_manager } =
  props.forestProps || {};

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

  const upload = ref<UploadInstance>()

  const handleExceed: UploadProps['onExceed'] = (files) => {
    upload.value!.clearFiles()
    const file = files[0] as UploadRawFile
    file.uid = genFileId()
    upload.value!.handleStart(file)
  }

  const submitUpload = () => {
    upload.value!.submit()
  }


  const fileList = ref<UploadUserFile[]>([]);

  const dialogImageUrl = ref('')
  const dialogVisible = ref(false)

  const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
    console.log(uploadFile, uploadFiles)
  }

  const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
    dialogImageUrl.value = uploadFile.url!
    dialogVisible.value = true
  }
  
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
}

</style>