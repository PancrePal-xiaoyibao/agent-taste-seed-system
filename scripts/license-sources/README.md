# 许可正文原文（vendor）

本目录存放三份许可的**官方正文原文**，供 `scripts/build_license.py`
组装仓库根 `LICENSE` 使用。改动本目录后重跑脚本即可重新生成 LICENSE。

| 文件 | 内容 | 官方来源 | 抓取日期 |
|---|---|---|---|
| `cc-by-4.0-legalcode.txt` | CC BY 4.0 英文法律条款全文（396 行） | <https://creativecommons.org/licenses/by/4.0/legalcode.txt> | 2026-10-24 |
| `ofl-1.1.txt` | SIL Open Font License 1.1 正文 | <https://scripts.sil.org/OFL>（经 Inter 项目 LICENSE.txt 逐字校验） | 2026-10-16 |
| `mit.txt` | MIT License 正文（含本项目版权行） | 标准文本 | 2026-10-16 |

## 为什么把正文放进仓库

1. **可复现**：`LICENSE` 由脚本 + 本目录组装，不再依赖运行时联网；
2. **可审计**：使用者能离线核对「我们声明的许可」与「官方原文」是否一致；
3. **版本可核对**：抓取日期与 URL 记录在上表，日后可对照上游是否修订。

## 这些文本本身的版权

- CC 官方明确声明其许可协议文本**不受著作权保护**，任何人都可复制；
- OFL 与 MIT 正文同样是「供复制使用」的许可模板文本。

因此本目录内容不与 §一 的资产分类冲突：它们是**许可文件本身**，
随 `LICENSE` 一并分发，不适用项目的内容许可。
