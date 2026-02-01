# `/idea-tracker` - Idea状态管理追踪

创建 Obsidian Bases 仪表盘，用于追踪和管理研究 Idea 的状态和进展。

## 与 obsidian-bases 的关系

obsidian-bases 是**格式参考**技能，提供完整的 Bases (.base) 语法规范文档。

本技能是**工作流封装**，组合 Read/Write/Edit 工具创建符合规范的 .base 文件。

## 功能说明

### 核心功能

- **状态追踪**：按状态（萌芽、思考中、已实现、已放弃）分组展示
- **主题分类**：按研究领域或主题自动分类
- **时间追踪**：计算 Idea 存在时长、最后更新时间
- **行动建议**：根据状态和时间自动生成行动建议

### 支持的视图

| 视图类型 | 说明 | 用途 |
|---------|------|------|
| Table | 表格视图 | 详细列表，支持排序和筛选 |
| Cards | 卡片视图 | 展示 Idea 概览 |
| List | 列表视图 | 简洁列表 |

## 前置条件

### Idea 笔记 Frontmatter 要求

Idea 笔记需要包含以下属性：

```yaml
---
title: "Idea 标题"
status: sprout | thinking | implemented | abandoned
date: YYYY-MM-DD
tags: ["CV", "Generation", "Diffusion"]
theme: "生成模型"  # 研究主题
difficulty: easy | medium | hard  # 实现难度
feasibility: high | medium | low  # 可行性
priority: high | medium | low  # 优先级
related_papers: ["论文1", "论文2"]  # 相关论文
created_date: 2024-01-15  # 创建日期
updated_date: 2024-01-20  # 最后更新日期
next_action: "查阅相关文献"  # 下一步行动
---
```

## Base 文件结构

### 完整示例

```yaml
filters:
  or:
    - file.inFolder("Inspiration")
    - file.inFolder("科研/IDEA")

formulas:
  # 状态图标
  status_icon: 'if(status == "sprout", "🌱", if(status == "thinking", "🤔", if(status == "implemented", "✅", "❌")))'

  # 状态标签（中文）
  status_label: 'if(status == "sprout", "萌芽", if(status == "thinking", "思考中", if(status == "implemented", "已实现", "已放弃")))'

  # 优先级图标
  priority_icon: 'if(priority == "high", "🔴", if(priority == "medium", "🟡", "🟢"))'

  # 难度图标
  difficulty_icon: 'if(difficulty == "easy", "😊", if(difficulty == "medium", "🙂", "😰"))'

  # 可行性图标
  feasibility_icon: 'if(feasibility == "high", "✅", if(feasibility == "medium", "⚠️", "❌"))'

  # Idea 存在天数
  days_since_created: 'if(created_date, ((now() - date(created_date)) / 86400000).round(0), "")'

  # 最后更新距今天数
  days_since_updated: 'if(updated_date, ((now() - date(updated_date)) / 86400000).round(0), "")'

  # 是否需要关注（超过7天未更新且状态为思考中）
  needs_attention: 'status == "thinking" && updated_date && (now() - date(updated_date)) > "7d"'

  # 是否为长期萌芽（超过30天仍是萌芽状态）
  long_sprout: 'status == "sprout" && created_date && (now() - date(created_date)) > "30d"'

  # 相关论文数量
  related_count: 'if(related_papers, related_papers.length, 0)'

  # 相关论文列表（格式化）
  related_list: 'if(related_papers, related_papers.join(", "), "")'

  # 行动建议（自动生成）
  action_suggestion: 'if(status == "sprout", "补充理论基础和文献调研", if(status == "thinking", if(days_since_updated > 7, "需要更新进展", "持续推进"), if(status == "implemented", "总结经验和写论文", "记录失败原因")))'

  # 颜色编码（用于卡片视图）
  status_color: 'if(status == "sprout", "#ffd700", if(status == "thinking", "#ffa500", if(status == "implemented", "#90ee90", "#a9a9a9")))'

properties:
  status:
    displayName: 状态
  formula.status_icon:
    displayName: ""
  formula.status_label:
    displayName: 状态
  formula.priority_icon:
    displayName: 优先级
  formula.difficulty_icon:
    displayName: 难度
  formula.feasibility_icon:
    displayName: 可行性
  theme:
    displayName: 主题
  difficulty:
    displayName: 难度
  feasibility:
    displayName: 可行性
  priority:
    displayName: 优先级
  formula.days_since_created:
    displayName: 存在天数
  formula.days_since_updated:
    displayName: 更新距今
  formula.related_count:
    displayName: 相关论文
  next_action:
    displayName: 下一步行动
  created_date:
    displayName: 创建日期
  updated_date:
    displayName: 更新日期

summaries:
  total_ideas: 'values.length'
  sprout_count: 'values.filter(v => v == "sprout").length'
  thinking_count: 'values.filter(v => v == "thinking").length'
  implemented_count: 'values.filter(v => v == "implemented").length'
  abandoned_count: 'values.filter(v => v == "abandoned").length'

views:
  # 视图1：按状态分组
  - type: table
    name: "状态总览"
    groupBy:
      property: status
      direction: ASC
    order:
      - formula.status_icon
      - file.name
      - formula.priority_icon
      - formula.days_since_updated
      - theme
      - next_action
    summaries:
      formula.days_since_created: Average
      formula.related_count: Sum

  # 视图2：萌芽 Idea
  - type: table
    name: "萌芽中的 Idea"
    filters:
      and:
        - 'status == "sprout"'
    order:
      - formula.priority_icon
      - created_date
      - file.name
      - theme
    groupBy:
      property: priority
      direction: ASC

  # 视图3：思考中
  - type: table
    name: "思考中的 Idea"
    filters:
      and:
        - 'status == "thinking"'
    order:
      - formula.days_since_updated
      - file.name
      - formula.priority_icon
      - next_action
      - formula.feasibility_icon

  # 视图4：需要关注
  - type: table
    name: "需要关注（超过7天未更新）"
    filters:
      and:
        - formula.needs_attention
    order:
      - formula.days_since_updated
      - file.name
      - next_action

  # 视图5：长期萌芽
  - type: table
    name: "长期萌芽（超过30天）"
    filters:
      and:
        - formula.long_sprout
    order:
      - formula.days_since_created
      - file.name
      - theme

  # 视图6：已实现
  - type: table
    name: "已实现的 Idea"
    filters:
      and:
        - 'status == "implemented"'
    order:
      - updated_date
      - file.name
      - theme

  # 视图7：已放弃
  - type: table
    name: "已放弃的 Idea"
    filters:
      and:
        - 'status == "abandoned"'
    order:
      - updated_date
      - file.name

  # 视图8：高优先级
  - type: table
    name: "高优先级 Idea"
    filters:
      and:
        - 'priority == "high"'
    order:
      - status
      - file.name
      - formula.days_since_updated

  # 视图9：按主题分组
  - type: table
    name: "主题分类"
    groupBy:
      property: theme
      direction: ASC
    order:
      - theme
      - file.name
      - status
      - formula.priority_icon

  # 视图10：高可行性
  - type: table
    name: "高可行性 Idea"
    filters:
      and:
        - 'feasibility == "high"'
        - 'status != "implemented"'
        - 'status != "abandoned"'
    order:
      - formula.priority_icon
      - file.name
      - difficulty

  # 视图11：卡片视图
  - type: cards
    name: "Idea 卡片"
    order:
      - cover
      - file.name
      - formula.status_icon
      - theme
      - formula.action_suggestion

  # 视图12：行动清单
  - type: list
    name: "行动清单"
    filters:
      and:
        - 'status != "implemented"'
        - 'status != "abandoned"'
        - next_action
    order:
      - formula.priority_icon
      - file.name
      - next_action

  # 视图13：Inspiration 目录（临时）
  - type: table
    name: "Inspiration 临时 Idea"
    filters:
      and:
        - file.inFolder("Inspiration")
    order:
      - created_date
      - file.name
      - formula.status_icon

  # 视图14：统计汇总
  - type: table
    name: "统计汇总"
    groupBy:
      property: status
      direction: ASC
    order:
      - formula.status_label
      - formula.status_label
    summaries:
      file.name: Count
      formula.days_since_created: Average
      formula.related_count: Sum
```

## 执行流程

### 1. 扫描 Idea 目录

使用 Glob 工具扫描 Inspiration 和 IDEA 目录：

```python
# 扫描 Inspiration 目录
inspiration_pattern = "Inspiration/**/*.md"
inspiration_ideas = glob.glob(inspiration_pattern, recursive=True)

# 扫描 IDEA 目录（需要授权）
idea_pattern = "科研/IDEA/**/*.md"
idea_ideas = glob.glob(idea_pattern, recursive=True)
```

### 2. 检查 Frontmatter 完整性

检查每个 Idea 笔记是否包含必要的属性：
- `status`: Idea 状态
- `priority`: 优先级
- `theme`: 研究主题
- `difficulty`: 实现难度
- `feasibility`: 可行性
- `created_date`: 创建日期
- `updated_date`: 更新日期

### 3. 生成 Base 文件

使用 Write 工具创建 `.base` 文件：

```yaml
# 文件路径：Inspiration/Idea追踪.base
# 或：科研/CV/Idea追踪.base

filters:
  or:
    - file.inFolder("Inspiration")
    - file.inFolder("科研/IDEA")

formulas:
  # ... 公式定义

views:
  # ... 视图定义
```

### 4. 嵌入到索引笔记

在索引笔记中嵌入 Base 文件：

```markdown
## Idea 状态追踪

### 总览

![[Idea追踪.base#状态总览]]

### 需要关注

![[Idea追踪.base#需要关注（超过7天未更新）]]

### 行动清单

![[Idea追踪.base#行动清单]]
```

## 使用场景

### 场景1：捕获新 Idea

1. 使用 `/idea-capture` 在 Inspiration 目录创建 Idea
2. 设置 `status: sprout`
3. 在仪表盘中跟踪进展

### 场景2：推进 Idea 状态

1. 查看"萌芽中的 Idea"或"思考中的 Idea"
2. 选择要推进的 Idea
3. 更新状态和 `updated_date`
4. 在仪表盘中查看变化

### 场景3：定期回顾

1. 查看"需要关注"视图
2. 查看"长期萌芽"视图
3. 决定是推进、放弃还是实现
4. 记录决策和原因

### 场景4：主题研究

1. 查看"主题分类"视图
2. 按主题查看所有 Idea
3. 发现同一主题下的多个 Idea
4. 考虑合并或聚焦

## 配置选项

### 目录配置

默认扫描 `Inspiration/` 和 `科研/IDEA/` 目录：
- `--inspiration-dir`: Inspiration 目录路径
- `--idea-dir`: IDEA 目录路径（需要授权）

### 状态配置

支持自定义状态枚举：
- 默认：sprout（萌芽）、thinking（思考中）、implemented（已实现）、abandoned（已放弃）
- 可添加新状态或修改现有状态

### 优先级配置

支持自定义优先级级别：
- 默认：high（高）、medium（中）、low（低）

### 颜色配置

可自定义状态颜色编码：
- 萌芽：黄色 (#ffd700)
- 思考中：橙色 (#ffa500)
- 已实现：绿色 (#90ee90)
- 已放弃：灰色 (#a9a9a9)

## 注意事项

1. **访问控制**：IDEA 目录需要授权才能访问
2. **Frontmatter 一致性**：确保所有 Idea 使用相同的属性名称
3. **日期格式**：使用 YYYY-MM-DD 格式
4. **状态更新**：推进 Idea 时及时更新 `updated_date`
5. **行动建议**：定期更新 `next_action` 字段

## 相关技能

- `/idea-capture` - 捕获 Idea
- `/idea-organize` - 整理 Idea
- `/idea-review` - 回顾 Idea
- `/idea-map` - Idea 概念关系图谱
