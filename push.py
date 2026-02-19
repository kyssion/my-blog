import os
import shutil
import sys
from datetime import datetime
import re

def slugify(value):
    """
    将字符串转换为 URL 友好的 slug。
    简单处理，可按需增强。
    """
    # 替换空格和特殊字符为连字符，并转为小写
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)
    return value

def get_user_input_for_file(filepath):
    """获取用户对单个文件的输入信息"""
    filename = os.path.splitext(os.path.basename(filepath))[0]
    
    print(f"\n正在处理文件: {os.path.basename(filepath)}")
    
    # 1. 获取 Title (默认为文件名)
    title = input(f"请输入文章标题 (回车使用文件名 '{filename}') : ").strip()
    if not title:
        title = filename
    
    # 2. 获取 Categories (多个类别用逗号分隔)
    categories_input = input("请输入分类 (多个分类用逗号','分隔): ").strip()
    categories = [cat.strip() for cat in categories_input.split(',') if cat.strip()]
    # 如果没有输入，则使用一个默认分类或留空
    if not categories:
        print("未输入分类，将使用 '未分类'。")
        categories = ['未分类']
        
    # 3. 获取 Tags (多个标签用逗号分隔)
    tags_input = input("请输入标签 (多个标签用逗号','分隔): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    # 如果没有输入，则使用一个默认标签或留空
    if not tags:
        print("未输入标签，将使用 'default'。")
        tags = ['default']

    return title, categories, tags

def add_hexo_front_matter(content, title, categories, tags):
    """在 Markdown 内容前添加 Hexo Front-matter"""
    # 检查原内容是否已有 front-matter
    existing_front_matter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if existing_front_matter_match:
        existing_front_matter_content = existing_front_matter_match.group(1)
        rest_of_content = existing_front_matter_match.group(2)
        # 解析现有 front-matter (这里简化处理，实际可能需要更复杂的解析器如 ruamel.yaml)
        # 为了简单起见，我们直接替换整个 front-matter
        # 或者，如果只想更新特定字段，逻辑会更复杂。
        # 这里我们选择替换，因为这是最常见的场景。
        pass

    # 构建新的 front-matter
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 处理列表格式
    categories_str = '\n'.join([f'  - {cat}' for cat in categories])
    tags_str = '\n'.join([f'  - {tag}' for tag in tags])
    
    new_front_matter = f"""---
title: {title}
date: {date_str}
categories:
{categories_str}
tags:
{tags_str}
---

"""

    # 返回新 front-matter + 原内容 (去掉旧 front-matter)
    if existing_front_matter_match:
        return new_front_matter + rest_of_content
    else:
        return new_front_matter + content

def main():
    # --- 配置区 ---
    # 请修改为你自己的 Hexo 博客 source/_posts 目录路径
    HEXO_POSTS_DIR = r"C:\Users\14099\Documents\my-blog\hexo-blog\source\_posts"
    # --- 配置结束 ---

    if len(sys.argv) < 2:
        print("用法: python md_to_hexo.py <markdown_file1.md> [markdown_file2.md ...]")
        print("或者将文件拖拽到此脚本上。")
        sys.exit(1)

    markdown_files = []
    for arg in sys.argv[1:]:
        if os.path.isfile(arg) and arg.lower().endswith('.md'):
            markdown_files.append(arg)
        else:
            print(f"警告: '{arg}' 不是有效的 .md 文件，已跳过。")

    if not markdown_files:
        print("错误: 没有找到有效的 Markdown 文件。")
        sys.exit(1)

    print(f"找到 {len(markdown_files)} 个 Markdown 文件待处理。")

    for src_file_path in markdown_files:
        try:
            # 获取用户输入
            title, categories, tags = get_user_input_for_file(src_file_path)

            # 读取原文件内容
            with open(src_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # 添加或修改 front-matter
            updated_content = add_hexo_front_matter(original_content, title, categories, tags)

            # 确定目标文件名 (slugified_title.md)
            dest_filename = slugify(title) + '.md'
            dest_file_path = os.path.join(HEXO_POSTS_DIR, dest_filename)

            # 检查目标文件是否存在，避免覆盖
            if os.path.exists(dest_file_path):
                counter = 1
                name_part, ext = os.path.splitext(dest_filename)
                while os.path.exists(os.path.join(HEXO_POSTS_DIR, f"{name_part}_{counter}{ext}")):
                    counter += 1
                dest_file_path = os.path.join(HEXO_POSTS_DIR, f"{name_part}_{counter}{ext}")
                print(f"  -> 目标文件已存在，重命名为: {os.path.basename(dest_file_path)}")

            # 将新内容写入目标文件
            with open(dest_file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print(f"  -> 成功复制并处理: {src_file_path} -> {dest_file_path}")

        except Exception as e:
            print(f"  -> 处理文件 '{src_file_path}' 时出错: {e}")

if __name__ == "__main__":
    main()