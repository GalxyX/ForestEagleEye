# ForestEagleEye

林上鹰眼——基于 MySQL 的一站式森林环境资源与信息平台
> ForestEagleEye — A One-Stop Forest Environmental Resources and Information Platform Based on MySQL

<!-- PROJECT SHIELDS -->
 
## 目录

- [上手指南](#上手指南)
  - [开发前的配置要求](#开发前的配置要求)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [开发的架构](#开发的架构)
- [部署](#部署)
- [使用到的框架](#使用到的框架)
- [贡献者](#贡献者)
- [版本控制](#版本控制)
- [作者](#作者)
- [其他文件](#其他文件)

### 上手指南

###### 项目介绍
本项目设计并实现了“林上鹰眼”森林环境资源监控网站。
该系统充分利用现代信息技术手段，通过集成实时数据采集、存储与分析功能，
极大提升了森林资源监控与管理效率，支持科学研究与政策决策的制定，并通过
增强公众环保意识，推动社会对森林保护的重视与行动。项目系统采用 Flask 框
架与 MySQL 数据库构建，前端提供直观且用户友好的网页界面，后端则通过强
大的数据处理能力支持全球及本地森林资源和环境数据的实时收集与分析。系统
通过为不同角色（普通用户、林业从业人员、林业管理人员和林业局监管人员）
提供定制化功能模块，包括森林资源查询、林业活动规划与审批、互动交流论坛
以及智能 AI 问答等，确保各类用户能够根据自身需求高效操作。  
> This project designs and implements the "ForestEagleEye" forest environmental resource monitoring website. The system leverages modern information technology to integrate real-time data collection, storage, and analysis, significantly enhancing the efficiency of forest resource monitoring and management. It supports scientific research and policy-making while raising public environmental awareness and promoting societal engagement in forest protection. Built with the Flask framework and MySQL database, the system offers an intuitive, user-friendly web interface on the front end and robust data processing capabilities on the back end for real-time global and local forest resource and environmental data collection and analysis. Customized functional modules for different roles (general users, forestry practitioners, managers, and regulatory personnel) include forest resource queries, forestry activity planning and approval, interactive forums, and intelligent AI Q&A, ensuring efficient operation according to user needs.

###### 开发前的配置要求

1. xxxxx x.x.x
2. xxxxx x.x.x

###### **安装步骤**

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo

```sh
git clone https://github.com/shaojintian/Best_README_template.git
```

### 文件目录说明
我们采用vue.js的前端框架，尽可能做到前端界面的组件化。在项目的文件结构中，`/assets`是项目运行所必须的文件，`/components`是我们封装好的组件，`/views`是主要界面。  
整个项目的文件目录结构如下：
> We utilize the Vue.js front-end framework, striving to achieve a component-based front-end interface. In the project's file structure, the `/assets` directory contains essential files required for the project's operation, the `/components` directory houses our encapsulated components, and the `/views` directory comprises the main interfaces.  
The overall file directory structure of the project is as follows:
```
FORESTEAGLEEYE\SRC
│ App.vue
│ main.ts
│
├─assets
│ ├─data
│ │ AMap_adcode_citycode.xlsx
│ │ biomass.csv
│ │ fire_count.csv
│ │ fire_loss.csv
│ │ iso_metadata.csv
│ │ primeval_tree_cover.csv
│ │ primeval_tree_loss.csv
│ │ soil_organic_carbon.csv
│ │ treecover_extent_2010_by_region__ha.csv
│ │ treecover_gain.csv
│ │ treecover_loss_in_primary_forests_2001_tropics_only__ha.csv
│ │ treecover_loss_year.csv
│ │
│ └─json
│ china.json
│ world.json
│
├─components
│ activity.vue
│ activity_detail.vue
│ AIfloating.vue
│ AImessage.vue
│ apply.vue
│ approve.vue
│ countrySelectbox.vue
│ create_activity.vue
│ encyclopediaMap.vue
│ encyclopediaSingleCountry.vue
│ enroll.vue
│ enroll_activity.vue
│ ForestAddView.vue
│ ForestDetailView.vue
│ ForestEditView.vue
│ fotmatTime.ts
│ imageViewer.vue
│ navbar.vue
│ postPreview.vue
│
├─router
│ index.ts
│
└─views
 activities.vue
 EncyclopediaView.vue
 ForumView.vue
 HomeView.vue
 LoginView.vue
 postDetailView.vue
 postWriteView.vue
 ProfileView.vue
 RegisterView.vue
```



### 开发的架构 
林上鹰眼项目前端使用 Vue.js 框架，在所有.vue 文件中包含了 html（<template>）、CSS（<style>）框架和 JavaScript（<script>）的前后端请求响应连接部分。
通过<script>向由 基于python的Flask 搭建的后端 API 发送请求，后端响应请求并于 MySQL 数据库交互，
将结果返回给前端，前端处理响应后，等待用户进一步操作。  
> The ForestEagleEye project utilizes the `Vue.js` framework on the front end. All .vue files encompass the HTML (`<template>`), CSS (`<style>`), and JavaScript (`<script>`) sections, which facilitate the connection between front-end and back-end request and response interactions.  
Through the `<script>` section, requests are sent to the back-end API, which is constructed using Python-based `Flask`. The back end processes these requests and interacts with the MySQL database. The results are then returned to the front end, which handles the responses and awaits further user actions.  
<img width="444" alt="系统开发架构" src="https://github.com/user-attachments/assets/4bd8bbbb-e0b1-45c0-b1fa-7c8686041b54" />


### 部署

暂无

### 使用到的框架

- [Vue.js](https://cn.vuejs.org/)
- [Elements-UI](https://element-plus.org/zh-CN/)
- [ECharts](https://echarts.apache.org/zh/index.html)
- [Flask](https://dormousehole.readthedocs.io/en/latest/index.html)
  
### 贡献者

感谢[GalxyX](https://github.com/GalxyX)、[RaraCai](https://github.com/RaraCai)、[vivi-Jiang](https://github.com/vivi-Jiang)、[5555555559](https://github.com/5555555559)对本仓库的贡献。
> Thanks to [GalxyX](https://github.com/GalxyX), [RaraCai](https://github.com/RaraCai), [vivi-Jiang](https://github.com/vivi-Jiang) and [5555555559](https://github.com/5555555559) for their contributions to this repo.


### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。


### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE.txt](https://github.com/shaojintian/Best_README_template/blob/master/LICENSE.txt)

### 其他文件
·[ER 图](https://kdocs.cn/l/cjCQcCVYziCP)<br>
·[关系模式图](https://kdocs.cn/l/cbSas2KOnVUp)<br>
·[loop](https://loop.cloud.microsoft)<br>
·[【金山文档 | WPS 云文档】 林上鹰眼项目进度表](https://kdocs.cn/l/crS6fVz2oakK)
·[axshare](https://snvv62.axshare.com/?g=14)
