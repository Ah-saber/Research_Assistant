# /note-link - 发现和建立笔记关联

## 触发词
- "建立关联"
- "链接笔记"
- "发现关联"
- "笔记关联"

## 功能描述
发现笔记之间的语义关联，创建合理的链接，增强笔记网络的连通性。

## 关联方式

### 1. 语义关联
- 基于内容相似度
- 基于主题相关性
- 基于概念关联

### 2. 标签相似
- 共享标签的笔记
- 标签层级关联
- 标签同义词关联

### 3. 共同引用
- 引用相同论文
- 提及相同概念
- 使用相同术语

## 链接类型

### 1. 内容链接
- 位置：相关段落中
- 格式：`[[笔记名称|描述文字]]`
- 用途：上下文引用

### 2. 主题链接
- 位置：笔记末尾
- 格式：列表形式
- 用途：主题索引

### 3. 双向链接
- 自动创建反向链接
- Obsidian自动维护
- 显示在反向链接面板

## 链接位置智能判断

| 情况 | 链接位置 | 格式 |
|------|----------|------|
| 内容中提及 | 相关段落 | `[[笔记\|描述]]` |
| 主题相关 | 笔记末尾 | `## 相关笔记\n- [[笔记]]` |
| 概念关联 | 概念定义处 | `[[笔记]]` |
| 扩展阅读 | 末尾独立节 | `## 扩展阅读` |

## 工作流程

### 1. 发现关联
```
分析笔记内容 → 提取关键词 → 搜索相关笔记 → 计算关联度
```

### 2. 建议链接
```
显示相关笔记 → 展示关联理由 → 用户选择（使用AskUserQuestion） → 添加链接
```

### 交互流程（重要）

发现关联后，**必须**使用AskUserQuestion让用户选择要添加的链接：

```markdown
## 发现的笔记关联

### 高度相关（关联度>80%）
1. [[自注意力机制]] (95%)
2. [[多头注意力]] (88%)

### 中度相关（关联度50-80%）
3. [[BERT模型]] (75%)
4. [[序列建模]] (65%)

使用AskUserQuestion询问用户：
- 要添加哪些链接？
- 允许多选
- 提供"全部添加"、"选择性添加"、"仅预览"、"取消"选项
```

### 3. 验证链接
```
检查链接有效性 → 确认双向链接 → 更新相关笔记
```

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| note | 目标笔记 | 否，默认当前笔记 |
| scope | 搜索范围 | 否，默认全部 |
| max_links | 最大链接数 | 否，默认5 |
| auto_add | 自动添加 | 否，默认false |

## 输出格式

### 建议链接格式

```markdown
# 发现的笔记关联

## 目标笔记：《Transformer架构》

### 高度相关（关联度>80%）
1. [[自注意力机制]] - 共同主题：注意力机制
   → 建议位置："架构"段落

2. [[多头注意力]] - 是Transformer的组成部分
   → 建议位置："架构组件"节

### 中度相关（关联度50-80%）
3. [[BERT模型]] - 基于Transformer
   → 建议位置：末尾"应用"

4. [[序列建模]] - Transformer解决此问题
   → 建议位置："问题背景"

### 标签关联
- 共享标签 #深度学习 的笔记：12篇

### 操作
请选择要添加的链接（输入序号，逗号分隔）：
或：
1. 添加全部高度相关
2. 选择性添加
3. 取消
```

## 链接建议算法

### 关联度计算
```python
关联度 = w1*标题相似 + w2*内容相似 + w3*标签重叠 + w4*引用关系

其中：
- 标题相似：关键词匹配
- 内容相似：语义相似度
- 标签重叠：共同标签数量
- 引用关系：是否互相引用
```

### 链接理由生成
- 直接引用：笔记A明确提到笔记B
- 主题相关：讨论相同主题
- 概念关联：包含相关概念
- 层级关系：上位/下位概念

## 使用示例

### 示例1：为当前笔记找关联
```bash
用户: /note-link

你: 正在分析当前笔记《Transformer架构》...

发现4篇高度相关笔记：

1. [[自注意力机制]] (95%)
   理由：核心组件，多次提及

2. [[多头注意力]] (88%)
   理由：架构组成部分

[...更多建议...]

请选择要添加的链接：
```

### 示例2：指定笔记
```bash
用户: /note-link "深度学习基础"

你: 正在分析《深度学习基础》...

发现6篇相关笔记...

请选择操作：
1. 添加所有链接
2. 选择性添加
3. 仅预览
```

### 示例3：批量处理
```bash
用户: /note-link --scope "深度学习" --auto_add

你: 正在为深度学习目录下的笔记添加链接...

✓ Transformer架构 → 添加3个链接
✓ CNN架构 → 添加2个链接
✓ RNN架构 → 添加4个链接

完成！共添加9个链接。
```

## 链接格式规范

**语法参考**：obsidian-markdown skill 提供完整的 Wikilink 语法规范

### ⚠️ 重要：表格中的Wikilink

在Markdown表格中，管道符 `|` 会被解析为列分隔符，因此**必须转义**：

| 上下文 | 格式 |
|--------|------|
| 普通文本 | `[[笔记名|显示]]` |
| **表格中** | `[[笔记名\|显示]]` |

### 基本链接
```markdown
[[笔记名称]]
```

### 带描述链接（推荐）
```markdown
[[笔记名称|显示的文字]]
```

### 表格中的链接（注意转义）
```markdown
| [[笔记名称\|显示的文字]] | 下一列 |
```

### 精确文件名链接（重要）
使用Glob工具获取精确文件名后创建链接：
```markdown
[[Flow-Based  Diffusion Model|Flow-Based Diffusion Model]]
```

**注意**：文件名中的空格数量必须精确匹配。使用Glob搜索获取实际文件名。

### 标题链接
```markdown
[[笔记名称#特定标题]]
[[笔记名称#特定标题|显示的文字]]
```

### 链接列表
```markdown
## 相关笔记
- [[笔记1]]
- [[笔记2]] - 关于xxx的详细说明
- [[笔记3#特定章节]]
```

**更多语法**：块链接 `[[笔记#^block-id]]`、搜索链接 `[[##keyword]]`（详见 obsidian-markdown skill）

### 链接创建流程（重要）

```python
# 1. 提取目标笔记关键词
target_name = extract_target_name(content)

# 2. 使用Glob精确搜索
pattern = f"**/*{target_name}*.md"
matches = glob.glob(pattern, recursive=True)

# 3. 验证并创建链接
if len(matches) == 1:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{target_name}]]"
elif len(matches) > 1:
    # 多个匹配，询问用户选择
    link = ask_user_to_select(matches)
else:
    # 无匹配，标记为潜在链接
    link = f"[[{target_name}]]  # TODO: 验证此链接"
```

## 注意事项

1. **适度链接**：不要过度链接，保持相关性
2. **描述准确**：使用描述性文字说明链接关系
3. **位置合理**：链接放在逻辑相关的位置
4. **双向维护**：Obsidian自动处理反向链接
5. **定期检查**：检查断链和无效链接

## 后续操作

链接完成后：
- 检查反向链接面板
- 更新相关笔记
- 使用图谱视图查看效果
- 生成可视化图谱预览（新增）← 调用 `/paper-graph`、`/idea-map`、`/knowledge-canvas`

**Canvas可视化选项**：
- 论文引用关系 → 调用 `/paper-graph` 生成层次布局图谱
- Idea概念关联 → 调用 `/idea-map` 生成力导向布局图谱
- 综合知识视图 → 调用 `/knowledge-canvas` 生成区域布局画布

这些技能参考 **json-canvas** 格式规范，使用 Read/Write/Edit + Glob 执行

## 高级功能

### 链接验证
使用Glob工具验证Wikilink是否有效：

```python
def verify_wikilink(link_text):
    # 提取链接目标
    target = extract_link_target(link_text)

    # 使用Glob搜索匹配文件
    pattern = f"**/*{target}*.md"
    matches = glob.glob(pattern, recursive=True)

    if matches:
        return True, matches[0]  # 有效，返回实际路径
    else:
        return False, None  # 无效，断链
```

**验证流程**：
1. 扫描笔记中的所有Wikilink
2. 对每个链接使用Glob验证目标文件是否存在
3. 报告断链列表
4. 询问是否修复断链

### 链接修复
自动修复失效的Wikilink：

```python
def fix_broken_link(link_text):
    target = extract_link_target(link_text)

    # 尝试模糊搜索
    possible_matches = glob.glob(f"**/*{target[:20]}*.md")

    if len(possible_matches) == 1:
        # 找到唯一匹配，更新链接
        actual_filename = possible_matches[0]
        return f"[[{actual_filename}|{target}]]"
    else:
        # 无法自动修复，需要人工确认
        return None
```

**修复示例**：
```markdown
# 修复前（文件名有双空格，链接用单空格）
[[Flow-Based Diffusion Model]]

# 修复后（使用精确文件名）
[[Flow-Based  Diffusion Model|Flow-Based Diffusion Model]]
```

### 链接建议学习
- 记录用户接受的建议
- 学习用户偏好
- 优化推荐算法

### 链接质量评估
- 检测孤立链接
- 识别单向链接
- 建议补全反向链接
- 发现断链并建议修复

### 链接分组
- 按关联度分组
- 按类型分组（引用/相关/扩展）
- 按时间分组

## 与 Canvas 可视化的关系

**三层协作架构**：

| 层级 | 组件 | 作用 |
|------|------|------|
| **格式参考** | json-canvas skill | 提供 Canvas (.canvas) 格式规范文档 |
| **执行工具** | Read/Write/Edit + Glob | 底层文件操作 |
| **工作流封装** | /paper-graph 等 | 业务逻辑 |

**分工明确**：
- **json-canvas**：提供 Canvas 格式规范文档
  - 节点类型（file、text、group）、边类型、布局算法
- **Visualization Skills**：提供可视化工作流
  - `/paper-graph` - 论文引用关系图谱（层次布局）
  - `/idea-map` - Idea概念关系图谱（力导向布局）
  - `/knowledge-canvas` - 综合知识画布（区域布局）
- **/note-link**：建立链接后，建议生成可视化图谱预览

**不是重复造轮子**：
- json-canvas 是**文档技能**，不执行文件操作
- Visualization Skills 是**工作流封装**，使用 Read/Write/Edit + Glob 创建Canvas文件
- 本技能是**链接层**，发现和建立笔记关联后，建议调用对应可视化技能预览关系图

**可视化预览触发条件**：
- 建立了多个链接（>5个）→ 建议调用 `/paper-graph` 或 `/idea-map` 预览关系网络
- 发现论文引用关系 → 建议调用 `/paper-graph` 生成引用关系图谱
- 发现概念关联网络 → 建议调用 `/knowledge-canvas` 生成综合知识画布
