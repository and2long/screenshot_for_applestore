
import argparse
import os
import sys
from typing import List, Optional

from PIL import Image

from snap2store.ipad_batch import process_image as process_ipad
from snap2store.iphone_batch import process_image as process_iphone


def is_landscape(img):
    """判断图片是否为横屏（宽度大于高度）"""
    width, height = img.size
    return width > height

def is_ipad_screenshot(image_path):
    """判断截图是否为iPad截图（基于宽高比）
    
    iPad 的宽高比约为 4:3 (1.33)
    iPhone 的宽高比约为 9:19.5 (0.46)
    
    返回:
        (bool, bool): (是否为iPad, 是否为横屏)
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 检查是否为横屏
            landscape = is_landscape(img)
            
            # 如果是横屏，交换宽高计算比例
            if landscape:
                aspect_ratio = height / width
            else:
                aspect_ratio = width / height
            
            # iPad 宽高比接近 3:4 (0.75)，iPhone 宽高比接近 9:19.5 (0.46)
            # 使用 0.6 作为区分阈值
            is_ipad = aspect_ratio > 0.6
            
            return is_ipad, landscape
    except Exception as e:
        print(f"❌ 读取图片时出错: {e}")
        return False, False


def process_auto(image_path, device=None, output_dir="output"):
    """自动处理截图，可指定设备类型或自动检测"""
    # 检查是否为横屏
    is_ipad, landscape = is_ipad_screenshot(image_path)
    
    # 如果是横屏，输出错误信息并退出程序
    if landscape:
        print(f"❌ 错误: 检测到横屏截图 {image_path}")
        print("❗ 当前工具仅支持竖屏截图，无法处理横屏截图")
        print("📱 请使用竖屏截图重新尝试")
        sys.exit(1)
    
    # 如果指定了设备类型
    if device:
        if device == "ipad":
            print(f"🔄 处理iPad截图: {image_path}")
            return process_ipad(image_path, output_dir=output_dir)
        else:  # device == "iphone"
            print(f"🔄 处理iPhone截图: {image_path}")
            return process_iphone(image_path, output_dir=output_dir)
    else:
        # 自动检测设备类型
        if is_ipad:
            print(f"🔍 检测到iPad截图: {image_path}")
            return process_ipad(image_path, output_dir=output_dir)
        else:
            print(f"🔍 检测到iPhone截图: {image_path}")
            return process_iphone(image_path, output_dir=output_dir)


def process_batch(input_dir: str, device: Optional[str] = None, output_dir: str = "output") -> List[str]:
    """批量处理文件夹中的所有截图"""
    processed_files = []
    
    if not os.path.exists(input_dir):
        print(f"❌ 输入目录不存在: {input_dir}")
        return processed_files
        
    files = [f for f in os.listdir(input_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    total = len(files)
    
    if total == 0:
        print("❌ 文件夹中没有截图文件")
        return processed_files
        
    print(f"📂 处理文件夹中的 {total} 张截图...")
    
    for i, f in enumerate(files, start=1):
        path = os.path.join(input_dir, f)
        print(f"⏳ [{i}/{total}] 处理: {f}")
        output_path = process_auto(path, device, output_dir)
        processed_files.append(output_path)
        
    print(f"✅ 批量处理完成! 已处理 {len(processed_files)} 张截图")
    return processed_files


def main():
    """CLI主入口函数"""
    parser = argparse.ArgumentParser(
        description="Snap2Store - Add device bezels to iOS/iPadOS screenshots to meet App Store requirements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  snap2store screenshot.png                  # Auto-detect device type and process single screenshot
  snap2store screenshots/                    # Process all screenshots in the folder
  snap2store -d iphone screenshot.png        # Specify as iPhone screenshot
  snap2store -d ipad -o custom_output/ img/  # Specify as iPad screenshot and custom output directory
        """
    )
    
    parser.add_argument("input", help="Screenshot file or folder path")
    parser.add_argument("-d", "--device", choices=["iphone", "ipad"], 
                        help="Specify device type (auto-detect if not provided)")
    parser.add_argument("-o", "--output", default="output",
                        help="Output directory (default: ./output/)")
    parser.add_argument("-v", "--version", action="version", 
                        version="%(prog)s 0.1.0")
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # 处理输入
    input_path = args.input
    if os.path.isdir(input_path):
        process_batch(input_path, args.device, args.output)
    elif os.path.isfile(input_path):
        if input_path.lower().endswith((".png", ".jpg", ".jpeg")):
            output_path = process_auto(input_path, args.device, args.output)
            print(f"✅ 处理完成: {output_path}")
        else:
            print(f"❌ 不支持的文件类型: {input_path}")
    else:
        print(f"❌ 输入路径不存在: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()