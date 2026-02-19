# 将项目中 GB2312/GBK 编码的文件转换为 UTF-8 编码
# 解决 Cursor 按 UTF-8 打开时中文变成问号和乱码的问题

param(
    [string]$Root = ".",
    [switch]$DryRun,
    [switch]$IncludeDemos
)

$ErrorActionPreference = "Stop"
$script:Converted = @()
$script:Skipped = @()
$script:Errors = @()

$TextExtensions = @('.cpp', '.h', '.c', '.hpp', '.cc', '.cxx', '.rc', '.xml', '.json', '.txt', '.md')
$ExcludeDirs = @('build', '.git', 'node_modules', '__pycache__', '.vs', '.history', '3rd')

function Test-HasChinese($text) {
    return $text -match '[\u4e00-\u9fff]'
}

function Convert-FileToUtf8($filePath) {
    try {
        $bytes = [System.IO.File]::ReadAllBytes($filePath)
        if ($bytes.Length -eq 0) {
            return $false, "空文件"
        }

        # 已有 UTF-8 BOM
        if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
            try {
                $text = [System.Text.Encoding]::UTF8.GetString($bytes)
                if (Test-HasChinese $text) {
                    return $false, "已是 UTF-8 (BOM)"
                }
            } catch {}
        }

        # 尝试 UTF-8 解码
        try {
            $utf8 = New-Object System.Text.UTF8Encoding $false
            $text = $utf8.GetString($bytes)
            # 检查是否包含替换字符（解码错误时产生）
            if ($text -notmatch '\uFFFD' -and (Test-HasChinese $text)) {
                return $false, "已是 UTF-8"
            }
        } catch {}

        # 尝试 GBK 解码
        $gbk = [System.Text.Encoding]::GetEncoding("GBK")
        try {
            $text = $gbk.GetString($bytes)
        } catch {
            return $false, "无法识别编码"
        }

        if (-not (Test-HasChinese $text)) {
            return $false, "GBK 解码成功但无中文"
        }

        if ($DryRun) {
            return $true, "将转换"
        }

        # 写入 UTF-8
        $useBom = [System.IO.Path]::GetExtension($filePath) -eq '.rc'
        $utf8Enc = New-Object System.Text.UTF8Encoding $useBom
        [System.IO.File]::WriteAllText($filePath, $text, $utf8Enc)
        return $true, "已转换为 UTF-8 ($(if($useBom){'BOM'}else{'无BOM'}))"
    }
    catch {
        return $false, "错误: $_"
    }
}

$rootPath = Resolve-Path $Root
if (-not (Test-Path $rootPath)) {
    Write-Error "目录不存在: $rootPath"
    exit 1
}

Get-ChildItem -Path $rootPath -Recurse -File | Where-Object {
    $pathParts = $_.FullName.Split([IO.Path]::DirectorySeparatorChar)
    $inExcludedDir = [bool]($pathParts | Where-Object { $_ -in $ExcludeDirs })
    $ext = $_.Extension.ToLower()
    $ext -in $TextExtensions -and -not $inExcludedDir -and
    ($IncludeDemos -or 'Demos' -notin $pathParts)
} | ForEach-Object {
    $relPath = $_.FullName.Replace($rootPath.Path + '\', '').Replace($rootPath.Path + '/', '')
    $ok, $msg = Convert-FileToUtf8 $_.FullName
    if ($ok) {
        $script:Converted += [PSCustomObject]@{ Path = $relPath; Msg = $msg }
    } elseif ($msg -match '失败|错误') {
        $script:Errors += [PSCustomObject]@{ Path = $relPath; Msg = $msg }
    }
}

if ($script:Converted.Count -gt 0) {
    $prefix = if ($DryRun) { "[预览] " } else { "" }
    Write-Host "`n${prefix}已转换 $($script:Converted.Count) 个文件:`n"
    $script:Converted | ForEach-Object { Write-Host "  $($_.Path)`n    -> $($_.Msg)" }
} else {
    Write-Host "`n无需转换。"
}

if ($script:Errors.Count -gt 0) {
    Write-Host "`n$($script:Errors.Count) 个文件处理异常:"
    $script:Errors | ForEach-Object { Write-Host "  $($_.Path): $($_.Msg)" }
}

if ($DryRun -and $script:Converted.Count -gt 0) {
    Write-Host "`n此为预览，未实际修改。移除 -DryRun 参数执行转换。"
}
