# BlogAutoPublish

A tool that supports automatic blog synchronization via Git commits, designed to sync Markdown files to the Typecho blogging platform, with automatic image uploads to Qiniu Cloud and seamless deployment through GitHub Actions.

[中文](./README.md)

## ✨ Features

- 🔄 **Auto Sync**: Automatically syncs local Markdown files to your Typecho blog.
- 🖼️ **Image Upload**: Automatically uploads local images referenced in Markdown to Qiniu Cloud Storage.
- 🚀 **CI/CD Ready**: Built-in GitHub Actions workflow for Push-to-Deploy.
- 📝 **Metadata Support**: Perfectly parses Markdown Front Matter (title, tags, categories, date, etc.).
- 🔍 **Smart Detection**: Intelligently detects file changes using SHA1 hashes, syncing only modified files.
- 📚 **Auto Indexing**: Automatically updates the post index in `README.md` after syncing.
- ⚙️ **Flexible Configuration**: Supports both `config.json` file and environment variables.
- 🛡️ **Robust Error Handling**: Comprehensive error handling and logging for a clear and traceable sync process.

## 📦 Installation

1.  Clone this repository to your local machine:
    ```bash
    git clone https://github.com/LLLLLuuusa/BlogAutoPublish.git
    cd typecho-markdown-sync
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

### Option 1: Using a Config File (for local execution)

1.  Copy the example config file `config.example.json` and rename it to `config.json`.

2.  Modify `config.json` with your own information:
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
            "domain": "https://your-qiniu-domain.com"
        },
        "posts": {
            "directory": "_posts",
            "default_tags": "blog",
            "default_category": "default"
        }
    }
    ```

### Option 2: Using Environment Variables (for GitHub Actions or Docker)

You can also configure the tool using environment variables, which is especially useful in automated workflows.

```bash
export USERNAME="your_username"
export PASSWORD="your_password"
export XMLRPC_PHP="https://your-domain.com/action/xmlrpc"

# If using Qiniu
export QINIU_ACCESS_KEY="your_access_key"
export QINIU_SECRET_KEY="your_secret_key"
# ... other configurations
```

## 🚀 Usage

### Manual Sync

To manually trigger a sync in your local environment, simply run the main script:
```bash
python main.py
```
If your configuration file is located elsewhere, you can specify its path:
```bash
python main.py /path/to/your/config.json
```

### Automated Sync (GitHub Actions)

This project comes with a pre-configured GitHub Actions workflow to automatically sync your posts upon pushing changes.

#### Setup Steps

1.  **Set Up Repository Secrets**

    To securely use your credentials in Actions, add the following to your GitHub repository's `Settings > Secrets and variables > Actions`:

    -   `USERNAME`: Your Typecho login username
    -   `PASSWORD`: Your Typecho login password
    -   `XMLRPC_PHP`: The XML-RPC endpoint URL for your Typecho blog
    -   `QINIU_ACCESS_KEY`: Your Qiniu Access Key (if used)
    -   `QINIU_SECRET_KEY`: Your Qiniu Secret Key (if used)
    -   `QINIU_BUCKET_NAME`: Your Qiniu bucket name (if used)
    -   `QINIU_DOMAIN`: Your Qiniu custom domain (if used)

2.  **Create the Workflow File**

    Create a file at `.github/workflows/main.yml` in your repository and paste the following content:

    ```yaml
    name: Typecho Post Auto Publish
    on:
      push:
        branches:
          - main # Or your primary branch name
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

          - name: Create Config from Secrets
            run: |
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
                  "domain": "${{ secrets.QINIU_DOMAIN }}"
                },
                "posts": {
                  "directory": "_posts"
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

After setting this up, every time you push new or modified Markdown files to the `main` branch, GitHub Actions will automatically execute the sync task and commit the updated `README.md` and hash cache file back to your repository.

## 📁 Project Structure

```
typecho-markdown-sync/
├── .github/workflows/    # GitHub Actions workflow
│   └── main.yml
├── src/                  # Core source code
│   ├── config.py         # Configuration management
│   ├── qiniu_client.py   # Qiniu client
│   ├── typecho_client.py # Typecho client
│   └── sync_manager.py   # Sync manager
├── _posts/               # Your Markdown posts directory
├── main.py               # Main script entry point
├── requirements.txt      # Python dependency list
├── config.example.json   # Example config file
└── README.md             # This documentation
```

## 📄 Markdown File Format

### Front Matter

The tool uses Front Matter at the top of your files to get post metadata.

```markdown
---
title: Post Title
tags: [Tag1, Tag2]
categories: [Category1]
date: 2024-01-01 12:00:00
---

Your post content starts here...
```

### Image Handling

The tool automatically handles **local relative-path images** in your Markdown:
```markdown
![Image description](./images/example.jpg)
```
The image will be uploaded to Qiniu Cloud and the link will be replaced with the CDN URL:
```markdown
![Image description](https://your-qiniu-domain.com/image-hash.jpg)
```

## 🛠️ Dependencies

- `pytypecho`: A Typecho XML-RPC client
- `python-frontmatter`: A library to parse Front Matter
- `pypinyin`: A library to convert Chinese characters to Pinyin (for slugs)
- `qiniu`: The official Qiniu Cloud SDK
- `markdown`: A library to convert Markdown to HTML
- `requests`: An elegant and simple HTTP library

## 🤝 Contributing

Contributions of any kind are welcome!

1. Fork this project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 