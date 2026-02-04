---
name: knowledge-canvas
description: Generate comprehensive knowledge canvas integrating papers, ideas, and concept notes. Use when creating a complete visual overview of a research topic, or when the user mentions "知识画布", "研究图谱", "生成知识画布".
version: 1.0.0
---

# 综合知识画布

创建综合研究主题画布，整合论文、Idea、概念笔记等多种内容类型，形成完整的知识可视化视图。

## When to Activate（何时启用）

- 用户说"知识画布"、"研究图谱"、"生成知识画布"
- 用户说"综合知识图谱"、"研究主题画布"
- 用户需要整合多种内容类型的可视化

## 格式参考

**执行前查阅**：
- [json-canvas.md](./ref/json-canvas.md) - 获取 Canvas (.canvas) 格式规范（节点、边、布局）

## 核心执行规则（CRITICAL）

### (CRITICAL) 访问控制
- **ALWAYS** Idea数据仅从 Inspiration 目录获取
- **NEVER** 访问 IDEA 目录（除非用户明确授权）
- **ALWAYS** 使用 AskUserQuestion 获取授权

### (CRITICAL) 链接有效性
- **ALWAYS** 使用 Glob 精确匹配文件名
- **ALWAYS** 验证链接目标存在
- **NEVER** 直接使用标题作为文件路径

### (REQUIRED) 内容量控制
- **RECOMMENDED** 论文超过30篇时提示用户筛选
- **RECOMMENDED** Idea超过20个时按状态筛选

## 核心功能

### 功能1：研究主题画布
- **用途**：以特定研究主题为中心整合相关内容
- **布局**：区域布局（Zoned Layout）
- **区域**：左侧论文区、右上Idea区、右下概念区、中心问题区

### 功能2：领域全景画布
- **用途**：展示整个研究领域的知识图谱
- **布局**：分层布局（Layered Layout）
- **层次**：顶层领域概览、中层子领域、底层具体内容

### 功能3：项目知识画布
- **用途**：围绕特定研究项目的知识管理
- **布局**：中心辐射布局（Hub-and-Spoke Layout）
- **中心**：项目核心问题

## 工作流程

### Step 1: 确定研究主题
- 用户指定主题
- 支持的主题：扩散模型、注意力机制、图像编辑等

### Step 2: 收集相关内容
- 使用 Glob 和 Read 搜索和提取
- 按目录扫描：Paper、Inspiration、Concepts
- 按标签或主题字段筛选

### Step 3: 构建知识图谱
- 创建节点：论文、Idea、概念、问题
- 创建边：跨类型关联
- 论文→论文（引用）、Idea→论文（基于）、Idea→概念（涉及）

### Step 4: 计算布局
- 区域布局：四个区域明确分隔
- 分层布局：层次清晰
- 中心辐射：核心问题居中

### Step 5: 生成Canvas文件
- 使用 Write 创建 .canvas 文件
- 创建节点：file、text、group 类型
- 创建边：跨类型关联

### Step 6: 报告结果
- 显示内容统计、区域说明和关键发现

## GOOD vs BAD（对比示例）

### 示例1：多数据源整合

#### ✅ GOOD
```python
# 分别处理不同类型，统一数据格式
papers = collect_papers(theme)
ideas = collect_ideas(theme)
concepts = collect_concepts(theme)

all_nodes = []
all_nodes.extend(format_as_paper_nodes(papers))
all_nodes.extend(format_as_idea_nodes(ideas))
all_nodes.extend(format_as_concept_nodes(concepts))
```

#### ❌ BAD
```python
# 混合处理不同类型
for item in all_items:
    if item.type == "paper":
        # 论文处理
    elif item.type == "idea":
        # Idea处理
    # 类型判断混乱，容易出错
```

### 示例2：区域布局

#### ✅ GOOD
```python
# 清晰的区域划分
def zoned_layout(papers, ideas, concepts):
    positions = {}
    # 左侧：论文区
    for i, paper in enumerate(papers):
        paper.x = -800
        paper.y = (i - len(papers)/2) * VERTICAL_SPACING
        positions[paper] = (paper.x, paper.y)
    # 右上：Idea区
    for i, idea in enumerate(ideas):
        row = i // 3
        col = i % 3
        idea.x = 400 + col * 300
        idea.y = -400 + row * 250
        positions[idea] = (idea.x, idea.y)
    return positions
```

#### ❌ BAD
```python
# 随机分布
for node in nodes:
    node.x = random.randint(-1000, 1000)
    node.y = random.randint(-500, 500)
```

### 示例3：跨类型关联

#### ✅ GOOD
```python
# 明确的关联类型
def create_cross_type_edges(ideas, papers, concepts):
    edges = []
    # Idea → 论文（基于）
    edges.extend(create_idea_paper_edges(ideas, papers))
    # Idea → 概念（涉及）
    edges.extend(create_idea_concept_edges(ideas, concepts))
    # 论文 → 论文（引用）
    edges.extend(create_paper_paper_edges(papers))
    return edges
```

#### ❌ BAD
```python
# 混乱的关联逻辑
for item1 in all_items:
    for item2 in all_items:
        if is_related(item1, item2):
            create_edge(item1, item2)  # 关联不清晰
```

### 示例4：链接验证

#### ✅ GOOD
```python
# 验证所有链接目标存在
for edge in edges:
    target_file = edge.to_node.file
    if not file_exists(target_file):
        # 移除无效链接或添加警告
        remove_edge(edge)
```

#### ❌ BAD
```python
# 直接创建链接不验证
create_edge(source, target)  # 目标可能不存在
```

## 区域划分

| 区域 | 位置 | 内容 | 布局 |
|------|------|------|------|
| 核心论文区 | 左侧 | 主题相关论文 | 层次布局 |
| Idea区 | 右上 | 相关Idea | 按状态分组 |
| 概念笔记区 | 右下 | 概念定义 | 网格布局 |
| 问题区 | 中心 | 核心问题/TODO | 文本节点 |

## 节点颜色编码

| 节点类型 | 颜色 | 颜色代码 |
|---------|------|----------|
| 论文（核心） | 红色 | "1" |
| 论文（重要） | 橙色 | "2" |
| Idea（萌芽） | 黄色 | "3" |
| Idea（思考中） | 橙色 | "2" |
| Idea（已实现） | 绿色 | "4" |
| 概念 | 蓝色 | "5" |
| 分组背景 | 青色 | "5" |

## 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| theme | 研究主题 | 是 | - |
| scope | 内容范围 | 否 | 全部 |
| type | 画布类型 | 否 | theme |

## 快速参考表

| 画布类型 | 布局算法 | 用途 |
|----------|----------|------|
| 研究主题 | 区域布局 | 整合论文、Idea、概念 |
| 领域全景 | 分层布局 | 展示整个领域知识图谱 |
| 项目画布 | 中心辐射 | 围绕项目核心问题 |

## 布局算法参数

### 区域布局
- `PAPER_ZONE_X` = -800
- `IDEA_ZONE_X` = 400
- `IDEA_ZONE_Y` = -400
- `CONCEPT_ZONE_X` = 400
- `CONCEPT_ZONE_Y` = 100
- `VERTICAL_SPACING` = 400

### 分层布局
- `LAYER_SPACING` = 600
- `GROUP_SPACING` = 800
- `NODE_SPACING` = 400

### 中心辐射布局
- `CENTER_X` = 0
- `CENTER_Y` = 0
- `FIRST_LAYER_RADIUS` = 400
- `SECOND_LAYER_RADIUS` = 800

## 内容筛选策略

### 论文筛选
```python
def filter_papers(theme):
    # 方法1：标签匹配
    if has_tag(theme):
        return True
    # 方法2：标题关键词
    if keyword_in_title(theme):
        return True
    # 方法3：Frontmatter主题字段
    if metadata.get('theme') == theme:
        return True
    return False
```

### Idea筛选
```python
def filter_ideas(theme):
    # 方法1：主题字段
    if metadata.get('theme') == theme:
        return True
    # 方法2：标签匹配
    if has_tag(theme):
        return True
    # 方法3：理论基础关联
    if is_related_to_theme(theory, theme):
        return True
    return False
```

## 文件保存

### 命名规则
- 研究主题：`{主题}知识画布.canvas`
- 领域全景：`{领域}全景画布.canvas`
- 项目画布：`{项目名}项目画布.canvas`

### 保存位置
- 与内容同目录
- 或专门的画布目录
- 或 Conclusion 目录
