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
                                  <el-menu-item index="2-1">单国家和地区查询</el-menu-item>
                                  <el-menu-item index="2-2">多国家和地区比较</el-menu-item>
                              </el-menu-item-group>
                              <el-menu-item-group>
                                  <template #title>按森林</template>
                                  <el-menu-item index="2-3">单林区查询</el-menu-item>
                                  <el-menu-item index="2-4">多林区比较</el-menu-item>
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
                    <!--多国家-->
                    <div v-if="activeIndex === '2-2'">多国家和地区比较页面内容</div>
                    <!--单林区-->
                    <div v-if="activeIndex === '2-3'">单林区查询页面内容</div>
                    <!--多林区-->
                    <div v-if="activeIndex === '2-4'">多林区比较页面内容</div>
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
import { useRouter } from 'vue-router';


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
      mapdata:[],  //世界地图的数据
      mapInstance: null,  // 地图实例

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
        case '2-2':// 多国家和地区
          
          break;
        case '2-3':// 单林区
          
          break;
        case '2-4':// 多林区
          
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
</style>