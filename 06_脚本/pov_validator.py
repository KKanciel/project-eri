"""
POV验证器
检测章节中的视角越界问题
"""

import re
import os
import sys
from pathlib import Path


# 已知角色列表
KNOWN_CHARACTERS = [
    "悟空", "卡卡罗特", "贝吉塔", "悟饭", "比克", "克林",
    "大特", "特兰克斯", "小特", "布尔玛", "雅木茶", "18号",
    "门德里", "比鲁斯", "维斯", "萨尔佐", "萨玛埃尔"
]

# 内心描写关键词
INNER_THOUGHT_PATTERNS = [
    r"他(?:心中|心里|内心|心想|暗想|暗道)",
    r"她(?:心中|心里|内心|心想|暗想|暗道)",
    r"(?:心中|心里)(?:暗想|想到|明白|清楚|知道)",
    r"他(?:感到|觉得|意识到|明白|知道)",
    r"她(?:感到|觉得|意识到|明白|知道)",
]


def extract_pov_declaration(content: str) -> list:
    """提取章节中的POV声明"""
    pov_patterns = [
        r"【POV[：:]\s*(.+?)】",
        r"POV[：:]\s*(.+?)(?:\n|$)",
        r"\[POV[：:]\s*(.+?)\]",
    ]

    povs = []
    for pattern in pov_patterns:
        matches = re.findall(pattern, content)
        povs.extend(matches)

    return povs


def check_pov_violations(content: str, declared_povs: list) -> list:
    """检测POV越界"""
    issues = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # 检测内心描写
        for pattern in INNER_THOUGHT_PATTERNS:
            matches = re.findall(pattern, line)
            if matches:
                # 检查是否是非POV角色的内心描写
                for char in KNOWN_CHARACTERS:
                    if char in line and char not in ' '.join(declared_povs):
                        issues.append({
                            'line': line_num,
                            'type': 'POV越界',
                            'content': line.strip()[:60],
                            'reason': f"非POV角色'{char}'的内心描写"
                        })
                        break

    return issues


def check_knowledge_boundary(content: str) -> list:
    """检测知识边界越界"""
    issues = []
    lines = content.split('\n')

    # 知识越界关键词
    knowledge_patterns = [
        (r"他不知道的是", "全知视角泄露"),
        (r"她不知道的是", "全知视角泄露"),
        (r"与此同时.*另一边", "可能的视角跳跃"),
        (r"此刻.*正在", "可能的全知描写"),
    ]

    for line_num, line in enumerate(lines, 1):
        for pattern, reason in knowledge_patterns:
            if re.search(pattern, line):
                issues.append({
                    'line': line_num,
                    'type': '知识边界',
                    'content': line.strip()[:60],
                    'reason': reason
                })

    return issues


def validate_file(file_path: str) -> dict:
    """验证单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'error': str(e)}

    # 提取POV声明
    declared_povs = extract_pov_declaration(content)

    # 检测问题
    pov_issues = check_pov_violations(content, declared_povs)
    knowledge_issues = check_knowledge_boundary(content)

    return {
        'declared_povs': declared_povs,
        'pov_issues': pov_issues,
        'knowledge_issues': knowledge_issues,
        'total_issues': len(pov_issues) + len(knowledge_issues)
    }


def print_report(file_path: str, result: dict):
    """打印检测报告"""
    print("\n" + "=" * 60)
    print("POV验证报告")
    print("=" * 60)
    print(f"文件: {file_path}")

    if 'error' in result:
        print(f"错误: {result['error']}")
        return

    print(f"声明的POV: {', '.join(result['declared_povs']) or '未声明'}")
    print("-" * 40)

    if result['pov_issues']:
        print("\n[POV越界问题]")
        for issue in result['pov_issues']:
            print(f"  第{issue['line']}行: {issue['reason']}")
            print(f"    内容: {issue['content']}...")

    if result['knowledge_issues']:
        print("\n[知识边界问题]")
        for issue in result['knowledge_issues']:
            print(f"  第{issue['line']}行: {issue['reason']}")
            print(f"    内容: {issue['content']}...")

    print("\n" + "=" * 60)
    print(f"总计: {result['total_issues']} 处潜在问题")
    print("=" * 60)

    if result['total_issues'] == 0:
        print("[OK] 未发现POV问题")


def main():
    if len(sys.argv) < 2:
        print("用法: python pov_validator.py <章节文件路径>")
        print("示例: python pov_validator.py ../03_正文/卷一_裂痕与回响/第05章_孤独狼嗥.md")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        sys.exit(1)

    result = validate_file(file_path)
    print_report(file_path, result)


if __name__ == "__main__":
    main()
