# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Filmarksの視聴済み映画リストをもとに、ジャンル別おすすめ選出 → YouTube動画台本生成までを行うエージェントシステム。コードは存在せず、Claude Codeのエージェント・スキル定義ファイルで構成されている。

## アーキテクチャ

```
[Filmarks HTML (手動コピー)]
        ↓  filmarks-fetcher agent
[output/filmarks/watched_movies.md]  ← 中央データストア
        ↓  movie-classifier agent
[output/recommendations/]           ← ジャンル分類・高評価選出結果
        ↓  youtube-script-generator agent
[output/drafts/]                    ← YouTube台本・タイトル案
```

フルパイプラインは `/filmarks-to-youtube` スキルで一括実行できる。

## エージェント・スキル定義

| ファイル | 役割 |
|--------|------|
| `.claude/agents/filmarks-fetcher.md` | FilmarksのHTMLから映画データを抽出し `watched_movies.md` に追記 |
| `.claude/agents/movie-classifier.md` | 映画リストをジャンル別に分類し、高評価作品を選出 |
| `.claude/agents/youtube-script-generator.md` | 分析結果からYouTube台本とタイトル案を生成 |
| `.claude/skills/filmarks-to-youtube/SKILL.md` | 上記3エージェントをパイプライン実行するオーケストレーションスキル |

## データ形式

`output/filmarks/watched_movies.md` は以下の Markdown テーブル形式で管理される：

```markdown
| タイトル | スコア | ジャンル | 公開年 | URL |
|--------|--------|---------|------|-----|
```

- **重複チェックはURLで行う**
- スコアはFilmarksの個人評価（0.5〜5.0）
- エントリは末尾に追記（ソートなし）

## エージェント永続メモリ

各エージェントは `.claude/agent-memory/<agent-name>/` 以下にファイルベースのメモリを持つ。HTMLパターン、ユーザーの好み、繰り返し適用するルールを蓄積する。

## 出力ファイル命名規則

- 分類結果: `output/recommendations/[ジャンル]_[N]選_YYYYMMDD.md`
- YouTube台本: `output/drafts/[ジャンル]_[N]選_YYYYMMDD.md`
