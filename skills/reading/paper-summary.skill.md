# /paper-summary - 总结论文内容

## 触发词
- "总结论文"
- "论文概要"
- "论文摘要"
- "总结xxx论文"

## 功能描述
生成论文的详细摘要，包括背景、问题、方法、结果和结论。

## 摘要结构

### 1. 研究背景（Background）
- 领域现状和背景
- 相关工作简介

### 2. 研究问题（Problem）
- 要解决的核心问题
- 现有方法的不足

### 3. 研究动机（Motivation）
- 为什么需要解决这个问题
- 解决这个问题的意义

### 4. 创新方法（Method）
- 核心方法和算法
- 关键技术细节
- 模型架构（如有图示）

### 5. 实验结果（Results）
- 主要实验设置
- 关键结果数据
- 与baseline的比较

### 6. 结论与贡献（Conclusion）
- 主要发现
- 贡献总结
- 局限性讨论

## 额外内容

### 关键公式提取
- 列出核心公式
- 解释公式含义
- 说明公式作用

### 技术深度
- 详细版：800字以上
- 包含技术细节
- 学术风格表达

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| paper | 论文（标题/ID/Zotero key） | 是 |
| detail | 详细程度（simple/detailed） | 否 |

## 输出格式

```markdown
# [论文标题] - 论文总结

## 基本信息
- **作者**：xxx
- **年份**：xxxx
- **发表**：xxx

## 研究背景
...

## 研究问题
...

## 核心方法
...

## 主要结果
...

## 关键公式
...

## 结论
...
```

## 使用的Zotero MCP工具

- `zotero_get_item_fulltext` - 获取论文全文
- `zotero_get_item_metadata` - 获取论文元数据

## 注意事项

- 使用学术风格表达
- 保持客观准确
- 中文总结，保留英文术语

## MCP工具使用注意事项

### 全文超限处理
当 `zotero_get_item_fulltext` 返回内容超过token限制时：
1. 系统会自动将内容保存到文件
2. 文件路径格式：`C:\Users\{用户}\.claude\projects\{项目ID}\tool-results\mcp-zotero-zotero_get_item_fulltext-{时间戳}.txt`
3. 读取方法：
   ```bash
   # 方案1：使用Bash（注意路径格式）
   head -500 "C:/Users/Ahs/.claude/projects/.../tool-results/filename.txt"

   # 方案2：使用Read工具（需要正确转义路径）
   Read("C:\\Users\\Ahs\\.claude\\projects\\...\\tool-results\\filename.txt", offset=1, limit=500)
   ```

### 路径格式问题
- **Bash工具**: 使用正斜杠 `/` 或双反斜杠 `\\`
- **Read工具**: 使用双反斜杠 `\\` 转义
- **路径变量**: 避免直接使用包含反斜杠的路径变量

### 降级策略
如果全文无法读取：
1. 基于摘要生成精简版总结
2. 明确告知用户数据来源（仅基于摘要）
3. 提供手动上传全文的选项
