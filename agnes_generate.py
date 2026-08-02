#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Agnes Media Generator - 跨平台图片和视频生成工具
# 基于 Agnes AI API，支持图像和视频生成

import json
import argparse
import time
import requests


import sys
import io

# 强制设置标准输出为 UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
class AgnesGenerator:
    """Agnes AI 媒体生成器类"""

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.api_key = self._load_api_key()
        self.api_base = "https://apihub.agnes-ai.cn"

    def _load_api_key(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"config.json JSON 格式解析失败: {e}")

        api_key = config.get('api_key', '').strip()
        if not api_key:
            raise ValueError("config.json 中缺少 'api_key' 字段或值为空")

        return api_key

    def generate_image(self, prompt: str, size: str = "2K", ratio: str = "16:9", model: str = "agnes-image-2.1-flash"):
        print(f"\n正在生成图片... ({size}x{ratio})")
        print(f"提示词: {prompt}")

        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "ratio": ratio,
            "extra_body": {"response_format": "url"}
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        url = f"{self.api_base}/v1/images/generations"

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            result = response.json()

            data = result.get("data", [{}])[0]
            image_url = data.get("url", "")

            if not image_url:
                raise ValueError("响应中未找到图片 URL")

            print(f"\n图片生成成功！")
            print(f"URL: {image_url}")

            return {"url": image_url}

        except requests.exceptions.RequestException as e:
            print(f"图片生成请求失败: {e}")
            raise
        except Exception as e:
            print(f"图片生成失败: {e}")
            raise

    def generate_video(self, prompt: str, width: int = 1088, height: int = 832,
                      num_frames: int = 121, frame_rate: int = 24):
        video_model = "agnes-video-v2.0"
        print(f"\n正在创建视频任务... ({width}x{height}, {frame_rate}fps)")
        print(f"提示词: {prompt}")

        payload = {
            "model": video_model,
            "prompt": prompt,
            "height": height,
            "width": width,
            "num_frames": num_frames,
            "frame_rate": frame_rate
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        url = f"{self.api_base}/v1/videos"

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            task_result = response.json()

            video_id = task_result.get("id", "")
            print(f"\n视频任务创建成功！")
            print(f"视频 ID: {video_id}")
            print(f"状态: {task_result.get('status', 'unknown')}")

            status_url = f"{self.api_base}/agnesapi?video_id={video_id}"
            max_attempts = 120
            wait_interval = 5

            print("\n轮询视频进度...")

            for attempt in range(1, max_attempts + 1):
                time.sleep(wait_interval)

                try:
                    status_response = requests.get(status_url, headers=headers, timeout=300)
                    status_response.raise_for_status()
                    status_info = status_response.json()

                    status = status_info.get("status", "")
                    progress = status_info.get("progress", 0)

                    if status == "queued":
                        print(f"[{attempt}/{max_attempts}] 队列中 - {progress}%")
                    elif status == "in_progress":
                        print(f"[{attempt}/{max_attempts}] 处理中 - {progress}%")
                    elif status == "completed":
                        video_url = status_info.get("url", "")
                        duration = status_info.get("seconds", 0)
                        resolution = status_info.get("size", "")

                        print(f"\n视频生成完成！")
                        print(f"时长: {duration}s")
                        print(f"分辨率: {resolution}")
                        print(f"下载链接: {video_url}")

                        return status_info
                    else:
                        print(f"[{attempt}/{max_attempts}] 未知状态: {status}, 进度: {progress}%")

                except requests.exceptions.RequestException as e:
                    print(f"[{attempt}/{max_attempts}] 检查状态出错: {e}")
                    continue

            print(f"\n达到最大尝试次数 ({max_attempts})，视频可能未完成")

        except requests.exceptions.RequestException as e:
            print(f"视频任务创建失败: {e}")
            raise
        except Exception as e:
            print(f"视频生成失败: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Agnes Media Generator - 使用 Agnes AI API 生成图片和视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --action image --prompt "夕阳下的山脉" --size 2K --ratio 16:9
  %(prog)s --action video --prompt "森林小溪流淌" --width 1088 --height 832 --frame-rate 24
        """
    )

    parser.add_argument("--action", choices=["image", "video"], required=True,
                       help="生成内容类型: image 或 video")
    parser.add_argument("--prompt", required=True, help="生成内容的描述文本")
    parser.add_argument("--size", default="2K", choices=["2K", "4K"],
                       help="图像分辨率 (默认: 2K)")
    parser.add_argument("--ratio", default="16:9",
                       help="图像比例 (默认: 16:9), 选项: 4:3, 16:9, 9:16")
    parser.add_argument("--model", default="agnes-image-2.1-flash",
                       help="图像模型名称 (默认: agnes-image-2.1-flash)")
    parser.add_argument("--width", type=int, default=1088,
                       help="视频宽度 (像素, 默认: 1088)")
    parser.add_argument("--height", type=int, default=832,
                       help="视频高度 (像素, 默认: 832)")
    parser.add_argument("--num-frames", type=int, default=121,
                       help="视频帧数 (默认: 121)")
    parser.add_argument("--frame-rate", type=int, default=24,
                       help="视频帧率 (fps, 默认: 24)")

    args = parser.parse_args()

    try:
        generator = AgnesGenerator()

        if args.action == "image":
            info = generator.generate_image(
                prompt=args.prompt,
                size=args.size,
                ratio=args.ratio,
                model=args.model
            )
            print(json.dumps(info, indent=2, ensure_ascii=False))

        else:
            info = generator.generate_video(
                prompt=args.prompt,
                width=args.width,
                height=args.height,
                num_frames=args.num_frames,
                frame_rate=args.frame_rate
            )
            print(json.dumps(info, indent=2, ensure_ascii=False))

    except FileNotFoundError as e:
        print(f"错误: {e}")
        print("\n请确保 config.json 文件存在且包含有效的 API Key")
        exit(1)
    except ValueError as e:
        print(f"错误: {e}")
        exit(1)
    except Exception as e:
        print(f"发生意外错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
