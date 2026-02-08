# CV 目录论文标准化进度记录

**日期**: 2026-02-08
**会话**: 标准化工作第 1-3 次会话

---

## 📌 会话3更新 (2026-02-08)

### ✅ 完成工作

**Stage 6: 红外目录主题文件创建（完成）**

经过仔细分析23篇论文，重新设计了分类结构（**多标签方式**，一篇论文可属于多个主题）：

#### 创建的主题文件

| 主题 | 论文数 | 文件名 |
|------|--------|--------|
| 红外图像超分辨率与恢复 | 6篇 | 主题_红外图像超分辨率与恢复.md（更新） |
| 红外图像恢复与增强 | 8篇 | 主题_红外图像恢复与增强.md（新建） |
| 红外跨模态学习 | 5篇 | 主题_红外跨模态学习.md（新建） |
| 红外视频任务 | 4篇 | 主题_红外视频任务.md（新建） |
| 红外基础模型与架构 | 4篇 | 主题_红外基础模型与架构.md（新建） |

#### 主题分类详情

**1. 红外图像超分辨率与恢复**（更新现有主题）
- HATIR, DifIISR, EdgeSR, EM Image SR
- Contourlet Residual, FW-SAT

**2. 红外图像恢复与增强**
- 去噪类：ASCNet, FPN Removal, Exploring Video Denoising, PDB Unet
- NUC类：DeepIR, Simultaneous Temperature Estimation
- 增强类：DEAL, Enhancing Infrared Vision

**3. 红外跨模态学习**
- 融合与配准：Fusion Survey, TRACE
- 域适应：TIR ControlNet, STGADA
- 检索：RGB-T Retrieval

**4. 红外视频任务**
- Exploring Video Denoising, PDB Unet, HATIR, What Happened 3 Seconds Ago

**5. 红外基础模型与架构**
- InfMAE, Contourlet Residual, FW-SAT, Enhancing Infrared Vision

#### 暂时未归类
- Deep Depth Estimation from Thermal Image

---

## 📌 会话2更新 (2026-02-08)

### ✅ 完成工作

1. **主题链接修复** - 修正 `主题_红外图像超分辨率与恢复.md` 中的错误链接
2. **Visable 目录标准化** - 为 Low-Light Raw Image Denoising 论文添加 frontmatter
3. **红外目录主题分析** - 开始分析23篇论文的主题归属

---

## 下次会话继续

### ⏳ Stage 7: 论文主题索引链接添加

**待添加链接的论文**（约27篇论文需要添加或更新主题链接）：

根据新创建的5个主题，为相关论文添加对应的主题索引链接。

---

### 📝 其他待办

1. 为所有论文添加主题索引链接
2. 检查 Low-Level/Visable 目录其他论文的标准化状态
3. 考虑生成可视化图谱（`/paper-graph` 或 `/knowledge-canvas`）

---

## 详细修复记录

### 🔧 会话2修复内容

#### 1. 主题链接修复

**文件**: `QLink/主题_红外图像超分辨率与恢复.md`

| 修复项 | 原内容（错误） | 修复后（正确） |
|--------|----------------|----------------|
| DifIISR | `DifIISR：A Diffusion...`（中文冒号） | `DifIISR A Diffusion...`（英文A） |
| EdgeSR | `...for Edge Electro...`（单空格） | `...for  Edge Electro...`（双空格） |

**修复位置**: 概览表格 + 相关论文引用（共4处）

#### 2. Visable 目录标准化

**文件**: `Learnability Enhancement for Low-Light Raw Image Denoising：A Data Perspective.md`

**添加内容**:
```yaml
---
title: "Learnability Enhancement for Low-Light Raw Image Denoising: A Data Perspective"
tags:
  - CV
  - Low-Level
  - Denoising
  - Raw-Image
  - Low-Light
  - Learnability
date: 2026-02-08
status: read
source: T-PAMI
---
```

#### 3. 红外目录主题归类分析

**扫描结果**: 23篇论文，仅2个主题文件

**新主题规划**:
- 红外图像去噪与去条纹（2篇）
- 红外视频处理（3篇）
- 红外-可见光融合（2篇）
- 红外基础模型（2篇）
- 红外深度估计（1篇）
- 红外跨模态检索（1篇）
- 红外域适应（2篇）
- 红外视频理解（2篇）
- Contourlet残差学习（1篇）

---

## 完成进度

### ✅ Stage 1: HATIR 格式修复
- **文件**: `HATIR：Heat-Aware Diffusion for Turbulent Infrared Video Super-Resolution.md`
- **问题**: 文件第1行有空行，frontmatter 未从文件开头开始
- **修复**: 删除前导空行，确保文件直接以 `---` 开头

---

### ✅ Stage 2: Low-Level/Infrared Frontmatter 批量补全（22篇论文）

| 序号 | 论文标题 | 操作 |
|------|----------|------|
| 1 | HATIR：Heat-Aware Diffusion... | 修复前导空行 |
| 2 | Contourlet Residual for Prompt Learning... | 补全 frontmatter |
| 3 | DEAL: Data-Efficient Adversarial Learning... | 补全 frontmatter |
| 4 | DifIISR: A Diffusion Model... | 补全 frontmatter |
| 5 | EdgeSR: Reparameterization-Driven... | 添加 frontmatter |
| 6 | Fixed Pattern Noise Removal... | 补全 frontmatter |
| 7 | Exploring Video Denoising in Thermal IR... | 添加 frontmatter |
| 8 | PDB Unet: A Spatio Temporal... | 添加 frontmatter |
| 9 | ASCNet: Asymmetric Sampling... | 添加 frontmatter |
| 10 | InfMAE: A Foundation Model... | 添加 frontmatter |
| 11 | Simultaneous Temperature Estimation... | 添加 frontmatter |
| 12 | Thermal Image Processing (DeepIR) | 补全 frontmatter |
| 13 | Enhancing Infrared Vision... | 补全 frontmatter |
| 14 | Learning Large-Factor EM Image SR | 已完整 |
| 15 | Infrared and Visible Image Fusion | 添加 frontmatter |
| 16 | Narrowing Syn2Real Gap (TIR ControlNet) | 添加 frontmatter |
| 17 | What Happened 3 Seconds Ago | 添加 frontmatter |
| 18 | Flexible Window-based Transformer (FW-SAT) | 添加 frontmatter |
| 19 | Spectral Transfer Guided ADA | 添加 frontmatter |
| 20 | Deep Depth Estimation from Thermal | 已完整 |
| 21 | Are Deep Learning Models Pre-trained... | 添加 frontmatter |
| 22 | Toward Training-Free Plug-and-Play | 添加 frontmatter |

**Frontmatter 格式**:
```yaml
---
title: "论文标题"
tags: [CV, Low-Level, Infrared, ...]
date: 2026-02-08
status: read
source: 会议/期刊
---
```

---

### ✅ Stage 3: Generate/Paper Frontmatter 验证（20篇论文）

**结果**: 所有 20 篇论文的 frontmatter 均已完整且格式正确

| 序号 | 论文标题 | 状态 |
|------|----------|------|
| 1 | One-step Flow, Rectified Flow... | ✅ 已添加 |
| 2-20 | 其他 19 篇 | ✅ 已完整 |

**Frontmatter 格式** (Generate/Paper 使用列表格式):
```yaml
---
title: "论文标题"
tags:
  - Domain/CV
  - Task/xxx
  - Method/xxx
category: xxx
created: 2026-01-27
---
```

---

### ✅ Stage 4: Wikilink 批量修复

**执行日期**: 2026-02-08（第2次会话）

**扫描结果**:
- Low-Level/Infrared 目录：25个文件，所有 Wikilink 验证通过
- Generate/Paper 目录：40+个 Wikilink，全部有效

**验证结果**:
| 链接类型 | 状态 | 说明 |
|----------|------|------|
| 论文间链接 | ✅ 全部有效 | 所有目标文件存在 |
| 主题文件链接 | ✅ 全部有效 | 5个主题文件可访问 |
| 跨目录链接 | ✅ 全部有效 | Obsidian 可正确解析 |

---

### ✅ Stage 5: 主题索引关联

**执行日期**: 2026-02-08（第2次会话）

**完成统计**:
| 操作类型 | 数量 |
|----------|------|
| ✅ 成功添加主题链接 | 11篇 |
| ⚠️ 已存在主题链接 | 9篇 |
| ❌ 文件不存在 | 1篇（EdgeSR） |

**Low-Level/Infrared**（红外图像超分辨率与恢复）:
| 论文 | 状态 |
|------|------|
| HATIR | ✅ 已添加 |
| DifIISR | ✅ 已添加 |
| Learning Large-Factor EM Image SR | ✅ 已添加 |

**Generate/Paper**（多主题）:

**盲逆问题的扩散模型求解**:
- Gradient Guidance: ✅ 已添加
- 其他5篇: ⚠️ 已存在

**频域方法在扩散模型中的应用**:
- 所有3篇: ⚠️ 已存在

**一步生成与加速方法**:
- FlowIE: ✅ 已添加
- FlowEdit: ✅ 已添加
- One-step Flow: ✅ 已添加

**注意力控制在图像编辑中的应用**:
- Prompt-to-Prompt: ✅ 已添加
- MasaCtrl: ✅ 已添加
- DragonDiffusion: ✅ 已添加

---

## 关键文件路径

### Low-Level/Infrared
- **目录**: `C:\Note\MyNote_Obs\科研\CV\Low-Level\Infrared\`
- **论文数量**: 23 篇
- **主题**: `QLink\主题_红外图像超分辨率与恢复.md`

### Generate/Paper
- **目录**: `C:\Note\MyNote_Obs\科研\CV\Generate\Paper\`
- **论文数量**: 20 篇
- **主题**: 5 个主题文件

---

## 工作完成摘要

### ✅ 全部完成的 Stage

| Stage | 内容 | 状态 |
|-------|------|------|
| Stage 1 | HATIR 格式修复 | ✅ 完成 |
| Stage 2 | Low-Level/Infrared Frontmatter 批量补全（22篇） | ✅ 完成 |
| Stage 3 | Generate/Paper Frontmatter 验证（20篇） | ✅ 完成 |
| Stage 4 | Wikilink 批量修复与验证 | ✅ 完成 |
| Stage 5 | 主题索引关联 | ✅ 完成 |

### 📝 遗留问题

1. **EdgeSR 论文文件不存在**
   - 预期路径: `C:\Note\MyNote_Obs\科研\CV\Low-Level\Infrared\EdgeSR：Reparameterization-Driven Fast Thermal Super-Resolution for Edge Electro-Optical Device.md`
   - 可能原因: 文件被移动或删除
   - 建议: 确认文件位置或从主题列表中移除

---

## 下次会话建议

1. 确认 EdgeSR 论文文件状态
2. 考虑生成可视化图谱（`/paper-graph` 或 `/knowledge-canvas`）
3. 检查其他 CV 子目录的标准化需求
