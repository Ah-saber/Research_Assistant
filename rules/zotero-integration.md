# Zotero 集成规范

本文档定义 Zotero MCP 工具的使用规范，参考 `docs/guides/mcp-best-practices.md`。

---

## MCP 工具概览

| 工具 | 用途 | 限制 | 建议 |
|------|------|------|------|
| `zotero_search_items` | 关键词搜索 | 适中 | 优先使用，返回元数据 |
| `zotero_semantic_search` | 语义搜索 | 适中 | 找相关论文的好方法 |
| `zotero_get_item_metadata` | 获取元数据 | 低 | **总是成功**，优先调用 |
| `zotero_get_item_fulltext` | 获取全文 | **高** | 可能超限，准备降级 |
| `zotero_get_annotations` | 获取注释 | **高** | 必须指定 item_key |
| `zotero_get_collections` | 获取集合 | 低 | 获取目录结构 |

---

## 全文超限处理

### 问题

论文全文通常超过 100KB，超过单次返回的 token 限制。

### 解决方案

**方案1：分页读取（推荐）**
```python
# 使用 Read 工具分段读取
Read(file_path, offset=1, limit=500)
Read(file_path, offset=501, limit=500)
```

**方案2：降级策略**
```python
# 如果全文无法读取，基于摘要生成
metadata = zotero_get_item_metadata(item_key)
if fulltext_exceeds_limit:
    content = metadata["abstract"]
    quality = "abstract"  # 明确标注质量级别
```

**方案3：摘要优先**
```python
# 先尝试摘要，摘要足够则不读取全文
abstract = metadata["abstract"]
if len(abstract) > 500:
    use_abstract_instead()
```

---

## Windows 路径格式

| 工具 | 正确格式 | 示例 |
|------|----------|------|
| Bash | 正斜杠 `/` | `"C:/Users/Ahs/file.txt"` |
| Read | 双反斜杠 `\\` | `"C:\\Users\\Ahs\\file.txt"` |
| Python raw string | 原始字符串 | `r"C:\Users\Ahs\file.txt"` |

### ✅ GOOD

```python
bash_path = "C:/Users/Ahs/file.txt"
read_path = "C:\\Users\\Ahs\\file.txt"
raw_path = r"C:\Users\Ahs\file.txt"
```

### ❌ BAD

```python
path = "C:\Users\Ahs\file.txt"  # \U 会被解析为转义字符
```

---

## 注释处理规范

### 按论文筛选（推荐）

```python
# 获取单篇论文的注释
annotations = zotero_get_annotations(item_key="THJPBR5X")
```

### 处理无注释情况

```python
result = zotero_get_annotations(item_key)
if "No annotations found" in result:
    # 友好提示，不阻塞流程
    return None
```

### 使用 limit

```python
# 限制返回数量
annotations = zotero_get_annotations(limit=20)
```

---

## 错误处理模式

```python
# 1. 优先使用元数据（总是成功）
metadata = zotero_get_item_metadata(item_key)
if not metadata:
    return error("论文不存在")

# 2. 尝试获取全文（可能超限）
try:
    fulltext = zotero_get_item_fulltext(item_key)
except TokenLimitError:
    # 降级到摘要
    fulltext = metadata.get("abstract", "")
    log("使用摘要替代全文")

# 3. 检查注释（可能为空）
annotations = zotero_get_annotations(item_key)
if "No annotations" in annotations:
    annotations = None

# 4. 生成内容
generate_note(metadata, fulltext, annotations)
```

---

## 质量标注

明确告知用户数据来源的质量：

| 标注 | 说明 |
|------|------|
| `full` | 完整全文 |
| `abstract` | 仅基于摘要 |
| `partial` | 部分全文（分页读取） |

---

## 参考

- **详细文档**：`docs/guides/mcp-best-practices.md`
- **MCP 配置**：`.mcp.json`
- **权限配置**：`.claude/settings.local.json`
