# Idea管理工作流

本文档描述使用Research Assistant捕捉、整理和回顾研究想法的工作流程。

## 工作流概览

```
捕捉Idea → 定期整理 → 回顾评估 → 推进实现 → 归档保存
```

## 目录结构

```
C:\Note\MyNote_Obs\
├── Inspiration\          # 临时Idea存放（可自由访问）
│   ├── 2024\
│   │   ├── 01-January\
│   │   └── 02-February\
│   └── themes\
└── 科研\
    └── IDEA\            # 确认后的Idea（需授权访问）
```

## 详细步骤

### 1. 捕捉Idea

使用 `/idea-capture` 快速记录想法。

```bash
记录Idea：用注意力机制解释CNN决策过程
```

**自动处理**：
- 保存到Inspiration目录
- 推断标签
- 关联相关笔记
- 生成标准格式
- **理论动机分析**（理论基础、可能性评估、跨领域关联、问题本质）

**捕捉方式**：
- **快速记录**：一句话描述
- **完整记录**：包含动机、可行性分析、**理论动机**
- **从笔记提取**：从现有笔记中提取想法

### 2. 定期整理

每周或每两周整理一次Inspiration中的Idea。

```bash
/idea-organize
```

**整理内容**：
- 标签规范化
- 去重检测
- 分组显示
- 状态更新建议

### 3. 回顾评估

使用 `/idea-review` 回顾所有Idea。

```bash
/idea-review
```

**回顾维度**：
- 按状态：萌芽、思考中、已实现、已放弃
- 按时间：最新、长期未更新
- 按主题：深度学习、实验想法等
- 按优先级：高、中、低

**行动建议**：
- 阅读建议：推荐相关论文
- 实验建议：可尝试的实验
- 笔记建议：需要细化的想法
- 状态更新：推进或搁置建议

### 4. 推进实现

将有价值的Idea从萌芽推进到实现。

```
萌芽 → 思考中 → 实验验证 → 已实现
```

**推进方式**：
- 阅读相关工作
- 设计验证实验
- 创建详细笔记
- 记录实验结果

### 5. 归档保存

将有价值的Idea从Inspiration移至科研/IDEA目录。

**手动操作**（用户执行）：
1. 在Inspiration中确认Idea价值
2. 整理完善Idea内容
3. 手动移至`科研/IDEA/相应主题目录`
4. 更新状态为"已实现"或"思考中"

### 6. 备份与归档

定期备份Inspiration目录，并清理过期Idea。

**备份建议**：
- 每月备份一次Inspiration目录
- 使用git commit保存版本历史
- 重要Idea导出为独立文档

**过期Idea处理**：
- 超过3个月未更新的"萌芽"状态Idea → 标记为"已放弃"
- 超过6个月未推进的"思考中"状态Idea → 评估是否放弃
- 已放弃的Idea每季度清理一次

**归档流程**：
```bash
/idea-organize
# 选择"清理过期Idea"选项
```

### 7. Idea可视化

使用可视化工具管理和浏览Idea。

**生成Idea图谱**：
```bash
/idea-map
```

**视图类型**：
- **状态分组视图**：按萌芽/思考中/已实现/已放弃分组
- **概念关联视图**：显示Idea之间的语义关联
- **优先级视图**：按高/中/低优先级着色

**与回顾结合**：
```bash
# 先生成图谱查看全貌
/idea-map

# 再按状态回顾
/idea-review --status sprout
```

## 完整示例

```
用户: 记录Idea：用注意力机制来解释CNN的决策

你: ✓ 已记录Idea

# 用注意力机制解释CNN决策

## 核心想法
在CNN中引入注意力机制，可视化模型决策依据

## 动机
CNN是黑盒，需要可解释性

## 下一步
- [ ] 调研注意力可视化方法
- [ ] 设计实验方案

保存：Inspiration/2024/01-15-注意力解释CNN.md

---

[两周后]

用户: /idea-organize

你: 正在整理Inspiration中的Idea...

发现15个Idea：
- 萌芽：8个
- 思考中：5个
- 已实现：2个

建议：
- "注意力解释CNN"已萌芽14天，建议推进

用户: /idea-review --status sprout

你: 回顾萌芽状态的Idea...

1. 注意力解释CNN (14天前)
   相关：[[Transformer架构]], [[CNN可视化]]
   建议：调研GradCAM方法

用户: 将这个Idea推进到思考中，添加笔记

你: ✓ 状态已更新为"思考中"
✓ 已添加详细思考笔记

---

[一个月后，实验成功]

用户: /idea-review --status thinking

你: 回顾思考中的Idea...

1. 注意力解释CNN (已实现)
   这个Idea已实验验证成功

建议：移至科研/IDEA目录保存

用户: [手动将Idea移至科研/IDEA/可解释性/]
```

## 快速工作流

### 快速记录
```bash
用户: 记录Idea：xxx
你: [立即记录到Inspiration]
```

### 快速回顾
```bash
用户: 查看最近的想法
你: [显示最近7天的Idea]
```

### 快速整理
```bash
用户: 整理Inspiration
你: [执行整理，报告结果]
```

## 高级用法

### 批量记录
```bash
用户: 从"Transformer架构"笔记提取Idea
你: [分析笔记，发现并记录潜在想法]
```

### 按主题回顾
```bash
/idea-review --theme 深度学习
```

### 状态批量更新
```bash
/idea-organize --status_update
```

## Idea状态管理

### 状态定义

| 状态 | 说明 | 典型停留时间 |
|------|------|-------------|
| sprout | 刚萌芽的想法，未深入思考 | 1-2周 |
| thinking | 正在思考和研究，有计划 | 1-3个月 |
| implemented | 已实现/验证成功 | 永久保存 |
| abandoned | 经评估后放弃 | 保留记录 |

### 状态转换规则

```
sprout → thinking → implemented
         ↓
      abandoned
```

**转换时机**：
- sprout → thinking：完成初步调研，认为可行
- thinking → implemented：实验验证成功
- thinking → abandoned：实验失败或不可行
- sprout → abandoned：初步评估不可行

## 最佳实践

1. **快速记录**：想法稍纵即逝，立即记录到Inspiration
2. **定期整理**：每周整理一次，保持Inspiration整洁
3. **及时回顾**：每月回顾一次，推进有价值的想法
4. **完善内容**：推进Idea时，添加详细思考和实验记录
5. **定期归档**：将有价值的Idea移至IDEA目录
6. **保留记录**：即使是已放弃的Idea，也保留记录供未来参考

## 常见问题

### Q: Inspiration和IDEA目录的区别？
A:
- **Inspiration**：临时存放，可自由访问，用于快速捕捉和初步思考
- **IDEA**：永久保存，需授权访问，存储有价值的完整想法

### Q: 什么时候将Idea移至IDEA目录？
A: 当Idea满足以下条件之一：
- 已实现（实验成功）
- 有深入思考和详细记录
- 长期研究的高价值想法

### Q: 如何处理已放弃的Idea？
A: 保留在Inspiration中，标记状态为"已放弃"，定期清理或归档。

### Q: Idea太多怎么办？
A:
- 使用`/idea-organize`分组整理
- 使用`/idea-review`按优先级回顾
- 定期清理无价值的想法
- 将成熟的Idea移至IDEA

## 访问权限说明

**重要**：
- `/idea-capture`、`/idea-organize`、`/idea-review` 仅访问Inspiration目录
- Inspiration目录可自由访问
- 科研/IDEA目录需要用户明确授权才能访问
- 移动Idea到IDEA由用户手动操作

## 相关技能

- `/idea-capture` - 捕捉Idea
- `/idea-organize` - 整理Idea
- `/idea-review` - 回顾Idea
- `/idea-map` - 生成Idea可视化图谱
- `/paper-notes` - 为Idea创建详细笔记
- `/note-link` - 建立Idea之间的关联
- `/note-standardize` - 标准化Idea笔记格式
