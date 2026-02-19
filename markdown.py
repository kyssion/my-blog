import re
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# ======================
# 配置区（根据你的项目结构调整）
# ======================
INPUT_ROOT = Path(".")                # Markdown 源文档根目录
BLOGIMG_DIR = Path("./blogimg")            # 原始图片目录（通常与 docs 同级）
OUTPUT_POSTS = Path("../hexo-blog/source/_posts")     # Hexo 文章输出目录
OUTPUT_IMAGES = Path("../hexo-blog/source/images")    # Hexo 图片资源输出目录

# ======================
# 步骤 1：迁移图片资源
# ======================
if BLOGIMG_DIR.exists():
    target_img_dir = OUTPUT_IMAGES / "blogimg"
    print(f"🔄 正在复制图片资源: {BLOGIMG_DIR} → {target_img_dir}")
    if target_img_dir.exists():
        shutil.rmtree(target_img_dir)  # 清空旧内容（可选）
    shutil.copytree(BLOGIMG_DIR, target_img_dir)
    print("✅ 图片资源已复制完成")
else:
    print(f"⚠️ 未找到 blogimg 目录: {BLOGIMG_DIR.absolute()}")

# ======================
# 步骤 2：收集并处理 Markdown 文件
# ======================
md_files = []

print("🔍 正在扫描 Markdown 文件（跳过含 'hexo-web' 的路径）...")
for md_path in INPUT_ROOT.rglob("*.md"):
    try:
        rel_path = md_path.relative_to(INPUT_ROOT)
    except ValueError:
        continue  # 安全防护：不应发生

    # ✅ 忽略任何路径中包含 'hexo-web' 的文件
    if "hexo-web" in rel_path.parts:
        continue

    parts = rel_path.parts
    if len(parts) < 2:
        print(f"⚠️ 跳过根目录下的文件（无分类）: {md_path}")
        continue

    category = parts[0]
    if len(parts) >= 3:
        tag = parts[1]
        title = md_path.stem
        md_files.append((md_path, category, [tag], title))
    else:
        # 无二级目录 → 无标签
        title = md_path.stem
        md_files.append((md_path, category, [], title))

# 稳定排序（确保每次运行顺序一致）
md_files.sort(key=lambda x: str(x[0]))

if not md_files:
    print("❌ 未找到符合条件的 Markdown 文件！")
    exit(1)

# ======================
# 步骤 3：生成 Hexo 文章
# ======================
start_date = datetime(2024, 12, 31, 23, 59, 0)
OUTPUT_POSTS.mkdir(parents=True, exist_ok=True)

for i, (md_path, category, tags, title) in enumerate(md_files):
    post_date = start_date - timedelta(minutes=i)
    date_str = post_date.strftime("%Y-%m-%d %H:%M:%S")

    # 读取原文
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取失败 {md_path}: {e}")
        continue

    # 替换图片路径：/blogimg/... → /images/blogimg/...
    content = re.sub(
        r'(!\[.*?\]\()(/blogimg/[^)]*?)(\))',
        r'\1/images/blogimg/\2\3',
        content
    )
    # 处理 HTML img 标签（可选但推荐）
    content = re.sub(
        r'(<img[^>]*src=")(/blogimg/[^"]*?)(")',
        r'\1/images/blogimg/\2\3',
        content
    )

    # 构建 tags 行
    tags_line = f"tags: [{', '.join(tags)}]" if tags else "tags: []"

    front_matter = f"""---
title: {title}
date: {date_str}
categories: [{category}]
{tags_line}
---
"""

    new_content = front_matter + "\n" + content

    # 生成安全文件名
    safe_title = re.sub(r'[^\w\-]', '-', title)
    output_filename = f"{safe_title}.md"
    output_path = OUTPUT_POSTS / output_filename

    # 避免覆盖
    counter = 1
    while output_path.exists():
        output_path = OUTPUT_POSTS / f"{safe_title}-{counter}.md"
        counter += 1

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    tag_info = f" | tags: {tags}" if tags else " | 无标签"
    print(f"✅ {title} → 分类: {category}{tag_info}")

print(f"\n🎉 共成功迁移 {len(md_files)} 篇文章到 {OUTPUT_POSTS}")
print("💡 请运行 `hexo clean && hexo generate` 预览效果")