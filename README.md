# App Store 截屏处理工具

这个项目专为苹果开发者设计，解决模拟器截屏无法直接用于 App Store 的问题。通过自动添加设备边框并调整到 App Store 要求的尺寸，让你的应用截屏更专业、更符合规范。

## 项目背景

从 iOS 模拟器截取的图片无法直接上传到 App Store，主要问题：
- ❌ 尺寸不符合 App Store 要求
- ❌ 缺少设备边框，显示效果不佳
- ❌ 需要手动处理，效率低下

本工具一键解决这些问题：
- ✅ 自动添加真实设备边框
- ✅ 输出符合 App Store 规范的图片尺寸
- ✅ 批量处理，提升开发效率

## 功能特点

- 🏪 **App Store 规范**: 输出符合 App Store 要求的截屏图片
- 📱 **设备支持**: 支持 iPhone 和 iPad 主流设备
- 🎭 **智能蒙版**: 完美处理圆角、刘海等复杂形状
- 📂 **批量处理**: 一键处理整个文件夹的截屏
- 🎨 **高质量输出**: 专业级图片质量和压缩

## 项目结构

```
├── ipad_batch.py        # iPad 截屏处理器
├── iphone_batch.py      # iPhone 截屏处理器
├── iPadPro13-M4-Silver-Portrait.psd     # iPad 设备边框模板
├── iPhone17ProMax-DeepBlue-Portrait.psd # iPhone 设备边框模板
├── output/              # 输出目录（自动创建）
└── README.md           # 项目说明文档
```

## 依赖要求

```bash
pip install pillow psd-tools
```

## 使用方法

### 典型工作流程

1. **从模拟器截屏** - 在 iOS 模拟器中截取应用界面
2. **运行处理工具** - 使用对应设备的脚本
3. **获得成品** - 得到符合 App Store 规范的截屏图片
4. **直接上传** - 可直接用于 App Store Connect

### iPad 截屏处理

```bash
# 处理单张截图
python ipad_batch.py screenshot.png

# 批量处理文件夹中的所有截图
python ipad_batch.py screenshots_folder/
```

### iPhone 截屏处理

```bash
# 处理单张截图
python iphone_batch.py screenshot.png

# 批量处理文件夹中的所有截图
python iphone_batch.py screenshots_folder/
```

## 技术实现

### iPad 版本 (ipad_batch.py)
- 使用 `iPadPro13-M4-Silver-Portrait.psd` 作为边框模板
- 图层结构：Background → Screen → Hardware
- 直接将截屏图片放置到 Screen 图层位置

### iPhone 版本 (iphone_batch.py)
- 使用 `iPhone17ProMax-DeepBlue-Portrait.psd` 作为边框模板
- 图层结构：Background → Hardware → Screen (带蒙版)
- 截屏图片应用 Screen 图层蒙版后放置在最顶层
- 支持圆角、刘海等复杂形状的蒙版处理

## 输出说明

- 📁 输出文件保存在 `output/` 目录
- 📝 文件命名格式：`原文件名_framed.jpg`
- 🎯 **符合 App Store 规范**：尺寸和格式完全符合要求
- 🖼️ JPEG 质量：85%，启用优化压缩
- 🎨 自动去除透明通道，转换为 RGB 模式
- 📏 自动调整到标准设备尺寸

## 支持的图片格式

**输入格式**: PNG, JPG, JPEG
**输出格式**: JPEG

## 技术栈

- **Python 3.x**
- **Pillow (PIL)**: 图像处理
- **psd-tools**: PSD 文件解析
