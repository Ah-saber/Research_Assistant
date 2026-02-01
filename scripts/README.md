# 笔记整理脚本

用于 `日志/` 目录下 Obsidian 笔记的批量整理和标准化。

## 脚本说明

### batch_standardize.py

**功能**：批量为 Markdown 文件添加 Frontmatter 和标签

**使用方法**：
```bash
cd D:/work_project/my_project/Research_Assistant/scripts
python batch_standardize.py
```

**处理内容**：
- 添加 YAML Frontmatter（title, date, category, tags）
- 根据文件路径和内容自动生成英文标签
- 智能提取标题（从首个 # 标题或文件名）

### fix_wikilinks_v2.py

**功能**：验证和修复 Wikilink 链接

**使用方法**：
```bash
cd D:/work_project/my_project/Research_Assistant/scripts
python fix_wikilinks_v2.py
```

**处理内容**：
- 扫描所有 Wikilink（包括图片、视频等资源）
- 将简单文件名链接更新为相对路径
- 支持 Obsidian 的附件目录结构

## 配置

脚本默认配置为处理 `C:\Note\MyNote_Obs\日志` 目录。

如需修改目标目录，请编辑脚本中的 `LOG_DIR` 变量。

## 标签映射规则

### 类别标签
- **课业**：`academic`, `study`, `course`, `notes`, `experiment`, `assignment`, `exam`
- **项目**：`project`, `research`, `competition`, `lab`, `innovation`
- **事务**：`affair`, `document`, `party`, `graduate`, `application`
- **杂项**：`misc`, `todo`, `attachment`

### 关键词标签
| 关键词 | 标签 |
|--------|------|
| Java/Python/C++ | 编程语言标签 |
| 深度学习 | `deep-learning`, `AI` |
| 数模/美赛 | `math-modeling`, `competition` |
| Linux | `Linux`, `os` |
| 数据库 | `database` |

## 注意事项

1. **备份**：运行脚本前建议先备份笔记
2. **编码**：脚本使用 UTF-8 编码
3. **路径**：Windows 路径使用正斜杠或双反斜杠
4. **重复运行**：脚本可以安全重复运行

## 故障排除

### 中文乱码
确保终端支持 UTF-8 编码：
```bash
chcp 65001
```

### 权限错误
以管理员身份运行终端或检查文件权限

### 路径错误
确认 `LOG_DIR` 路径格式正确：
```python
LOG_DIR = r"C:\Note\MyNote_Obs\日志"
```
