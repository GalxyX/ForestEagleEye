# ForestEagleEye

## 安装与部署

### 前端

1. **克隆仓库**：

    ```bash
    git clone https://github.com/你的用户名/ForestEagleEye.git
    ```

2. **进入前端目录并安装依赖**：

    ```bash
    cd ForestEagleEye/ForestEagleEye
    npm install
    ```

3. **启动开发服务器**：

    ```bash
    npm run serve
    ```

### 后端

1. **启动后端服务器**：

    ```bash
    python app.py
    ```

## 使用说明

### 用户注册与登录

- **注册**：访问 `/register` 页面，填写必要信息完成注册。
- **登录**：访问 `/login` 页面，输入注册时的邮箱和密码进行登录。

### 活动管理

- **创建活动**：林业从业人员和监管人员登录后，可在“活动管理”页面创建新活动，上传封面图片，设置活动类型及参与人数。
- **审批流程**：创建的活动需经过管理员审核，审核通过后活动将对普通用户开放报名。
- **活动报名**：普通用户可浏览活动列表，选择感兴趣的活动进行报名。
- **报名管理**：用户可在个人中心查看已报名的活动，并可选择取消报名。

### 资源与灾害管理

- **资源分布**：在“资源管理”页面查看森林内各种资源的分布情况，包括类型、位置及范围。
- **灾害信息**：实时查看和统计森林灾害数据，支持按类型和损失进行筛选和展示。

### 论坛社区

- **发帖与评论**：用户可在论坛中发表帖子、评论他人帖子，分享经验与见解。
- **点赞与分享**：支持对帖子进行点赞，并可将帖子分享至社交媒体平台。

### 数据可视化

- **图表展示**：通过ECharts库展示森林资源和灾害数据的图表，便于直观分析。
- **地图集成**：集成高德地图API，展示森林资源的地理分布及相关信息。

### AI助手

- **智能问答**：内置AI聊天助手，用户可咨询关于森林管理和活动的相关问题，获取智能回复。

## 贡献指南

欢迎贡献！请按照以下步骤进行：

1. **Fork 本仓库**。
2. **创建新分支** (`git checkout -b feature/新功能`)。
3. **提交更改** (`git commit -m '添加新功能'`)。
4. **推送到分支** (`git push origin feature/新功能`)。
5. **创建 Pull Request**。

请确保所有新功能和修复的代码都有相应的测试，并遵循项目的编码规范。

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Run End-to-End Tests with [Playwright](https://playwright.dev)

```sh
# Install browsers for the first run
npx playwright install

# When testing on CI, must build the project first
npm run build

# Runs the end-to-end tests
npm run test:e2e
# Runs the tests only on Chromium
npm run test:e2e -- --project=chromium
# Runs the tests of a specific file
npm run test:e2e -- tests/example.spec.ts
# Runs the tests in debug mode
npm run test:e2e -- --debug
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
