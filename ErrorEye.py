import os
import requests
import os
import sys
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# Tu API key de Groq - PEGALA AQUÍ (obtené una gratis en https://console.groq.com/keys)
api_key = "PEGA_TU_GROQ_API_KEY_AQUI"

if api_key == "PEGA_TU_GROQ_API_KEY_AQUI" or not api_key:
    print(Fore.RED + Style.BRIGHT + "\n⚠️  ERROR: Falta tu Groq API key")
    print(Fore.YELLOW + "→ Andá a https://console.groq.com/keys y creá una gratis")
    print(Fore.YELLOW + "→ Pegala arriba, reemplazando todo entre las comillas")
    print(Fore.YELLOW + "→ Guardá el archivo y ejecutá de nuevo")
    print(Fore.MAGENTA + "¡Es rápido y gratis! 🚀\n")
    sys.exit()
if not api_key:
    print(Fore.RED + "Error: No encontré tu Groq API key.")
    print(Fore.YELLOW + "Ejecutá: export GROQ_API_KEY=gsk_tuclave")
    print(Fore.YELLOW + "O creá un archivo .env con GROQ_API_KEY=tuclave")
    sys.exit()

url = "https://api.groq.com/openai/v1/chat/completions"

HISTORIAL_FILE = "historial_error_eye.txt"

def guardar_historial(log, analisis):
    with open(HISTORIAL_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Log analizado:\n{log}\n\n")
        f.write(f"Análisis:\n{analisis}\n")
        f.write(f"{'='*60}\n")

def mostrar_historial():
    if os.path.exists(HISTORIAL_FILE):
        print(Fore.MAGENTA + Style.BRIGHT + "\n📜 HISTORIAL DE ANÁLISIS\n")
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print(Fore.YELLOW + "No hay historial aún.")

print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════════╗
       ERROR EYE PRO - Analizador Avanzado v2.0
          Especialista en Ciberseguridad con IA
╔══════════════════════════════════════════════════╗
""")
print(Fore.GREEN + "Opciones:")
print("  1. Pegar log manualmente")
print("  2. Analizar archivo de log")
print("  3. Ver historial de análisis")
print("  4. Salir\n")

opcion = input(Fore.YELLOW + "Elige una opción (1-4): ").strip()

if opcion == "4":
    print(Fore.MAGENTA + "¡Hasta pronto! ErrorEye PRO se despide 👋")
    sys.exit()

elif opcion == "3":
    mostrar_historial()
    sys.exit()

elif opcion == "2":
    ruta = input(Fore.YELLOW + "Ruta del archivo de log (ej: /sdcard/auth.log): ").strip()
    if not os.path.exists(ruta):
        print(Fore.RED + "Archivo no encontrado. Chau!")
        sys.exit()
    with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
        user_input = f.read()
    print(Fore.GREEN + f"Archivo {ruta} cargado ({len(user_input.splitlines())} líneas).\n")

elif opcion == "1":
    print(Fore.GREEN + "Pegá tu log (presiona Enter dos veces para terminar):\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    user_input = "\n".join(lines)
    if len(user_input.strip()) < 10:
        print(Fore.RED + "Log muy corto. Intenta de nuevo.")
        sys.exit()

else:
    print(Fore.RED + "Opción inválida.")
    sys.exit()

system_prompt = """
Sos ErrorEye PRO, un analista senior de ciberseguridad forense.
Analizá el log proporcionado con máxima precisión.
Respondé SOLO en español, estructurado y profesional:

1. **Resumen Ejecutivo**: Una frase con el evento principal.
2. **Tipo de Log Detectado**: SSH, Web (Apache/Nginx), Auth, Syslog, etc.
3. **Amenazas Detectadas**: Brute force, inyección SQL, XSS, port scan, etc.
4. **IPs/Usuarios Sospechosos**: Listalos con conteo.
5. **Nivel de Riesgo**: Bajo / Medio / Alto / Crítico + justificación.
6. **Acciones Inmediatas Recomendadas**:
   - Comandos Linux listos para copiar (ufw, iptables, fail2ban).
   - Mejores prácticas.
7. **Prevención a Largo Plazo**.

Sé conciso pero exhaustivo.
"""

payload = {
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analizá este log completo:\n\n{user_input}"}
    ],
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.4,
    "max_tokens": 1500
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print(Fore.CYAN + Style.BRIGHT + "\n🔍 ANALIZANDO CON ERROR EYE PRO...\n")

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    analisis = response.json()["choices"][0]["message"]["content"]

    print(Fore.WHITE + Style.BRIGHT + analisis)
    print("\n" + "="*70 + "\n")

    guardar_historial(user_input, analisis)
    print(Fore.GREEN + "Análisis guardado en historial_error_eye.txt")

except requests.exceptions.HTTPError as http_err:
    print(Fore.RED + f"Error API: {http_err}")
    if response.status_code == 401:
        print(Fore.RED + "Clave inválida. Crea una nueva en groq.com")
except Exception as e:
    print(Fore.RED + f"Error: {e}")

print(Fore.MAGENTA + "\n¡Listo! Ejecutá de nuevo para otro análisis.")
