# Research Assistant 技能升级需求记录

**创建日期**: 2026-02-01
**文档类型**: 需求与理解记录

---

## 一、用户需求总结

### 1.1 核心需求

用户希望基于 `everything-claude-code` 参考项目，对 Research Assistant 的技能系统进行标准化升级：

1. **格式标准化**：添加 YAML frontmatter，统一文件名为 SKILL.md，添加 When to Activate
2. **添加对比示例**：在技能中添加 GOOD/BAD 对比示例
3. **创建插件配置**：创建 plugin.json 配置文件
4. **快速参考表**：在技能末尾添加速查表
5. **Hooks 自动化**：创建 hooks/ 实现自动化触发

### 1.2 技能触发方式

**用户选择**：两者都支持
- Slash command 触发（如 `/research-assistant:paper-search`）
- 自然语言自动匹配触发

### 1.3 目录结构决策

**用户选择**：扁平单层结构
- 每个技能一个子目录：`skills/paper-search/SKILL.md`
- 便于 Claude Code 插件机制扫描和加载

### 1.4 文件命名规范

**用户选择**：kebab-case
- 使用小写字母和连字符：`note-standardize`, `paper-search`

### 1.5 架构层次

**用户选择**：两层架构
- Command → Skill（直接调用，不需要 agents/ 层）

---

## 二、改进优先级

**用户指定的优先级顺序**：
1. **Notes Skills**（最高优先级）
2. **Reading Skills**
3. **Ideas Skills**
4. **Visualization & Dashboard**

---

## 三、Hooks 自动化场景

**用户选择的触发场景**：
1. **PostToolWrite**: 笔记格式检查 - Write .md 文件后自动检查格式
2. **PostToolEdit**: 格式化建议 - Edit .md 文件后建议标准化
3. **SessionEnd**: 持久化状态 - 会话结束时保存状态

---

## 四、语言规范

**用户明确要求**：
- **编写语言**：简体中文
- **技能/命令名称**：保持英文（kebab-case）
- **具体内容**：保持中文
- **确保 AI 理解这一点**

---

## 五、文档输出位置

**用户要求**：
- 计划保存到：`PLAN/UPD.md`
- 进展保存到：`PLAN/PRO_UPD.md`
- 不影响现有文件

---

## 六、阶段划分（用户确认）

**用户确认的6个阶段**：
1. **阶段1**: 基础架构（plugin.json、目录重组）
2. **阶段2**: Notes Skills（优先级1）
3. **阶段3**: Reading Skills（优先级2）
4. **阶段4**: Ideas + Visualization（优先级3-4）
5. **阶段5**: Commands + CLAUDE.md + 工作流 + rules
6. **阶段6**: 审查总结

---

## 七、文档同步更新

**用户要求同步更新的文档**：
- `docs/workflows/` - 工作流文档
- `PLAN/references/` - 参考模板
- `docs/guides/mcp-best-practices.md` - MCP 最佳实践

**用户要求**：参考 everything-claude-code 的实现方式

---

## 八、自我进化需求

**用户需求**：
- 确保项目可以做到"自我进化"
- 参考 everything-claude-code 的 continuous-learning-v2 实现
- 完成一种自动进化的工作流

**参考项目的关键组件**：
- `continuous-learning-v2/SKILL.md` - 基于 instinct 的学习系统
- `continuous-learning-v2/config.json` - 配置观察、本能、进化参数
- `commands/learn.md` - 提取可重用模式的命令
- `commands/evolve.md` - 聚类本能为 skills/commands

---

## 九、规范化要求

**用户强调**：
1. 保证规范化（参考 everything-claude-code）
2. 语言简洁、明确
3. 每个阶段的具体计划要具体

---

## 十、AI 对用户需求的理解

### 10.1 项目定位

Research Assistant 是一个**个人学术助理系统**，专为计算机视觉学者设计：
- 整合 Zotero 文献库
- 整合 Obsidian 笔记系统
- 通过自定义 Skills 封装工作流

### 10.2 与参考项目的区别

| 维度 | everything-claude-code | Research Assistant |
|------|----------------------|-------------------|
| 领域 | 通用软件开发 | CV 学术研究 |
| 技术栈 | Python/Django/React/Go | Zotero/Obsidian/MCP |
| 用户 | 多人开发团队 | 个人学者 |
| 复杂度 | 30+ skills，三层架构 | 18 skills，单层技能 |

### 10.3 需要保留的特色

1. **概率与统计视角**：论文笔记包含概率框架分析
2. **理论导向**：Idea 包含理论动机分析
3. **中文输出**：笔记内容使用中文
4. **Obsidian 深度集成**：Wikilink、Callout、Frontmatter、Embeds

### 10.4 参考项目值得借鉴的核心

1. **SKILL.md 标准格式**：YAML frontmatter + When to Activate + GOOD/BAD + 速查表
2. **plugin.json 配置**：支持插件化分发
3. **两层命令系统**：Commands → Skills 清晰分层
4. **Hooks 自动化**：PostToolWrite/Edit 自动触发
5. **模块化 Rules**：将 CLAUDE.md 拆分为 rules/*.md
6. **自我进化**：continuous-learning-v2 的 instinct 模型

---

## 十一、待商谈的细节

下个会话需要详细商谈的内容：

1. **阶段1的具体实施细节**：
   - plugin.json 的完整配置
   - hooks/hooks.json 的具体匹配规则
   - 目录迁移的脚本设计

2. **SKILL.md 格式模板**：
   - Notes Skills 的通用模板
   - 如何将现有内容迁移到新格式

3. **Commands 格式设计**：
   - Command 文件的统一格式
   - Command 如何调用对应的 Skill

4. **Rules 模块化方案**：
   - CLAUDE.md 如何拆分为 rules/*.md
   - 每个 rule 文件的内容范围

5. **自我进化的具体实现**：
   - 是否需要完整的 continuous-learning-v2
   - 还是简化版的 /learn 命令即可

6. **测试验证方案**：
   - 如何验证技能触发正确
   - 如何验证 Hooks 工作正常

---

## 十二、参考项目关键文件路径

```
D:\work_project\my_project\Ref_pro\everything-claude-code\
├── .claude-plugin/
│   ├── plugin.json                    # 插件配置模板
│   └── PLUGIN_SCHEMA_NOTES.md         # 重要约束说明
├── skills/
│   ├── python-patterns/SKILL.md       # SKILL.md 格式参考
│   ├── continuous-learning-v2/
│   │   ├── SKILL.md                   # 自我进化参考
│   │   └── config.json                # 配置参考
│   └── golang-testing/SKILL.md        # 带对比示例的参考
├── commands/
│   ├── plan.md                        # Command 格式参考
│   └── learn.md                       # 学习命令参考
├── agents/
│   └── planner.md                     # Agent 格式参考
├── rules/
│   ├── coding-style.md                # Rules 格式参考
│   └── hooks.md                       # Hooks 说明参考
└── examples/
    └── CLAUDE.md                      # 项目 CLAUDE.md 参考
```

---

## 十三、当前项目关键文件

```
D:\work_project\my_project\Research_Assistant\
├── skills/
│   ├── notes/         # 5个技能 (.skill.md)
│   ├── reading/       # 4个技能 (.skill.md)
│   ├── ideas/         # 3个技能 (.skill.md)
│   ├── visualization/ # 3个技能 (.skill.md)
│   └── dashboard/     # 3个技能 (.skill.md)
├── docs/
│   ├── workflows/     # 3个工作流文档
│   └── guides/        # MCP最佳实践指南
├── PLAN/
│   ├── PRD.md
│   ├── PRO.md
│   └── references/    # 4个参考模板
├── .mcp.json
├── .claude/
│   └── settings.local.json
├── .cursorrules
├── PERSONA.md
├── CLAUDE.md
└── README.md
```
