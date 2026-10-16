#!/usr/bin/env python3
"""
浏览器定位助手（供 render_shots.py / qa_layout.py 共用）。

## 为什么不能写死路径

最初这里写死了 `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`。
在本机能跑，一进 CI 就挂——因为：

  · CI 上 Playwright 装的是**当时最新**的版本号，不是 1243
  · 目录名也不同：新版是 `chrome-linux64/`，旧版是 `chrome-linux/`

写死路径 = 把「本机快照」当成「通用事实」。这类故障很隐蔽：
本地永远绿，CI 永远红，而且报错信息只说「文件不存在」。

## 解析顺序

  1. `CHROME` 环境变量（显式指定优先，便于排查）
  2. 在 Playwright 缓存目录里按 glob 找任意已安装版本（取版本号最大的）
  3. 都找不到 → 返回 None，交给 Playwright 自己解析
     （`launch()` 不传 executable_path 时，Playwright 会用它自己安装的那份）

第 3 条是关键兜底：**「找不到」不应该等于「报错」，而应该等于「让对方自己来」**。
"""

import os
from pathlib import Path

# 按优先级排列的候选路径模式（覆盖新旧两种目录布局）
PATTERNS = (
    "chromium-*/chrome-linux64/chrome",       # 新版（含 headless shell 拆分的版本）
    "chromium-*/chrome-linux/chrome",         # 旧版
    "chromium_headless_shell-*/chrome-linux/headless_shell",
)


def _version_key(path: Path) -> int:
    """从路径里抽出 chromium 的版本号用于排序。"""
    for part in path.parts:
        if part.startswith("chromium-"):
            try:
                return int(part.split("-", 1)[1])
            except ValueError:
                pass
    return 0


def find_chrome(verbose: bool = True) -> Path | None:
    """定位 Chromium 可执行文件；找不到返回 None（调用方应回退到 Playwright 默认）。"""
    env = os.environ.get("CHROME")
    if env:
        p = Path(os.path.expanduser(env))
        if p.is_file():
            if verbose:
                print(f"Chromium（来自 CHROME 环境变量）：{p}")
            return p
        raise SystemExit(f"❌ CHROME 指向的文件不存在：{p}")

    root = Path(os.path.expanduser("~/.cache/ms-playwright"))
    hits = []
    for pat in PATTERNS:
        hits.extend(root.glob(pat))
    if hits:
        best = max(hits, key=_version_key)
        if verbose:
            print(f"Chromium（自动探测）：{best}")
        return best

    if verbose:
        print("未探测到 Playwright 缓存的 Chromium，回退到 Playwright 默认解析")
    return None


def launch_kwargs(extra_args=None) -> dict:
    """组装 `p.chromium.launch(**kwargs)` 的参数。

    找不到显式路径时**不传** executable_path，让 Playwright 自己解析。
    """
    exe = find_chrome()
    kw = {"args": list(extra_args or [])}
    if exe is not None:
        kw["executable_path"] = str(exe)
    return kw
