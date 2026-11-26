import os
import glob
import re
import sys

def theme_pacman_svgs(dist_dir="dist"):
    if not os.path.isdir(dist_dir):
        print(f"Directory {dist_dir} not found.")
        return

    svg_files = glob.glob(os.path.join(dist_dir, "*.svg"))
    if not svg_files:
        print(f"No SVG files found in {dist_dir}")
        return

    for svg_file in svg_files:
        with open(svg_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Canvas Background: Obsidian-velvet #07020E with rounded corners and subtle card stroke
        content = re.sub(
            r'<rect width="100%" height="100%" fill="[^"]+"/>',
            r'<rect x="0.75" y="0.75" width="1164.5" height="182.5" rx="10" fill="#07020E" stroke="#250B3D" stroke-width="1.5"/>',
            content
        )

        # 2. Empty grid cells: #16082C
        content = re.sub(r'#161b22', '#16082C', content)
        content = re.sub(r'#ebedf0', '#16082C', content)

        # 3. Maze walls: Electric Neon Violet #C084FC
        content = re.sub(r'fill="#ffffff"', 'fill="#C084FC"', content)
        content = re.sub(r'fill="#000000"', 'fill="#C084FC"', content)

        # 4. Commit levels: Luminous Emerald Glow matching beacon #34D399 & TrustNest #10B981
        content = re.sub(r'#0e4429', '#064e3b', content)
        content = re.sub(r'#9be9a8', '#064e3b', content)

        content = re.sub(r'#006d32', '#059669', content)
        content = re.sub(r'#40c463', '#059669', content)

        content = re.sub(r'#26a641', '#10b981', content)
        content = re.sub(r'#30a14e', '#10b981', content)

        content = re.sub(r'#39d353', '#34d399', content)
        content = re.sub(r'#216e39', '#34d399', content)

        # 5. Month labels text: #C084FC
        content = re.sub(r'fill="#8b949e"', 'fill="#C084FC"', content)
        content = re.sub(r'fill="#57606a"', 'fill="#C084FC"', content)

        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully themed {svg_file}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "dist"
    theme_pacman_svgs(target)
