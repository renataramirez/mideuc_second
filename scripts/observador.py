import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import errores 

class MiHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            print(f"Detectado cambio en: {event.src_path}")
            errores.main()

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            print(f"Detectado nuevo archivo JSON: {event.src_path}")
            errores.main()

def watch_folder():
    resultados_dir = Path(__file__).parent.parent / "resultados" / "02"
    print(f"Observando carpeta: {resultados_dir}")

    event_handler = MiHandler()
    observer = Observer()
    observer.schedule(event_handler, str(resultados_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_folder()