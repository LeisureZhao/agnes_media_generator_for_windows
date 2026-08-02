---
name: Agnes Media Skill (Python)
description: AI-powered image and video generation via Agnes API, cross-platform Python implementation. Supports direct command execution from Claude Code context.
type: skill
---

# Agnes Media Skill for Claude Code

## 简介

通过 Agnes AI API 生成图片和视频的跨平台 Python 工具。API Key 存储在 `config.json` 中，无需环境变量。

## 快速使用

**1. 配置 API Key**

> ⚠️ **注意**：执行前请先 `cd` 进入技能目录（即本文档所在目录），否则 `config.json` 会因路径错误而找不到。

编辑项目根目录下的 `config.json`：

```json
{
  "api_key": "你的 Agnes API Key"
}
```

**2. 安装依赖**

```bash
pip install -r requirements.txt
```

**3. 生成图片**

```bash
python agnes_generate.py --action image --prompt "夕阳下的山脉" --size 4K --ratio 16:9
```

**4. 生成视频**

```bash
python agnes_generate.py --action video --prompt "猫咪在海滩上散步，夕阳西下" --width 1088 --height 832
```

## 完整参数说明

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| Action | string | (必填) | `image` 或 `video` |
| Prompt | string | (必填) | 生成内容的文本描述 |
| Size | string | `2K` | 图像分辨率（`2K` / `4K`） |
| Ratio | string | `16:9` | 图像比例（`4:3` / `16:9` / `9:16`） |
| Model | string | `agnes-image-2.1-flash` | 图像模型标识符 |
| Width | int | `1088` | 视频宽度（像素） |
| Height | int | `832` | 视频高度（像素） |
| NumFrames | int | `121` | 视频帧数 |
| FrameRate | int | `24` | 视频帧率（fps） |

## 功能特性

- **跨平台支持**: 运行在 Windows/macOS/Linux 上的任意 Python 3.8+ 环境
- **自动配置加载**: 从 `config.json` 读取 API Key
- **智能轮询**: 视频生成功能会自动轮询状态直至完成（最长等待 600 秒）
- **详细错误处理**: 提供清晰的错误信息和调试追踪

## 输出示例

**图片生成返回:**

```json
{
  "type": "image",
  "prompt": "夕阳下的山脉",
  "size": "2K",
  "ratio": "16:9",
  "model": "agnes-image-2.1-flash",
  "url": "https://platform-outputs.agnes-ai.space/images/..."
}
```

**视频生成返回:**

```json
{
  "type": "video",
  "prompt": "猫咪在海滩上散步",
  "width": 1088,
  "height": 832,
  "num_frames": 121,
  "frame_rate": 24,
  "model": "agnes-video-v2.0",
  "url": "https://platform-outputs.agnes-ai/videos/..."
}
```

## 错误处理

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| `FILE_NOT_FOUND` | `config.json` 不存在 | 创建配置文件并放入 API Key |
| `INVALID_API_KEY` | `config.json` 中 api_key 为空 | 填入有效的 API Key |
| `JSON_PARSE_ERROR` | `config.json` JSON 格式错误 | 修复 JSON 语法 |
| `API_REQUEST_FAILED` | API 请求失败 | 检查网络连接或重试 |

## 集成方式

### 在 Claude Code 终端中直接调用

> ⚠️ **注意**：执行前请先 `cd` 进入技能目录（即本 README 所在目录），否则 `config.json` 会因路径错误而找不到。

```bash
# 生成图片
python agnes_generate.py --action image --prompt "城市夜景，霓虹灯光" --size 4K

# 生成视频
python agnes_generate.py --action video --prompt "森林溪流，阳光透过树叶"
```

## 项目结构

```
agnes_media_generator/
├── README.md        ← 中文用户文档
├── Skill.md         ← Claude Code 技能描述
├── agnes_generate.py ← 主实现脚本（Python 3.8+）
├── config.json      ← API 密钥配置
├── requirements.txt ← Python 依赖
└── package.json     ← NPM 脚本配置（可选）
