import os
import glob
import re
import sys

def theme_pacman_svg(svg_content):
    content = svg_content

    # 1. Defs injection: Gradient backgrounds, nebula glow, wall neon glow filter
    defs_to_inject = '''
    <!-- Obsidian Velvet Gradients & Glow Filters -->
    <linearGradient id="canvas-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#07020E"/>
      <stop offset="30%" stop-color="#120524"/>
      <stop offset="70%" stop-color="#180730"/>
      <stop offset="100%" stop-color="#06020C"/>
    </linearGradient>
    <radialGradient id="canvas-nebula1" cx="15%" cy="30%" r="50%">
      <stop offset="0%" stop-color="#A855F7" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#07020E" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="canvas-nebula2" cx="85%" cy="70%" r="45%">
      <stop offset="0%" stop-color="#EC4899" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#07020E" stop-opacity="0"/>
    </radialGradient>
    <filter id="wall-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="dot-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="canvas-clip">
      <rect x="0.5" y="0.5" width="1165" height="183" rx="12"/>
    </clipPath>
'''

    if '<defs>' in content:
        content = content.replace('<defs>', f'<defs>{defs_to_inject}', 1)
    else:
        content = content.replace('<svg ', f'<svg ><defs>{defs_to_inject}</defs>', 1)

    # 2. Canvas Background replacement
    # Wrap base background in clipPath and draw rich nebula velvet canvas with subtle architectural border
    bg_replacement = '''<g clip-path="url(#canvas-clip)">
      <rect x="0.5" y="0.5" width="1165" height="183" fill="url(#canvas-bg)"/>
      <rect x="0.5" y="0.5" width="1165" height="183" fill="url(#canvas-nebula1)"/>
      <rect x="0.5" y="0.5" width="1165" height="183" fill="url(#canvas-nebula2)"/>
      <!-- Precision Architectural Corner Accents -->
      <g stroke="#60A5FA" stroke-width="1" opacity="0.35">
        <path d="M 8 18 L 8 8 L 18 8"/>
        <path d="M 1158 18 L 1158 8 L 1148 8"/>
        <path d="M 8 166 L 8 176 L 18 176"/>
        <path d="M 1158 166 L 1158 176 L 1148 176"/>
      </g>
    </g>
    <rect x="0.75" y="0.75" width="1164.5" height="182.5" rx="12" fill="none" stroke="#250B3D" stroke-width="1.5"/>'''

    # Replace existing background rect
    content = re.sub(
        r'<rect width="100%" height="100%" fill="[^"]+"/>',
        bg_replacement,
        content
    )
    content = re.sub(
        r'<rect x="0\.75" y="0\.75" width="1164\.5" height="182\.5" rx="10" fill="[^"]+" stroke="[^"]+" stroke-width="1\.5"/>',
        bg_replacement,
        content
    )

    # 3. Empty grid cells: Deep obsidian plum #150727 with rx="4"
    content = re.sub(r'fill="#161b22"', 'fill="#150727"', content)
    content = re.sub(r'fill="#ebedf0"', 'fill="#150727"', content)
    content = re.sub(r'fill="#16082C"', 'fill="#150727"', content)

    # 4. Maze walls: Electric Neon Violet #C084FC with wall glow filter
    # Wall rects have id="wh-..." or id="wv-..."
    content = re.sub(
        r'(<rect id="w[hv]-[0-9]+-[0-9]+"[^>]*fill=")[^"]+(")',
        r'\g<1>#C084FC\2 filter="url(#wall-glow)"',
        content
    )
    # Generic fill fallback
    content = re.sub(r'fill="#ffffff"', 'fill="#C084FC" filter="url(#wall-glow)"', content)

    # 5. Commit levels: Luminous Emerald Glow matching beacon #34D399 & TrustNest #10B981
    content = re.sub(r'#0e4429', '#064e3b', content)
    content = re.sub(r'#9be9a8', '#064e3b', content)

    content = re.sub(r'#006d32', '#059669', content)
    content = re.sub(r'#40c463', '#059669', content)

    content = re.sub(r'#26a641', '#10b981', content)
    content = re.sub(r'#30a14e', '#10b981', content)

    content = re.sub(r'#39d353', '#34d399', content)
    content = re.sub(r'#216e39', '#34d399', content)

    # 6. Pac-Man dissolve & empty cells in animation values
    content = content.replace(';#16082C;', ';#150727;')
    content = content.replace(';#16082C"', ';#150727"')

    # 7. Month labels: High-fashion monospace uppercase in electric violet #C084FC with letter-spacing
    content = re.sub(
        r'<text ([^>]+) fill="#[0-9a-fA-F]+"([^>]*)>([A-Za-z]+)</text>',
        r'<text \1 fill="#C084FC"\2 font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-weight="600" letter-spacing="1.5">\3</text>',
        content
    )
    content = re.sub(r'fill="#8b949e"', 'fill="#C084FC"', content)
    content = re.sub(r'fill="#57606a"', 'fill="#C084FC"', content)

    return content

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

        themed = theme_pacman_svg(content)

        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(themed)
        print(f"Successfully themed {svg_file}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "dist"
    if os.path.isfile(target):
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
        themed = theme_pacman_svg(content)
        with open(target, "w", encoding="utf-8") as f:
            f.write(themed)
        print(f"Successfully themed file {target}")
    else:
        theme_pacman_svgs(target)
