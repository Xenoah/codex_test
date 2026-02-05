# Solar Origin Prototype 取扱説明書

このドキュメントは、`Solar Origin Prototype` の実行方法と基本的な使い方を説明します。

## 1. 対象
- ローカル環境でシミュレーションを試したい方
- 物理挙動（軌道・エネルギー・運動量）を簡易確認したい方

## 2. 動作要件
- Python 3.10+
- `pytest`（テスト実行時のみ）

## 3. ファイル構成（主要）
- `src/solar_sim/bodies.py`: 天体モデル（質量・位置・速度）
- `src/solar_sim/engine.py`: N体シミュレーション本体（Leapfrog積分）
- `src/solar_sim/scenario.py`: 太陽系初期配置（Sun + 8惑星）
- `src/solar_sim/cli.py`: コマンドライン実行エントリ
- `tests/test_engine.py`: 回帰テスト

## 4. クイックスタート
プロジェクトルートで以下を実行してください。

```bash
PYTHONPATH=src python -m solar_sim.cli --steps 365 --dt 86400 --gravity-scale 1.0
```

### 主要オプション
- `--steps`: 積分ステップ数（例: `365`）
- `--dt`: 1ステップあたり秒数（例: `86400` は1日）
- `--gravity-scale`: 重力定数Gの倍率（例: `1.0` が実値）

## 5. 出力の見方
実行後、以下の情報が出力されます。

1. `Energy drift ratio`
   - シミュレーション前後の全エネルギー相対変化量。
   - 絶対値が小さいほど、数値的に安定です。
2. `Momentum norm`
   - 全運動量ノルムの開始時→終了時。
   - 差が小さいほど、保存則に沿った挙動です。
3. `Center of mass (AU)`
   - 系全体の重心位置。
4. 各天体の `x/y` 位置（AU）

## 6. テスト実行
```bash
PYTHONPATH=src pytest -q
```

テストでは、以下を確認します。
- 地球軌道半径が1年後も1AU近傍であること
- snapshot/restore が正しく往復できること
- エネルギードリフトが許容範囲内であること
- 運動量保存の相対誤差が小さいこと
- 不正パラメータ入力で適切に例外が出ること

## 7. よくあるエラー

### Q1. `ModuleNotFoundError: No module named 'solar_sim'`
`PYTHONPATH=src` を付けて実行してください。

### Q2. `ValueError: dt_seconds must be positive`
`--dt` に正の値を設定してください。

### Q3. `ValueError: Gravity scale must be positive`
`--gravity-scale` に `0` 以下を指定しないでください。

## 8. 制約事項
- 初期値は近似的な円軌道で、厳密暦元期（J2000等）準拠ではありません。
- 計算量は O(N^2) のため、大量天体には不向きです。

## 9. 今後の拡張案
- JPL/SPICE準拠の初期条件ローダー
- Barnes-Hut/FMMによる高速化
- Unity/C#（Jobs/Burst）への移植
