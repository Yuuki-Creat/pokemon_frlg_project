# 目的: Windowsローカル環境で動作する、ファイアレッド／リーフグリーン相当の2DドットRPG（以降 "本作" と呼ぶ）を、学習向けに分かりやすく実装する。

- 動作環境: Windows（ローカル実行／インストール可能）
- 言語/フレームワーク: Python + pygame
- メモリ: モジュール全体（ディスク上の総容量ではなく、実行可能モジュールや資産の合計）は**24MB**まで。ゲーム起動中の**最大メモリ使用量**も**24MB**を超えないこと。
- ポケモン数: **150匹**（ナンバリングは 1..150）
- 伝説: ファイヤー / フリーザー / サンダー、幻（ミュウツー） を再現。伝説はフィールド上でアイコン遭遇。
- グラフィック: 2Dドット（フルカラー不要だが明暗を表現）
- BGM: マップ単位、バトル、ジム、伝説バトル等に別BGMを用意
- ステータス: 努力値（EV）を含む。特殊攻撃/特殊防御の分離（金銀以降仕様）
- セーブ: PCメモリ（プロセスRAM）を直接使わず、セーブファイルに最小限データを保存
- ネットワーク: ポケモン交換のみ（セキュリティ重視）
- 設定: 言語（英/日）、性別選択、セリフ速度、技エフェクトON/OFF
- キー操作: 上下左右=移動、A=決定、B=キャンセル、D=便利登録

# 仮想環境
powershell
python -m venv env
.\env\Scripts\Activate.ps1
    または cmd.exe なら: .\env\Scripts\activate.bat
pip install --upgrade pip

# ディレクトリ構成（想定）
project_root/
  src/
    main.py                # エントリポイント（pygame初期化、Engine起動）
    engine/
      engine.py
      scene_manager.py
      game_loop.py
    resource/
      resource_manager.py
      tile_pack.py
    world/
      map_loader.py
      map.py
      npc.py
      encounter.py
    battle/
      battle_manager.py
      combatant.py
      move.py
    data/
      pokedex.json (最小化バイナリ推奨)
      moves.json
      items.json
      maps/ (ランタイムで読み込み可能)
    save/
      save_manager.py
    net/
      net_server.py
      net_client.py
      exchange_protocol.py
    ui/
      hud.py
      menu.py
    assets/
      tiles/ sprites/ audio/
  tests/
    test_battle.py
    test_save.py
  build/
  README.md
