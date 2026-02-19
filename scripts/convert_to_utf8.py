#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将项目中 GB2312/GBK 编码的文件转换为 UTF-8 编码。
解决 Cursor 按 UTF-8 打开时中文变成问号和乱码的问题。
"""

import os
import sys
import argparse
from pathlib import Path

# 需要转换的文件扩展名
TEXT_EXTENSIONS = {'.cpp', '.h', '.c', '.hpp', '.cc', '.cxx', '.rc', '.xml', '.json', '.txt', '.md'}

# 排除的目录
EXCLUDE_DIRS = {'build', '.git', 'node_modules', '__pycache__', '.vs', '.history', '3rd'}


def is_chinese_char(c: str) -> bool:
    """判断是否为中文字符（CJK 统一汉字范围）"""
    return '\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf'


def has_chinese(text: str) -> bool:
    """检查文本是否包含中文"""
    return any(is_chinese_char(c) for c in text)


def detect_and_convert(file_path: Path, dry_run: bool = False):
    """
    检测文件编码并转换为 UTF-8。
    返回 (是否已转换, 状态信息)
    """
    try:
        raw = file_path.read_bytes()
    except Exception as e:
        return False, f"读取失败: {e}"

    if len(raw) == 0:
        return False, "空文件"

    # 已有 UTF-8 BOM，尝试 UTF-8 解码
    if raw.startswith(b'\xef\xbb\xbf'):
        try:
            text = raw.decode('utf-8')
            if has_chinese(text):
                return False, "已是 UTF-8 (BOM)"
            return False, "已是 UTF-8 (BOM)"
        except UnicodeDecodeError:
            pass

    # 尝试 UTF-8 解码（无 BOM）
    try:
        text_utf8 = raw.decode('utf-8', errors='strict')
        if has_chinese(text_utf8):
            return False, "已是 UTF-8"
        return False, "已是 UTF-8 (无中文)"
    except UnicodeDecodeError:
        # UTF-8 解码失败，尝试 GBK
        pass

    # 尝试 GBK/GB2312 解码
    try:
        text_gbk = raw.decode('gbk', errors='strict')
    except (UnicodeDecodeError, LookupError):
        try:
            text_gbk = raw.decode('gb2312', errors='strict')
        except (UnicodeDecodeError, LookupError):
            return False, "无法识别编码，跳过"

    # 确认包含中文（避免误转纯 ASCII/英文文件）
    if not has_chinese(text_gbk):
        return False, "GBK 解码成功但无中文"

    if dry_run:
        return True, f"将转换: {len(text_gbk)} 字符，含中文"

    # 写入 UTF-8
    # .rc 文件建议带 BOM，以便 Windows 资源编译器正确识别
    use_bom = file_path.suffix.lower() == '.rc'
    try:
        utf8_bytes = text_gbk.encode('utf-8')
        if use_bom:
            utf8_bytes = b'\xef\xbb\xbf' + utf8_bytes
        file_path.write_bytes(utf8_bytes)
        return True, f"已转换为 UTF-8 ({'BOM' if use_bom else '无BOM'})"
    except Exception as e:
        return False, f"写入失败: {e}"


def main():
    parser = argparse.ArgumentParser(description='将 GB2312/GBK 文件转换为 UTF-8')
    parser.add_argument('root', nargs='?', default='.', help='项目根目录')
    parser.add_argument('-n', '--dry-run', action='store_true', help='仅预览，不实际修改')
    parser.add_argument('--include-demos', action='store_true', help='包含 Demos 目录')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"错误: 目录不存在: {root}")
        sys.exit(1)

    converted = []
    skipped = []
    errors = []

    for file_path in root.rglob('*'):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if any(ex in file_path.parts for ex in EXCLUDE_DIRS):
            continue
        if not args.include_demos and 'Demos' in file_path.parts:
            continue

        success, msg = detect_and_convert(file_path, dry_run=args.dry_run)
        rel_path = file_path.relative_to(root)
        if success:
            converted.append((str(rel_path), msg))
        elif "失败" in msg or "错误" in msg:
            errors.append((str(rel_path), msg))
        else:
            skipped.append((str(rel_path), msg))

    # 输出结果
    if converted:
        print(f"\n{'[预览] ' if args.dry_run else ''}已转换 {len(converted)} 个文件:\n")
        for path, msg in converted:
            print(f"  {path}")
            print(f"    -> {msg}")
    else:
        print("\n无需转换或转换失败。")

    if errors:
        print(f"\n{len(errors)} 个文件处理异常:")
        for path, msg in errors:
            print(f"  {path}: {msg}")

    if args.dry_run and converted:
        print("\n此为预览，未实际修改。移除 -n 参数执行转换。")


if __name__ == '__main__':
    main()
