# /knowledge-canvas - 综合知识画布

## 触发词
- "知识画布"
- "研究图谱"
- "生成知识画布"
- "综合知识图谱"
- "研究主题画布"

## 功能描述
创建综合研究主题画布，整合论文、Idea、概念笔记等多种内容类型，形成完整的知识可视化视图。

## 画布类型

### 1. 研究主题画布
以特定研究主题为中心，整合相关的论文、Idea、概念笔记。

**布局**：区域布局（Zoned Layout）
- 左侧：核心论文区
- 右上：相关Idea区
- 右下：概念笔记区
- 中心：主题问题/TODO

### 2. 领域全景画布
展示整个研究领域（如CV/NLP）的知识图谱。

**布局**：分层布局（Layered Layout）
- 顶层：领域概览
- 中层：子领域分组
- 底层：具体论文和Idea

### 3. 项目知识画布
围绕特定研究项目的知识管理画布。

**布局**：中心辐射布局（Hub-and-Spoke Layout）
- 中心：项目核心问题
- 周围：相关的论文、Idea、笔记

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| theme | 研究主题 | 是 |
| scope | 内容范围（论文/Idea/概念/全部） | 否，默认全部 |
| type | 画布类型（theme/domain/project） | 否，默认theme |
| layout | 布局方式（zoned/layered/hub） | 否，根据type自动选择 |

## 输出格式

### Canvas文件结构

```json
{
  "nodes": [
    {
      "id": "paper1",
      "type": "file",
      "x": -800,
      "y": -200,
      "width": 300,
      "height": 200,
      "file": "科研/CV/Paper/DDPM.md",
      "color": "1"
    },
    {
      "id": "idea1",
      "type": "file",
      "x": 400,
      "y": -400,
      "width": 250,
      "height": 180,
      "file": "Inspiration/Idea_加速采样.md",
      "color": "3"
    },
    {
      "id": "concept1",
      "type": "file",
      "x": 400,
      "y": 100,
      "width": 250,
      "height": 150,
      "file": "科研/CV/Concepts/扩散基础.md",
      "color": "5"
    },
    {
      "id": "question1",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 100,
      "text": "核心问题：如何加速采样过程？",
      "color": "6"
    },
    {
      "id": "zone_papers",
      "type": "group",
      "x": -900,
      "y": -400,
      "width": 700,
      "height": 800,
      "label": "核心论文区",
      "color": "5"
    }
  ],
  "edges": [
    {
      "id": "edge1",
      "fromNode": "idea1",
      "toNode": "paper1",
      "fromEnd": "none",
      "toEnd": "arrow",
      "label": "基于",
      "color": "6"
    },
    {
      "id": "edge2",
      "fromNode": "idea1",
      "toNode": "concept1",
      "label": "涉及概念",
      "style": "dashed",
      "color": "6"
    }
  ]
}
```

### 区域划分

| 区域 | 位置 | 内容 | 布局 |
|------|------|------|------|
| 核心论文区 | 左侧 | 主题相关论文 | 层次布局 |
| Idea区 | 右上 | 相关Idea | 按状态分组 |
| 概念笔记区 | 右下 | 概念定义 | 网格布局 |
| 问题区 | 中心 | 核心问题/TODO | 文本节点 |

### 节点类型

| 类型 | 说明 | 颜色编码 |
|------|------|----------|
| 论文节点 | 核心论文红色，重要进展橙色 | "1"/"2" |
| Idea节点 | 按状态着色（黄/橙/绿/灰） | "3"/"2"/"4"/"6" |
| 概念节点 | 蓝色 | "5" |
| 文本节点 | 灰色 | "6" |
| 分组节点 | 青色背景 | "5" |

## 数据来源

### 1. 论文数据
- 指定目录的论文笔记
- 标签筛选（如#CV/Generation/Diffusion）
- Zotero搜索结果

### 2. Idea数据
- Inspiration目录
- 按主题标签筛选
- 按状态筛选

### 3. 概念笔记
- 科研/CV/Concepts/
- 标签为#Concept的笔记
- 相关方法/模型笔记

### 4. 关联关系
- Frontmatter中的related字段
- Wikilink
- 语义相似度分析

## 工作流程

### 步骤1：确定研究主题
```
用户指定主题，如：
- 扩散模型
- 注意力机制
- 图像编辑
- 生成式模型
```

### 步骤2：收集相关内容
```
1. 搜索相关论文
   - 扫描论文目录
   - 按标签筛选
   - 解析Frontmatter

2. 搜索相关Idea
   - 扫描Inspiration
   - 按主题筛选

3. 搜索相关概念
   - 概念目录
   - 标签筛选

4. 提取关联关系
   - related字段
   - Wikilink
```

### 步骤3：构建知识图谱
```
1. 创建节点
   - 论文节点
   - Idea节点
   - 概念节点
   - 问题文本节点

2. 创建边
   - 论文→论文（引用）
   - Idea→论文（基于）
   - Idea→概念（涉及）
   - 论文→概念（使用）

3. 设置属性
   - 类型、颜色、大小
   - 标签、说明
```

### 步骤4：计算布局
```
区域布局算法：

function zoned_layout(papers, ideas, concepts):
    # 左侧：论文区
    for i, paper in enumerate(papers):
        paper.x = -800
        paper.y = (i - len(papers)/2) * VERTICAL_SPACING

    # 右上：Idea区
    for i, idea in enumerate(ideas):
        idea.x = 400
        idea.y = -400 + (i % IDEAS_PER_ROW) * SPACING

    # 右下：概念区
    for i, concept in enumerate(concepts):
        concept.x = 400
        concept.y = 100 + (i % CONCEPTS_PER_ROW) * SPACING

    # 中心：问题区
    question.x = 0
    question.y = 0
```

### 步骤5：生成Canvas
```
1. 创建分组节点（区域背景）
2. 创建内容节点
3. 创建关联边
4. 设置样式和颜色
5. 保存为.canvas文件
```

### 步骤6：报告结果
```
报告内容：
- Canvas文件路径
- 内容统计
- 区域说明
- 关键发现
- 使用建议
```

## 使用方式

### 方式1：指定主题
```bash
用户: /knowledge-canvas 扩散模型

你: 正在创建"扩散模型"知识画布...

✓ 搜索相关论文：17篇
✓ 搜索相关Idea：5个
✓ 搜索相关概念：8个
✓ 构建知识图谱
✓ 计算布局

## 知识画布生成完成

**文件**: 科研/CV/扩散模型知识画布.canvas

**内容统计**:
- 论文节点：17个
- Idea节点：5个
- 概念节点：8个
- 关联边：42条

**区域划分**:
- 左侧：核心论文区（17篇）
- 右上：Idea区（5个，2萌芽+2思考中+1已实现）
- 右下：概念笔记区（8个）
- 中心：核心问题区

**核心问题**:
如何加速扩散模型的采样过程？

**相关Idea**:
- 小波引导的多尺度扩散（萌芽）
- 自适应采样策略（思考中）
- ...
```

### 方式2：指定范围
```bash
用户: /knowledge-canvas --scope papers 扩散模型

你: 正在创建扩散模型论文知识画布...
（只包含论文，不包含Idea和概念）
```

### 方式3：领域全景
```bash
用户: /knowledge-canvas --type domain CV生成

你: 正在创建CV生成领域全景画布...
```

### 方式4：项目画布
```bash
用户: /knowledge-canvas --type project 对抗鲁棒性

你: 正在创建"对抗鲁棒性"项目知识画布...
```

## 画布示例

### 研究主题画布
```
┌────────────────────────────────────────────────────────────┐
│              研究主题：扩散模型                              │
├──────────────────┬───────────────────┬────────────────────┤
│   核心论文区     │    Idea区         │   概念笔记区       │
│  ┌────────────┐  │  ┌─────────────┐  │  ┌──────────────┐ │
│  │  [DDPM] 🔴 │  │  │[小波扩散] 🟡│  │  │ [扩散基础] 🔵│ │
│  │     ↓      │  │  │[自适应] 🟠  │  │  │ [变分推断] 🔵│ │
│  │  [DDIM] 🟠 │  │  │[质量改进] 🟡│  │  │ [ELBO推导] 🔵│ │
│  │     ↓      │  │  └─────────────┘  │  └──────────────┘ │
│  │[Score-based]│  │                   │                    │
│  └────────────┘  │                   │                    │
├──────────────────┴───────────────────┴────────────────────┤
│                        核心问题区                          │
│          如何加速采样过程？                                │
│          ↓                                                │
│          当前Idea：自适应采样策略                           │
└────────────────────────────────────────────────────────────┘
```

### 领域全景画布
```
┌────────────────────────────────────────────────────────────┐
│              CV生成领域全景                                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │   扩散模型       │  │   生成对抗网络   │              │
│  │  ┌──────────┐   │  │  ┌──────────┐   │              │
│  │  │ [DDPM]   │   │  │  │ [DCGAN]  │   │              │
│  │  │ [DDIM]   │   │  │  │ [StyleGAN]│  │              │
│  │  └──────────┘   │  │  └──────────┘   │              │
│  └──────────────────┘  └──────────────────┘              │
│                                                            │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │   流模型         │  │   VAE            │              │
│  │  ┌──────────┐   │  │  ┌──────────┐   │              │
│  │  │[FlowMatching]│ │  │  │ [VAE]    │   │              │
│  │  │[Glow]    │   │  │  │ [VQ-VAE] │   │              │
│  │  └──────────┘   │  │  └──────────┘   │              │
│  └──────────────────┘  └──────────────────┘              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 项目知识画布
```
┌────────────────────────────────────────────────────────────┐
│         项目：对抗鲁棒性研究                                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│                    [核心问题]                               │
│            如何提高模型的对抗鲁棒性？                       │
│                    ↓   ↓   ↓                              │
│         ┌─────────┼───┼─────────┐                        │
│         ↓         ↓   ↓         ↓                        │
│    [对抗训练] [防御方法] [检测] [认证]                     │
│         ↓         ↓         ↓        ↓                    │
│    [相关论文] [相关Idea] [概念] [实验]                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## 与其他Skills集成

### /note-analyze集成
```markdown
## 语义分析发现

发现以下笔记形成"扩散模型"主题簇：
- 论文：DDPM, DDIM, Score-based等
- Idea：小波引导、自适应采样等
- 概念：扩散基础、变分推断等

是否生成综合知识画布？
- [ ] 生成研究主题画布
- [ ] 生成论文关系图谱
- [ ] 生成Idea概念图
- [ ] 跳过

用户选择后调用 /knowledge-canvas
```

### /paper-search集成
```markdown
搜索完成！找到17篇扩散模型相关论文。

是否生成知识画布？
- [ ] 生成包含这些论文的知识画布
- [ ] 生成论文关系图谱
- [ ] 跳过
```

## 布局算法详细说明

### 区域布局（Zoned Layout）

**适用场景**：研究主题画布

**算法**：
1. 将画布划分为4个区域
2. 左侧：论文区（层次布局）
3. 右上：Idea区（按状态分组）
4. 右下：概念区（网格布局）
5. 中心：问题区（文本节点）

**参数**：
- `PAPER_ZONE_X` = -800
- `IDEA_ZONE_X` = 400
- `IDEA_ZONE_Y` = -400
- `CONCEPT_ZONE_X` = 400
- `CONCEPT_ZONE_Y` = 100
- `VERTICAL_SPACING` = 400

### 分层布局（Layered Layout）

**适用场景**：领域全景画布

**算法**：
1. 顶层：领域概览（文本节点）
2. 中层：子领域分组（组节点）
3. 底层：具体内容（论文、Idea）

**参数**：
- `LAYER_SPACING` = 600
- `GROUP_SPACING` = 800
- `NODE_SPACING` = 400

### 中心辐射布局（Hub-and-Spoke Layout）

**适用场景**：项目知识画布

**算法**：
1. 中心：项目核心问题
2. 第一层：主要研究方向
3. 第二层：相关论文、Idea、概念

**参数**：
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

    # 方法4：内容分析
    if keyword_in_content(theme):
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
    theory = metadata.get('theoretical_basis', [])
    for t in theory:
        if is_related_to_theme(t, theme):
            return True

    return False
```

### 概念筛选
```python
def filter_concepts(theme):
    # 方法1：标签匹配
    if has_tag(theme):
        return True

    # 方法2：被论文引用
    papers = get_papers_with_theme(theme)
    for paper in papers:
        if paper.references_concept(concept):
            return True

    return False
```

## 核心问题生成

### 自动提取核心问题
```markdown
从Idea中提取：
- 萌芽Idea的"问题描述"
- 思考中Idea的"研究问题"

从论文中提取：
- Abstract中的研究问题
- Introduction中的motivation

从主题词推断：
- "扩散模型" → "如何加速采样？"
- "对抗鲁棒性" → "如何提高鲁棒性？"
```

### 手动指定核心问题
```markdown
用户可直接指定核心问题：
/knowledge-canvas 扩散模型 --question "如何实现零样本图像编辑？"
```

## 注意事项

1. **内容量控制**
   - 论文超过30篇时提示用户筛选
   - Idea超过20个时按状态或优先级筛选
   - 概念超过15个时只显示核心概念

2. **布局可读性**
   - 避免节点重叠
   - 保持适当的间距
   - 分组标签清晰

3. **链接有效性**
   - 使用Glob验证所有链接
   - 处理断链情况
   - 确保文件路径正确

4. **性能考虑**
   - 大量内容时可能需要较长时间
   - 可分批生成或限制范围

## 文件保存

### 命名规则
- 研究主题：`{主题}知识画布.canvas`
- 领域全景：`{领域}全景画布.canvas`
- 项目画布：`{项目名}项目画布.canvas`

### 保存位置
- 与内容同目录
- 或专门的画布目录
- 或Conclusion目录（总结性内容）

## 示例输出

### Canvas文件示例

```json
{
  "nodes": [
    {
      "id": "paper_ddpm",
      "type": "file",
      "x": -800,
      "y": -200,
      "width": 300,
      "height": 200,
      "file": "科研/CV/Paper/DDPM.md",
      "color": "1"
    },
    {
      "id": "idea_sampling",
      "type": "file",
      "x": 400,
      "y": -400,
      "width": 250,
      "height": 180,
      "file": "Inspiration/Idea_自适应采样.md",
      "color": "2"
    },
    {
      "id": "concept_diffusion",
      "type": "file",
      "x": 400,
      "y": 100,
      "width": 250,
      "height": 150,
      "file": "科研/CV/Concepts/扩散基础.md",
      "color": "5"
    },
    {
      "id": "question_main",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 100,
      "text": "核心问题：如何加速采样过程？",
      "color": "6"
    }
  ],
  "edges": [
    {
      "id": "idea_to_paper",
      "fromNode": "idea_sampling",
      "toNode": "paper_ddpm",
      "fromEnd": "none",
      "toEnd": "arrow",
      "label": "基于",
      "color": "6"
    }
  ]
}
```

### 报告示例

```markdown
## 知识画布生成完成

**文件**: 科研/CV/Generate/扩散模型知识画布.canvas

### 内容统计
| 类型 | 数量 | 说明 |
|------|------|------|
| 论文 | 17篇 | 核心论文及引用关系 |
| Idea | 5个 | 2萌芽+2思考中+1已实现 |
| 概念 | 8个 | 基础概念和方法 |
| 问题 | 1个 | 核心研究问题 |

### 区域说明
**左侧：核心论文区**
- 按引用关系排列
- DDPM（被引用5次）作为根节点
- DDIM、Score-based等重要进展突出显示

**右上：Idea区**
- 按状态着色分组
- 萌芽状态需要关注
- 思考中状态可推进

**右下：概念笔记区**
- 扩散模型基础概念
- 变分推断、ELBO等理论
- 采样方法相关

**中心：核心问题**
"如何加速采样过程？"
- 当前有2个相关Idea
- 3篇论文涉及此问题

### 关键发现
1. 研究脉络清晰：DDPM → DDIM → DDPM++
2. 待推进Idea：小波引导的多尺度扩散（萌芽超过30天）
3. 缺失概念：缺少"分数匹配"详细笔记

### 使用建议
- 点击论文节点查看详细笔记
- 点击Idea节点评估是否推进
- 根据关联关系发现新内容
- 可手动调整布局优化显示

### 相关操作
- 查看论文关系图谱：/paper-graph 扩散模型
- 查看Idea概念图：/idea-map --theme 扩散模型
- 回顾相关Idea：/idea-review --theme 扩散模型
```

## 与json-canvas skill的关系

**json-canvas是文档技能**，提供Canvas格式规范参考。

**/knowledge-canvas是工作流封装**，提供综合知识画布生成的业务逻辑。

**协作方式**：
1. 参考 json-canvas 的格式规范创建Canvas文件
2. 使用Write工具写入.canvas文件
3. 组合Read/Glob/Write实现完整工作流

## 技术要点

1. **多数据源整合**
   ```python
   papers = collect_papers(theme)
   ideas = collect_ideas(theme)
   concepts = collect_concepts(theme)

   # 统一数据格式
   all_nodes = []
   all_nodes.extend(format_as_paper_nodes(papers))
   all_nodes.extend(format_as_idea_nodes(ideas))
   all_nodes.extend(format_as_concept_nodes(concepts))
   ```

2. **跨类型关联**
   ```python
   def create_cross_type_edges(papers, ideas, concepts):
       edges = []

       # Idea → 论文
       for idea in ideas:
           for paper in papers:
               if is_based_on(idea, paper):
                   edges.append(create_edge(idea, paper))

       # Idea → 概念
       for idea in ideas:
           for concept in concepts:
               if involves_concept(idea, concept):
                   edges.append(create_edge(idea, concept))

       return edges
   ```

3. **区域布局计算**
   ```python
   def zoned_layout(papers, ideas, concepts):
       positions = {}

       # 左侧：论文区
       for i, paper in enumerate(papers):
           positions[paper] = (-800, (i - len(papers)/2) * 400)

       # 右上：Idea区
       for i, idea in enumerate(ideas):
           row = i // 3
           col = i % 3
           positions[idea] = (400 + col * 300, -400 + row * 250)

       # 右下：概念区
       for i, concept in enumerate(concepts):
           row = i // 3
           col = i % 3
           positions[concept] = (400 + col * 250, 100 + row * 200)

       return positions
   ```

4. **核心问题提取**
   ```python
   def extract_core_question(theme, papers, ideas):
       # 从Idea提取
       for idea in ideas:
           if idea.status == 'thinking':
               return idea.problem

       # 从论文提取
       for paper in papers:
           if paper.has_core_question():
               return paper.core_question

       # 推断生成
       return infer_question_from_theme(theme)
   ```
