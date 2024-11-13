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
      >
        <el-descriptions-item label="气候概况">{{f_id}}</el-descriptions-item>
        <el-descriptions-item label="资源分布">{{f_id}}</el-descriptions-item>
        <el-descriptions-item label="植被覆盖">{{f_id}}</el-descriptions-item>
        <el-descriptions-item label="历史文化">{{f_id}}</el-descriptions-item>
        <el-descriptions-item label="灾害情况">{{f_id}}</el-descriptions-item>
        <el-descriptions-item label="野生动物">{{f_id}}</el-descriptions-item>
        <el-descriptions-item label="经济价值">{{f_id}}</el-descriptions-item>
      </el-descriptions>
        
     
    </div>

  </template>
  
  <script lang="ts" setup>
  import { ref, reactive, defineProps, defineEmits } from 'vue';
  import { ArrowLeft } from '@element-plus/icons-vue'
import { normalize } from 'echarts/types/src/scale/helper.js';



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
  
</script>