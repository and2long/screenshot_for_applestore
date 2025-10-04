import os
import sys

from PIL import Image
from psd_tools import PSDImage

# 固定 PSD 文件路径，始终以项目根目录为基准
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSD_FILE = os.path.join(BASE_DIR, "psd", "iPadPro13-M4-Silver-Portrait.psd")
# 输出目录固定为当前目录下的 output 文件夹
OUTPUT_DIR = "output"

def process_image(screenshot_path, psd_path=PSD_FILE, output_dir=OUTPUT_DIR):
    """处理单张截图并生成带边框的 JPEG 图片"""
    # 打开 PSD
    psd = PSDImage.open(psd_path)

    # 查找目标图层
    hardware_layer = None
    screen_layer = None
    background_layer = None

    for layer in psd:
        name_lower = layer.name.lower()
        if layer.name == "Hardware":
            hardware_layer = layer
        elif layer.name == "Screen":
            screen_layer = layer
        elif "background" in name_lower or "背景" in name_lower:
            background_layer = layer

    if not hardware_layer or not screen_layer:
        raise RuntimeError("❌ PSD 文件中未找到 Hardware 或 Screen 图层")

    # 获取图层图片
    hw_img = hardware_layer.composite().convert("RGBA")
    hw_box = hardware_layer.bbox
    sc_box = screen_layer.bbox
    bg_img = background_layer.composite().convert("RGBA") if background_layer else None

    # 打开并调整截图大小
    screenshot = Image.open(screenshot_path).convert("RGBA")
    sw, sh = sc_box[2] - sc_box[0], sc_box[3] - sc_box[1]
    screenshot = screenshot.resize((sw, sh), Image.LANCZOS)

    # 创建画布
    canvas_size = psd.size
    canvas = bg_img.copy() if bg_img else Image.new("RGBA", canvas_size, (255, 255, 255, 255))

    # 贴入截图
    canvas.paste(screenshot, (sc_box[0], sc_box[1]), screenshot)
    # 贴入 Hardware 图层
    canvas.alpha_composite(hw_img, dest=(hw_box[0], hw_box[1]))

    # 去掉透明通道，转换为 RGB
    final_image = canvas.convert("RGB")

    # 输出路径
    filename = os.path.basename(screenshot_path)
    name, _ = os.path.splitext(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, f"{name}_framed.jpg")

    # 保存为 JPEG 并压缩体积
    final_image.save(output_path, "JPEG", quality=85, optimize=True)
    return output_path

def main(input_path):
    if not os.path.exists(PSD_FILE):
        print(f"❌ PSD 文件不存在: {PSD_FILE}")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 判断输入是文件还是文件夹
    if os.path.isfile(input_path):
        print(f"📷 处理单张截图: {input_path}")
        out = process_image(input_path)
        print(f"✅ 输出: {out}")
    elif os.path.isdir(input_path):
        files = [f for f in os.listdir(input_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        total = len(files)
        if total == 0:
            print("❌ 文件夹中没有截图文件")
            return
        print(f"📂 处理文件夹中的 {total} 张截图...")
        for i, f in enumerate(files, start=1):
            path = os.path.join(input_path, f)
            print(f"⏳ 正在处理第 {i}/{total} 张: {f}")
            out = process_image(path)
            print(f"✅ 输出: {out}")
        print("🎉 批量处理完成")
    else:
        print("❌ 输入路径不存在")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python ipad_batch.py 截图文件或文件夹路径")
        sys.exit(1)

    input_path = sys.argv[1]
    main(input_path)
