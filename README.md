# BlogAutoPublish

[English](./README_EN.md)

一个支持提交 Git 自动同步博客的工具，用于将 Markdown 文件同步到 Typecho 博客平台，支持自动上传图片到七牛云存储和 GitHub Actions 自动化部署。

## ✨ 功能特性

- 🔄 **自动同步**: 自动将本地 Markdown 文件同步到 Typecho 博客。
- 🖼️ **图片上传**: 自动上传 Markdown 中引用的本地图片到七牛云存储。
- 🚀 **CI/CD 支持**: 内置 GitHub Actions 工作流，实现 Push-to-Deploy。
- 📝 **元数据支持**: 完美解析 Markdown Front Matter (文章标题、标签、分类、日期等)。
- 🔍 **智能检测**: 通过 SHA1 哈希值智能检测文件变化，仅同步已修改的文件。
- 📚 **自动索引**: 同步完成后自动更新 `README.md` 中的文章索引。
- ⚙️ **灵活配置**: 支持 `config.json` 文件和环境变量两种配置方式。
- 🛡️ **错误处理**: 完善的错误处理和日志记录，同步过程清晰可追溯。

## 📦 安装

1.  克隆本仓库到你的本地：
    ```bash
    git clone https://github.com/LLLLLuuusa/BlogAutoPublish.git
    cd BlogAutoPublish
    ```

2.  安装所需的依赖：
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ 配置

### 方式一：使用配置文件 (本地运行)

1.  复制配置示例文件 `config.example.json` 并重命名为 `config.json`。

2.  根据你的信息修改 `config.json` 文件：
    ```json
    {
        "typecho": {
            "username": "your_username",
            "password": "your_password",
            "xmlrpc_php": "https://your-domain.com/action/xmlrpc"
        },
        "qiniu": {
            "access_key": "your_access_key",
            "secret_key": "your_secret_key",
            "bucket_name": "your_bucket_name",
            "domain": "https://your-qiniu-domain.com",
            "show": "https://your-show-domain.com"
        },
        "posts": {
            "directory": "_posts",
            "default_tags": "blog",
            "default_category": "default"
        }
    }
    ```

### 方式二：使用环境变量 (GitHub Actions 或 Docker)

你也可以使用环境变量来配置，这在自动化流程中特别有用。

```bash
export USERNAME="your_username"
export PASSWORD="your_password"
export XMLRPC_PHP="https://your-domain.com/action/xmlrpc"

# 如果使用七牛云
export QINIU_ACCESS_KEY="your_access_key"
export QINIU_SECRET_KEY="your_secret_key"
export QINIU_SHOW="https://your-show-domain.com"
# ... 其他配置
```

## 🚀 使用方法

### 手动同步

在本地环境中，可以直接运行主程序来手动触发同步：
```bash
python main.py
```
如果你的配置文件在其他路径，可以指定它：
```bash
python main.py /path/to/your/config.json
```

### 自动化同步 (GitHub Actions)

本项目已内置 GitHub Actions 工作流，可实现 `push` 代码后自动同步文章。

#### 设置步骤

1.  **设置仓库 Secrets**

    为了安全地在 Actions 中使用你的凭据，请将以下信息添加到你的 GitHub 仓库的 `Settings > Secrets and variables > Actions` 中：

    -   `USERNAME`: Typecho 登录用户名
    -   `PASSWORD`: Typecho 登录密码
    -   `XMLRPC_PHP`: Typecho 的 XML-RPC 接口地址
    -   `QINIU_ACCESS_KEY`: 七牛云 Access Key 
    -   `QINIU_SECRET_KEY`: 七牛云 Secret Key 
    -   `QINIU_BUCKET_NAME`: 七牛云存储空间名称 
    -   `QINIU_DOMAIN`: 七牛云自定义域名 
    -   `QINIU_SHOW`: 七牛云外链展示域名 

    > **注意**：如果你需要自定义 `posts.default_tags` 和 `posts.default_category`，可以在 workflow 里直接修改默认值，或通过 Secrets 传递并在 workflow 中引用。

2.  **创建 Workflow 文件**

    在你的仓库根目录下创建 `.github/workflows/main.yml` 文件，并粘贴以下内容：

    ```yaml
    name: Typecho Post Auto Publish
    on:
      push:
        branches:
          - main # 或者你的主分支名
    jobs:
      push:
        runs-on: ubuntu-latest
        permissions:
          contents: write
        steps:
          - name: Checkout Repository
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.10'

          - name: Install Dependencies
            run: pip install -r requirements.txt

          - name: Check for existing config.json
            id: check_config
            run: |
              if [ -f config.json ]; then
                echo "config_exists=true" >> $GITHUB_OUTPUT
              else
                echo "config_exists=false" >> $GITHUB_OUTPUT
              fi

          - name: Create Config from Secrets if not exists
            if: steps.check_config.outputs.config_exists == 'false'
            run: |
              echo "config.json not found. Creating from secrets..."
              echo '{
                "typecho": {
                  "username": "${{ secrets.USERNAME }}",
                  "password": "${{ secrets.PASSWORD }}",
                  "xmlrpc_php": "${{ secrets.XMLRPC_PHP }}"
                },
                "qiniu": {
                  "access_key": "${{ secrets.QINIU_ACCESS_KEY }}",
                  "secret_key": "${{ secrets.QINIU_SECRET_KEY }}",
                  "bucket_name": "${{ secrets.QINIU_BUCKET_NAME }}",
                  "domain": "${{ secrets.QINIU_DOMAIN }}",
                  "show": "${{ secrets.QINIU_SHOW }}"
                },
                "posts": {
                  "directory": "_posts",
                  "default_tags": "blog",
                  "default_category": "default"
                }
              }' > config.json

          - name: Run Sync Tool
            run: python main.py config.json

          - name: Commit and Push Changes
            uses: stefanzweifel/git-auto-commit-action@v5
            with:
              commit_message: 'docs: Auto update README and hash cache'
              file_pattern: '.md_sha1 README.md'
    ```

设置完成后，每次向 `main` 分支 `push` 新的 Markdown 文件或修改，GitHub Actions 都会自动执行同步任务，并将更新后的 `README.md` 和哈希缓存文件提交回仓库。

## 📁 项目结构

```
typecho-markdown-sync/
├── .github/workflows/    # GitHub Actions 工作流
│   └── main.yml
├── src/                  # 核心源码
│   ├── config.py         # 配置管理
│   ├── qiniu_client.py   # 七牛云客户端
│   ├── typecho_client.py # Typecho 客户端
│   └── sync_manager.py   # 同步管理器
├── _posts/               # 你的 Markdown 文章目录
├── main.py               # 主程序入口
├── requirements.txt      # Python 依赖列表
├── config.example.json   # 配置示例
└── README.md             # 本文档
```

## 📄 Markdown 文件格式

### Front Matter

工具通过文件头部的 Front Matter 来获取文章的元数据。

```markdown
---
title: 文章标题
tags: [标签1, 标签2]
categories: [分类1]
date: 2024-01-01 12:00:00
---

这里是你的文章正文...
```

### 图片处理

工具会自动处理 Markdown 中的**本地相对路径图片**：
```markdown
![图片描述](./images/example.jpg)
```
图片会被自动上传到七牛云并替换为 CDN 链接：
```markdown
![图片描述](https://your-qiniu-domain.com/image-hash.jpg)
```

## 🛠️ 依赖项

- `pytypecho`: Typecho XML-RPC 客户端
- `python-frontmatter`: Front Matter 解析库
- `pypinyin`: 中文转拼音，用于生成文章 slug
- `qiniu`: 七牛云官方 SDK
- `markdown`: Markdown 转 HTML
- `requests`: HTTP 请求库

## 🤝 贡献

欢迎任何形式的贡献！

1. Fork 本项目
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交一个 Pull Request

## 📜 许可证

本项目采用 MIT 许可证。详情请查看 [LICENSE](LICENSE) 文件。 