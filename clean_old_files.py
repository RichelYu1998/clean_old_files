#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理所有下载日期超过7天的文件
"""

import os
import re
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


def setup_logger(log_file: Optional[str] = None, log_level: int = logging.INFO) -> logging.Logger:
    """
    设置日志记录器，按照clean.py的日志规格
    
    Args:
        log_file: 日志文件路径
        log_level: 日志级别
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger('FileCleaner')
    logger.setLevel(log_level)
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def format_size(size_bytes: int) -> str:
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
    
    Returns:
        str: 格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_type(extension: str) -> str:
    """
    根据文件扩展名获取文件类型描述
    
    Args:
        extension: 文件扩展名
    
    Returns:
        str: 文件类型描述
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg'}
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'}
    document_extensions = {'.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'}
    archive_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz'}
    
    if extension in image_extensions:
        return "图片"
    elif extension in video_extensions:
        return "视频"
    elif extension in document_extensions:
        return "文档"
    elif extension in archive_extensions:
        return "压缩包"
    else:
        return "其他"


def clean_files_older_than_days(
        directory: str,
        days: int = 7,
        dry_run: bool = False,
        log_file: Optional[str] = None,
        log_level: int = logging.INFO
) -> None:
    """
    清理下载时间超过指定天数的所有文件
    
    Args:
        directory: 要清理的目录
        days: 保留的天数（超过此天数的文件将被删除）
        dry_run: 测试模式，不实际删除文件
        log_file: 日志文件路径
        log_level: 日志级别
    """
    logger = setup_logger(log_file, log_level)
    
    # 标准化目录路径（跨平台兼容）
    directory_path = Path(directory).resolve()
    
    logger.info("=" * 60)
    logger.info("开始清理旧文件")
    logger.info(f"清理目录: {directory_path}")
    logger.info(f"删除规则: 删除所有超过 {days} 天的文件")
    logger.info(f"删除规则: 删除所有空文件夹（不考虑时间）")
    logger.info(f"排除规则: 保留.log文件和脚本文件本身")
    logger.info(f"排序方式: 按文件下载到本地的修改时间")
    logger.info(f"测试模式: {'是' if dry_run else '否'}")
    logger.info("=" * 60)

    if not directory_path.exists():
        logger.error(f"目录不存在: {directory_path}")
        return

    if not directory_path.is_dir():
        logger.error(f"路径不是目录: {directory_path}")
        return

    current_time = datetime.now()
    cutoff_time = current_time.timestamp() - (days * 24 * 60 * 60)

    all_files = []
    files_to_delete = []
    
    logger.info("扫描文件中...")
    
    # 递归扫描目录中的所有文件
    for file_path in directory_path.rglob('*'):
        if file_path.is_file():
            try:
                # 排除规则：不删除.log文件和脚本文件本身
                if file_path.suffix.lower() == '.log' or file_path.name == 'clean_old_files.py':
                    continue
                    
                file_stat = file_path.stat()
                mtime = file_stat.st_mtime
                download_time = datetime.fromtimestamp(mtime)
                age_days = (current_time - download_time).days
                
                file_info = {
                    'path': file_path,
                    'name': file_path.name,
                    'size': file_stat.st_size,
                    'mtime': mtime,
                    'download_time': download_time,
                    'age_days': age_days,
                    'extension': file_path.suffix.lower(),
                    'file_type': get_file_type(file_path.suffix.lower())
                }
                
                all_files.append(file_info)
                
                # 如果文件超过指定天数，添加到删除列表
                if mtime < cutoff_time:
                    files_to_delete.append(file_info)
                    
            except (PermissionError, FileNotFoundError) as e:
                logger.warning(f"无法访问文件 {file_path}: {e}")

    if not all_files:
        logger.warning("目录中没有文件")
        return

    if not files_to_delete:
        logger.info(f"没有超过 {days} 天的旧文件需要删除")
        return

    # 按下载时间排序（从旧到新）
    files_to_delete.sort(key=lambda x: x['mtime'])
    
    total_files = len(all_files)
    delete_count = len(files_to_delete)
    delete_size = sum(f['size'] for f in files_to_delete)
    
    logger.info(f"扫描完成，共找到 {total_files} 个文件")
    logger.info(f"需要删除 {delete_count} 个超过 {days} 天的旧文件")
    logger.info(f"释放空间: {format_size(delete_size)}")
    
    logger.info("\n待删除文件列表（从最旧到最新）：")
    for i, file_info in enumerate(files_to_delete[:30], 1):
        download_time_str = file_info['download_time'].strftime('%Y-%m-%d %H:%M:%S')
        logger.info(
            f"{i:3d}. {file_info['name']} ({file_info['file_type']}, {format_size(file_info['size'])}, "
            f"下载时间: {download_time_str}, 已存在: {file_info['age_days']}天)")
    
    if len(files_to_delete) > 30:
        logger.info(f"... 还有 {len(files_to_delete) - 30} 个文件")

    if dry_run:
        logger.info("\n[测试模式] 未实际删除文件")
        logger.info("清理完成（测试模式）")
        return

    logger.info("\n开始删除文件...")
    deleted_count = 0
    failed_count = 0
    deleted_size = 0

    for file_info in files_to_delete:
        try:
            file_info['path'].unlink()
            deleted_count += 1
            deleted_size += file_info['size']
            logger.info(f"已删除: {file_info['name']} ({file_info['file_type']}, {format_size(file_info['size'])})")
        except PermissionError:
            logger.error(f"删除失败（权限不足）: {file_info['name']}")
            failed_count += 1
        except FileNotFoundError:
            logger.warning(f"文件不存在（可能已被删除）: {file_info['name']}")
            failed_count += 1
        except Exception as e:
            logger.error(f"删除失败 {file_info['name']}: {e}")
            failed_count += 1

    logger.info("\n" + "=" * 60)
    logger.info("清理完成")
    logger.info("删除统计信息:")
    logger.info(f"  - 成功删除文件数量: {deleted_count} 个")
    logger.info(f"  - 删除失败文件数量: {failed_count} 个")
    logger.info(f"  - 释放空间总计: {format_size(deleted_size)}")
    
    # 详细统计信息
    if deleted_count > 0:
        logger.info("\n详细统计:")
        logger.info(f"  - 平均文件大小: {format_size(deleted_size / deleted_count)}")
        logger.info(f"  - 删除文件占比: {deleted_count}/{total_files} ({deleted_count/total_files*100:.1f}%)")
        logger.info(f"  - 剩余文件数量: {total_files - deleted_count} 个")
    
    # 文件类型统计
    if deleted_count > 0:
        file_type_stats = {}
        for file_info in files_to_delete:
            file_type = file_info['file_type']
            if file_type not in file_type_stats:
                file_type_stats[file_type] = {'count': 0, 'size': 0}
            file_type_stats[file_type]['count'] += 1
            file_type_stats[file_type]['size'] += file_info['size']
        
        logger.info("\n文件类型统计:")
        for file_type, stats in sorted(file_type_stats.items(), key=lambda x: x[1]['size'], reverse=True):
            logger.info(f"  - {file_type}: {stats['count']} 个文件, {format_size(stats['size'])}")
    
    # 总结信息
    logger.info("\n总结:")
    if deleted_count > 0:
        logger.info(f"✓ 成功清理了 {deleted_count} 个旧文件")
        logger.info(f"✓ 释放了 {format_size(deleted_size)} 磁盘空间")
    else:
        logger.info("ℹ 没有需要删除的旧文件")
    
    if failed_count > 0:
        logger.warning(f"⚠ 有 {failed_count} 个文件删除失败")
    
    # 删除所有空文件夹（不考虑下载时间）
    logger.info("\n开始扫描和删除空文件夹...")
    folders_to_delete = []
    
    # 递归扫描所有文件夹
    for folder_path in directory_path.rglob('*'):
        if folder_path.is_dir():
            try:
                # 检查文件夹是否为空
                folder_items = list(folder_path.iterdir())
                is_empty = len(folder_items) == 0
                
                # 如果文件夹为空，添加到删除列表（不考虑时间）
                if is_empty:
                    # 获取文件夹信息（仅用于日志记录）
                    folder_stat = folder_path.stat()
                    folder_mtime = folder_stat.st_mtime
                    folder_download_time = datetime.fromtimestamp(folder_mtime)
                    folder_age_days = (current_time - folder_download_time).days
                    
                    folders_to_delete.append({
                        'path': folder_path,
                        'name': folder_path.name,
                        'mtime': folder_mtime,
                        'download_time': folder_download_time,
                        'age_days': folder_age_days,
                        'reason': '空文件夹'
                    })
                    
            except (PermissionError, FileNotFoundError) as e:
                logger.warning(f"无法访问文件夹 {folder_path}: {e}")
    
    if folders_to_delete:
        logger.info(f"需要删除 {len(folders_to_delete)} 个文件夹")
        logger.info("\n待删除文件夹列表：")
        for i, folder_info in enumerate(folders_to_delete[:20], 1):
            download_time_str = folder_info['download_time'].strftime('%Y-%m-%d %H:%M:%S')
            logger.info(
                f"{i:3d}. {folder_info['name']} ({folder_info['reason']}, "
                f"创建时间: {download_time_str}, 已存在: {folder_info['age_days']}天)")
        
        if len(folders_to_delete) > 20:
            logger.info(f"... 还有 {len(folders_to_delete) - 20} 个文件夹")
        
        if not dry_run:
            deleted_folders_count = 0
            failed_folders_count = 0
            
            for folder_info in folders_to_delete:
                try:
                    folder_info['path'].rmdir()  # 使用rmdir只能删除空文件夹
                    deleted_folders_count += 1
                    logger.info(f"已删除文件夹: {folder_info['name']} ({folder_info['reason']})")
                except OSError as e:
                    # 如果文件夹不为空，rmdir会失败，这是正常的
                    if "目录不是空的" in str(e) or "The directory is not empty" in str(e):
                        logger.warning(f"文件夹不为空，跳过删除: {folder_info['name']}")
                    else:
                        logger.error(f"删除文件夹失败 {folder_info['name']}: {e}")
                        failed_folders_count += 1
                except PermissionError:
                    logger.error(f"删除文件夹失败（权限不足）: {folder_info['name']}")
                    failed_folders_count += 1
                except FileNotFoundError:
                    logger.warning(f"文件夹不存在（可能已被删除）: {folder_info['name']}")
                except Exception as e:
                    logger.error(f"删除文件夹失败 {folder_info['name']}: {e}")
                    failed_folders_count += 1
            
            logger.info(f"\n文件夹删除统计:")
            logger.info(f"  - 成功删除文件夹数量: {deleted_folders_count} 个")
            logger.info(f"  - 删除失败文件夹数量: {failed_folders_count} 个")
            
            if deleted_folders_count > 0:
                logger.info(f"✓ 成功清理了 {deleted_folders_count} 个文件夹")
            
            if failed_folders_count > 0:
                logger.warning(f"⚠ 有 {failed_folders_count} 个文件夹删除失败")
    else:
        logger.info("没有需要删除的文件夹")
    
    logger.info("=" * 60)


def main():
    """主函数，提供命令行接口"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='清理所有下载日期超过指定天数的文件')
    parser.add_argument('directory', nargs='?', default='.', help='要清理的目录路径（默认当前目录）')
    parser.add_argument('-d', '--days', type=int, default=7, help='保留的天数（默认7天）')
    parser.add_argument('--dry-run', action='store_true', help='测试模式，不实际删除文件')
    parser.add_argument('--log-file', help='日志文件路径（默认自动生成）')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='日志级别（默认INFO）')
    parser.add_argument('--no-log-file', action='store_true', help='不保存日志文件，只输出到控制台')
    
    args = parser.parse_args()
    
    # 转换为绝对路径
    target_directory = os.path.abspath(args.directory)
    
    # 设置日志级别
    log_level = getattr(logging, args.log_level)
    
    # 自动生成日志文件名（如果未指定且未禁用）
    log_file_path = args.log_file
    if not args.no_log_file and not log_file_path:
        # 生成基于目录和日期的日志文件名（跨平台兼容）
        current_date = datetime.now().strftime('%Y%m%d')
        # 使用Path对象获取目录名，确保跨平台兼容
        target_path = Path(target_directory).resolve()
        # 使用目录名和日期生成安全的文件名
        dir_name = target_path.name if target_path.name else 'current'
        # 替换可能出现在文件名中的非法字符
        safe_dir_name = re.sub(r'[<>:"/\\|?*]', '_', dir_name)
        # 使用跨平台兼容的文件名格式
        log_file_path = f"clean_{safe_dir_name}_{current_date}.log"
    
    print("文件清理工具")
    print("=" * 40)
    print(f"清理目录: {target_directory}")
    print(f"保留天数: {args.days}")
    print(f"测试模式: {args.dry_run}")
    print(f"日志文件: {log_file_path if log_file_path else '控制台输出'}")
    print(f"日志级别: {args.log_level}")
    print()
    
    # 确认操作（仅在非测试模式且非日志文件模式时）
    if not args.dry_run and not log_file_path:
        response = input(f"确认删除超过 {args.days} 天的文件？(y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("操作已取消")
            return
    
    # 执行清理
    clean_files_older_than_days(
        directory=target_directory,
        days=args.days,
        dry_run=args.dry_run,
        log_file=log_file_path,
        log_level=log_level
    )


if __name__ == "__main__":
    main()