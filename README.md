# Agente Inteligente ReAct + KB en Redis (Python + OpenAI API)

Este proyecto implementa un agente inteligente capaz de resolver dudas sobre la normativa ISO 27001 utilizando una arquitectura ReAct (Reasoning and Acting) y una base de conocimientos vectorial en Redis.



## Requisitos Previos
* Docker o Acceso a un Servidor Redis.
* Python 3.10
* Una API Key de OpenAI.

_Con el objetivo de evitar problemas de compatibilidad se utilizó **Conda** para generar un ambiente seguro de desarrollo con **Python 3.10**, sin embargo esto no es requisito excluyente._

## Configuración del Entorno
**1. (Opcional) Levantar Redis**
Copiar docker-compose.yml.example como docker-compose.yml, escribir clave para Redis (esta misma deberá ir en el .env), ejecutar:
```
docker compose up -d
```
**2. Configurar vairables de entorno**
Copiar .env.example como .env, escribir los siguientes valores:
```
OPENAI_KEY=api_key_openai
REDIS_HOST=servidor_redis
REDIS_PORT=6379
REDIS_USER=default
REDIS_PASSWORD=la_misma_del_docker-compose_o_la_redis
REDIS_INDEX_NAME=nombre_del_indice
FILES_PATH=/carpeta_con_archivos_txt_para_la_kb
```
**3. Instalar Dependencias de Python**
```
pip install -r requirements.txt
```
o
```
pip install langchain langchain-openai langchain-community redis openai numpy python-dotenv
```
## Estructura del Proyecto

* config.py: Configuración, carga de variables de entorno y lógica de Logging.
* ingest.py: Script encargado de leer los archivos .txt, aplicar chunking y persistir los vectores en Redis.
* agent.py: Motor principal del agente. Implementa el loop ReAct con las herramientas search_kb y get_doc.
* del-db.py: Utilitario para "vaciar" la base de datos Redis, borrando los registros relacionados con el indice.
* trace.log: Archivo generado automáticamente que registra toda la trazabilidad de las acciones del agente.

## Instrucciones de Uso
**1. Ingesta de Datos**
Asegúrate de tener tus archivos técnicos en la carpeta definida en FILES_PATH y ejecuta:
```
python ingest.py
```
**2 Ejecución del Agente**
```
python agent.py
```
El agente se mantendrá activo permitiendo múltiples consultas. Para salir, escribe **terminar agente**.


## Trazabilidad y Guardrails

**Umbral de Confianza (Score > 0.25):** Si la consulta del usuario es irrelevante o no hay suficiente evidencia en la KB, el agente informará que no tiene soporte para responder, evitando alucinaciones.

**Logging:** Cada consulta genera una traza en consola y en el archivo trace.log.
