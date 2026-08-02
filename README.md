# Agnes Media Generator

## 功能描述

一个基于 Python 的跨平台工具，用于通过 Agnes AI API 生成图片和视频。

## 快速开始

### 安装依赖

```bash
pip install requests
```

### 配置 API Key

编辑 `config.json` 文件，填入你的 Agnes AI API Key：

```json
{
  "api_key": "你的 Agnes AI API Key"
}
```

### 使用示例

**生成图片：**

```bash
python agnes_generate.py --action image --prompt "A beautiful sunset over mountains" --size 2K --ratio 16:9
```

**生成视频：**

```bash
python agnes_generate.py --action video --prompt "A serene forest stream flowing through trees" --width 1088 --height 832 --frame-rate 24
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Action (必需) | - | image 或 video |
| Prompt (必需) | - | 生成的内容描述 |
| Size | 2K | 图像分辨率 (2K/4K) |
| Ratio | 16:9 | 图像比例 (4:3/16:9/9:16) |
| Model | agnes-image-2.1-flash | 图像模型名称 |
| Width | 1088 | 视频宽度（像素） |
| Height | 832 | 视频高度（像素） |
| NumFrames | 121 | 帧数 |
| FrameRate | 24 | 帧率 (fps) |

## 注意事项

1. 请确保在生成资源前正确设置了 `config.json` 中的 API Key。
2. 视频生成为异步任务，脚本会自动轮询直到任务完成（最多等待 600 秒）。
