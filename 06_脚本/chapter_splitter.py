"""
章节拆分工具
将单个正文文件拆分为独立的章节文件
"""

import os
import re
import sys
from pathlib import Path


def split_chapters(input_file: str, output_dir: str):
    """将正文文件拆分为独立章节"""

    # 读取原文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 {input_file}: {e}")
        return

    # 章节分割模式
    # 匹配: 序章、第X章、【第X章】等格式
    chapter_pattern = r'(?=(?:^|\n)(?:---\n)?(?:序章|【?第\d+章】?))'

    # 分割章节
    chapters = re.split(chapter_pattern, content)

    # 过滤空章节
    chapters = [c.strip() for c in chapters if c.strip()]

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    print(f"发现 {len(chapters)} 个章节")

    for i, chapter in enumerate(chapters):
        # 提取章节标题
        title_match = re.search(r'(?:序章[①②③]?|【?第(\d+)章】?)[：:]?\s*(.+?)(?:\n|$)', chapter)

        if title_match:
            if '序章' in chapter[:20]:
                filename = f"序章.md"
            else:
                chapter_num = title_match.group(1) or str(i)
                chapter_title = title_match.group(2) if title_match.group(2) else ""
                filename = f"第{chapter_num.zfill(2)}章_{chapter_title[:10]}.md"
        else:
            filename = f"章节_{i:02d}.md"

        # 清理文件名中的非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)

        # 写入文件
        output_path = os.path.join(output_dir, filename)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(chapter)
            print(f"  [OK] Created: {filename}")
        except Exception as e:
            print(f"  [FAIL] {filename}: {e}")

    print(f"\n完成! 章节已保存到: {output_dir}")


def main():
    if len(sys.argv) < 3:
        print("用法: python chapter_splitter.py <输入文件> <输出目录>")
        print("示例: python chapter_splitter.py ../【!!!小说正文】.txt ../03_正文/卷一_裂痕与回响/")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"错误: 输入文件 {input_file} 不存在")
        sys.exit(1)

    split_chapters(input_file, output_dir)


if __name__ == "__main__":
    main()
