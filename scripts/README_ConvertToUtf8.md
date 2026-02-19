# 编码转换脚本

## 问题

项目中原有不少文件使用 GB2312/GBK 编码保存，包含中文注释。当用 Cursor（默认 UTF-8）打开并编辑时，这些中文会变成问号或乱码。

## 解决方案

已将 **61 个文件** 从 GBK 转为 UTF-8 编码，包括：

- DuiLib 主库源码（.cpp, .h）
- bin\skin 下的部分 XML 配置
- Help 下的说明文档

## 脚本用法

### PowerShell 脚本（推荐，Windows 原生）

```powershell
# 预览（不实际修改）
.\scripts\ConvertToUtf8.ps1 -DryRun

# 执行转换
.\scripts\ConvertToUtf8.ps1

# 包含 Demos 目录
.\scripts\ConvertToUtf8.ps1 -IncludeDemos

# 指定根目录
.\scripts\ConvertToUtf8.ps1 -Root "D:\path\to\project"
```

### Python 脚本（需安装 Python 3）

```bash
# 预览
python scripts/convert_to_utf8.py -n

# 执行转换
python scripts/convert_to_utf8.py

# 包含 Demos
python scripts/convert_to_utf8.py --include-demos
```

## 排除目录

- build, .git, node_modules, .vs, .history, 3rd

## 说明

- `.rc` 资源文件会写入 UTF-8 BOM，便于 MSVC 识别 Unicode
- 其他源文件为 UTF-8 无 BOM
- 仅对检测到 GBK 编码且含中文的文件进行转换
