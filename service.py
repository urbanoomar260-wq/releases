import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Ruta pública estándar en Android para la carpeta de descargas
CARPETA_VIGILADA = "/storage/emulated/0/Download"

class ManejadorForense(FileSystemEventHandler):
    def procesar_alerta(self, tipo_evento, ruta):
        nombre_archivo = os.path.basename(ruta)
        linea_log = f"[{time.strftime('%H:%M:%S')}] ALERTA DE RADAR: {tipo_evento} detectado en -> {nombre_archivo}\n"
        
        # Imprime en la consola interna del sistema
        print(linea_log)
        
        # Guarda la alerta en un archivo de texto en el almacenamiento del celular
        # para que la UI pueda leerlo y mostrarlo en la pantalla táctica
        try:
            with open("/storage/emulated/0/Download/avi_alertas.txt", "a") as f:
                f.write(linea_log)
        except Exception:
            pass

    def on_created(self, event):
        if not event.is_directory:
            self.procesar_alerta("CREACIÓN (NUEVO ARCHIVO ➕)", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.procesar_alerta("MODIFICACIÓN (SOSPECHOSO 📝)", event.src_path)

if __name__ == '__main__':
    # Configurar el servicio de fondo para que no se muera
    if not os.path.exists(CARPETA_VIGILADA):
        # Si corre en emulador o la ruta cambia por permisos iniciales
        CARPETA_VIGILADA = "."

    event_handler = ManejadorForense()
    observer = Observer()
    observer.schedule(event_handler, path=CARPETA_VIGILADA, recursive=False)
    observer.start()

    # Bucle infinito de alta eficiencia para mantener vivo el servicio sin consumir CPU
    try:
        while True:
            time.sleep(2) # Pausa de optimización para evitar lag o "lentejas"
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
