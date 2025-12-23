"""
简报生成器
根据大纲自动生成章节创作简报初稿
"""

import os
import sys
from datetime import datetime


def generate_briefing(volume: int, chapter: int, outline_content: str = None):
    """生成章节创作简报"""

    briefing = f"""# 章节创作简报

> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 一、章节基本信息

### 1. 章节编号
第 {chapter} 章

### 2. 章节名（暂定）
[待填写]

### 3. 本章关键词
- [关键词1]
- [关键词2]
- [关键词3]

### 4. 主要 POV 与顺序
- POV1：[角色名]
- POV2：[无/角色名]

---

## 二、上下文与本章任务

### 1. 上文简要承接
[上一章的结尾是什么]

### 2. 下文简要预告
[本章结束后，大方向要走向哪里]

### 3. 本章核心任务（逻辑层）
- [任务1]
- [任务2]
- [任务3]

### 4. 本章核心事件列表
1. [事件1]
2. [事件2]
3. [事件3]

---

## 三、场景与镜头（骨架级）

### 场景一
- **场景名**：[名称]
- **场景功能**：[功能描述]
- **氛围标签**：[压抑/紧张/温馨/...]

### 场景二
- **场景名**：[名称]
- **场景功能**：[功能描述]
- **氛围标签**：[氛围]

---

## 四、角色弧光与语言要求

### 1. 本章关键角色弧光
- [角色名]：从 [起点] → [终点]

### 2. 语言风格 / 句式指纹使用提示
- 参考 `02_人物设定/[阵营]/[角色].md` 中的句式指纹
- 本章是否需要刻意打破：[是/否]

### 3. 预期高光句（可选）
- "[高光台词]"

---

## 五、反 AI 味 & 约束提示

### 1. 本章禁止项
- 禁止使用"没有 XX，没有 XX"句式
- 禁止使用"世界仿佛被按下XX键"比喻
- 禁止出现赛博朋克、新生人、芯片等后传词汇

### 2. 信息量约束
- [本章的信息密度要求]

### 3. 长度与节奏提示
- [长度建议]
- [节奏建议]

---

## 六、给 AI 的执行指令

### 执行 1
按本简报生成章节草稿时：
- 优先完成「本章核心任务」中的要点
- 其余细节与过渡由模型自行填充，但不得违反禁止项

### 执行 2
生成后自动进行一次自查：
1. 是否有视角越界？
2. 是否出现解释型总结句？
3. 是否使用了被列入黑名单的比喻/句式？

### 执行 3
如需补足信息，请优先从以下文档中抽取：
- `00_核心文档/创作圣经.md`
- `00_核心文档/附录_进度蒸馏.md`
- `02_人物设定/[相关角色].md`

---

*请根据实际需求修改上述内容后，再让 AI 生成章节草稿*
"""

    return briefing


def main():
    if len(sys.argv) < 3:
        print("用法: python briefing_generator.py --volume <卷号> --chapter <章节号>")
        print("示例: python briefing_generator.py --volume 2 --chapter 20")
        sys.exit(1)

    volume = None
    chapter = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--volume' and i + 1 < len(sys.argv):
            volume = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--chapter' and i + 1 < len(sys.argv):
            chapter = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    if volume is None or chapter is None:
        print("错误: 请指定 --volume 和 --chapter 参数")
        sys.exit(1)

    briefing = generate_briefing(volume, chapter)

    # 输出文件名
    output_file = f"简报_第{chapter:02d}章.md"
    output_dir = f"04_创作简报/卷{['一', '二', '三', '四'][volume - 1]}"

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(briefing)

    print(f"✓ 简报已生成: {output_path}")
    print("\n请根据实际需求修改简报内容后，再让 AI 生成章节草稿。")


if __name__ == "__main__":
    main()
