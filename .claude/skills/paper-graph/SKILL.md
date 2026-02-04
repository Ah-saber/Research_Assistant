---
name: paper-graph
description: Generate Canvas visualization of paper citation relationships and thematic associations. Use when visualizing how papers cite each other, or when the user mentions "论文图谱", "论文关系图", "生成论文图谱".
version: 1.0.0
---

# 论文引用关系图谱

生成论文引用关系的可视化Canvas图谱，展示论文之间的引用、主题关联和跨领域联系。

## When to Activate（何时启用）

- 用户说"论文图谱"、"论文关系图"、"生成论文图谱"
- 用户说"论文引用网络"、"可视化论文关系"
- 用户需要查看论文之间的引用关系

## 格式参考

**执行前查阅**：
- [json-canvas.md](./ref/json-canvas.md) - 获取 Canvas (.canvas) 格式规范（节点、边、布局）

## 核心执行规则（CRITICAL）

### (CRITICAL) 链接有效性
- **ALWAYS** 使用 Glob 精确匹配文件名
- **ALWAYS** 验证链接目标存在
- **NEVER** 直接使用论文标题作为文件路径

### (CRITICAL) 布局质量
- **ALWAYS** 避免节点重叠
- **ALWAYS** 保持适当间距
- **ALWAYS** 使用合适的节点大小

### (REQUIRED) 性能考虑
- **RECOMMENDED** 论文超过50篇时提示用户筛选

## 核心功能

### 功能1：直接引用图谱
- **用途**：展示论文之间的直接引用关系
- **布局**：层次布局（Hierarchical Layout）
- **边**：有向边表示引用方向

### 功能2：主题关联图谱
- **用途**：基于主题、方法、应用场景建立关联
- **布局**：力导向布局（Force-Directed Layout）
- **边**：虚线表示主题关联

### 功能3：时间演进图谱
- **用途**：按发表时间展示论文发展脉络
- **布局**：时间线布局（Timeline Layout）
- **轴**：横轴表示时间，纵轴表示主题分类

## 工作流程

### Step 1: 确定论文范围
- 使用 Glob 扫描指定范围
- 按目录扫描或按标签筛选
- 提示用户确认范围

### Step 2: 收集论文数据
- 使用 Read 读取每个论文笔记
- 提取 Frontmatter：title、citations、related、tags
- 构建论文数据结构

### Step 3: 分析引用关系
- 构建引用图
- 识别关键节点（被引用最多的论文）
- 识别桥梁论文（连接不同主题）

### Step 4: 计算布局
- 层次布局：按引用深度分层
- 力导向布局：相关节点自然聚集
- 时间线布局：按时间排列

### Step 5: 生成Canvas文件
- 使用 Write 创建 .canvas 文件
- 创建节点：file、group 类型
- 创建边：根据关系类型设置样式

### Step 6: 报告结果
- 显示生成的图谱统计信息
- 提供文件路径

## GOOD vs BAD（对比示例）

### 示例1：文件名匹配

#### ✅ GOOD
```python
# 使用 Glob 精确匹配文件名
pattern = f"**/Paper/**/*{paper_title}*.md"
matches = glob_search(pattern, recursive=True)
if matches:
    actual_filename = matches[0]
    node['file'] = actual_filename
```

#### ❌ BAD
```python
# 直接使用论文标题作为文件名
node['file'] = f"科研/CV/Paper/{paper_title}.md"  # 文件名可能不准确
```

### 示例2：布局算法

#### ✅ GOOD
```python
# 层次布局避免重叠
def hierarchical_layout(papers):
    root = find_root_papers(papers)
    levels = build_levels(root)
    positions = {}
    for level_idx, level in enumerate(levels):
        y = level_idx * VERTICAL_SPACING  # 400px 间距
        for node_idx, node in enumerate(level):
            x = (node_idx - len(level)/2) * HORIZONTAL_SPACING
            positions[node] = (x, y)
    return positions
```

#### ❌ BAD
```python
# 简单排列可能导致重叠
for i, paper in enumerate(papers):
    paper.x = i * 200  # 间距太小
    paper.y = 0  # 所有节点在同一行
```

### 示例3：颜色编码

#### ✅ GOOD
```python
# 清晰的颜色编码
def get_node_color(paper):
    if paper.importance == "core":
        return "1"  # 红色
    elif paper.importance == "important":
        return "2"  # 橙色
    elif paper.importance == "extension":
        return "3"  # 黄色
    else:
        return "4"  # 绿色
```

#### ❌ BAD
```python
# 没有颜色区分或使用随机颜色
node['color'] = random.choice(["1", "2", "3", "4", "5", "6"])
```

### 示例4：节点大小

#### ✅ GOOD
```python
# 根据重要性调整节点大小
def get_node_size(paper):
    if paper.importance == "core":
        return (350, 250)  # 宽, 高
    elif paper.importance == "important":
        return (300, 200)
    else:
        return (250, 180)
```

#### ❌ BAD
```python
# 固定大小
node['width'] = 300
node['height'] = 200
```

## 颜色编码

| 颜色 | 说明 | 颜色代码 |
|------|------|----------|
| 红色 | 核心/奠基论文 | "1" |
| 橙色 | 重要进展 | "2" |
| 黄色 | 扩展工作 | "3" |
| 绿色 | 应用论文 | "4" |
| 青色 | 分组背景 | "5" |
| 灰色 | 辅助说明 | "6" |

## 边样式

| 样式 | 说明 | 使用场景 |
|------|------|----------|
| 实线箭头 | 直接引用 | A引用B |
| 虚线 | 主题关联 | 相同主题但无直接引用 |
| 点线 | 跨领域关联 | 跨领域的概念联系 |

## 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| scope | 论文范围 | 否 | 全部 |
| type | 图谱类型 | 否 | citation |
| depth | 分析深度 | 否 | 直接引用 |

## 快速参考表

| 图谱类型 | 布局算法 | 用途 |
|----------|----------|------|
| 直接引用 | 层次布局 | 展示引用方向和传承关系 |
| 主题关联 | 力导向布局 | 发现主题簇和关联 |
| 时间演进 | 时间线布局 | 展示发展脉络 |

## 布局算法参数

### 层次布局
- `VERTICAL_SPACING` = 400
- `HORIZONTAL_SPACING` = 500
- `NODE_WIDTH` = 300
- `NODE_HEIGHT` = 200

### 力导向布局
- `REPULSION_STRENGTH` = 1000
- `ATTRACTION_STRENGTH` = 0.1
- `MAX_ITERATIONS` = 500

### 时间线布局
- `TIME_SCALE` = 100（每年像素）
- `THEME_HEIGHT` = 300
- `TIME_START` = 最早论文年份

## 文件保存

### 命名规则
- 默认：`论文关系图谱.canvas`
- 主题：`{主题}论文图谱.canvas`
- 目录：`{目录名}/00-论文图谱.canvas`

### 保存位置
- 与论文同一目录
- 或专门的图谱目录
- 或 Conclusion 目录
