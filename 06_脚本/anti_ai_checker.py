"""
反AI味句式检测器
检测正文中违反《创作圣经》7.11条款的句式
"""

import re
import os
import sys
from pathlib import Path

# 反AI味句式黑名单
BLACKLIST_PATTERNS = [
    # 结构级AI味句式
    (r"没有.{1,20}，没有.{1,20}。", "禁用句式：'没有XX，没有XX。'"),
    (r"没有.{1,20}，只有.{1,20}。", "禁用句式：'没有XX，只有XX。'"),
    (r"不是.{1,20}，而是.{1,20}。", "禁用句式：'不是XX，而是XX。'"),
    (r"仿佛.{1,20}一般", "限量使用：'仿佛XX一般'"),
    (r"仿佛.{1,20}一样", "限量使用：'仿佛XX一样'"),
    (r"世界仿佛被按下了.{1,10}键", "禁用比喻：'世界仿佛被按下了XX键'"),

    # 总结性废话
    (r"这体现了", "总结性废话：'这体现了'"),
    (r"他心中充满了", "直接情绪描写：'他心中充满了'"),
    (r"她心中充满了", "直接情绪描写：'她心中充满了'"),
    (r"他感到一阵", "直接情绪描写：'他感到一阵'"),
    (r"她感到一阵", "直接情绪描写：'她感到一阵'"),
    (r"这让他更加", "总结性废话：'这让他更加'"),
    (r"这让她更加", "总结性废话：'这让她更加'"),

    # 直接情绪描写（应改为生理反应）
    (r"他很害怕", "直接情绪：'他很害怕' -> 改用生理反应"),
    (r"她很害怕", "直接情绪：'她很害怕' -> 改用生理反应"),
    (r"他非常绝望", "直接情绪：'他非常绝望' -> 改用生理反应"),
    (r"她非常绝望", "直接情绪：'她非常绝望' -> 改用生理反应"),
    (r"他感到恐惧", "直接情绪：'他感到恐惧' -> 改用生理反应"),
    (r"她感到恐惧", "直接情绪：'她感到恐惧' -> 改用生理反应"),
]


def check_file(file_path: str) -> list:
    """检查单个文件中的反AI味句式"""
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [f"无法读取文件: {e}"]

    for line_num, line in enumerate(lines, 1):
        for pattern, description in BLACKLIST_PATTERNS:
            matches = re.findall(pattern, line)
            if matches:
                issues.append({
                    'line': line_num,
                    'content': line.strip()[:50] + ('...' if len(line.strip()) > 50 else ''),
                    'pattern': description,
                    'match': matches[0] if matches else ''
                })

    return issues


def check_directory(dir_path: str) -> dict:
    """检查目录下所有md文件"""
    results = {}

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.md') or file.endswith('.txt'):
                file_path = os.path.join(root, file)
                issues = check_file(file_path)
                if issues:
                    results[file_path] = issues

    return results


def print_report(results: dict):
    """打印检测报告"""
    print("\n" + "=" * 60)
    print("反AI味检测报告")
    print("=" * 60)

    total_issues = 0

    for file_path, issues in results.items():
        print(f"\n文件: {file_path}")
        print("-" * 40)

        for issue in issues:
            if isinstance(issue, str):
                print(f"  {issue}")
            else:
                print(f"  [第{issue['line']}行] {issue['pattern']}")
                print(f"    内容: {issue['content']}")
            total_issues += 1

    print("\n" + "=" * 60)
    print(f"总计: {total_issues} 处问题")
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("用法: python anti_ai_checker.py <文件或目录路径>")
        print("示例: python anti_ai_checker.py 03_正文/")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        issues = check_file(target)
        if issues:
            print_report({target: issues})
        else:
            print(f"✓ {target} 未发现反AI味句式")
    elif os.path.isdir(target):
        results = check_directory(target)
        if results:
            print_report(results)
        else:
            print(f"✓ {target} 目录下未发现反AI味句式")
    else:
        print(f"错误: {target} 不存在")
        sys.exit(1)


if __name__ == "__main__":
    main()
