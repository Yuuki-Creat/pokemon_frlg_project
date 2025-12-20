import json
import pygame
from utils.memory_profiler import MemoryProfiler
import os # ファイルパス操作のためimport

class Engine:
    def __init__(self, screen, clock, fps=60):
        """
        GameEngineの初期化。画面と時計を外部から受け取り、プロファイラをセットアップ
        """
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.running = False
        self.profiler = MemoryProfiler(interval_sec=5)

        self.player_pos = [100 + 16, 100]
        self.player_speed = 1

        self.tile_w = 16
        self.tile_h = 16
        self.tileset_cols = 20

        # ファイルが存在するか確認する処理を追加 (assets/player.pngは必須)
        try:
            self.player_img = pygame.image.load(os.path.join("assets", "player.png")).convert_alpha() # 透過を考慮
            self.tileset = pygame.image.load(os.path.join('assets', 'tilesets.png')).convert_alpha()
        except pygame.error as e:
            print(f'[ERROR] Pygame resource load failed: {e}')
            raise

        self.map_data = self._load_map('data/map001.json')

        map_width_px = self.map_data.get("width", 20) * self.tile_w
        map_height_px = self.map_data.get("height", 16) * self.tile_h
        self.screen = pygame.display.set_mode((map_width_px, map_height_px))
        pygame.display.set_caption("Masara Town Engine") # キャプションを設定

        print("[INIT] Engine initialized.")

    def _load_map(self, path):
        # JSONマップをローディング
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f'[LOAD] Map loaded: {path}')

                map_w = data.get('width', 0)
                map_h = data.get('height', 0)

                raw_tiles = data.get('tiles', [])
                raw_collision = data.get('collision_map', [])

                # 二次元リストをフラットリストに変換（描画と衝突判定ロジックがフラットリストを前提としているため）
                flat_tiles = [tile for row in raw_tiles for tile in row]
                flat_collision = [coll for row in raw_collision for coll in row]

                return {
                    'width': map_w,
                    'height': map_h,
                    'tiles': flat_tiles,
                    'collision_map': flat_collision
                }
        except FileNotFoundError:
            print(f'[WARN] Map file not found: {path}, using empty fallback')
            raise

    def _tile_rect(self, tile_id):
        """
        タイルセット画像から「指定された tile_id に対応する 1枚のタイルの領域（Rect）」を切り出して返却
        """
        # tile_idが1から始まる場合、0ベースに変換
        if tile_id > 0:
            tile_id -= 1

        x = (tile_id % self.tileset_cols) * self.tile_w
        y = (tile_id // self.tileset_cols) * self.tile_h
        return pygame.Rect(x, y, self.tile_w, self.tile_h)

    def _handle_events(self):
        """"イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _get_tile_attribute(self, x, y):
        """ピクセル座標(x, y)に対応するタイル属性を取得"""
        x_adjusted = x - self.tile_w
        tile_x = int(x_adjusted // self.tile_w)
        tile_y = int(y // self.tile_w)

        map_w = self.map_data.get("width", 0)
        map_h = self.map_data.get("height", 0)

        # タイル座標をフラットリストのインデックスに変換
        index = tile_y * map_w + tile_x
        if 0 <= tile_x < map_w and 0 <= tile_y < map_h and 0 <= index < len(self.map_data["collision_map"]):
            # 衝突マップから属性値を取得
            return self.map_data["collision_map"][index]
        return 1 # マップ外は衝突ありとみなす

    def _check_collision_and_move(self, dx, dy):
        """
        新しい位置での衝突判定
        移動可能であればプレイヤー座標を更新
        """
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy

        player_width = self.player_img.get_width()
        player_height = self.player_img.get_height()

        check_x = new_x + player_width // 2
        check_y = new_y + player_height - 3

        attribute = self._get_tile_attribute(check_x, check_y)

        # 衝突判定マップのルール
        if attribute == 1: # 属性値 1: Solid / 完全に通行止め
            return
        elif attribute == 4: # 属性値 4: Water / 水域
            return # 水も通行止めとします
        elif attribute == 0: # 属性値 0: Walkable / 通行可能
            pass
        elif attribute == 2: # 属性値 2: Tall Grass / 草むら
            pass
        elif attribute == 3: # 属性値 3: Door / 入口
            pass

        self.player_pos[0] = new_x
        self.player_pos[1] = new_y

    def _update(self):
        # 処理は変更なし
        keys = pygame.key.get_pressed()
        
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy -= self.player_speed
        if keys[pygame.K_DOWN]:
            dy += self.player_speed
        if keys[pygame.K_LEFT]:
            dx -= self.player_speed
        if keys[pygame.K_RIGHT]:
            dx += self.player_speed

        self._check_collision_and_move(dx, dy)
        self.profiler.update(tag="mainloop_update")

    def _draw(self):
        """描画処理"""
        # 背景描画
        self.screen.fill((80, 120, 255)) # 青系の色

        map_w = self.map_data.get("width", 0)
        map_h = self.map_data.get("height", 0)
        # ★ マップ描画オフセットを定義 (1タイル分右にずらす = 16px)
        offset_x = 0 # 16ピクセル

        # マップ描画のループ
        # マップデータはフラットリスト形式（Tiled形式の想定）
        for i, tile_id in enumerate(self.map_data["tiles"]):
            x_tile = i % map_w
            y_tile = i // map_w

            # マップデータに含まれるグラフィックIDを元に描画
            tile_rect = self._tile_rect(tile_id)
            self.screen.blit(
                self.tileset, 
                (x_tile * self.tile_w + offset_x, y_tile * self.tile_h),
                tile_rect
            )

        self.screen.blit(self.player_img, self.player_pos)

        pygame.display.flip()

    def run(self):
        # 処理は変更なし
        self.running = True

        self.profiler.start()
        print("[RUN] Game loop started.")

        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(self.fps)

        # 終了時にメモリ統計を表示
        self.profiler.summary()
        print("[QUIT] Game loop finished.")

def engine_run(screen, clock):
    return Engine(screen, clock, fps=60)
