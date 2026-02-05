# Solar Origin Prototype

太陽を原点とした宇宙シミュレーションの **実装プロトタイプ** です。  
Android / Windows を最終ターゲットにしつつ、まずはローカルで動くシミュレーションコアを Python で実装しています。

## 実装内容（MVP）
- Sun + 8惑星のN体シミュレーション（Leapfrog積分）
- 重力定数スケール変更 (`--gravity-scale`)
- スナップショット保存/復元
- 1日刻みの時間進行デモCLI

## 構成
- `src/solar_sim/bodies.py`: 天体データ構造
- `src/solar_sim/engine.py`: N体計算エンジン
- `src/solar_sim/scenario.py`: 太陽系初期シナリオ
- `src/solar_sim/cli.py`: 実行CLI
- `tests/test_engine.py`: 基本動作テスト

## 使い方
```bash
PYTHONPATH=src python -m solar_sim.cli --steps 365 --dt 86400 --gravity-scale 1.0
```

## テスト
```bash
PYTHONPATH=src pytest -q
```

## セルフコードレビュー
### 良い点
- 物理積分をEulerではなくLeapfrogにして、長期安定性を改善。
- エンジン層とシナリオ層を分離し、将来Unity/C#移植時に責務を維持しやすい構造。
- snapshot/restore APIを先に用意し、巻き戻し機能の実装余地を確保。

### 改善余地
- 現在は惑星初期条件が近似値で、厳密な暦元期を使っていない。
- O(N^2)の全対全計算なので、恒星数を増やすならBarnes-Hut等が必要。
- Android実運用を見据えると、将来はUnity Jobs/BurstやGPU計算への置換が必要。
