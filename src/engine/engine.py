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

        print("[INIT] Engine initialized.")

    def _handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self):
        """ゲームロジックの更新処理"""
        # TODO:
        self.profiler.update(tag="mainloop_update")

    def _draw(self):
        """描画処理"""
        # 背景描画
        self.screen.fill((80, 120, 255))

        # TODO:

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
    game_engine_instance = Engine(screen, clock, fps=60)
    return game_engine_instance
