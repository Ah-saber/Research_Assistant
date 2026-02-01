# /paper-graph - 论文引用关系图谱

## 触发词
- "论文图谱"
- "论文关系图"
- "生成论文图谱"
- "论文引用网络"
- "可视化论文关系"

## 功能描述
生成论文引用关系的可视化Canvas图谱，展示论文之间的引用、主题关联和跨领域联系。

## 图谱类型

### 1. 直接引用图谱
展示论文之间的直接引用关系，使用有向边表示引用方向。

**布局算法**：层次布局（Hierarchical Layout）
- 根节点（被引用最多的论文）在顶部或中心
- 子节点按引用深度分层排列
- 箭头从引用论文指向被引用论文

### 2. 主题关联图谱
基于论文的主题、方法、应用场景建立关联，不限于直接引用。

**布局算法**：力导向布局（Force-Directed Layout）
- 相似主题的论文自然聚集
- 跨领域关联用虚线表示

### 3. 时间演进图谱
按发表时间展示论文的发展脉络。

**布局算法**：时间线布局（Timeline Layout）
- 横轴表示时间
- 纵轴表示主题分类
- 连线表示传承关系

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| scope | 论文范围（目录/标签/搜索结果） | 否 |
| type | 图谱类型（citation/theme/timeline） | 否，默认citation |
| depth | 分析深度（直接引用/主题关联/跨领域） | 否，默认直接引用 |
| layout | 布局算法（hierarchical/force/timeline） | 否，根据type自动选择 |

## 输出格式

### Canvas文件结构

```json
{
  "nodes": [
    {
      "id": "paper1",
      "type": "file",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 200,
      "file": "科研/CV/Paper/DDPM.md",
      "color": "1"
    },
    {
      "id": "group1",
      "type": "group",
      "x": -50,
      "y": -50,
      "width": 700,
      "height": 300,
      "label": "扩散模型基础",
      "color": "5"
    },
    {
      "id": "text1",
      "type": "text",
      "x": 400,
      "y": 100,
      "width": 200,
      "height": 100,
      "text": "核心概念：去噪过程"
    }
  ],
  "edges": [
    {
      "id": "edge1",
      "fromNode": "paper1",
      "toNode": "paper2",
      "fromEnd": "arrow",
      "toEnd": "none",
      "label": "based on",
      "color": "6"
    }
  ]
}
```

### 节点类型

| 类型 | 说明 | 用途 |
|------|------|------|
| file | 文件节点 | 链接到论文笔记或PDF |
| group | 分组节点 | 按研究领域分组 |
| text | 文本节点 | 标注核心概念或说明 |

### 边样式

| 样式 | 说明 | 使用场景 |
|------|------|----------|
| 实线箭头 | 直接引用 | A引用B |
| 虚线 | 主题关联 | 相同主题但无直接引用 |
| 点线 | 跨领域关联 | 跨领域的概念联系 |

### 颜色编码

| 颜色 | 说明 | 颜色代码 |
|------|------|----------|
| 红色 | 核心/奠基论文 | "1" |
| 橙色 | 重要进展 | "2" |
| 黄色 | 扩展工作 | "3" |
| 绿色 | 应用论文 | "4" |
| 青色 | 分组背景 | "5" |
| 灰色 | 辅助说明 | "6" |

## 数据来源

### 1. 从Zotero获取
使用Zotero MCP工具搜索和获取论文元数据：
- `zotero_search_items` - 搜索论文
- `zotero_get_item_metadata` - 获取引用关系（如果可用）
- `zotero_semantic_search` - 语义搜索相关论文

### 2. 从Obsidian笔记获取
扫描论文笔记，解析Frontmatter和内容：
- `related`字段 - 相关论文
- `citations`字段 - 引用的论文
- 标签 - 主题分类
- 内容中的Wikilink - 链接关系

### 3. 引用关系推断
基于论文内容推断引用关系：
- 相似的方法论
- 共同的核心概念
- 明确的"based on"、"extends"等表述

## 工作流程

### 步骤1：确定论文范围
```
用户可指定：
- 特定目录（如：科研/CV/Generate/Paper/）
- 标签筛选（如：#CV/Generation/Diffusion）
- 搜索关键词
- Zotero搜索结果
```

### 步骤2：收集论文数据
```
1. 扫描指定范围的论文笔记
2. 解析Frontmatter获取元数据
3. 提取引用关系（related字段、Wikilink）
4. 从Zotero补充元数据（如果需要）
```

### 步骤3：分析关系
```
1. 构建引用图
   - 节点：每篇论文
   - 边：引用关系

2. 识别关键节点
   - 被引用次数最多的论文
   - 连接不同主题的桥梁论文

3. 主题聚类
   - 基于标签和内容
   - 识别研究主题分组
```

### 步骤4：计算布局
```
层次布局算法（论文引用）：

function hierarchical_layout(papers):
    # 构建引用树
    root = find_root_papers(papers)  # 被引用最多的论文
    levels = build_levels(root)      # 按引用深度分层

    # 计算坐标
    VERTICAL_SPACING = 400
    HORIZONTAL_SPACING = 500

    for level_idx, level in enumerate(levels):
        y = level_idx * VERTICAL_SPACING
        for node_idx, node in enumerate(level):
            x = (node_idx - len(level)/2) * HORIZONTAL_SPACING
            node.position = (x, y)
```

### 步骤5：生成Canvas
```
1. 创建节点（论文、分组、文本）
2. 创建边（引用关系）
3. 设置颜色和样式
4. 保存为.canvas文件
```

### 步骤6：报告结果
```
报告内容：
- Canvas文件路径
- 论文数量
- 引用关系统计
- 关键论文识别
- 主题分组说明
```

## 使用方式

### 方式1：目录范围
```bash
用户: /paper-graph 科研/CV/Generate/Paper/

你: 正在分析论文引用关系...

✓ 扫描17篇论文
✓ 分析引用关系
✓ 构建引用图谱
✓ 计算布局

## 图谱生成完成

**文件**: 科研/CV/Paper/论文关系图谱.canvas

**统计**:
- 论文节点：17个
- 引用边：23条
- 主题分组：5个

**关键论文**:
- DDPM（被引用5次）
- DDIM（被引用3次）
- Score-based（被引用4次）
```

### 方式2：标签筛选
```bash
用户: /paper-graph --tag #CV/Generation/Diffusion

你: 正在生成扩散模型论文图谱...
```

### 方式3：指定类型
```bash
用户: /paper-graph 科研/CV/Generate/ --type theme

你: 正在生成主题关联图谱（力导向布局）...
```

### 方式4：从搜索结果
```bash
用户: /paper-search diffusion
[选择3篇论文]
用户: /paper-graph [选中的论文]

你: 为选中的3篇论文生成关系图谱...
```

## 图谱示例

### 直接引用图谱
```
┌─────────────────────────────────────────────────────────┐
│                   论文引用关系图谱                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              [DDPM论文]                                  │
│                  ↓                                       │
│        ┌───────┴───────┐                                │
│        ↓               ↓                                │
│   [DDIM论文]      [Score-based论文]                      │
│        ↓               ↓                                │
│   [DDPM++论文]    [NCSN++论文]                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 主题关联图谱
```
┌─────────────────────────────────────────────────────────┐
│                  扩散模型主题图谱                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌───────────────┐      ┌───────────────┐            │
│   │ 扩散模型基础   │ ←──→ │   采样加速    │            │
│   └───────────────┘      └───────────────┘            │
│          ↓                      ↓                       │
│   ┌───────────────┐      ┌───────────────┐            │
│   │   图像生成    │ ←──→ │   图像编辑    │            │
│   └───────────────┘      └───────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 与其他Skills集成

### /note-analyze集成
```markdown
## 语义分析发现

发现以下笔记形成"注意力机制"主题簇：
- Transformer架构.md
- 自注意力机制.md
- 多头注意力.md

是否生成可视化图谱？
- [ ] 生成主题关系图谱
- [ ] 生成论文引用网络
- [ ] 跳过

用户选择后调用 /paper-graph
```

### /paper-notes集成
创建论文笔记时，可自动关联到相关图谱：
```markdown
## 相关图谱
- ![[科研/CV/Paper/扩散模型论文图谱.canvas]]
```

## 布局算法详细说明

### 层次布局（Hierarchical Layout）

**适用场景**：论文引用关系

**算法**：
1. 识别根节点（被引用最多的论文）
2. 按引用深度构建层次
3. 每层水平排列节点
4. 垂直方向表示引用方向

**优点**：
- 清晰展示引用方向
- 易于识别论文传承关系
- 适合展示研究脉络

**参数**：
- `VERTICAL_SPACING` = 400（垂直间距）
- `HORIZONTAL_SPACING` = 500（水平间距）
- `NODE_WIDTH` = 300
- `NODE_HEIGHT` = 200

### 力导向布局（Force-Directed Layout）

**适用场景**：主题关联图谱

**算法**：
1. 初始化随机位置
2. 迭代优化位置
   - 斥力：所有节点互相排斥
   - 引力：相关节点互相吸引
3. 收敛到稳定状态

**优点**：
- 相关节点自然聚集
- 易于发现主题簇
- 适合探索式浏览

**参数**：
- `REPULSION_STRENGTH` = 1000（斥力强度）
- `ATTRACTION_STRENGTH` = 0.1（引力强度）
- `MAX_ITERATIONS` = 500（最大迭代次数）

### 时间线布局（Timeline Layout）

**适用场景**：论文演进脉络

**算法**：
1. 按发表时间排序
2. 横轴表示时间
3. 纵轴表示主题分类
4. 连线表示传承关系

**优点**：
- 清晰展示时间演进
- 易于识别发展趋势
- 适合历史回顾

**参数**：
- `TIME_SCALE` = 100（每年像素）
- `THEME_HEIGHT` = 300（每主题高度）
- `TIME_START` = 最早论文年份

## 注意事项

1. **性能考虑**
   - 大量论文（>50篇）可能需要较长计算时间
   - 可考虑限制节点数量或分批处理

2. **布局质量**
   - 自动布局可能不完美
   - 用户可手动调整Canvas
   - 提供重新布局选项

3. **链接有效性**
   - 使用Glob验证链接目标存在
   - 确保Wikilink正确指向文件

4. **引用关系准确性**
   - 优先使用显式引用（related字段）
   - 推断关系需要谨慎标注
   - 提供编辑和修正机制

## 文件保存

### 命名规则
- 默认：`论文关系图谱.canvas`
- 主题：`{主题}论文图谱.canvas`
- 目录：`{目录名}/00-论文图谱.canvas`

### 保存位置
- 与论文同一目录
- 或专门的图谱目录
- 或Conclusion目录（总结性内容）

## 示例输出

### Canvas文件示例

```json
{
  "nodes": [
    {
      "id": "ddpm",
      "type": "file",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 200,
      "file": "科研/CV/Paper/DDPM.md",
      "color": "1"
    },
    {
      "id": "ddim",
      "type": "file",
      "x": -500,
      "y": 400,
      "width": 300,
      "height": 200,
      "file": "科研/CV/Paper/DDIM.md",
      "color": "2"
    },
    {
      "id": "group_diffusion",
      "type": "group",
      "x": -600,
      "y": -100,
      "width": 1700,
      "height": 900,
      "label": "扩散模型",
      "color": "5"
    }
  ],
  "edges": [
    {
      "id": "ddim_based_on_ddpm",
      "fromNode": "ddim",
      "toNode": "ddpm",
      "fromEnd": "arrow",
      "label": "based on",
      "color": "6"
    }
  ]
}
```

### 报告示例

```markdown
## 论文图谱生成完成

**文件**: 科研/CV/Generate/Paper/论文关系图谱.canvas

### 统计信息
- 论文节点：17个
- 引用边：23条
- 主题分组：5个
- 布局算法：层次布局

### 关键论文
1. **DDPM** - 被引用5次，扩散模型奠基工作
2. **Score-based** - 被引用4次，分数匹配理论
3. **DDIM** - 被引用3次，快速采样方法

### 主题分组
1. 扩散模型基础（5篇）
2. 采样加速（4篇）
3. 图像编辑（3篇）
4. 图像恢复（3篇）
5. 逆问题求解（2篇）

### 操作建议
- 点击节点可打开对应论文笔记
- 拖动节点可调整布局
- 双击空白处可添加说明
```

## 与json-canvas skill的关系

**json-canvas是文档技能**，提供Canvas格式规范参考。

**/paper-graph是工作流封装**，提供论文图谱生成的业务逻辑。

**协作方式**：
1. 参考 json-canvas 的格式规范创建Canvas文件
2. 使用Write工具写入.canvas文件
3. 组合Read/Glob/Write实现完整工作流

## 技术要点

1. **使用Glob精确匹配文件名**
   ```python
   pattern = f"**/*{paper_title}*.md"
   matches = glob.glob(pattern, recursive=True)
   if matches:
       actual_filename = matches[0]
   ```

2. **解析Frontmatter获取引用关系**
   ```python
   import yaml
   metadata = yaml.safe_extract(content)
   related_papers = metadata.get('related', [])
   ```

3. **构建引用图**
   ```python
   graph = {}
   for paper in papers:
       graph[paper] = {
           'cites': get_citations(paper),
           'cited_by': get_cited_by(paper)
       }
   ```

4. **层次布局计算**
   ```python
   def compute_hierarchy(graph):
       roots = find_root_nodes(graph)
       levels = {}
       for root in roots:
           levels[root] = 0
       # BFS构建层次
       ...
       return levels
   ```
