# 抖音无水印视频文本提取 MCP 服务器

[![PyPI version](https://badge.fury.io/py/douyin-video-mcp.svg)](https://badge.fury.io/py/douyin-video-mcp)
[![Python version](https://img.shields.io/pypi/pyversions/douyin-video-mcp.svg)](https://pypi.org/project/douyin-video-mcp/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

一个基于 Model Context Protocol (MCP) 的服务器，可以从抖音分享链接下载无水印视频，提取音频并转换为文本。

## 📋 项目声明

**官方文档地址：** https://github.com/fancyboi999/douyin-video-mcp

**重要提醒：** 第三方平台如因自身 MCP Server 功能支持度限制而无法正常使用，请联系相应平台方。本项目不提供任何形式的技术支持或保证，用户需自行承担使用本项目可能产生的任何损失或损害。

**法律声明：**
1. 本项目基于 MIT 协议发布
2. 本项目仅供学习和研究使用，不得用于任何违法或违规目的
3. 本项目的使用必须遵守相关法律法规
4. 本项目的作者和贡献者不对项目的任何部分承担法律责任

## ✨ 功能特性

- 🎵 **无水印视频获取** - 从抖音分享链接获取高质量无水印视频
- 🎧 **智能音频提取** - 自动从视频中提取音频内容
- 📝 **AI 文本识别** - 使用先进的语音识别技术提取文本内容
- 🧹 **自动清理** - 智能清理处理过程中的临时文件
- 🔧 **灵活配置** - 支持自定义 API 配置，默认使用 [阿里云百炼 API](https://help.aliyun.com/zh/model-studio/get-api-key?)

## 🚀 快速开始

### 步骤 1：获取 API 密钥

前往 [阿里云百炼 API](https://help.aliyun.com/zh/model-studio/get-api-key?) 获取您的 `DASHSCOPE_API_KEY`：

![获取阿里云百炼API](https://files.mdnice.com/user/43439/36e658be-1ccf-41dd-87cf-d43fefde5c4e.png)

### 步骤 2：选择传输方式并配置

#### 方式 A：STDIO（推荐，本地即用）

STDIO 由客户端启动服务进程，最简单的方式是直接使用 `uvx`：

```json
{
  "mcpServers": {
    "douyin-video-mcp": {
      "command": "uvx",
      "args": ["douyin-video-mcp"],
      "env": {
        "ASR_PROVIDER": "dashscope",
        "DASHSCOPE_API_KEY": "sk-xxxx",
        "FISH_API_KEY": "fish-api-key-here"
      }
    }
  }
}
```

#### 方式 B：HTTP（适合部署或多客户端访问）

HTTP 模式需要先启动一个长期运行的服务进程，然后客户端通过 URL 连接。

**启动服务（本地示例）：**

```bash
uv run python -m douyin_video_mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp/
# 或者用 uvx（会自动下载并启动）
uvx douyin-video-mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp/
```

**也可以仅用环境变量控制启动方式：**

```bash
export MCP_TRANSPORT=http
export MCP_HOST=127.0.0.1
export MCP_PORT=8000
export MCP_PATH=/mcp/
uv run python -m douyin_video_mcp
```

**客户端配置：**

```json
{
  "mcpServers": {
    "douyin-video-mcp": {
      "transport": "http",
      "url": "http://127.0.0.1:8000/mcp/"
    }
  }
}
```

### 步骤 3：开始使用

配置完成后，您就可以在支持的应用中正常调用 MCP 工具了。

## ⚙️ API 配置说明

### 当前版本（>= 1.0.0）

最新版本默认使用阿里云百炼 API，具有以下优势：
- ✅ 识别效果更好
- ✅ 处理速度更快
- ✅ 本地资源消耗更小

**配置步骤：**
1. 前往 [阿里云百炼](https://help.aliyun.com/zh/model-studio/get-api-key?) 开通 API 服务
2. 获取 API Key 并配置到环境变量 `DASHSCOPE_API_KEY` 中

## 🛠️ 工具说明

### `get_douyin_download_link`

获取抖音视频的无水印下载链接。

**参数：**
- `share_link` (string): 抖音分享链接或包含链接的文本

**返回：**
- JSON 格式的下载链接和视频信息

**特点：** 无需 API 密钥即可使用

### `extract_douyin_text`

完整的文本提取工具，一站式完成视频到文本的转换。

**处理流程：**
1. 解析抖音分享链接
2. 直接使用视频 URL 进行语音识别
3. 返回提取的文本内容

**参数：**
- `share_link` (string): 抖音分享链接或包含链接的文本
- `model` (string, 可选): 语音识别模型，默认使用 `paraformer-v2`（仅 DashScope 生效）
- `provider` (string, 可选): ASR 提供方（默认读取环境变量 `ASR_PROVIDER`）

**环境变量要求：**
- `ASR_PROVIDER`: 默认 ASR 提供方（可选，例如 `dashscope` / `fish`）
- `DASHSCOPE_API_KEY`: 阿里云百炼 API 密钥（DashScope 必需）
- `FISH_API_KEY`: Fish Audio API 密钥（Fish 必需）

### `parse_douyin_video_info`

轻量级视频信息解析工具。

**参数：**
- `share_link` (string): 抖音分享链接

**特点：** 仅解析视频基本信息，不下载视频文件

### 资源访问

- `douyin://video/{video_id}`: 通过视频 ID 获取详细信息

## 📦 系统要求

### 运行环境
- **Python**: 3.10 或更高版本

### 依赖库
- `requests` - HTTP 请求处理
- `ffmpeg-python` - 音视频处理
- `tqdm` - 进度条显示
- `mcp` - Model Context Protocol 支持
- `dashscope` - 阿里云百炼 API 客户端

## ⚠️ 注意事项

- 🔑 **API 密钥必需**：文本提取功能需要有效的 ASR API 密钥（DashScope 或 Fish）
- 🆓 **部分功能免费**：获取下载链接功能无需 API 密钥
- 📱 **格式支持**：支持大部分抖音视频格式

## 🔧 开发指南

### 本地开发环境搭建

```bash
# 克隆项目
git clone https://github.com/fancyboi999/douyin-video-mcp.git
cd douyin-video-mcp

# 安装依赖（开发模式）
pip install -e .
```

### 运行测试

```bash
# STDIO（默认）
python -m douyin_video_mcp

# HTTP
python -m douyin_video_mcp --transport http --host 127.0.0.1 --port 8000 --path /mcp/
```

### Claude Desktop 本地开发配置

在 Claude Desktop 配置文件中添加本地开发配置：

```json
{
  "mcpServers": {
    "douyin-video-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/douyin-video-mcp",
        "python",
        "-m",
        "douyin_video_mcp"
      ],
      "env": {
        "ASR_PROVIDER": "dashscope",
        "DASHSCOPE_API_KEY": "your-api-key-here",
        "FISH_API_KEY": "your-fish-api-key-here"
      }
    }
  }
}
```

## ⚠️ 免责声明

### 使用风险
- 使用者对本项目的使用完全自主决定，并自行承担所有风险
- 作者对使用者因使用本项目而产生的任何损失、责任或风险概不负责

### 代码质量
- 本项目基于现有知识和技术开发，作者努力确保代码的正确性和安全性
- 但不保证代码完全没有错误或缺陷，使用者需自行评估和测试

### 第三方依赖
- 本项目依赖的第三方库、插件或服务遵循各自的开源或商业许可
- 使用者需自行查阅并遵守相应协议
- 作者不对第三方组件的稳定性、安全性及合规性承担责任

### 法律合规
- 使用者必须自行研究相关法律法规，确保使用行为合法合规
- 任何违反法律法规导致的法律责任和风险，均由使用者自行承担
- 禁止使用本工具从事任何侵犯知识产权的行为
- 开发者不参与、不支持、不认可任何非法内容的获取或分发

### 数据处理
- 本项目不对使用者的数据收集、存储、传输等处理活动的合规性承担责任
- 使用者应自行遵守相关法律法规，确保数据处理行为合法正当

### 责任限制
- 使用者不得将项目作者、贡献者或相关方与使用行为联系起来
- 不得要求作者对使用项目产生的任何损失或损害负责
- 基于本项目的二次开发、修改或编译程序与原作者无关

### 知识产权
- 本项目不授予使用者任何专利许可
- 若使用本项目导致专利纠纷或侵权，使用者自行承担全部风险和责任
- 未经书面授权，不得用于商业宣传、推广或再授权

### 服务终止
- 作者保留随时终止向违反声明的使用者提供服务的权利
- 可能要求违规使用者销毁已获取的代码及衍生作品
- 作者保留在不另行通知的情况下更新本声明的权利

**⚠️ 重要提醒：在使用本项目前，请认真阅读并完全理解上述免责声明。如有疑问或不同意任何条款，请勿使用本项目。继续使用即视为完全接受上述声明并自愿承担所有风险和后果。**

## 📄 许可证

MIT License

## 👨‍💻 作者

- **fancyboi999** - [fancyboi999@gmail.com](mailto:fancyboi999@gmail.com)
- GitHub: [https://github.com/fancyboi999](https://github.com/fancyboi999)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！我们期待您的参与和贡献。

## 📝 更新日志

### v1.0.0
- 🎉 **首次发布**：初始版本
- ✨ **核心功能**：支持抖音视频文本提取
- 🔗 **链接获取**：支持获取无水印视频下载链接
- 🔐 **环境配置**：从环境变量读取 API 密钥
- 🧹 **自动清理**：自动清理临时文件
- ⚙️ **灵活配置**：支持自定义 API 配置
