<template>
    <div style="display: flex; gap: 10px;">
        <CountrySelectbox @select-change="handleSelectChange" />
        <el-button type="success" plain style="width: 80px;" @click="searchOneCountry">查询</el-button>
    </div> 
    <div v-if="isEmpty==true">
        <el-empty description="来到了没有森林的荒原..." />
    </div>
    <div v-else style="margin-left: 15px; margin-top: 30px;">
        <el-row>
            <el-col :span="6"><el-statistic title="过去10年林木覆盖增长(公顷²)" :value=tree_cover_gain /></el-col>
            <el-col :span="6"><el-statistic title="过去10年原生林覆盖面积(公顷²)" :value=primeval_tree_cover /></el-col>
            <el-col :span="6"><el-statistic title="过去10年原生林面积损失(公顷²)" :value=primeval_tree_loss /></el-col>
            <el-col :span="6"><el-statistic title="过去10年土壤有机碳总量(kg)" :value=organic_carbon_total /></el-col>
            <el-col :span="6"><el-statistic title="过去10年土壤有机碳密度(kg/m²)" :value=organic_carbon_density /></el-col>
            <el-col :span="6"><el-statistic title="过去10年林木生物量(kg)" :value=biomass /></el-col>
            <el-col :span="6"><el-statistic title="过去10年林木二氧化碳吸收量(kg)" :value=co2 /></el-col>
        </el-row>
        <div class='charts'>
            <div v-if="tree_cover_year_loss" ref="TreeCoverYearLoss" style="width: 450px; height:400px;"></div>
            <div v-if="forest_fire_count" ref="ForestFireCount" style="width: 450px; height:400px;"></div>
            <div v-if="forest_fire_loss" ref="ForestFireLoss" style="width: 450px; height:400px;"></div>
        </div>
        <h3>*数据来源：Global Forest Watch, 所有数据截至2024年</h3>
    </div>
    
    
    
    
    
    
</template>


<script>
import { ref } from 'vue';
import axios from 'axios';
import CountrySelectbox from '../components/countrySelectbox.vue';
import * as echarts from 'echarts';

export default{
    name: 'encyclopedia',
    components: {
        CountrySelectbox,
    },
    data(){
        return{
            iso:'CHN',

            isLoading: false,
            isEmpty:true,

            tree_cover_gain: 0,
            tree_cover_year_loss:[],
            primeval_tree_cover:0,
            primeval_tree_loss:0,
            organic_carbon_total:0,
            organic_carbon_density:0,
            forest_fire_count:[],
            forest_fire_loss:[],
            biomass:0,
            co2:0,

            //echarts实例化
            tree_cover_year_loss_Instance:null,
            forest_fire_count_Instance:null,
            forest_fire_loss_Instance:null,
        }
    },
    methods:{
        async searchOneCountry(){
            this.isEmpty = false;
            try{
                const params= new URLSearchParams;
                params.append('iso',this.iso);
                const response = await axios.post('http://127.0.0.1:5000/fetchSingleCountryAllForestData',params,{
                    headers: {'Content-Type': 'application/x-www-form-urlencoded',},
                });
                this.tree_cover_gain = response.data.tree_cover_gain || '数据暂无';
                this.tree_cover_year_loss = response.data.tree_cover_year_loss || [];
                this.primeval_tree_cover = response.data.primeval_tree_cover || '数据暂无';
                this.primeval_tree_loss = response.data.primeval_tree_loss || '数据暂无';
                this.organic_carbon_total = response.data.organic_carbon_total || '数据暂无';
                this.organic_carbon_density = response.data.organic_carbon_density || '数据暂无';
                this.forest_fire_count = response.data.forest_fire_count || [];
                this.forest_fire_loss = response.data.forest_fire_loss|| [];
                this.biomass = response.data.biomass || '数据暂无';
                this.co2 = response.data.co2 || '数据暂无';

                this.drawTreeCoverYearLoss();
                this.drawForestFireCount();
                this.drawForestFireLoss();
            }
            catch(error){}            
        },
        async handleSelectChange(value){
            //接收子组件countrySelectbox选中的ISO
            this.iso = value;
        },
        async drawTreeCoverYearLoss(){
            if(this.tree_cover_year_loss){
                this.tree_cover_year_loss_Instance = echarts.init(this.$refs.TreeCoverYearLoss);
                const year = this.tree_cover_year_loss.map(item => item.year);
                const loss = this.tree_cover_year_loss.map(item => item.loss);
                const option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                    },
                    xAxis: {
                        type: 'category',
                        data: year
                    },
                    yAxis: {
                        type: 'value',
                        name: '林木覆盖损失'
                    },
                    series: [{
                        name: '损失',
                        type: 'bar',
                        data: loss,
                        itemStyle: {color: '#60a130'}
                    }]
                };
                this.tree_cover_year_loss_Instance.setOption(option);
            }
        },
        async drawForestFireCount(){
            if(this.forest_fire_count){
                this.forest_fire_count_Instance = echarts.init(this.$refs.ForestFireCount);
                const year = this.forest_fire_count.map(item => item.year);
                const count = this.forest_fire_count.map(item => item.count);
                const option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                    },
                    xAxis: {
                        type: 'category',
                        data: year
                    },
                    yAxis: {
                        type: 'value',
                        name: '森林火灾次数'
                    },
                    series: [{
                        name: '次数',
                        type: 'bar',
                        data: count,
                        itemStyle: {color: '#60a130'}
                    }]
                };
                this.forest_fire_count_Instance.setOption(option);
            }
        },
        async drawForestFireLoss(){
            if(this.forest_fire_loss){
                this.forest_fire_loss_Instance = echarts.init(this.$refs.ForestFireLoss);
                const year = this.forest_fire_loss.map(item => item.year);
                const loss = this.forest_fire_loss.map(item => item.loss);

                const option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                    },
                    xAxis: {
                        type: 'category',
                        data: year
                    },
                    yAxis: {
                        type: 'value',
                        name: '森林火灾损失'
                    },
                    series: [{
                        name: '损失',
                        type: 'bar',
                        data: loss,
                        itemStyle: {color: '#60a130'}
                    }]
                };
                this.forest_fire_loss_Instance.setOption(option);
            }
        },
    }
}


</script>


<style>
h3{
  font-size: xx-small;
  font-weight: normal;
  color:grey;
  margin-top:-20px;
}
.charts{
    display: flex;
}
</style>