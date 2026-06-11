import os
import time
from flask import Flask, render_template_string, jsonify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

app = Flask(__name__)
LOGS = [" [SISTEMA] BioShield EDR Iniciado. Núcleo de seguridad ONLINE..."]

class MonitorHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            nom_archivo = os.path.basename(event.src_path)
            tipo = event.event_type.upper()
            msg = f" [{time.strftime('%H:%M:%S')}] Alerta de Actividad: {tipo} -> {nom_archivo}"
            LOGS.append(msg)

def iniciar_radar():
    path_to_watch = "."
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    while True:
        time.sleep(1)

HTML_TACTICO = """
<!DOCTYPE html>
<html>
<head>
    <title>BioShield EDR - Panel Táctico</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background-color: #06090f; color: #58a6ff; font-family: 'Courier New', monospace; padding: 15px; margin: 0; }
        .bunker { border: 2px solid #238636; padding: 20px; background: #0d1117; border-radius: 8px; box-shadow: 0 0 15px rgba(35,134,54,0.3); }
        h1 { color: #238636; font-size: 22px; text-shadow: 0 0 8px rgba(35,134,54,0.6); margin-top: 0; }
        .status { color: #7ee787; font-weight: bold; animation: parpadeo 2s infinite; }
        .console { background: #010409; border: 1px solid #30363d; padding: 12px; height: 350px; overflow-y: auto; color: #7ee787; border-radius: 6px; font-size: 13px; }
        .log-line { margin-bottom: 6px; border-left: 3px solid #238636; padding-left: 8px; line-height: 1.4; }
        @keyframes parpadeo { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    </style>
    <script>
        setInterval(async () => {
            try {
                let r = await fetch('/api/logs');
                let logs = await r.json();
                let c = document.getElementById('console');
                c.innerHTML = logs.map(l => `<div class="log-line">${l}</div>`).join('');
                c.scrollTop = c.scrollHeight;
            } catch(e) {}
        }, 1000);
    </script>
</head>
<body>
    <div class="bunker">
        <h1>🛡️ BIOSHIELD EDR v1.0</h1>
        <p>Radar de Archivos: <span class="status">● MONITOREANDO EN TIEMPO REAL</span></p>
        <div class="console" id="console">Estableciendo conexión con el bunker de análisis...</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TACTICO)

@app.route('/api/logs')
def get_logs():
    return jsonify(LOGS[-25:])

if __name__ == '__main__':
    t = threading.Thread(target=iniciar_radar, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=8080)
