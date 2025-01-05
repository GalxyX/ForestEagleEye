<script setup>
import { onMounted, ref, watch } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';
import worldJSON from '@/assets/json/world.json';


// tab索引
const activeTab = ref('treeCover');

const treeCover_radio = ref(1);// 世界林木覆盖选择【增长】【损失】
const primevalTree_radio = ref(1);// 世界原生林选择【覆盖】【损失】
const forestFire_radio = ref(1);// 森林火灾选择【数量】【损失】
const organicCarbon_radio = ref(1);//土壤有机碳选择【总数】【密度】
const biomass_radio = ref(1);//世界存活林木生物量【生物量】【二氧化碳量】




// 地图数据
const mapData = ref([]);
const mapContainer = ref(null);
const mapInstance = ref(null);

onMounted(() => {
    fetchMapData(activeTab.value);
    echarts.registerMap('world', worldJSON);
});

//依据tab索引和radio动态向后端请求地图数据
watch([
    activeTab,
    treeCover_radio,
    primevalTree_radio,
    forestFire_radio,
    organicCarbon_radio,
    biomass_radio
], ([new_activeTab]) => {
    fetchMapData(new_activeTab);
});

const fetchMapData = async (activeTab) => {
    if (activeTab === 'treeCover') {//林木覆盖率
        try {
            const response = await axios.get('http://127.0.0.1:5000/fetchWorldTreeCover', {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });
            if (treeCover_radio.value === 1) {//增长
                mapData.value = response.data.gain;
                drawMap(['#5B9C4B', '#86C06C', '#B8DCA1', '#F3E1AF']);
            }
            else if (treeCover_radio.value === 2) {//损失
                const selectedYearData = response.data.loss.find(item => item.year === year.value);
                mapData.value = selectedYearData.datalist;
                drawMap(['#5B9C4B', '#86C06C', '#B8DCA1', '#F3E1AF']);
            }

        }
        catch (error) { alert('failed to fetch map data!'); }
    }
    else if (activeTab === 'primevalTree') {//原生林
        try {
            const response = await axios.get('http://127.0.0.1:5000/fetchWorldPrimevalTree', {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });
            if (primevalTree_radio.value === 1) {//覆盖
                mapData.value = response.data.cover;
                drawMap(['#AFB428', '#F0F4C3', '#CDDC39', '#FFC107']);
            }
            else if (primevalTree_radio.value === 2) {//损失
                mapData.value = response.data.loss;
                drawMap(['#AFB428', '#F0F4C3', '#CDDC39', '#FFC107']);
            }
        }
        catch (error) { alert('failed to fetch map data!'); }
    }
    else if (activeTab === 'organicCarbon') {//土壤有机碳
        try {
            const response = await axios.get('http://127.0.0.1:5000/fetchWorldOrganicCarbon', {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });
            if (organicCarbon_radio.value === 1) {//总数
                mapData.value = response.data.total;
                drawMap(['#00BCD4', '#B3E5FC', '#ffffff']);
            }
            else if (organicCarbon_radio.value === 2) {//密度
                mapData.value = response.data.density;
                drawMap(['#00BCD4', '#B3E5FC', '#ffffff']);
            }
        }
        catch (error) { alert('failed to fetch map data!'); }
    }
    else if (activeTab === 'ForestFire') {//森林火灾
        try {
            const response = await axios.get('http://127.0.0.1:5000/fetchWorldForestFire', {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });
            if (forestFire_radio.value === 1) {//数量
                const selectedYearData = response.data.count.find(item => item.year === year.value);
                mapData.value = selectedYearData.datalist;
                drawMap(['#AFB42B', '#F0F4C3', '#CDDC39', '#FFC107']);
            }
            else if (forestFire_radio.value === 2) {//损失
                const selectedYearData = response.data.loss.find(item => item.year === year.value);
                mapData.value = selectedYearData.datalist;
                drawMap(['#AFB42B', '#F0F4C3', '#CDDC39', '#FFC107']);
            }
        }
        catch (error) { alert('failed to fetch map data!'); }
    }
    else if (activeTab === 'BiomassCO2') {//生物量和二氧化碳
        try {
            const response = await axios.get('http://127.0.0.1:5000/fetchWorldBiomass', {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });
            if (biomass_radio.value === 1) {
                mapData.value = response.data.biomass;
                drawMap(['#AFB42B', '#F0F4C3', '#CDDC39', '#FFC107']);
            }
            else if (biomass_radio.value === 2) {
                mapData.value = response.data.co2;
                drawMap(['#AFB42B', '#F0F4C3', '#CDDC39', '#FFC107']);
            }
        }
        catch (error) { alert('failed to fetch map data!'); }
    }

}

const drawMap = async (colormap) => {
    mapInstance.value = echarts.init(mapContainer.value);
    if (mapData.value) {
        //请求成功则绘图
        const valueMin = Math.min(...mapData.value.map(item => item.value));
        const valueMax = Math.max(...mapData.value.map(item => item.value));

        const option = {
            tooltip: {
                trigger: 'item',
                formatter: function (params) {
                    return `${params.name}: ${params.value}`;
                }
            },
            visualMap: {
                min: valueMin,
                max: valueMax,
                calculable: false,
                left: '70px',
                top: '210px',
                inRange: {
                    color: colormap.reverse(), // 颜色渐变
                },
            },
            series: [
                {
                    type: 'map',
                    mapType: 'world',
                    geoIndex: 0,
                    data: mapData.value.map(
                        item => ({
                            name: item.name,
                            value: item.value
                        })
                    ),
                    geo: {
                        zoom: 5
                    }
                }
            ]
        };
        mapInstance.value.setOption(option, true, false);
    }
}

const year = ref(2023);
const years = [
    { "value": 2001, "label": "2001" },
    { "value": 2002, "label": "2002" },
    { "value": 2003, "label": "2003" },
    { "value": 2004, "label": "2004" },
    { "value": 2005, "label": "2005" },
    { "value": 2006, "label": "2006" },
    { "value": 2007, "label": "2007" },
    { "value": 2008, "label": "2008" },
    { "value": 2009, "label": "2009" },
    { "value": 2010, "label": "2010" },
    { "value": 2011, "label": "2011" },
    { "value": 2012, "label": "2012" },
    { "value": 2013, "label": "2013" },
    { "value": 2014, "label": "2014" },
    { "value": 2015, "label": "2015" },
    { "value": 2016, "label": "2016" },
    { "value": 2017, "label": "2017" },
    { "value": 2018, "label": "2018" },
    { "value": 2019, "label": "2019" },
    { "value": 2020, "label": "2020" },
    { "value": 2021, "label": "2021" },
    { "value": 2022, "label": "2022" },
    { "value": 2023, "label": "2023" }
]

const searchOneYear = async () => {
    fetchMapData(activeTab.value);
}
</script>

<template>
    <el-tabs type="border-card" v-model="activeTab">
        <el-tab-pane label="世界林木覆盖" name="treeCover">
            <el-alert title="小知识：林木覆盖是指地球上被林木覆盖的总面积，通常以百分比或平方公里为单位来表示。它反映了全球森林资源的分布情况和森林生态系统在全球范围内的覆盖程度。" type="warning"
                :closable="false" style="font-size: small;width: 1250px;">
            </el-alert>
            <el-radio-group v-model="treeCover_radio" class="treeCover-radio-group">
                <el-radio :value="1">世界林木覆盖增长</el-radio>
                <el-radio :value="2">世界林木覆盖损失</el-radio>
            </el-radio-group>
            <div v-if="treeCover_radio === 1">
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
            <div v-if="treeCover_radio === 2">
                <div style="display: flex; gap: 10px;">
                    <el-select v-model="year" placeholder="请选择年份" style="width: 485px" popper-class="dropdown">
                        <el-option v-for="item in years" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                    <el-button type="success" plain style="width: 80px;" @click="searchOneYear">查询</el-button>
                </div>
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
        </el-tab-pane>
        <el-tab-pane label="世界原生林" name="primevalTree">
            <el-alert title="小知识：原生林是指未经人为干扰或经过长期自然恢复后，保持自然演替过程和生态结构完整的森林。它具有丰富的生物多样性、稳定的生态系统功能和独特的自然景观特征。"
                type="warning" :closable="false" style="font-size: small;width: 1250px;">
            </el-alert>
            <el-radio-group v-model="primevalTree_radio" class="primevalTree-radio-group">
                <el-radio :value="1">世界原生林覆盖</el-radio>
                <el-radio :value="2">世界原生林损失</el-radio>
            </el-radio-group>
            <div v-if="primevalTree_radio === 1">
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
            <div v-if="primevalTree_radio === 2">
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
        </el-tab-pane>
        <el-tab-pane label="世界土壤有机碳" name="organicCarbon">
            <el-alert title="小知识：土壤有机碳是指土壤中以有机形式存在的碳元素，主要来源于植物残体、动物遗骸和微生物的代谢产物。它是土壤有机质的重要组成部分，对土壤肥力和生态系统碳循环具有重要影响。"
                type="warning" :closable="false" style="font-size: small; width: 1250px;">
            </el-alert>
            <el-radio-group v-model="organicCarbon_radio" class="organicCarbon-radio-group">
                <el-radio :value="1">土壤有机碳分布</el-radio>
                <el-radio :value="2">土壤有机碳密度</el-radio>
            </el-radio-group>
            <div v-if="organicCarbon_radio === 1">
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
            <div v-if="organicCarbon_radio === 2">
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>

        </el-tab-pane>
        <el-tab-pane label="世界森林火灾" name="ForestFire">
            <el-alert title="小知识：森林火灾是指在森林中发生的火灾，通常由自然因素或人为因素引起。它会导致森林植被的破坏、生物多样性的损失以及土壤和水文条件的改变。" type="warning"
                :closable="false" style="font-size: small;width: 1250px;">
            </el-alert>
            <el-radio-group v-model="forestFire_radio" class="forestFire-radio-group">
                <el-radio :value="1">世界森林火灾数量</el-radio>
                <el-radio :value="2">世界森林火灾损失</el-radio>
            </el-radio-group>
            <div v-if="forestFire_radio === 1">
                <el-select v-model="year" placeholder="请选择年份" style="width: 485px" popper-class="dropdown">
                    <el-option v-for="item in years" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
                <el-button type="success" plain style="width: 80px;" @click="searchOneYear">查询</el-button>
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
            <div v-if="forestFire_radio === 2">
                <el-select v-model="year" placeholder="请选择年份" style="width: 485px" popper-class="dropdown">
                    <el-option v-for="item in years" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
                <el-button type="success" plain style="width: 80px;" @click="searchOneYear">查询</el-button>
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
        </el-tab-pane>
        <el-tab-pane label="世界存活林木生物量" name="BiomassCO2">
            <el-alert title="小知识：林木生物量是指森林中所有林木的总重量，通常以干重（去除水分后的重量）来计算。它反映了森林生态系统中林木的生长状况和生产力水平。" type="warning"
                :closable="false" style="font-size: small;width: 1250px;">
            </el-alert>
            <el-radio-group v-model="biomass_radio" class="biomass-radio-group">
                <el-radio :value="1">世界存活林木生物量</el-radio>
                <el-radio :value="2">世界存活林木二氧化碳吸收量</el-radio>
            </el-radio-group>
            <div v-if="biomass_radio === 1">
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
            <div v-if="biomass_radio === 2">
                <div ref="mapContainer" style="width: 1200px; height: 500px;"></div>
            </div>
        </el-tab-pane>
    </el-tabs>
    <h3>*数据来源：Global Forest Watch，使用鼠标与数据互动</h3>
</template>


<style>
.el-select-dropdown__item.selected {
    color: green !important;
}

.dropdown {
    background-color: #fff;
    color: #333;
    font-size: 14px;
    padding: 8px 12px;
    box-sizing: border-box;
    z-index: 99999 !important;
}

.dropdown .el-select-dropdown__item {
    color: grey;
}

.dropdown .el-select-dropdown__item.hover,
.dropdown .el-select-dropdown__item:hover {
    background-color: rgba(149, 242, 4, 0.01);
    box-shadow: 0px 0px 78px rgba(149, 242, 4, 0.1) inset;
    color: #60a103;
}

h3 {
    font-size: xx-small;
    font-weight: normal;
    color: grey;
    margin-bottom: 10px;
}

::v-deep .el-tabs__item.is-active {
    color: red;
    opacity: 1;
}
</style>