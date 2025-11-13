"""
memory_profiler.py
M0段階：軽量メモリ監視クラス
----------------------------------------
- tracemalloc と psutil を併用してメモリ使用量を定期観測
- compare_to により差分を行単位で特定
- ループ中でも軽負荷で動作
"""
import tracemalloc
import time
import os
import psutil

class MemoryProfiler:
    """ゲーム中でも定期的にメモリを監視できるクラス"""
    def __init__(self, interval_sec=5):
        self.interval_sec = interval_sec
        self.start_snapshot = None
        self.last_snapshot = None
        self.last_time = time.time()

    def start(self):
        """トレースを開始し、初回スナップショットを記録"""
        tracemalloc.start()
        self.start_snapshot = tracemalloc.take_snapshot()
        self.last_snapshot = self.start_snapshot
        print("[MEM] Tracemalloc started.")

    def update(self, tag="loop"):
        """一定間隔ごとに呼び出し、差分を出力"""
        now = time.time()
        if now - self.last_time >= self.interval_sec:
            new_snapshot = tracemalloc.take_snapshot()
            top_stats = new_snapshot.compare_to(self.last_snapshot, 'lineno')
            total_diff = sum(stat.size_diff for stat in top_stats)
            print(f"[MEM] Δ({tag}) {total_diff/1024:.2f} KB")

            # 実メモリ(RSS)出力
            process = psutil.Process(os.getpid())
            rss = process.memory_info().rss / (1024 * 1024)
            print(f"[MEM_REAL] RSS={rss:.2f} MB")

            # 更新
            self.last_snapshot = new_snapshot
            self.last_time = now

    def summary(self):
        """終了時に全体の増減を出力"""
        end_snapshot = tracemalloc.take_snapshot()
        stats = end_snapshot.compare_to(self.start_snapshot, 'lineno')
        print("\n[MEM] --- TOTAL MEMORY CHANGE ---")
        total = 0
        for stat in stats[:10]:
            print(stat)
            total += stat.size_diff
        print(f"[MEM] Total diff: {total/1024:.2f} KB")

        process = psutil.Process(os.getpid())
        rss = process.memory_info().rss / (1024 * 1024)
        print(f"[MEM_REAL_END] RSS={rss:.2f} MB")
