<template>
     <el-page-header :icon="ArrowLeft" @click="handleClick" style="margin-top: 5px;">
        <template #content>
        <span class="text-large font-600 mr-3"> 编辑详情 </span>
        </template>
    </el-page-header>
    <el-divider></el-divider>


    <div>
      <!-- 创建和编辑森林的表单 -->
      <text>森林ID={{props.forestID}}</text>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, reactive, defineProps, defineEmits } from 'vue';
  import { ArrowLeft } from '@element-plus/icons-vue'


  const props = defineProps({
    forestID: String,
    // 这里可以继续定义其他可能需要接收的Props属性
});

// 此时就可以在子组件中使用props.forestID来访问接收到的forestID值了
    console.log(props.forestID);
  // 定义可以触发的事件
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