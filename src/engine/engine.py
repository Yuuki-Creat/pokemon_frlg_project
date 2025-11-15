import json
import pygame
from utils.memory_profiler import MemoryProfiler

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

        self.player_pos = [100, 100]
        self.player_speed = 2
        self.player_img = pygame.image.load("assets/player.png").convert()
        self.tileset = pygame.image.load('assets/tilesets.png').convert()
        self.map_data = self._load_map('data/map001.json')

        self.tileset_meta = self._load_tileset_meta("assets/tilesets_meta.json")
        self.tile_w = self.tileset_meta["tile_width"]
        self.tile_h = self.tileset_meta["tile_height"]
        self.tileset_cols = self.tileset_meta["columns"]

        print("[INIT] Engine initialized.")

    def _load_map(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f'[LOAD] Map loaded: {path}')
                return data
        except FileNotFoundError:
            print(f'[WARN] Map file not found: {path}, using empty fallback')
            return {'width': 10, 'heigth': 8, 'tiles': [[0]*10 for _ in range(8)]}

    def _load_tileset_meta(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                print(f'[LOAD] tileset_meta loaded: {path}')
                return json.load(f)
        except FileNotFoundError:
            print(f'[WARN] tileset_meta file not found: {path}')
            raise 

    def _tile_rect(self, tile_id):
        """
        タイルセット画像から「指定された tile_id に対応する 1枚のタイルの領域（Rect）」を切り出して返却
        """
        x = (tile_id % self.tileset_cols) * self.tile_w
        y = (tile_id // self.tileset_cols) * self.tile_h
        return pygame.Rect(x, y, self.tile_w, self.tile_h)

    def _handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self):
        """ゲームロジックの更新処理"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_pos[1] -= self.player_speed
        if keys[pygame.K_DOWN]:
            self.player_pos[1] += self.player_speed
        if keys[pygame.K_LEFT]:
            self.player_pos[0] -= self.player_speed
        if keys[pygame.K_RIGHT]:
            self.player_pos[0] += self.player_speed

        self.profiler.update(tag="mainloop_update")

    def _draw(self):
        """描画処理"""
        # 背景描画
        self.screen.fill((80, 120, 255))

        for y in range(self.map_data["height"]):
            for x in range(self.map_data["width"]):
                tile_id = self.map_data["tiles"][y][x]
                tile_rect = self._tile_rect(tile_id)
                self.screen.blit(self.tileset, (x*self.tile_w, y*self.tile_h), tile_rect)

        self.screen.blit(self.player_img, self.player_pos)

        pygame.display.flip()  

    def run(self):
        """メインゲームループを実行"""
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
