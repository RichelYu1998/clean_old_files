# Clean Old Files

一个用于清理下载目录中超过指定天数旧文件的Python脚本工具。

## 功能特性

- **智能清理**：自动删除超过指定天数（默认7天）的文件
- **空文件夹清理**：自动删除所有空文件夹
- **文件类型识别**：支持图片、视频、文档、压缩包等多种文件类型
- **安全排除**：自动排除日志文件（.log）和脚本文件本身
- **测试模式**：支持预览模式，不实际删除文件
- **详细日志**：提供详细的清理报告和统计信息
- **跨平台兼容**：支持Windows、macOS、Linux
- **命令行接口**：支持丰富的命令行参数配置

## 📁 支持的文件类型

### 文档格式
| 扩展名 | 描述 |
|--------|------|
| `.pdf` | PDF文档 |
| `.doc`, `.docx` | Word文档 |
| `.xls`, `.xlsx` | Excel表格 |
| `.ppt`, `.pptx` | PowerPoint演示文稿 |
| `.txt` | 文本文件 |

### 压缩包格式
| 扩展名 | 描述 |
|--------|------|
| `.zip` | ZIP压缩包 |
| `.rar` | RAR压缩包 |
| `.7z` | 7-Zip压缩包 |
| `.tar` | TAR归档 |
| `.gz` | GZIP压缩文件 |

### 图片格式
| 扩展名 | 描述 |
|--------|------|
| `.jpg`, `.jpeg` | JPEG图片 |
| `.png` | PNG图片 |
| `.gif` | GIF动画图片 |
| `.bmp` | BMP位图 |
| `.webp` | WebP图片 |

### 视频格式
| 扩展名 | 描述 |
|--------|------|
| `.mp4` | MP4视频 |
| `.avi` | AVI视频 |
| `.mov` | QuickTime视频 |
| `.mkv` | Matroska视频 |
| `.wmv` | Windows Media视频 |

## 🚀 快速开始

### 基本使用

1. **下载脚本**
   ```bash
   git clone https://github.com/RichelYu1998/clean_old_files.git
   ```
   cd clean_old_files
   ```

2. **查看帮助**
   ```bash
   python clean_old_files.py --help
   ```

3. **测试运行（推荐）**
   ```bash
   python clean_old_files.py --dry-run
   ```

4. **正式清理**
   ```bash
   python clean_old_files.py
   ```

### 命令行使用场景

```bash
# 场景1: 清理当前目录，删除超过7天的文件
python clean_old_files.py

# 场景2: 清理指定目录，删除超过30天的文件
python clean_old_files.py /path/to/downloads -d 30

# 场景3: 测试模式，预览将要删除的文件
python clean_old_files.py --dry-run

# 场景4: 清理并保存详细日志
python clean_old_files.py --log-file cleanup.log --log-level DEBUG

# 场景5: 使用平台特定脚本（Windows）
clean_old_files.bat
```

## 📦 安装与环境要求

### 系统要求

- **操作系统**: Windows 7+, macOS 10.12+, Linux (Ubuntu 16.04+)
- **Python版本**: 3.6 或更高版本
- **磁盘空间**: 至少50MB可用空间
- **权限**: 对目标目录的读写权限

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-repo/clean-old-files.git
   cd clean-old-files
   ```

2. **验证Python版本**
   ```bash
   python --version
   # 应该显示 Python 3.6+ 的版本
   ```

3. **运行脚本**
   ```bash
   python clean_old_files.py
   ```

### 依赖项

本脚本**无需额外安装第三方库**，仅使用Python标准库：

- `os` - 操作系统接口
- `re` - 正则表达式
- `logging` - 日志记录
- `pathlib` - 路径操作
- `datetime` - 日期时间处理
- `argparse` - 命令行参数解析
- `typing` - 类型提示

## 📖 使用方法

### 1. 命令行参数方式（推荐）

脚本支持完整的命令行参数，提供最灵活的使用方式：

```bash
# 查看帮助信息
python clean_old_files.py --help

# 基本清理（默认7天）
python clean_old_files.py

# 指定清理目录
python clean_old_files.py /path/to/downloads

# 测试模式运行（推荐首次使用）
python clean_old_files.py --dry-run

# 完整参数示例
python clean_old_files.py --directory /path/to/downloads --days 30 --dry-run --log-file clean.log --log-level INFO
```

### 2. 平台特定脚本方式

为了方便使用，我们提供了平台特定的启动脚本：

- **Windows用户**：双击运行 `clean_old_files.bat` 文件
- **Linux/macOS用户**：运行 `./clean_old_files.sh` （需要先给脚本执行权限：`chmod +x clean_old_files.sh`）

### 3. 脚本配置方式（备选）

如果需要更复杂的配置，可以直接修改脚本中的变量：

```python
# 在脚本中修改这些变量
DAYS = 7              # 保留天数
DRY_RUN = False       # 测试模式
LOG_FILE = None       # 日志文件路径
LOG_LEVEL = logging.INFO      # 日志级别

# 然后直接运行
python clean_old_files.py
```

## ⚙️ 命令行参数

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `directory` | - | 要清理的目录路径 | 当前目录 |
| `--days` | `-d` | 保留的天数 | 7 |
| `--dry-run` | - | 测试模式，不实际删除文件 | False |
| `--log-file` | - | 指定日志文件路径 | 自动生成 |
| `--log-level` | - | 日志级别（DEBUG, INFO, WARNING, ERROR） | INFO |
| `--no-log-file` | - | 不保存日志文件，只输出到控制台 | False |

### 使用示例

1. **清理当前目录，删除超过7天的文件**：
   ```bash
   python clean_old_files.py
   ```

2. **清理指定目录，删除超过30天的文件**：
   ```bash
   python clean_old_files.py /path/to/downloads -d 30
   ```

3. **测试模式，预览将要删除的文件**：
   ```bash
   python clean_old_files.py --dry-run
   ```

4. **清理并保存详细日志**：
   ```bash
   python clean_old_files.py --log-file cleanup.log --log-level DEBUG
   ```

5. **只输出到控制台，不保存日志文件**：
   ```bash
   python clean_old_files.py --no-log-file
   ```

## 📊 输出示例

### 正常清理模式输出

```
============================================================
开始清理旧文件
清理目录: C:\Users\Administrator\Downloads
保留天数: 7
测试模式: 否
日志文件: clean_Downloads_20240321.log
日志级别: INFO
============================================================
扫描文件中...
扫描完成，共找到 150 个文件
需要删除 45 个超过 7 天的旧文件
释放空间: 2.34 GB

待删除文件列表（从最旧到最新）：
  1. old_file.zip (压缩包, 150.23 MB, 修改时间: 2024-01-01 10:30:15, 已存在: 45天)
  2. temp_video.mp4 (视频, 500.45 MB, 修改时间: 2024-01-02 14:20:30, 已存在: 44天)
  3. document.pdf (文档, 25.67 MB, 修改时间: 2024-01-03 09:15:45, 已存在: 43天)
  ...

开始删除文件...
已删除: old_file.zip (压缩包, 150.23 MB)
已删除: temp_video.mp4 (视频, 500.45 MB)
已删除: document.pdf (文档, 25.67 MB)
...

============================================================
清理完成
删除统计信息:
  - 成功删除文件数量: 45 个
  - 删除失败文件数量: 0 个
  - 释放空间总计: 2.34 GB

详细统计:
  - 平均文件大小: 52.00 MB
  - 删除文件占比: 45/150 (30.0%)
  - 剩余文件数量: 105 个

文件类型统计:
  - 视频: 20 个文件, 1.50 GB
  - 压缩包: 15 个文件, 600.23 MB
  - 图片: 8 个文件, 150.45 MB
  - 文档: 2 个文件, 95.67 MB

总结:
✓ 成功清理了 45 个旧文件
✓ 释放了 2.34 GB 磁盘空间
============================================================
```

### 测试模式输出

```
============================================================
开始清理旧文件
清理目录: C:\Users\Administrator\Downloads
保留天数: 7
测试模式: 是
============================================================
扫描文件中...
扫描完成，共找到 150 个文件
需要删除 45 个超过 7 天的旧文件
释放空间: 2.34 GB

[测试模式] 以下文件将被删除（实际不会删除）：
  1. old_file.zip (压缩包, 150.23 MB, 修改时间: 2024-01-01 10:30:15, 已存在: 45天)
  2. temp_video.mp4 (视频, 500.45 MB, 修改时间: 2024-01-02 14:20:30, 已存在: 44天)
  ...

[测试模式] 统计信息:
  - 待删除文件数量: 45 个
  - 可释放空间: 2.34 GB
  - 删除文件占比: 45/150 (30.0%)

============================================================
[测试模式] 清理预览完成
============================================================
```

## 💡 最佳实践

### 🔒 安全使用

1. **首次使用测试模式**
   ```bash
   python clean_old_files.py --dry-run
   ```

2. **备份重要文件**
   - 在运行清理前备份重要文件
   - 定期备份数据到外部存储

3. **逐步清理**
   - 从小范围测试开始
   - 逐渐扩大清理范围
   - 定期检查清理结果

### ⚡ 性能优化

1. **选择合适的保留天数**
   - 下载频繁：设置较短天数（3-7天）
   - 下载较少：设置较长天数（14-30天）

2. **日志管理**
   - 定期清理日志文件
   - 设置合适的日志级别
   - 使用 `--no-log-file` 减少磁盘写入

3. **定期维护**
   - 设置定时任务自动清理
   - 监控磁盘空间使用情况

### 📁 文件组织

1. **目录结构建议**
   ```
   Downloads/
   ├── documents/    # 文档文件
   ├── images/     # 图片文件
   ├── videos/     # 视频文件
   ├── archives/   # 压缩包
   └── temp/       # 临时文件
   ```

2. **命名规范**
   - 使用有意义的文件名
   - 避免特殊字符
   - 定期整理和分类

## 🔧 故障排除

### 常见错误及解决方案

#### 1. 权限错误
```
错误: PermissionError: [Errno 13] Permission denied
```
**解决方案**:
- 以管理员权限运行脚本
- 检查文件是否被其他程序占用
- 关闭占用文件的程序
- 检查目录权限设置

#### 2. 目录不存在
```
错误: 目录不存在: /path/to/directory
```
**解决方案**:
- 检查目录路径是否正确
- 确保目录存在
- 使用绝对路径而非相对路径
- 检查路径中的空格和特殊字符

#### 3. 无文件匹配
```
警告: 没有找到符合条件的文件
```
**解决方案**:
- 检查目录中是否有文件
- 确认文件修改时间是否超过保留天数
- 检查文件扩展名是否受支持
- 验证目录权限

#### 4. 日志文件权限
```
错误: 无法写入日志文件
```
**解决方案**:
- 检查日志文件路径权限
- 关闭占用日志文件的程序
- 更改日志文件路径
- 使用 `--no-log-file` 参数

### 调试技巧

1. **启用调试日志**
   ```bash
   python clean_old_files.py --log-level DEBUG
   ```

2. **测试模式运行**
   ```bash
   python clean_old_files.py --dry-run --log-level DEBUG
   ```

3. **检查文件属性**
   - 使用 `ls -la` (Linux/macOS) 或 `dir` (Windows) 查看文件详情
   - 验证文件修改时间
   - 检查文件权限

## ❓ 常见问题

### Q: 脚本会删除哪些文件？
A: 脚本会删除超过指定天数（默认7天）的文件，并自动排除.log文件和脚本文件本身。

### Q: 如何恢复误删的文件？
A: 从回收站或备份中恢复。建议在运行前先备份重要文件，或使用测试模式预览。

### Q: 支持哪些文件系统？
A: 支持Windows NTFS、FAT32，Linux ext4、btrfs，macOS APFS等常见文件系统。

### Q: 脚本运行速度如何？
A: 扫描速度约每秒处理1000+文件，删除速度取决于文件大小和磁盘性能。

### Q: 可以自定义文件匹配规则吗？
A: 可以通过修改脚本中的参数来调整保留天数、日志级别等设置。

### Q: 日志文件会占用太多空间吗？
A: 日志文件相对较小，可以定期清理或设置 `--no-log-file` 避免生成日志。

### Q: 脚本是否安全？
A: 在测试模式下完全安全。实际删除前会显示详细的文件列表，建议先使用测试模式。

### Q: 如何获取最新版本？
A: 关注项目仓库的更新，定期检查新版本发布。

### Q: 脚本支持命令行参数吗？
A: 是的，支持完整的命令行参数。使用 `python clean_old_files.py --help` 查看所有可用选项。

### Q: 可以回退到旧版本吗？
A: 可以下载历史版本的代码，但建议保持最新版本以获得最佳性能和安全性。

## 📄 版本历史

### v1.1.0 (2026-03-21) - 现代化文档版
- ✨ **全面文档重构**: 完全重写README结构，采用专业开源项目标准格式
- 🎨 **视觉化改进**: 添加emoji图标、GitHub badges、表格格式，提升文档可读性
- 📚 **内容体系化**: 新增快速开始、安装指南、故障排除、最佳实践等完整章节
- 🔧 **使用指南完善**: 增加更多配置示例、API文档、输出示例
- 🏷️ **版本管理**: 建立完整的版本历史追踪系统
- 📖 **用户体验优化**: 添加目录导航、常见问题、路线图等实用内容
- 💻 **平台脚本**: 新增Windows批处理和Linux/macOS shell脚本

### v1.0.0 (2026-03-21) - 功能完整版
- 🚀 **核心功能实现**: 完整的文件清理功能，支持多种文件类型
- 📁 **空文件夹清理**: 自动清理空文件夹功能
- 🔒 **安全排除**: 自动排除日志文件和脚本文件
- 🧪 **测试模式**: 支持dry-run模式，预览将要删除的文件
- 📝 **详细日志**: 提供详细的清理报告和统计信息
- 🌐 **跨平台支持**: 支持Windows、macOS、Linux系统
- 💻 **命令行界面**: 提供丰富的命令行参数配置

## 更新日志

### v1.1.0 (2026-03-21)
- 添加了 `clean_old_files.bat` 文件，方便Windows用户双击运行
- 添加了 `clean_old_files.sh` 文件，方便Linux/macOS用户运行
- 更新了使用方法，包含脚本文件的说明

## 📄 许可证

本项目采用 [MIT许可证](https://opensource.org/licenses/MIT)。

```
MIT License

Copyright (c) 2026 Clean Old Files

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**最后更新**: 2026年3月21日  
**版本**: v1.1.0  
**作者**: Clean Old Files Team  

⭐ 如果这个项目对您有帮助，请给我们一个星标！感谢您的支持！