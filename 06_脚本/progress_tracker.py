"""
进度追踪器
统计创作进度，生成进度报告
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime


def count_chinese_chars(text: str) -> int:
    """统计中文字符数（排除标点和空格）"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))


def count_file_words(file_path: str) -> int:
    """统计单个文件的字数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return count_chinese_chars(content)
    except Exception as e:
        print(f"警告: 无法读取 {file_path}: {e}")
        return 0


def count_chapters(volume_dir: str) -> tuple:
    """统计卷目录下的章节数和总字数"""
    chapter_count = 0
    total_words = 0

    if not os.path.exists(volume_dir):
        return 0, 0

    for file in os.listdir(volume_dir):
        if file.endswith('.md') and not file.startswith('_'):
            chapter_count += 1
            file_path = os.path.join(volume_dir, file)
            total_words += count_file_words(file_path)

    return chapter_count, total_words


def get_volume_status(chapter_count: int, expected: int = None) -> str:
    """获取卷的完成状态"""
    if expected and chapter_count >= expected:
        return "✅"
    elif chapter_count > 0:
        return "🔄"
    else:
        return "⏳"


def generate_report(base_dir: str):
    """生成进度报告"""
    print("\n" + "=" * 60)
    print("《龙珠：厄日序曲》创作进度报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 目标字数
    target_min = 350000
    target_max = 450000

    # 各卷目录
    volumes = [
        ("卷一", "03_正文/卷一_裂痕与回响", 19),  # 预期19章
        ("卷二", "03_正文/卷二_红云与黑龙", None),
        ("卷三", "03_正文/卷三_希望与失控", None),
        ("卷四", "03_正文/卷四_献祭与黎明", None),
    ]

    total_words = 0
    total_chapters = 0

    print("\n各卷进度:")
    print("-" * 40)

    for vol_name, vol_path, expected in volumes:
        full_path = os.path.join(base_dir, vol_path)
        chapters, words = count_chapters(full_path)
        total_words += words
        total_chapters += chapters

        status = get_volume_status(chapters, expected)
        expected_str = f"/{expected}" if expected else "/?"

        print(f"  {vol_name}: {chapters}{expected_str}章 {status} ({words:,}字)")

    print("-" * 40)

    # 总体进度
    completion = (total_words / target_min) * 100 if target_min > 0 else 0

    print(f"\n总字数: {total_words:,} / 目标 {target_min:,}-{target_max:,}")
    print(f"完成度: {completion:.1f}%")
    print(f"总章节: {total_chapters}章")

    # 进度条
    bar_length = 40
    filled = int(bar_length * min(completion, 100) / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\n[{bar}] {completion:.1f}%")

    print("\n" + "=" * 60)


def main():
    # 默认使用当前目录
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.exists(base_dir):
        print(f"错误: 目录 {base_dir} 不存在")
        sys.exit(1)

    generate_report(base_dir)


if __name__ == "__main__":
    main()
