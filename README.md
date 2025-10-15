# API Control-M - Reemplazo de Ambientes

API REST para modificar configuraciones JSON de Control-M cambiando referencias de ambiente (Q5A, Q7A, Q8A) desde Jira Automation.

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API localmente

```bash
python api_control_m.py
```

La API estará disponible en: `http://localhost:5000`

### 3. Probar la API

```bash
python test_api.py
```

## 📡 Endpoints Disponibles

### 1. Health Check

**GET** `/health`

Verifica que la API está funcionando.

**Respuesta:**
```json
{
    "status": "ok",
    "message": "API Control-M está funcionando correctamente"
}
```

### 2. Reemplazar Ambiente

**POST** `/api/replace-environment`

Reemplaza todas las referencias de ambiente en el JSON.

**Request Body:**
```json
{
    "environment": "Q5",
    "json_data": {
        // Tu JSON de Control-M aquí
    }
}
```

**Respuesta:**
```json
{
    "success": true,
    "environment": "Q5A",
    "modified_json": {
        // JSON modificado
    }
}
```

### 3. Reemplazar Ambiente desde Jira

**POST** `/api/replace-environment-from-jira`

Endpoint optimizado para recibir datos desde Jira Automation.

**Request Body (Opción 1 - Simple):**
```json
{
    "environment": "Q5",
    "json_data": {
        // Tu JSON de Control-M aquí
    }
}
```

**Request Body (Opción 2 - Estructura Jira):**
```json
{
    "issue": {
        "fields": {
            "customfield_xxxxx": "Q5"
        }
    },
    "json_data": {
        // Tu JSON de Control-M aquí
    }
}
```

## 🔄 Lógica de Reemplazo

La API realiza los siguientes reemplazos según el ambiente especificado:

- **Si environment = "Q5"**: Reemplaza todas las referencias de `Q7A` y `Q8A` por `Q5A`
- **Si environment = "Q7"**: Reemplaza todas las referencias de `Q5A` y `Q8A` por `Q7A`
- **Si environment = "Q8"**: Reemplaza todas las referencias de `Q5A` y `Q7A` por `Q8A`

### Ejemplos de campos que se modifican:

- `RunAs`: `Q7ABATCH` → `Q5ABATCH`
- `OS400-CURLIB`: `Q7AHIFILES` → `Q5AHIFILES`
- `OS400-JOB_OWNER`: `Q7ABATCH` → `Q5ABATCH`
- Y cualquier otra referencia en el JSON

## 🏭 Despliegue en Producción

### Opción 1: Servidor Local

```bash
# Usar gunicorn para producción
gunicorn -w 4 -b 0.0.0.0:5000 api_control_m:app
```

### Opción 2: Docker

Crear un archivo `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_control_m.py .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api_control_m:app"]
```

Construir y ejecutar:

```bash
docker build -t control-m-api .
docker run -p 5000:5000 control-m-api
```

### Opción 3: Cloud (Heroku, Railway, etc.)

1. Crear archivo `Procfile`:
```
web: gunicorn api_control_m:app
```

2. Desplegar según la plataforma elegida

## 🔗 Integración con Jira Automation

### Paso 1: Crear Campo Personalizado en Jira

1. Ve a **Configuración de Jira** → **Problemas** → **Campos personalizados**
2. Crea un campo de tipo **Select List** o **Text Field**
3. Llámalo "Ambiente" o "Environment"
4. Añade las opciones: Q5, Q7, Q8
5. Añade el campo a las pantallas de tu proyecto

### Paso 2: Configurar Regla de Automation

1. Ve a **Configuración del proyecto** → **Automation**
2. Crea una nueva regla
3. Configura el **Trigger** (ej: "When: Issue created" o "When: Field value changed")
4. Añade una condición si es necesario
5. Añade la acción **"Send web request"**

#### Configuración del Web Request:

**URL**: `https://tu-servidor.com/api/replace-environment-from-jira`

**HTTP Method**: POST

**Headers**:
```
Content-Type: application/json
```

**Body** (Custom data):
```json
{
    "environment": "{{issue.customfield_xxxxx}}",
    "json_data": {
        "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
            "Type": "SimpleFolder",
            "ControlmServer": "COOPEUCH",
            "OrderMethod": "Manual",
            "CC1040P2": {
                "Type": "Job:OS400:Full:CommandLine",
                "CommandLine": "CALL PGM(RBIENVFCL)  PARM('CTINTDEM' 'NEXDEM')",
                "SubApplication": "GENER_NEXUS-DEMOGRAFICO-CARLOS",
                "RunAs": "Q7ABATCH",
                "Variables": [
                    {"OS400-CURLIB": "Q7AHIFILES"},
                    {"OS400-JOB_OWNER": "Q7ABATCH"}
                ]
            }
        }
    }
}
```

**Nota**: Reemplaza `customfield_xxxxx` con el ID real de tu campo personalizado.

### Paso 3: Guardar Respuesta (Opcional)

Puedes añadir otra acción después del web request para:
- Añadir un comentario con el JSON modificado
- Guardar en un campo personalizado
- Enviar a otra API o servicio

## 🧪 Ejemplos de Uso

### Ejemplo con cURL

```bash
curl -X POST http://localhost:5000/api/replace-environment \
  -H "Content-Type: application/json" \
  -d '{
    "environment": "Q5",
    "json_data": {
      "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
        "CC1040P2": {
          "RunAs": "Q7ABATCH",
          "Variables": [
            {"OS400-CURLIB": "Q7AHIFILES"}
          ]
        }
      }
    }
  }'
```

### Ejemplo con Python

```python
import requests

response = requests.post(
    'http://localhost:5000/api/replace-environment',
    json={
        'environment': 'Q5',
        'json_data': {
            # Tu JSON aquí
        }
    }
)

result = response.json()
print(result['modified_json'])
```

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Port 5000 is already in use"
Cambia el puerto en `api_control_m.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### La API no responde desde Jira
- Verifica que la URL sea accesible desde internet
- Verifica que no haya firewall bloqueando
- Revisa los logs de la API

## 📝 Logs

Los logs se muestran en la consola donde ejecutas la API. Para guardarlos en un archivo:

```bash
python api_control_m.py > api.log 2>&1
```

## 🤝 Soporte

Si tienes problemas o preguntas, verifica:
1. Los logs de la API
2. Los logs de Jira Automation
3. Que el JSON enviado sea válido

## 📄 Licencia

Este proyecto es para uso interno de Coopeuch.


