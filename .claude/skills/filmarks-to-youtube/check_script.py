#!/usr/bin/env python3
"""台本本文が「読み上げ原稿」になっているか検査するリンター。

台本セクション内は、セクション見出しと角括弧の演出指示を除き、
すべて演者が声に出して読む発話でなければならない。
記事の記法（小見出しラベル・箇条書き・太字・表組み）が混ざっていたら失格とする。

usage: python3 check_script.py <台本ファイル>
exit code: 0=合格 / 1=違反あり / 2=ファイル異常
"""

import re
import sys

# 見出しは絵文字の有無に関わらず拾う（`## 動画台本` / `## 📝 動画台本` の両方に対応）
RE_SECTION_START = re.compile(r"^##\s+\S*\s*動画台本")
RE_SECTION_END = re.compile(r"^##\s+\S*\s*制作メモ")

# 日本語ナレーションの発話速度（文字/分）。カジュアルな語りで概ね250〜350字/分。
# 英語の 150〜200 words/min をそのまま文字数に当てはめると倍近く過大に出るので注意。
CPM_SLOW = 250   # ゆっくりめ（間を多く取る）
CPM_FAST = 350   # 速め（テンポよく喋る）

# 台本本文で許可される非発話行
RE_HEADING = re.compile(r"^###\s*【.+】")          # ### 【フック】(0〜30秒)
RE_DIRECTION = re.compile(r"^\[.+\]$")             # [BGM: ...] [テロップ: ...]
RE_SEPARATOR = re.compile(r"^-{3,}$")              # ---

# 違反パターン
CHECKS = [
    (re.compile(r"^\s*\*\*【.+】\*\*\s*$"), "小見出しラベル（演者が読み上げられない）"),
    (re.compile(r"^\s*[-*]\s+\S"), "箇条書き"),
    (re.compile(r"^\s*\d+\.\s+\S"), "番号付きリスト"),
    (re.compile(r"^\s*\|"), "表組み"),
    (re.compile(r"\*\*"), "太字強調（記事の記法）"),
]


def extract_body(lines):
    """台本セクションの行を (行番号, 本文) で返す。"""
    start = end = None
    for i, line in enumerate(lines):
        if start is None and RE_SECTION_START.match(line):
            start = i + 1
        elif start is not None and RE_SECTION_END.match(line):
            end = i
            break
    if start is None:
        return None
    return [(i + 1, lines[i]) for i in range(start, end if end is not None else len(lines))]


def main():
    if len(sys.argv) != 2:
        print("usage: python3 check_script.py <台本ファイル>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError as e:
        print(f"✗ ファイルを読めません: {e}", file=sys.stderr)
        return 2

    body = extract_body(lines)
    if body is None:
        print("✗ 「## 動画台本」セクションが見つかりません", file=sys.stderr)
        return 2

    violations = []
    speech_chars = 0
    for lineno, line in body:
        stripped = line.strip()
        if not stripped or RE_HEADING.match(stripped) or RE_DIRECTION.match(stripped) \
                or RE_SEPARATOR.match(stripped):
            continue
        for pattern, label in CHECKS:
            if pattern.search(line):
                violations.append((lineno, label, stripped))
                break
        # 違反行も発話量には数える（修正前後で文字数を比較できるようにするため）
        speech_chars += len(stripped)

    print(f"検査対象: {path}")
    print(f"台本セクション: {len(body)}行 / 発話文字数: {speech_chars}字 "
          f"(推定尺 {speech_chars / CPM_FAST:.1f}〜{speech_chars / CPM_SLOW:.1f}分)")

    if violations:
        print(f"\n✗ 不合格: {len(violations)}件の違反\n")
        for lineno, label, text in violations:
            print(f"  L{lineno}: [{label}]")
            print(f"        {text[:70]}")
        print("\n→ これらを「繋ぎの発話」に書き換えてから再保存すること。")
        return 1

    print("\n✓ 合格: 台本本文は発話と演出指示のみで構成されています")
    return 0


if __name__ == "__main__":
    sys.exit(main())
