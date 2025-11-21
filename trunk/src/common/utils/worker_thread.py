from PyQt5.QtCore import QThread, pyqtSignal
from typing import Callable, Optional


class WorkerThread(QThread):
    """工作线程类 - 用于在后台执行耗时任务"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ThreadManager:
    """线程管理器 - 管理 WorkerThread 的生命周期"""

    def __init__(self):
        self._worker_threads = []

    def run_in_thread(self, func: Callable, *args,
                      on_finished: Optional[Callable] = None,
                      on_error: Optional[Callable] = None,
                      **kwargs) -> WorkerThread:
        worker = WorkerThread(func, *args, **kwargs)
        if on_finished:
            worker.finished.connect(on_finished)
        if on_error:
            worker.error.connect(on_error)

        worker.finished.connect(lambda: self._cleanup_thread(worker))
        worker.error.connect(lambda: self._cleanup_thread(worker))
        self._worker_threads.append(worker)
        worker.start()
        return worker

    def _cleanup_thread(self, worker: WorkerThread):
        if worker in self._worker_threads:
            self._worker_threads.remove(worker)

    def cleanup_all(self):
        self._worker_threads.clear()
