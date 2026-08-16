---
name: Filmarks視聴済みページのHTMLパターン
description: Filmarks watched pageで映画データを抽出するためのCSSクラスとHTML構造
type: project
---

各映画は `.c-content-item` のブロックに含まれる。

- タイトル: `h3.c-content-item__title a` のテキスト
- スコア: `.c-content-item-infobar__item--star .c-content-item-infobar__body` のテキスト
- 映画URL: `a` タグの `href` で `/movies/{id}` を含むもの（`#mark-...` フラグメントは除去して使う）
- 完全URL: `https://filmarks.com/movies/{id}` の形式

**Why:** 実際のHTMLで確認済み。ユーザーから提供されたHTMLに基づく。

**How to apply:** 次回HTMLが貼り付けられたらこのセレクターで優先的に解析する。構造が変わっていたら柔軟に対応してこのメモリを更新する。
