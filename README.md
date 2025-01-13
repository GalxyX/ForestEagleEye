# ForestEagleEye

林上鹰眼——基于 MySQL 的一站式森林环境资源与信息平台
> ForestEagleEye — A One-Stop Forest Environmental Resources and Information Platform Based on MySQL

<!-- PROJECT SHIELDS -->
 
## 目录

- [上手指南(Guide)](#上手指南(Guide))
  - [项目介绍(Project Introduction)](#项目介绍(Project-Introduction))
  - [开发前的配置要求(Pre-development Configuration Requirements)](#开发前的配置要求(Pre-development-Configuration-Requirements))
  - [安装步骤(Installation Steps)](#安装步骤(Installation-Steps))
- [文件目录说明(Directory Structure Explanation)](#文件目录说明(Directory-Structure-Explanation))
- [开发的架构(Development Architecture)](#开发的架构(Development-Architecture))
- [部署(Deployment)](#部署(Deployment))
- [使用到的框架(Frameworks Used)](#使用到的框架(Frameworks-Used))
- [贡献者(Contributors)](#贡献者(Contributors))
- [版本控制(Version Control)](#版本控制(Version-Control))
- [项目概览(Project Overview)](#项目概览(Project-Overview))
- [其他文件(Other Files)](#其他文件(Other-Files))

## 上手指南(Guide)

#### 项目介绍(Project-Introduction)
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

#### 开发前的配置要求(Pre-development-Configuration-Requirements)

1. vite运行环境及相关依赖  
2. pip运行环境及相关依赖  
3. [高德开放平台API](https://lbs.amap.com/)  
4. MySQL数据库及密钥  
> 1. Vite runtime environment and related dependencies  
> 2. Pip runtime environment and related dependencies  
> 3. [Gaode Open Platform API](https://lbs.amap.com/)  
> 4. MySQL database and keys  

#### **安装步骤(Installation-Steps)**
1. 克隆仓库  
2. 使用`npm install`安装vite运行环境及相关依赖  
3. 使用`pip install`安装pip运行环境及相关依赖  
4. 在高德开放平台注册您的API，并在`app.py`中替换为您的密钥  
5. 在`app.py`在将数据库及及其密钥配置为您的数据库  
6. 分别启动前后端，运行项目  
```sh
npm run dev
python app.py
```
>
> 1. Clone the repo  
> ```sh
> git clone https://github.com/GalxyX/ForestEagleEye.git
> ```
> 2. npm install  
> ```sh
>npm install
> ```
> 3. pip install  
> ```sh
> pip install
> ```
> 4. Get a free API Key at [https://lbs.amap.com/](https://lbs.amap.com/) and replace the  `app.py`  
> 5. Use your MySQL configuration to replace `app.py`  
> 6. run the project  
> ```sh
> npm run dev
> python app.py
> ```

### 文件目录说明(Directory-Structure-Explanation)
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



## 开发的架构(Development-Architecture)
林上鹰眼项目前端使用 Vue.js 框架，在所有.vue 文件中包含了 html（<template>）、CSS（<style>）框架和 JavaScript（<script>）的前后端请求响应连接部分。
通过<script>向由 基于python的Flask 搭建的后端 API 发送请求，后端响应请求并于 MySQL 数据库交互，
将结果返回给前端，前端处理响应后，等待用户进一步操作。  
> The ForestEagleEye project utilizes the `Vue.js` framework on the front end. All .vue files encompass the HTML (`<template>`), CSS (`<style>`), and JavaScript (`<script>`) sections, which facilitate the connection between front-end and back-end request and response interactions.  
Through the `<script>` section, requests are sent to the back-end API, which is constructed using Python-based `Flask`. The back end processes these requests and interacts with the MySQL database. The results are then returned to the front end, which handles the responses and awaits further user actions.  
<img width="444" alt="系统开发架构" src="https://github.com/user-attachments/assets/4bd8bbbb-e0b1-45c0-b1fa-7c8686041b54" />


## 部署(Deployment)

暂无

### 使用到的框架(Frameworks-Used)

- [Vue.js](https://cn.vuejs.org/)
- [Elements-UI](https://element-plus.org/zh-CN/)
- [ECharts](https://echarts.apache.org/zh/index.html)
- [Flask](https://dormousehole.readthedocs.io/en/latest/index.html)
  
## 贡献者(Contributors)

感谢[@GalxyX](https://github.com/GalxyX)、[@RaraCai](https://github.com/RaraCai)、[@vivi-Jiang](https://github.com/vivi-Jiang)、[@5555555559](https://github.com/5555555559)对本仓库的贡献。
> Thanks to [@GalxyX](https://github.com/GalxyX), [@RaraCai](https://github.com/RaraCai), [@vivi-Jiang](https://github.com/vivi-Jiang) and [@5555555559](https://github.com/5555555559) for their contributions to this repo.


## 版本控制(Version-Control)

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。


## 项目概览(Project-Overview)
本项目由4个主要模块组成：  
**· 森林百科**：查看世界各个国家和地区的各种森林以及管理员自建数据库内所有单个林区的数据与可视化结果  
**· 林业活动**：集林业活动风采展示、活动报名、活动创建与审批为一体的一站式林业活动审批流  
**· 林上论坛**：与森林爱好者交换灵感，在论坛与社区发帖、评论、点赞  
**· 小林问答**：AI问答助手，帮助您解决与森林相关的所有问题  
> This project comprises four main modules:  
**· Forest Encyclopedia**: View data and visualizations of forests worldwide and individual forest areas in the administrator-built database.  
**· Forestry Activities**: A one-stop approval process for showcasing, registering, creating, and approving forestry events.  
**· Forest Forum**: Exchange ideas with forest enthusiasts and engage in community posts, comments, and likes.  
**· Forest Q&A**: An AI-powered assistant to answer all your forest-related questions.  

森林百科-百科编辑(Forest Encyclopedia-Edit)：  
![森林百科-编辑](https://github.com/user-attachments/assets/946ebbed-4a46-4c10-b0cb-c6741b08deae)  
森林百科-世界森林数据查询(Forest Encyclopedia-World Data Query)：  
![森林百科-世界](https://github.com/user-attachments/assets/43fd09aa-ef06-43a4-8901-9c6bb576e9d0)  
森林百科-单林区数据查询(Forest Encyclopedia-Single Forest Data Query)：  
![森林百科-单一](https://github.com/user-attachments/assets/e3771feb-c437-4176-ad89-7abf1e3bccdc)
林业活动-活动风采(Forest Activities-All Activities)：  
<img width="1182" alt="林业活动-活动风采" src="https://github.com/user-attachments/assets/0eaf8184-1583-4f54-a9e7-292d48b5020c" />  
林业活动-活动详情(Forest Activities-Activitiy Detail)：  
![林业活动-活动详情](https://github.com/user-attachments/assets/7c615b98-04c4-4ac0-b5dd-3e6e916ec911)  
林业活动-活动申请(Forest Activities-Apply Activities)：  
![林业活动-我的申请](https://github.com/user-attachments/assets/e5672213-53b6-41ae-b6bd-084627d7b2f6)  
林业活动-活动驳回(Forest Activities-Dismiss Activities)：  
![林业活动-驳回](https://github.com/user-attachments/assets/1592753e-97d5-42a8-9653-48eb2a91cda5)  
林上论坛-论坛广场(Forest Forum-All Posts)：  
<img width="890" alt="论坛广场" src="https://github.com/user-attachments/assets/275faa3a-1f6c-485a-8b62-99644a8a6731" />  
林上论坛-帖子详情(Forest Forum-Post Detail)：  
![帖子详情](https://github.com/user-attachments/assets/061bc35e-d340-4b50-8587-7c9acf51f4dc)  
林上论坛-创作中心(Forest Forum-Write Posts)：  
<img width="1196" alt="创作中心" src="https://github.com/user-attachments/assets/6f1b31c5-a13a-4c53-836e-360ff9b27cd1" />  
小林问答(Forest Q&A)：  
<img width="435" alt="小林问答" src="https://github.com/user-attachments/assets/a88af2b3-9ebc-4d08-b641-dd3617942c68" />  


## 其他文件(Other-Files)
·[ER 图](https://kdocs.cn/l/cjCQcCVYziCP)<br>
·[关系模式图](https://kdocs.cn/l/cbSas2KOnVUp)<br>
·[loop](https://loop.cloud.microsoft)<br>
·[【金山文档 | WPS 云文档】 林上鹰眼项目进度表](https://kdocs.cn/l/crS6fVz2oakK)
·[axshare](https://snvv62.axshare.com/?g=14)
