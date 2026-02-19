import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# --- 配置区域 ---
# 请修改为你自己的 Hexo 源文件夹路径 (通常是 hexo/source/_posts)
DEFAULT_HEXO_POSTS_DIR = Path("~/my-hexo-blog/source/_posts").expanduser()
# --- 配置结束 ---

def get_categories_and_tags(source_path: Path, file_path: Path):
    """
    根据源路径和文件路径计算 categories 和 tags。
    """
    # 获取相对于源路径的相对路径
    rel_path = file_path.relative_to(source_path)
    
    parts = list(rel_path.parent.parts)
    
    if not parts or parts == ['.']: # 文件在源路径根目录下
        return [], []
    elif len(parts) == 1: # 文件在一级子目录下
        category = [parts[0]]
        tag = [parts[0]]
    else: # 文件在多级子目录下
        category = [parts[0]] # 第一层为 category
        tag = parts[1:] + [parts[0]] # 其余层及第一层都作为 tag
    
    return category, tag

def generate_front_matter(title, date_str, categories, tags, author):
    """
    生成 Hexo 兼容的 front-matter 字符串。
    """
    fm_parts = ["---"]
    fm_parts.append(f"title: {title}")
    fm_parts.append(f"date: {date_str}")
    fm_parts.append("categories:")
    for cat in categories:
        fm_parts.append(f"  - {cat}")
    fm_parts.append("tags:")
    for tag in tags:
        fm_parts.append(f"  - {tag}")
    if author:
        fm_parts.append(f"author: {author}")
    fm_parts.append("---\n") # 添加一个换行以与内容分开
    return "\n".join(fm_parts)

def process_markdown_file(src_file: Path, dest_dir: Path, source_root: Path, args):
    """
    处理单个 Markdown 文件：读取、添加 front-matter、写入目标目录。
    """
    print(f"正在处理文件: {src_file}")

    # 1. 确定标题
    default_title = src_file.stem # 去掉 .md 后缀的文件名
    title = args.title or default_title

    # 2. 确定日期
    date_str = args.date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 3. 确定分类和标签
    default_categories, default_tags = get_categories_and_tags(source_root, src_file)
    categories = args.categories.split(',') if args.categories else default_categories
    tags = args.tags.split(',') if args.tags else default_tags

    # 4. 生成最终文件名 (修改：直接使用原始文件名)
    final_filename = src_file.name # 直接使用原始文件名，例如 'my_note.md'
    final_dest_path = dest_dir / final_filename

    # 5. 读取原文件内容
    with open(src_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # 6. 生成新的 front-matter
    new_front_matter = generate_front_matter(
        title=title,
        date_str=date_str,
        categories=categories,
        tags=tags,
        author=args.author
    )

    # 7. 写入新文件
    try:
        with open(final_dest_path, 'w', encoding='utf-8') as f:
            f.write(new_front_matter)
            f.write(original_content) # 写入原始内容
        print(f"  -> 成功复制并处理到: {final_dest_path}")
    except Exception as e:
        print(f"  -> 写入文件失败: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="将 Markdown 文件复制到 Hexo _posts 目录，并自动生成 front-matter。\n注意：此版本保留原始文件名。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "source",
        type=str,
        help="源文件路径或源文件夹路径。如果是指向文件，则处理该文件；如果是指向文件夹，则递归处理文件夹内所有 .md 文件。"
    )
    parser.add_argument(
        "-d", "--dest",
        type=str,
        default=str(DEFAULT_HEXO_POSTS_DIR),
        help=f"目标 Hexo _posts 文件夹路径 (默认: {DEFAULT_HEXO_POSTS_DIR})"
    )
    parser.add_argument(
        "-t", "--title",
        type=str,
        help="手动指定文章标题。如果不提供，则使用文件名 (不含 .md)。"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="手动指定发布日期 (格式: YYYY-MM-DD HH:MM:SS)。如果不提供，则使用当前时间。"
    )
    parser.add_argument(
        "-c", "--categories",
        type=str,
        help="手动指定分类，多个分类用逗号分隔 (e.g., '技术,Python')。如果不提供，则按规则自动生成。"
    )
    parser.add_argument(
        "-T", "--tags",
        type=str,
        help="手动指定标签，多个标签用逗号分隔 (e.g., '编程,学习')。如果不提供，则按规则自动生成。"
    )
    parser.add_argument(
        "-a", "--author",
        type=str,
        help="指定作者名字。"
    )

    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    dest_dir = Path(args.dest).resolve()

    # 确保目标目录存在
    dest_dir.mkdir(parents=True, exist_ok=True)

    if not source_path.exists():
        print(f"错误: 源路径不存在 -> {source_path}")
        return

    # 如果源是一个单独的文件
    if source_path.is_file() and source_path.suffix.lower() == '.md':
        # 在这种情况下，source_root 是其父目录
        source_root_for_file = source_path.parent
        process_markdown_file(source_path, dest_dir, source_root_for_file, args)
        return

    # 如果源是一个目录
    if source_path.is_dir():
        # 在这种情况下，source_root 就是该目录本身
        source_root_for_dir = source_path
        md_files_found = False
        for md_file in source_path.rglob("*.md"): # 递归查找所有 .md 文件
            md_files_found = True
            process_markdown_file(md_file, dest_dir, source_root_for_dir, args)
        
        if not md_files_found:
            print(f"在目录 '{source_path}' 及其子目录中未找到任何 .md 文件。")
        return

    print(f"错误: 源路径不是一个有效的 .md 文件或目录 -> {source_path}")


if __name__ == "__main__":
    main()