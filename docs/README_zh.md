# Snap2Store

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

## 安装

```bash
pip install snap2store
```

## 使用方法

### 典型工作流程

1. **从模拟器截屏** - 在 iOS 模拟器中截取应用界面
2. **运行处理工具** - 使用对应设备的脚本
3. **获得成品** - 得到符合 App Store 规范的截屏图片
4. **直接上传** - 可直接用于 App Store Connect

### CLI 命令

```bash
# 处理单张截图（自动检测设备类型）
snap2store screenshot.png

# 批量处理文件夹中的所有截图
snap2store screenshots_folder/

# 指定设备类型（iPhone）
snap2store -d iphone screenshot.png

# 指定设备类型（iPad）和自定义输出目录
snap2store -d ipad -o custom_output/ screenshot.png

# 显示帮助信息
snap2store --help
```

### 命令选项

```
usage: snap2store [-h] [-d {iphone,ipad}] [-o OUTPUT] [-v] input

Snap2Store - Add device bezels to iOS/iPadOS screenshots to meet App Store requirements

positional arguments:
  input                 Screenshot file or folder path

options:
  -h, --help            show this help message and exit
  -d {iphone,ipad}, --device {iphone,ipad}
                        Specify device type (auto-detect if not provided)
  -o OUTPUT, --output OUTPUT
                        Output directory (default: ./output/)
  -v, --version         show program's version number and exit

Examples:
  snap2store screenshot.png                  # Auto-detect device type and process single screenshot
  snap2store screenshots/                    # Process all screenshots in the folder
  snap2store -d iphone screenshot.png        # Specify as iPhone screenshot
  snap2store -d ipad -o custom_output/ img/  # Specify as iPad screenshot and custom output directory
```

## 输出说明

- 📁 输出文件保存在 `output/` 目录
- 📝 文件命名格式：`原文件名_framed.jpg`
- 🎯 **符合 App Store 规范**：尺寸和格式完全符合要求
- 🖼️ JPEG 质量：85%，启用优化压缩
- 🎨 自动去除透明通道，转换为 RGB 模式

### 输出图片尺寸

- 📱 **iPhone**: 1242 × 2688 像素
- 📱 **iPad**: 2064 × 2752 像素

这些尺寸完全符合 App Store Connect 的要求，可直接用于应用商店截屏上传。

## 技术栈

- **Python 3.x**
- **Pillow (PIL)**: 图像处理
- **psd-tools**: PSD 文件解析
