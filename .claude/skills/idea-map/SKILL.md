---
name: idea-map
description: Generate Canvas visualization of idea concept relationships and thematic associations. Use when visualizing how ideas connect to each other and to theoretical foundations, or when the user mentions "Idea图谱", "想法地图", "生成Idea图谱".
version: 1.0.0
---

# Idea概念关系图谱

生成Inspiration中Idea的可视化概念图谱，展示Idea之间的关联、理论基础和跨领域联系。

## When to Activate（何时启用）

- 用户说"Idea图谱"、"想法地图"、"生成Idea图谱"
- 用户说"可视化想法"、"Idea概念图"
- 用户需要查看Idea之间的关联关系

## 格式参考

**执行前查阅**：
- [json-canvas.md](./ref/json-canvas.md) - 获取 Canvas (.canvas) 格式规范（节点、边、布局）

## 核心执行规则（CRITICAL）

### (CRITICAL) 访问控制
- **ALWAYS** 仅访问 Inspiration 目录
- **NEVER** 访问 IDEA 目录（除非用户明确授权）
- **ALWAYS** 使用 AskUserQuestion 获取授权

### (CRITICAL) 链接有效性
- **ALWAYS** 使用 Glob 精确匹配文件名
- **ALWAYS** 验证链接目标存在
- **NEVER** 直接使用理论名称作为文件路径

### (REQUIRED) 性能考虑
- **RECOMMENDED** Idea超过50个时提示用户筛选

## 核心功能

### 功能1：状态分组图谱
- **用途**：按Idea状态（萌芽/思考中/已实现/已放弃）分组展示
- **布局**：分组布局（Grouped Layout）
- **颜色**：按状态着色

### 功能2：概念关联图谱
- **用途**：基于理论基础、跨领域关联建立语义关联
- **布局**：力导向布局（Force-Directed Layout）
- **边**：虚线表示理论基础，点线表示跨领域

### 功能3：优先级图谱
- **用途**：按Idea优先级和紧急程度展示
- **布局**：优先级布局（Priority Layout）
- **大小**：按优先级调整节点大小

## 工作流程

### Step 1: 扫描Inspiration目录
- 使用 Glob 扫描所有 Idea 笔记
- **ALWAYS** 限制在 Inspiration 目录内

### Step 2: 解析Idea数据
- 使用 Read 读取每个文件
- 提取 Frontmatter：status、priority、related、theoretical_basis、cross_domain
- 构建Idea数据结构

### Step 3: 构建关系图
- 节点：每个Idea + 理论基础
- 边：Idea关联关系、Idea→Theory关系

### Step 4: 计算布局
- 分组布局：按状态分组排列
- 力导向布局：相关节点自然聚集
- 优先级布局：按优先级环形排列

### Step 5: 生成Canvas文件
- 使用 Write 创建 .canvas 文件
- 创建节点：file、text、group 类型
- 创建边：根据关系类型设置样式

### Step 6: 报告结果
- 显示图谱统计信息和关键发现

## GOOD vs BAD（对比示例）

### 示例1：访问控制

#### ✅ GOOD
```python
# 询问用户后访问IDEA目录
user_authorize = ask_user("是否访问IDEA目录？", ["是", "否"])
if user_authorize == "是":
    idea_files = scan_idea_directory()
else:
    idea_files = []
```

#### ❌ BAD
```python
# 直接访问IDEA目录
idea_files = scan_idea_directory()  # 违反访问控制
```

### 示例2：文件名匹配

#### ✅ GOOD
```python
# 使用 Glob 精确匹配理论基础文件名
for theory in idea['theoretical_basis']:
    pattern = f"**/*{theory}*.md"
    matches = glob_search(pattern, recursive=True)
    if matches:
        actual_filename = matches[0]
        create_edge(idea, actual_filename)
```

#### ❌ BAD
```python
# 直接使用理论名称创建链接
create_edge(idea, f"科研/CV/Concepts/{theory}.md")  # 文件名可能不准确
```

### 示例3：节点大小

#### ✅ GOOD
```python
# 根据优先级调整节点大小
def get_node_size(priority):
    sizes = {
        "high": (300, 220),
        "medium": (250, 180),
        "low": (200, 150)
    }
    return sizes.get(priority, (250, 180))
```

#### ❌ BAD
```python
# 固定大小
node['width'] = 250
node['height'] = 180
```

### 示例4：关系强度

#### ✅ GOOD
```python
# 根据关联类型设置边的样式
def get_edge_style(relation_type):
    if relation_type == "related":
        return {"style": "solid", "color": "6"}
    elif relation_type == "based_on":
        return {"style": "dashed", "color": "5"}
    elif relation_type == "cross_domain":
        return {"style": "dotted", "color": "4"}
```

#### ❌ BAD
```python
# 所有边使用相同样式
edge["style"] = "solid"
edge["color"] = "6"
```

## 颜色编码

| 节点类型 | 状态 | 颜色 | 颜色代码 |
|---------|------|------|----------|
| Idea节点 | 萌芽 | 黄色 | "3" |
| Idea节点 | 思考中 | 橙色 | "2" |
| Idea节点 | 已实现 | 绿色 | "4" |
| Idea节点 | 已放弃 | 灰色 | "6" |
| 理论基础 | 核心理论 | 红色 | "1" |
| 理论基础 | 概念笔记 | 蓝色 | "5" |

## 边样式

| 样式 | 说明 | 使用场景 |
|------|------|----------|
| 实线 | 强关联 | 直接相关的Idea |
| 虚线 | 理论基础 | Idea→理论基础 |
| 点线 | 弱关联/跨领域 | 可能的相关性 |

## 节点大小

| 优先级 | 宽度 | 高度 |
|--------|------|------|
| high | 300 | 220 |
| medium | 250 | 180 |
| low | 200 | 150 |

## 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| scope | Idea范围 | 否 | Inspiration全部 |
| type | 图谱类型 | 否 | status |
| filter | 筛选条件 | 否 | - |

## 快速参考表

| 图谱类型 | 布局算法 | 用途 |
|----------|----------|------|
| 状态分组 | 分组布局 | 清晰展示状态分布 |
| 概念关联 | 力导向布局 | 发现主题簇和关联 |
| 优先级 | 优先级布局 | 突出重要Idea |

## 布局算法参数

### 分组布局
- `GROUP_SPACING` = 600
- `NODE_SPACING` = 400
- `GROUP_PADDING` = 100

### 力导向布局
- `REPULSION_STRENGTH` = 1500
- `ATTRACTION_STRENGTH` = 0.05
- `MAX_ITERATIONS` = 1000

### 优先级布局
- `HIGH_PRIORITY_RADIUS` = 300
- `MEDIUM_PRIORITY_RADIUS` = 700
- `LOW_PRIORITY_RADIUS` = 1200

## Frontmatter规范

Idea笔记应包含以下字段：

```yaml
---
title: Idea标题
status: sprout | thinking | implemented | abandoned
priority: high | medium | low
theme: 主题名称
related:
  - 相关Idea1
theoretical_basis:
  - 理论基础笔记1
cross_domain:
  - 跨领域关联1
tags:
  - #领域/子领域
---
```

## 文件保存

### 命名规则
- 默认：`Idea概念图谱.canvas`
- 状态：`Idea_{状态}图谱.canvas`
- 主题：`Idea_{主题}图谱.canvas`

### 保存位置
- `Inspiration/` 目录根目录
- 或 `Inspiration/2024/` 当前年份目录
