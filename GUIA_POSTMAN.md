# 📬 Guía Completa de Postman

## 🚀 Inicio Rápido

### Paso 1: Iniciar la API
```bash
python api_control_m.py
```
Deja esta terminal abierta.

### Paso 2: Importar Colección en Postman
1. Abrir Postman
2. Clic en **"Import"**
3. Seleccionar archivo: `Control-M-API.postman_collection.json`
4. Clic en **"Import"**

### Paso 3: Ejecutar Tests
Haz clic en cada request y luego en **"Send"**

---

## 📋 Lista de Requests en la Colección

### 1️⃣ Health Check (GET)
**Qué hace:** Verifica que la API está funcionando

**URL:** `http://localhost:5000/health`

**Respuesta esperada:**
```json
{
    "status": "ok",
    "message": "API Control-M está funcionando correctamente"
}
```

**Status esperado:** 200 OK

---

### 2️⃣ Reemplazar Ambiente a Q5 (POST)
**Qué hace:** Cambia todas las referencias Q7A y Q8A por Q5A

**URL:** `http://localhost:5000/api/replace-environment`

**Body enviado:**
```json
{
    "environment": "Q5",
    "json_data": {
        "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
            "CC1040P2": {
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

**Qué verificar en la respuesta:**
- ✅ `"success": true`
- ✅ `"environment": "Q5A"`
- ✅ `"RunAs": "Q5ABATCH"` (era Q7ABATCH)
- ✅ `"OS400-CURLIB": "Q5AHIFILES"` (era Q7AHIFILES)
- ✅ `"OS400-JOB_OWNER": "Q5ABATCH"` (era Q7ABATCH)

**Status esperado:** 200 OK

---

### 3️⃣ Reemplazar Ambiente a Q7 (POST)
**Qué hace:** Cambia todas las referencias Q5A y Q8A por Q7A

**URL:** `http://localhost:5000/api/replace-environment`

**Body enviado:**
```json
{
    "environment": "Q7",
    "json_data": {
        "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
            "CC1040P2": {
                "RunAs": "Q5ABATCH",
                "Variables": [
                    {"OS400-CURLIB": "Q5AHIFILES"},
                    {"OS400-JOB_OWNER": "Q5ABATCH"}
                ]
            }
        }
    }
}
```

**Qué verificar:**
- ✅ Q5ABATCH → Q7ABATCH
- ✅ Q5AHIFILES → Q7AHIFILES

**Status esperado:** 200 OK

---

### 4️⃣ Reemplazar Ambiente a Q8 (POST)
**Qué hace:** Cambia todas las referencias Q5A y Q7A por Q8A

**Qué verificar:**
- ✅ Q7ABATCH → Q8ABATCH
- ✅ Q7AHIFILES → Q8AHIFILES

**Status esperado:** 200 OK

---

### 5️⃣ Endpoint Jira - Formato Simple (POST)
**Qué hace:** Prueba el endpoint que usará Jira con formato simple

**URL:** `http://localhost:5000/api/replace-environment-from-jira`

**Body:** Mismo formato que el endpoint normal

**Status esperado:** 200 OK

---

### 6️⃣ Endpoint Jira - Formato Issue (POST)
**Qué hace:** Prueba el endpoint con estructura de issue de Jira

**URL:** `http://localhost:5000/api/replace-environment-from-jira`

**Body enviado:**
```json
{
    "issue": {
        "fields": {
            "customfield_10001": "Q5"
        }
    },
    "json_data": {
        "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
            "CC1040P2": {
                "RunAs": "Q8ABATCH",
                "Variables": [
                    {"OS400-CURLIB": "Q8AHIFILES"}
                ]
            }
        }
    }
}
```

**Qué hace:** La API extrae "Q5" del campo custom de Jira

**Status esperado:** 200 OK

---

### 7️⃣ Test Error - Ambiente Inválido (POST)
**Qué hace:** Prueba manejo de errores con ambiente inválido

**Body enviado:**
```json
{
    "environment": "PROD",
    "json_data": {
        "test": "data"
    }
}
```

**Respuesta esperada:**
```json
{
    "error": "Ambiente inválido. Debe ser uno de: Q5, Q7, Q8, Q5A, Q7A, Q8A"
}
```

**Status esperado:** 400 Bad Request ✅ (esto es correcto, es un error intencional)

---

### 8️⃣ Test Error - Sin Environment (POST)
**Qué hace:** Prueba manejo de errores cuando falta el campo environment

**Body enviado:**
```json
{
    "json_data": {
        "test": "data"
    }
}
```

**Respuesta esperada:**
```json
{
    "error": "Falta el campo \"environment\""
}
```

**Status esperado:** 400 Bad Request ✅ (esto es correcto, es un error intencional)

---

## 📊 Configuración Manual (Sin importar colección)

Si prefieres crear los requests manualmente:

### Configuración General para todos los POST

**Headers:**
| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Body:**
- Tipo: **raw**
- Formato: **JSON**

### Request GET (Health Check)

```
Method: GET
URL: http://localhost:5000/health
Headers: (ninguno necesario)
Body: (ninguno necesario)
```

### Request POST (Reemplazar ambiente)

```
Method: POST
URL: http://localhost:5000/api/replace-environment
Headers:
  Content-Type: application/json
Body (raw, JSON):
{
    "environment": "Q5",
    "json_data": { ... tu JSON aquí ... }
}
```

---

## 🎯 Flujo de Prueba Recomendado

### Prueba Básica (5 minutos)
1. ✅ **Test 1**: Health Check
2. ✅ **Test 2**: Reemplazar a Q5
3. ✅ Verificar que cambió Q7ABATCH → Q5ABATCH

### Prueba Completa (10 minutos)
1. ✅ **Test 1**: Health Check
2. ✅ **Test 2**: Reemplazar a Q5
3. ✅ **Test 3**: Reemplazar a Q7
4. ✅ **Test 4**: Reemplazar a Q8
5. ✅ **Test 5**: Endpoint Jira formato simple
6. ✅ **Test 6**: Endpoint Jira formato issue

### Prueba de Errores (5 minutos)
7. ✅ **Test 7**: Ambiente inválido (debe fallar con 400)
8. ✅ **Test 8**: Sin environment (debe fallar con 400)

---

## 🔍 Cómo Leer las Respuestas

### ✅ Respuesta Exitosa

```json
{
    "success": true,
    "environment": "Q5A",
    "modified_json": {
        "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
            "CC1040P2": {
                "RunAs": "Q5ABATCH",  // ← VERIFICAR ESTO
                "Variables": [
                    {"OS400-CURLIB": "Q5AHIFILES"},  // ← Y ESTO
                    {"OS400-JOB_OWNER": "Q5ABATCH"}  // ← Y ESTO
                ]
            }
        }
    }
}
```

**Indicadores de éxito:**
- Status Code: **200 OK**
- `"success": true`
- Los campos tienen el ambiente correcto (Q5A, Q7A, o Q8A)

### ❌ Respuesta de Error

```json
{
    "error": "Mensaje de error descriptivo"
}
```

**Indicadores de error:**
- Status Code: **400 Bad Request** o **500 Internal Server Error**
- Campo `"error"` con descripción

---

## 🆘 Solución de Problemas

### Error: "Could not send request"
**Causa:** La API no está corriendo

**Solución:**
```bash
python api_control_m.py
```

### Error: "Connection refused"
**Causa:** Puerto incorrecto o API no iniciada

**Solución:**
- Verifica que la API esté en http://localhost:5000
- Verifica que la terminal con la API siga abierta

### Status 404 Not Found
**Causa:** URL incorrecta

**Solución:**
- Verifica la URL: `http://localhost:5000/api/replace-environment`
- Sin espacios ni caracteres extra

### Status 400 Bad Request
**Causas posibles:**
1. JSON mal formado
2. Falta campo "environment"
3. Falta campo "json_data"
4. Ambiente inválido (ej: "PROD")

**Solución:**
- Verifica el JSON en un validador: https://jsonlint.com/
- Asegúrate de incluir "environment" y "json_data"
- Usa solo: Q5, Q7, Q8 (o Q5A, Q7A, Q8A)

### Status 500 Internal Server Error
**Causa:** Error en el servidor

**Solución:**
- Mira la terminal donde está corriendo la API
- Verás el error detallado ahí
- Copia el error y búscalo

---

## 💡 Tips de Postman

### 1. Guardar los requests
Haz clic en **"Save"** después de crear cada request para no perderlos.

### 2. Organizar en carpetas
Crea carpetas para:
- Tests exitosos
- Tests de errores
- Tests de Jira

### 3. Usar variables
En Postman, puedes crear una variable de entorno:
```
{{base_url}} = http://localhost:5000
```
Luego usar: `{{base_url}}/api/replace-environment`

### 4. Ver el JSON formateado
En la respuesta, haz clic en **"Pretty"** para ver el JSON formateado bonito.

### 5. Copiar como cURL
Haz clic en **"Code"** → **"cURL"** para obtener el comando cURL equivalente.

---

## 📸 Screenshots (Descripción)

### Vista de la Colección
```
📁 Control-M API - Reemplazo de Ambientes
  ├─ 1. Health Check (GET)
  ├─ 2. Reemplazar Ambiente a Q5 (POST)
  ├─ 3. Reemplazar Ambiente a Q7 (POST)
  ├─ 4. Reemplazar Ambiente a Q8 (POST)
  ├─ 5. Endpoint Jira - Formato Simple (POST)
  ├─ 6. Endpoint Jira - Formato Issue (POST)
  ├─ 7. Test Error - Ambiente Inválido (POST)
  └─ 8. Test Error - Sin Environment (POST)
```

### Vista de un Request POST
```
[POST] http://localhost:5000/api/replace-environment

Tabs: [ Params | Authorization | Headers | Body | Pre-request Script | Tests ]

Headers:
  Content-Type: application/json

Body: (• raw | JSON ▼)
{
    "environment": "Q5",
    "json_data": { ... }
}

[Send] ← Botón azul
```

---

## ✅ Checklist de Prueba

Marca cada test conforme lo completes:

### Tests Básicos
- [ ] Health Check responde 200 OK
- [ ] Reemplazar a Q5 funciona
- [ ] Reemplazar a Q7 funciona
- [ ] Reemplazar a Q8 funciona

### Tests de Jira
- [ ] Endpoint Jira formato simple funciona
- [ ] Endpoint Jira formato issue funciona

### Tests de Errores
- [ ] Ambiente inválido retorna 400
- [ ] Sin environment retorna 400

### Verificaciones de Datos
- [ ] Q7ABATCH cambia a Q5ABATCH
- [ ] Q7AHIFILES cambia a Q5AHIFILES
- [ ] Todos los campos se reemplazan correctamente

---

## 🎓 Próximos Pasos

Una vez que todas las pruebas pasen:

1. ✅ API probada localmente con Postman
2. ➡️ Desplegar la API en Railway/Heroku
3. ➡️ Configurar Jira Automation
4. ➡️ Probar desde Jira

---

**¿Tienes algún error?** Revisa la sección "Solución de Problemas" arriba.

**¿Todo funciona?** ¡Perfecto! Ya puedes pasar a desplegar la API.

