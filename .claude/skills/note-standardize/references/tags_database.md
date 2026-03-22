# 标签数据库

此文件存储已规范化的标签，用于推荐新标签时参考和保持一致性。

## 使用说明

当为新论文推荐标签时：
1. 先在此表中查找语义相似的已存在标签
2. 如果找到相似标签，优先使用
3. 如果是全新标签类别，添加到此表

---

## 任务标签 (Task Tags)

### Low-Level / Infrared

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `CV/Low-Level/Infrared/NUC` | 非均匀校正、固定模式噪声去除 | FPN, Destriping, Fixed Pattern Noise, Non-Uniformity Correction |
| `CV/Low-Level/Infrared/Enhancement` | 红外图像增强 | Enhancement, Improve, Boost |
| `CV/Low-Level/Infrared/Dehazing` | 红外去雾 | Dehazing, Haze Removal, Defog |
| `CV/Low-Level/Infrared/Super-Resolution` | 红外超分辨率 | SR, Super Resolution, Upscaling, Enlarge |
| `CV/Low-Level/Infrared/Fusion` | 红外图像融合 | Fusion, Merge, Combine, Integrate |
| `CV/Low-Level/Infrared/Denoising` | 红外去噪 | Denoising, Noise Removal, Noise Reduction |
| `CV/Low-Level/Infrared/Deconvolution` | 去卷积 | Deconvolution, Deblur, Blur Removal |

### Low-Level / Visible

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `CV/Low-Level/Enhancement` | 可见光图像增强 | Enhancement, Brighten |
| `CV/Low-Level/Denoising` | 可见光去噪 | Denoising, Noise Removal |
| `CV/Low-Level/Super-Resolution` | 可见光超分辨率 | SR, Upscaling |

### Generation

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `CV/Generation/Image-Generation` | 图像生成 | Image Synthesis, Generate Images |
| `CV/Generation/Image-Editing` | 图像编辑 | Edit, Manipulate, Modify |
| `CV/Generation/Restoration` | 图像恢复 | Restoration, Recover, Repair |
| `CV/Generation/Video-Generation` | 视频生成 | Video Synthesis |
| `CV/Generation/Image-to-Image` | 图像到图像转换 | I2I, Image Translation |

### Detection & Segmentation

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `CV/Detection/Object-Detection` | 目标检测 | Detect Objects, Bounding Box |
| `CV/Segmentation/Semantic-Segmentation` | 语义分割 | Pixel-wise Classification |
| `CV/Segmentation/Instance-Segmentation` | 实例分割 | Instance-wise |

---

## 方法标签 (Method Tags)

### Generation Methods

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `Method/Generation/Diffusion` | 扩散模型 | DDPM, DDIM, Diffusion Model, Denoising Diffusion |
| `Method/Generation/Flow` | 流模型 | Flow-based, Rectified Flow, Normalizing Flow |
| `Method/Generation/GAN` | 生成对抗网络 | Generative Adversarial Network |
| `Method/Generation/VAE` | 变分自编码器 | Variational Autoencoder |

### Learning Methods

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `Method/Learning/Self-Supervised` | 自监督学习 | Self-supervised, Unsupervised |
| `Method/Learning/Deep` | 深度学习 | Deep Learning, CNN, Neural Network |
| `Method/Learning/Weakly-Supervised` | 弱监督学习 | Weak Supervision |
| `Method/Learning/Few-Shot` | 少样本学习 | Few-shot, One-shot |

### Architecture

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `Method/Architecture/Attention` | 注意力机制 | Attention, Self-Attention, Cross-Attention |
| `Method/Architecture/Transformer` | Transformer | ViT, Vision Transformer |
| `Method/Architecture/CNN` | 卷积神经网络 | ConvNet, Convolutional |
| `Method/Architecture/UNet` | U-Net 架构 | U-Net, Encoder-Decoder |

### Optimization

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `Method/Optimization/Regularization` | 正则化优化 | L1, L2, Sparse, ADMM, IRLS |
| `Method/Optimization/Gradient` | 梯度方法 | Gradient Descent, SGD, Adam |
| `Method/Optimization/Adversarial` | 对抗训练 | Adversarial Training |

### Other Methods

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `Method/Frequency-Domain` | 频域方法 | Fourier, DCT, Wavelet, Spectral |
| `Method/Physics-Inspired` | 物理启发 | Physics-based, Physics-informed |
| `Method/Filter` | 滤波方法 | Guided Filter, Bilateral Filter |
| `Method/Train-Free` | 无需训练 | Train-free, Training-free, Zero-shot |

---

## 数学/理论标签 (Math/Theory Tags)

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `Math/Sampling/Posterior-Sampling` | 后验采样 | Posterior Sampling, MCMC |
| `Math/Sampling/Langevin` | Langevin 采样 | Langevin Dynamics |
| `Math/Information/Entropy` | 熵相关 | Entropy, KL Divergence |
| `Math/Probability/Bayesian` | 贝叶斯方法 | Bayesian, Prior, Posterior |

---

## 发表场所标签 (Venue Tags)

| 标签 | 说明 |
|------|------|
| `Venue/CVPR` | CVPR 会议 |
| `Venue/ICCV` | ICCV 会议 |
| `Venue/ECCV` | ECCV 会议 |
| `Venue/NeurIPS` | NeurIPS 会议 |
| `Venue/ICML` | ICML 会议 |
| `Venue/AAAI` | AAAI 会议 |
| `Venue/IJCAI` | IJCAI 会议 |
| `Venue/TPAMI` | TPAMI 期刊 |
| `Venue/TIP` | TIP 期刊 |

---

## 新标签记录区

当发现全新类型的标签时，添加到这里：

| 标签 | 说明 | 相似关键词 |
|------|------|-----------|
| `CV/Low-Level/low-light` | 低光照图像处理 | Low-light, Dark Image, Night Scene |
| `CV/Low-Level/Visable` | 可见光图像处理（通用） | Visible Light, RGB Image |
| `Method/Learning/Transfer` | 迁移学习/微调 | Transfer Learning, Fine-tuning, Adaptation |
| `Method/Learning/Fine-Tuning` | 微调策略 | Fine-tuning, Joint Optimization, Unified Training |
| `Method/Optimization/Sampling` | 采样优化 | Sampling, Inference Acceleration, Feature Caching |
| `Method/Architecture/Adapter` | 适配器架构 | Adapter, LoRA, Parameter-Efficient |
| `CV/Domain/Remote-Sensing` | 遥感图像处理领域 | Remote Sensing, Satellite Image, Aerial Image |
