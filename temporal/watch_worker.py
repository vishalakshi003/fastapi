# watch_worker.py

import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WorkerReloader(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = subprocess.Popen(self.command, shell=True)

    def on_any_event(self, event):
        print("🔁 Change detected. Restarting worker...")
        self.process.kill()
        self.process = subprocess.Popen(self.command, shell=True)

if __name__ == "__main__":
    path = "."  # current directory
    event_handler = WorkerReloader("python worker.py")
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print("👀 Watching for changes...")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
