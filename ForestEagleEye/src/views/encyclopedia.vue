<template>
  <NavigationBar />
  <div class="common-layout">
      <el-container>
          <el-container>
              <el-aside width="250px">
                  <el-scrollbar>
                      <el-menu 
                        :default-active="activeIndex"
                        @select="handleSelect"
                        >
                          <el-menu-item index="1">
                              <template #title>
                              <el-icon><icon-message /></el-icon>概要
                              </template>
                          </el-menu-item>

                          <el-sub-menu index="2">
                              <template #title>
                              <el-icon><icon-menu /></el-icon>数据查询
                              </template>
                              <el-menu-item-group>
                                  <template #title>按国家和地区</template>
                                  <el-menu-item index="2-1">世界森林数据</el-menu-item>
                              </el-menu-item-group>
                              <el-menu-item-group>
                                  <template #title>按森林</template>
                                  <el-menu-item index="2-2">单林区数据</el-menu-item>
                              </el-menu-item-group>
                          </el-sub-menu>

                          <el-menu-item index="3" v-if="role =='林业管理人员' || role == '林业监管人员'">
                              <template #title>
                              <el-icon><icon-menu /></el-icon>百科编辑
                              </template>
                          </el-menu-item>
                      </el-menu>
                  </el-scrollbar>
              </el-aside>
              <el-container>
                  <!--子页面内容-->
                  <el-main>
                    <!--概要-->
                    <div v-if="activeIndex === '1'">
                      <div class="container">
                        <div style="margin-left: 50px; margin-top: 50px;">
                          <h1 style="font-size: x-large; margin-bottom: 10px; color: #60a130;">Forest Encyclopedia</h1>
                          <h2 style="font-size: xx-large; margin-top: 10px;">森林百科</h2>
                        </div>
                        <div style="display: flex; gap: 50px;">
                          <!--世界林区覆盖地图-->
                          <div style="display: flex; flex-direction: column;margin-left:50px;">
                            <div id="world-map" style="width: 800px; height: 400px; border: 1px solid grey;"></div>
                            <text style="font-size: xx-small; color: grey;">全球国家和地区森林覆盖面积(2010~2024) from Global Forest Watch,使用鼠标与数据互动</text>
                          </div>
                          <!--森林百科简介-->
                          <div style="display: flex; flex-direction: column; width: 380px; margin-top: 20px;">
                            <h2 style="font-size: x-large;margin-top: 10px;">我们的森林百科有什么？</h2>
                            <h2 style="font-size: large; margin-top: 5px;">What do we have in Forest Encyclopedia?</h2>
                            <text style="margin-bottom: 10px;line-height: 1.5;">
                              在林上鹰眼的森林百科获取来自世界各个国家和地区、主要林区的森林数据。您可以在数据查询界面进行单点查询、多点比较，并获得精确的可视化结果。
                            </text>
                            <text style="color: grey;line-height: 1.5; font-family: Georgia, 'Times New Roman', Times, serif;">
                              Get global forest data from the Forest Encyclopedia of ForestEagleEye. Query single points, compare multiple, and view accurate visualizations.
                            </text>
                            <el-button class="try-btn" type="success" plain style="margin-top: 20px;"@click="scrolldown">立即体验</el-button>
                          </div>
                        </div>
                        <!--森林百科功能详细介绍-->
                        <div style="margin-left: 50px; margin-top: 50px;">
                          <h2 style="font-size: large; margin-top: 5px;">全球森林资源数据</h2>
                          <h2 style="font-size: large; margin-top: 5px;">全球森林火灾详情</h2>
                          <h2 style="font-size: large; margin-top: 5px;">全球林木生物概况</h2>
                          <h2 style="font-size: large; margin-top: 5px;">主要林区数据详情</h2>
                          <h2 style="font-size: large; margin-top: 5px;">进行数据的可视化比较</h2>
                        </div>

                        <div id="anchorPoint" style="margin-top: 60px; margin-left: 50px; width:93%">
                          <el-carousel :interval="4000" type="card" height="200px">
                            <el-carousel-item v-for="item in 6" :key="item">
                              <h3 text="2xl" justify="center">{{ item }}</h3>
                            </el-carousel-item>
                          </el-carousel>
                        </div>
                      </div>

                    </div>
                    <!--单国家-->
                    <div v-if="activeIndex === '2-1'">单国家和地区查询页面内容</div>


                    <!--单林区-->
                    <div v-if="activeIndex === '2-2'">
                      <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                        <el-select id="forest" v-model="forest" placeholder="请选择待查询的森林" popper-class="dropdown" style="width: 500px;">
                          <el-option v-for="f in forests" 
                          :key="f.value"
                          :label="f.label"
                          :value="f.value"
                          </el-option>
                        </el-select>
                        <el-button type="success" plain style="width: 80px;" @click="searchOneForest">查询</el-button>
                      </div>

                      <div class="container">
                        <el-empty v-if="singleForestNothing===true" description="来到了没有森林的荒原..." />
                        <div v-else="">
                          <label style="margin-bottom: 0px;margin-top: 15px; font-size: small; color: grey">查询结果</label>
                          <el-divider />
                          
                          <el-skeleton v-if="singleForestLoading===true":rows="20" animated />
                          <div v-else="" style="margin-left: 20px;">
                            <!--基本信息和森林相册-->
                            <div style="display: flex; gap: 50px;">
                              <div style="display: block; width: 600px; ">
                                <h1 style="font-size: x-large;">{{sf_name}}</h1>
                                <el-descriptions column='1' style="margin-left: 10px;">
                                  <el-descriptions-item label="森林序号">{{sf_id}}</el-descriptions-item>
                                  <el-descriptions-item label="森林面积">{{sf_area}}</el-descriptions-item>
                                  <el-descriptions-item label="管理机构"><el-tag size="normal" type="success">{{sf_manager}}</el-tag></el-descriptions-item>
                                  <el-descriptions-item label="地理位置">{{sf_location}}</el-descriptions-item>
                                  <el-descriptions-item label="森林简介">{{sf_intro}}</el-descriptions-item>
                                </el-descriptions>
                              </div>
                              <!--森林相册图片轮播-->
                              <el-carousel interval="2000" indicator-position="outside" class="forestImages" style="padding-top: 40px;">
                                <el-carousel-item v-for="(image,index) in sf_images" :key="index">
                                  <img :src="image" style="width: 100%; height: 100%;" alt="Forest Image">
                                </el-carousel-item>
                              </el-carousel>
                            </div>

                            <!--资源分布-->
                            <h2 style="font-size: large;">资源分布</h2>
                            <div ref="resourceMapChart" style="width: 1200px; height: 500px; margin-left: 15px;"></div>
                            <label style="font-size: xx-small; font-weight: normal; color:#60a130; margin-left:20px;">*资源数据来源：林上鹰眼自建数据库</label>
                            <!--气候概况-->
                            <h2 style="font-size: large;">气候概况</h2>
                            <div style="display: flex;">
                              <div ref="weatherChart" style="width: 600px; height: 400px;"></div>
                              <div ref="windChart" style="width: 600px; height: 400px;"></div>
                            </div>
                            <h4 style="">*气象数据来源：高德开放平台-Web服务API</h4>
                            <!--灾害统计-->
                            <h2 style="font-size: large;">灾害统计</h2>
                            <div style="display: flex;">
                              <div ref="disasterRankingChart" style="width: 600px; height: 400px;"></div>
                              <el-table 
                                :data="disasterTableData" 
                                :default-sort="{ prop: 'date', order: 'descending' }"
                                stripe
                                style="width: 600px; height: 350px; padding-top: 50px;">
                                <el-table-column label="日期" prop="date" sortable/>
                                <el-table-column label="类型" prop="type" />
                                <el-table-column label="损失(公顷)" prop="loss" sortable/>
                                <el-table-column type="expand">
                                  <template #default="props">
                                    <div style="margin-left: 15px; margin-bottom: 0px; margin-top: 10px;">
                                      <label style="font-size: normal; font-weight: bold;">灾情详述</label>
                                      <p v-for="(desc, index) in props.row.disaster.desc" :key="index">{{ desc }}</p>
                                    </div>
                                  </template>
                                </el-table-column>
                              </el-table>
                            </div>
                            <h4 style="">*灾害数据来源：林上鹰眼自建数据库</h4>

                          </div>
                          


                        </div>
                      </div>
                      



                      
                    </div>
                    
                    <!--百科编辑-->
                    <div v-if="activeIndex === '3'">
                      <div class="container" >
                        <ForestAddBox v-if="showAddBox" @back="onAddBoxClose"/>
                        <ForestEditBox v-else-if="showEditBox" @back="onEditBoxClose":forestProps="forestProps"/>
                        <div v-else="">
                          <el-table :data="allForestTableData" stripe style="width: 100%; ">
                          <el-table-column fixed="left" prop="value" label="序号" width="200" />
                          <el-table-column prop="label" label="名称" width="200" />
                          <el-table-column prop="location" label="地理位置" width="200" />
                          <el-table-column prop="area" label="占地面积" width="200" />
                          <el-table-column prop="manager" label="管理机构" width="300" />
                          <el-table-column fixed="right" label="操作" min-width="120">
                            <template #default="scope">
                              <el-button
                                link
                                type="success"
                                size="small"
                                @click.prevent="editRow(scope.row)"
                              >
                                编辑
                              </el-button>
                              <el-button
                                link
                                type="info"
                                size="small"
                                @click.prevent="deleteRow(scope.row)"
                              >
                                删除
                              </el-button>
                            </template>
                          </el-table-column>
                        </el-table>
                        <el-button class="mt-4" type="success" plain style="width: 100%" @click="onAddForest">
                          新增森林
                        </el-button>
                        </div>

                        


                      </div>
                    </div>
                  </el-main>
                  <el-footer>&copy; 2024 同济大学·ForestEagleEye·项目开发组. All rights reserved.</el-footer>
              </el-container>
          </el-container>
    </el-container>
  </div>
</template>


<script>
import { ref } from 'vue';
import axios from 'axios';
import NavigationBar from '../components/navbar.vue';
import ForestAddBox from '../components/ForestAddView.vue'
import ForestEditBox from '../components/ForestEditView.vue'
import * as echarts from 'echarts';
import worldJSON from '@/assets/json/world.json';
import chinaMap from '@/assets/json/china.json';
import { ElNotification } from 'element-plus';

export default {
  name: 'encyclopedia',
  components: {
    NavigationBar,
    ForestEditBox,
    ForestAddBox
  },
  data() {
    return {
      role: sessionStorage.getItem('role'),
      activeIndex: '1',
      defaultOpeneds: ['2'], // 默认展开的子菜单
      //概要
      mapdata:[],  //世界地图的数据
      mapInstance: null,  // 地图实例

      //单林区查询
      forests:ref(),
      forest:null,
      singleForestLoading: true,
      singleForestNothing: true,
      sf_name:'',
      sf_area:'',
      sf_location:'',
      sf_manager:'',
      sf_intro:'',
      sf_id:'',
      sf_images:ref([]),
      /* 气候数据 */
      weatherInstance: null,//单林区的天气echarts
      windInstance: null,//单林区的风力echarts
      weatherData: {//单林区的天气数据
        dates: [],
        temperatures: [],
        humidities: [],
        winddirections: [],
        windpowers: [],
      },

      /* 资源数据 */
      resourceData:{
        id: [],
        name: [],
        type: [],
        latitude: [],
        longitude: [],
        radius: []
      },
      resourceMapInstance:null,//资源分布地图实例

      /* 灾害数据 */
      disasterRankingInstance:null,
      disasterRankingCounts:{},//存储灾害类型统计结果
      disasterData:{
        dates:[],
        type:[],
        loss:[],
        desc:[],
      },
      disasterColors: {}, // 初始化颜色映射对象
      disasterTableData: ref([]),


      //百科编辑-编辑详情
      showEditBox:false,
      forestProps:ref([]),

      //百科编辑-创建森林
      showAddBox:false,
      f_name:'',
      f_location:ref(),
      f_area:'',
      f_soilType:'',
      f_manager:'',
      f_intro:'',

      allForestTableData:ref([]),
    };
  },
  mounted(){
    this.drawMap();
    this.fetchAllForestData();
  },
  methods: {
    async handleSelect(index, indexPath) {
      this.activeIndex = index;
      // 根据选择的索引加载相应的数据或执行相应的操作
      switch (index) {
        case '1':// 概要
          this.drawMap();
          break;
        case '2-1':// 单国家和地区
          
          break;
        case '2-2':// 单林区
          this.fetchForest();
          
          break;
        case '3':// 编辑百科
          this.fetchAllForestData();
        break;
      }
    },
    async fetchAllForestData(){
      //向后端请求全部森林数据
      try{    
        const response = await axios.get('http://127.0.0.1:5000/get_all_forests',{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        this.allForestTableData=response.data.forests;
        }
      catch(error){}
    },
    //获取全部森林名称
    async fetchForest(){
      try{
        const response =await axios.get('http://127.0.0.1:5000/get_all_forests');
        this.forests=response.data.forests;
      }catch(error){
        console.error('Error Fetching options:', error);
      }
    },
    async drawMap(){
      //向后端请求地图数据
      try{    
        const response = await axios.get('http://127.0.0.1:5000/get_world_tree_cover_json',{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
      });
      this.mapdata = response.data.datalist;
      }catch(error){
        //失败弹窗数据请求失败
        alert('failed to get map data!');
      }
      if(this.mapdata){
        //若请求数据成功则绘制地图
        this.mapInstance = echarts.init(document.getElementById('world-map'));
        // 注册世界地图的 GeoJSON 数据
        echarts.registerMap('world', worldJSON);
        // 根据 mapdata 中的 value 范围设置 visualMap 的 min 和 max
        const valueMin = Math.min(...this.mapdata.map(item => item.value));
        const valueMax = Math.max(...this.mapdata.map(item => item.value));

        const option = {
          tooltip: {
            trigger: 'item', // 触发类型为数据项图形触发
            formatter: function (params) {
              // 自定义 tooltip 显示内容
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
              color: ['#5B9C4B', '#86C06C', '#B8DCA1', '#F3E1AF'].reverse(), // 颜色渐变
            },
          },
          series: [
            {
              type: 'map',
              mapType: 'world',
              geoIndex: 0,
              data: this.mapdata.map(item => ({
                name: item.name,
                value: item.value
              })),
            }
          ]
        };
        this.mapInstance.setOption(option);
      }//end of drawing map
    },
    async scrolldown(){
      const anchorPoint = document.getElementById('anchorPoint');
      anchorPoint.scrollIntoView({
        behavior:'smooth'
      });
    },
    async onAddForest(){
      this.showAddBox=true;
    },
    async onAddBoxClose(){
      this.showAddBox=false;
      this.fetchAllForestData();
    },
    async onEditBoxClose(){
      this.showEditBox=false;
      this.fetchAllForestData();
    },
    async editRow(forest){
      this.forestProps = forest;
      this.showEditBox=true;
    },
    async deleteRow(forest){
      //获取当前森林
      //向后端发送删除请求
      try{    
        const params= new URLSearchParams;
        params.append('f_id',forest.value);
        const response = await axios.post('http://127.0.0.1:5000/delete_forest', params,{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        //这里的ElNotification标红不是因为报错，是因为全局导入的el-ui这里无需再写，编译器的问题，不用管可以直接跑
        ElNotification({
          title: '删除成功',
          message: response.data.message,
          type: 'success',
        })
        this.fetchAllForestData();
      }
      catch(error){
        //这里的ElNotification标红不是因为报错，是因为全局导入的el-ui这里无需再写，编译器的问题，不用管可以直接跑
        ElNotification({
          title: '删除失败',
          message: response.data.message,
          type: 'error',
        })
      }
    },
    async searchOneForest(){
      
      //检查forest的值是否为空
      this.singleForestNothing=false;

      try{    
        const params= new URLSearchParams;
        params.append('f_id',this.forest);

        const response = await axios.post('http://127.0.0.1:5000/searchOneForest',params,{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        //获取基本信息
        const singleForest = response.data.baseInfo[0];
        this.sf_id=singleForest.sf_id;
        this.sf_area=singleForest.sf_area;
        this.sf_location=singleForest.sf_location;
        this.sf_manager=singleForest.sf_manager;
        this.sf_name=singleForest.sf_name;
        this.sf_intro=singleForest.sf_intro;

        //获取森林相册图片
        this.sf_images=response.data.sf_images;

        //获取动态信息-天气
        this.weatherData.dates=response.data.weather.dates;
        this.weatherData.temperatures=response.data.weather.temperatures;
        this.weatherData.humidities=response.data.weather.humidities;
        this.weatherData.winddirections=response.data.weather.winddirections;
        this.weatherData.windpowers=response.data.weather.windpowers;
      
        //获取动态信息-资源
        this.resourceData.id = response.data.resource.id;
        this.resourceData.name = response.data.resource.name;
        this.resourceData.type = response.data.resource.type;
        this.resourceData.latitude = response.data.resource.latitude;
        this.resourceData.longitude = response.data.resource.longitude;
        this.resourceData.radius = response.data.resource.radius;

        //获取动态信息-灾害
        this.disasterData.dates = response.data.disaster.dates;
        this.disasterData.type = response.data.disaster.type;
        this.disasterData.loss = response.data.disaster.loss;
        this.disasterData.desc = response.data.disaster.desc;

        //绘图
        this.initResourceMapChart();

        this.initTemperatureHumidityChart();
        this.initWindChart();

        this.initDisasterRankingChart();
        this.initDisasterTable();

        }
      catch(error){}

      //设置不需要loading
      this.singleForestLoading=false;
    },
    async initTemperatureHumidityChart() {
      this.weatherInstance = echarts.init(this.$refs.weatherChart);
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          },
          formatter: function (params) {
            let result = params[0].name + '<br/>';
            params.forEach(function (item) {
              if (item.seriesName === '温度') {
                result += item.seriesName + ': ' + item.value[1] + ' °C<br/>';
              } else if (item.seriesName === '湿度') {
                result += item.seriesName + ': ' + item.value[2] + ' %<br/>';
              }
            });
            return result;
          }
        },
        legend: {
          data: ['温度', '湿度']
        },
        xAxis: {
          type: 'category',
          data: this.weatherData.dates
        },
        yAxis: [
          {
            type: 'value',
            name: '温度',
            position: 'left',
            axisLabel: {
              formatter: '{value} °C'
            }
          },
          {
            type: 'value',
            name: '湿度',
            position: 'right',
            axisLabel: {
              formatter: '{value} %'
            }
          }
        ],
        series: [
          {
            name: '温度',
            type: 'line',
            yAxisIndex: 0, // 指定使用第一个y轴（温度）
            data: this.weatherData.temperatures
          },
          {
            name: '湿度',
            type: 'line',
            yAxisIndex: 1, // 指定使用第二个y轴（湿度）
            data: this.weatherData.humidities
          }
        ]
      };
    this.weatherInstance.setOption(option);
    },
    async initWindChart() {
      this.windInstance = echarts.init(this.$refs.windChart);
      const windPowers = this.weatherData.windpowers.map(this.mapWindpowerToValue);

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          formatter: (params) => {
            const dataIndex = params[0].dataIndex;
            return `${this.weatherData.dates[dataIndex]}<br>${this.weatherData.winddirections[dataIndex]}: ${windPowers[dataIndex]}`;
          }
        },
        xAxis: {
          type: 'category',
          data: this.weatherData.dates,
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}'
          }
        },
        series: [{
          name: '风力',
          type: 'line',
          smooth: true, // 使线条平滑
          data: windPowers,
          markPoint: {
            data: this.weatherData.dates.map((date, index) => ({
              coord: [date, windPowers[index]],
              label: {
                formatter: () => this.weatherData.winddirections[index], // 直接使用原始风向值
                color: '#ffffff',
              },
            }))
          }
        }]
      };

      this.windInstance.setOption(option);
    },
    mapWindpowerToValue(power) {
      const powerMap = {
        '≤3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8
      };
      return powerMap[power] || 3; // 默认值为0
    },
    
    async initDisasterRankingChart(){
      this.disasterRankingInstance = echarts.init(this.$refs.disasterRankingChart);
      //计算灾害类型计数
      this.calDisasterCounts();
      //图表配置
      const types = Object.keys(this.disasterRankingCounts).sort((a, b) => this.disasterRankingCounts[b] - this.disasterRankingCounts[a]);
      const counts = Object.values(this.disasterRankingCounts);
      const colors = this.disasterColors;

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: 'category',
          data: types,
          inverse: true // 反转Y轴，使得条形图从上到下排列
        },
        series: [
          {
            name: '数量',
            type: 'bar',
            label: {
              show: true,
              position: 'right'
            },
            data: counts.map((count, index) => ({
              value: count,
              itemStyle: {
                color: colors[index] // 为每个条形分配颜色
              }
            }))
          }
        ]
      };

      this.disasterRankingInstance.setOption(option);
    },
    calDisasterCounts(){
      //为每种灾害类型分配颜色
      const colormap = {
        "火灾": "#FFC0CB",
        "极端天气": "#F0E68C",
        "干旱": "#FFD700",
        "土壤侵蚀": "#87CEFA",
        "酸雨": "#B0E0E6",
        "地质灾害": "#FF6347",
        "生物灾害": "#FF69B4",
        "人为灾害": "#ADD8E6"
      };
      
      this.disasterRankingCounts={};

      this.disasterData.type.forEach(
        type=>{
          if(this.disasterRankingCounts[type]){
            this.disasterRankingCounts[type]++;
          }else{
            this.disasterRankingCounts[type]=1;
          }
          this.disasterColors[type] = colormap[type]; // 为每种灾害类型分配固定颜色
        }
      );
    },

    initDisasterTable(){
      //清空上次计数
      this.disasterTableData=[];
      //本次计数
      const maxLength = Math.max(this.disasterData.dates.length, this.disasterData.type.length, this.disasterData.loss.length, this.disasterData.desc.length)
      for (let i = 0; i < maxLength; i++) {
        this.disasterTableData.push({
          date: this.disasterData.dates[i] || '',
          type: this.disasterData.type[i] || '',
          loss: this.disasterData.loss[i] || 0,
          disaster: {
            dates: [this.disasterData.dates[i] || ''],
            desc: [this.disasterData.desc[i] || ''],
            loss: [this.disasterData.loss[i] || 0],
            type: [this.disasterData.type[i] || '']
          }
        })
      }
    },

    async initResourceMapChart(){
      this.resourceMapInstance = echarts.init(this.$refs.resourceMapChart);
      echarts.registerMap('china',chinaMap);//注册中国地图

      const option = {
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            const type = params.value[2] ? params.value[2].type : '未知类型';
            const radius = params.value[2] ? params.value[2].radius : '未知半径';
            return params.name + '<br>类型: ' + type + '<br>分布半径: ' + radius +'Km';
          }
        },
        series: [
          {
            name: '资源分布',
            type: 'scatter',
            coordinateSystem: 'geo',
            data: this.resourceData.id.map((item, index) => {
              return {
                name: this.resourceData.name[index],
                value: [this.resourceData.longitude[index], this.resourceData.latitude[index], {
                  type: this.resourceData.type[index],
                  radius: this.resourceData.radius[index]
                }]
              };
            }),
            symbolSize: function (val) {
              return val[2].radius / 10;
            },
            label: {
              normal: {
                formatter: '{b}',
                position: 'right',
                show: true
              },
              emphasis: {
                show: true
              }
            },
            itemStyle: {
              normal: {
                color: function (params) {
                  const typeColor = {
                    '动物': '#ddb926',
                    '植物': '#149bdf'
                  };
                  return typeColor[params.value[2] ? params.value[2].type : '未知类型'] || '#149bdf';
                }
              }
            }
          }
        ],
        geo: {
          map: 'china',
          roam: true,
          label: {
            emphasis: {
              show: false
            }
          },
          silent: true,
          zoom: 4 // 初始缩放比例400%
        }
      };
    this.resourceMapInstance.setOption(option);
  },
}};
</script>

<style scoped>
.common-layout{
  padding-top: 50px;
  background-color: #F0F2F5;
}
.el-scrollbar{
  background-color: white;
  position:fixed;
  width: 250px;
}
.el-menu-item:hover{
  background-color: rgba(149, 242, 4, 0.1); 
}
.el-menu-item.is-active{
  color:#60a103;
}
.el-footer{
  background-color: transparent;
  color: #ababab;
  text-align: center;
  bottom: 0;
  font-size:xx-small;
}
.dropdown {
  background-color: #fff;
  color: #333;
  font-size: 14px;
  padding: 8px 12px;
}

.dropdown {
    box-sizing: border-box;
    z-index: 99999 !important;

    box-shadow: 0px 0px 78px rgba(149, 242, 4, 0.1) inset;
    .el-select-dropdown__item {
      color: grey;
    }

    .el-select-dropdown__item.hover,
    .el-select-dropdown__item:hover {
        background-color: rgba(149, 242, 4, 0.01);
        box-shadow: 0px 0px 78px rgba(149, 242, 4, 0.1) inset;
        color: #60a103;
    }
}


.container{
  background-color: white;
  width:95%;
  margin-bottom: 20px;
  padding:10px 40px 30px 40px;
}
.try-btn{
  color:#60a103;
  border: 1px solid#60a103;
}
.try-btn:hover{
  background-color:#60a103;
  color:white;
}
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.forestImages{
  width:600px;
}

h4{
  font-size: xx-small;
  font-weight: normal;
  color:#60a130;
  margin-top: -20px;
  margin-left:20px;
}
</style>