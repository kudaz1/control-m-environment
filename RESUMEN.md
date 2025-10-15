# 📦 Resumen del Proyecto

## ¿Qué es esto?

Una API REST que permite modificar configuraciones JSON de Control-M cambiando referencias de ambiente (Q5A, Q7A, Q8A) automáticamente desde Jira Automation.

## 🎯 Problema que resuelve

**Antes**: 
- Manual: Copiar JSON → Buscar y reemplazar Q7A por Q5A → Pegar en Control-M
- Propenso a errores
- Lento y tedioso

**Ahora**:
- Automático: Campo en Jira "Ambiente: Q5" → API modifica JSON → Listo
- Sin errores
- Instantáneo

## 📁 Archivos del Proyecto

### 🔧 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `api_control_m.py` | **API principal** - Código Python con Flask que procesa los requests |
| `requirements.txt` | Dependencias de Python necesarias |
| `test_api.py` | Script para probar la API localmente antes de integrar |

### 📖 Documentación

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Documentación completa de la API |
| `INICIO_RAPIDO.md` | **EMPIEZA AQUÍ** - Guía de 5 minutos |
| `CONFIGURACION_JIRA.md` | Guía paso a paso para configurar Jira Automation |
| `DEPLOYMENT.md` | Guía para desplegar en diferentes plataformas |
| `RESUMEN.md` | Este archivo - Vista general del proyecto |

### 🚀 Scripts de Inicio

| Archivo | Descripción |
|---------|-------------|
| `start.bat` | Script para iniciar en Windows (doble clic) |
| `start.sh` | Script para iniciar en Linux/Mac |

### 🐳 Docker

| Archivo | Descripción |
|---------|-------------|
| `Dockerfile` | Configuración para crear imagen Docker |
| `docker-compose.yml` | Orquestación de contenedores |

### ⚙️ Configuración

| Archivo | Descripción |
|---------|-------------|
| `.gitignore` | Archivos ignorados por Git |
| `Procfile` | Para despliegue en Heroku/Railway |
| `EJEMPLO_JIRA_WEBHOOK.json` | Ejemplo del JSON que Jira enviará |

## 🔄 Flujo de Trabajo

```
┌─────────────┐
│ Ticket Jira │
│ Ambiente: Q5│
└──────┬──────┘
       │
       │ 1. Trigger automation
       ▼
┌─────────────────────┐
│  Jira Automation    │
│  Send Web Request   │
└──────┬──────────────┘
       │
       │ 2. POST request con JSON
       ▼
┌─────────────────────┐
│   API Control-M     │
│  (api_control_m.py) │
└──────┬──────────────┘
       │
       │ 3. Procesa y reemplaza
       │    Q7A → Q5A
       │    Q8A → Q5A
       ▼
┌─────────────────────┐
│  JSON Modificado    │
│  RunAs: Q5ABATCH    │
│  CURLIB: Q5AHIFILES │
└──────┬──────────────┘
       │
       │ 4. Respuesta
       ▼
┌─────────────────────┐
│  Jira Automation    │
│  Añade comentario   │
└─────────────────────┘
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Flask**: Framework web para la API REST
- **Flask-CORS**: Permitir requests desde Jira
- **Gunicorn**: Servidor WSGI para producción
- **Docker**: Containerización (opcional)

## 📡 Endpoints de la API

### `GET /health`
Verifica que la API está funcionando.

**Respuesta:**
```json
{
    "status": "ok",
    "message": "API Control-M está funcionando correctamente"
}
```

### `POST /api/replace-environment`
Reemplaza ambiente en el JSON.

**Request:**
```json
{
    "environment": "Q5",
    "json_data": { /* Tu JSON aquí */ }
}
```

**Respuesta:**
```json
{
    "success": true,
    "environment": "Q5A",
    "modified_json": { /* JSON modificado */ }
}
```

### `POST /api/replace-environment-from-jira`
Optimizado para recibir datos desde Jira Automation.

**Request:**
```json
{
    "environment": "Q5",
    "json_data": { /* Tu JSON aquí */ }
}
```

## 🎯 Casos de Uso

### Caso 1: Deploy en Q5
- Usuario crea ticket con "Ambiente: Q5"
- API cambia todo Q7A y Q8A por Q5A
- JSON listo para desplegar en Q5

### Caso 2: Deploy en Q7
- Usuario crea ticket con "Ambiente: Q7"
- API cambia todo Q5A y Q8A por Q7A
- JSON listo para desplegar en Q7

### Caso 3: Deploy en Q8
- Usuario crea ticket con "Ambiente: Q8"
- API cambia todo Q5A y Q7A por Q8A
- JSON listo para desplegar en Q8

## 📊 Campos que se Modifican

La API busca y reemplaza en TODO el JSON:

| Campo Original | Con Q5 | Con Q7 | Con Q8 |
|----------------|--------|--------|--------|
| `RunAs: Q7ABATCH` | `Q5ABATCH` | `Q7ABATCH` | `Q8ABATCH` |
| `OS400-CURLIB: Q7AHIFILES` | `Q5AHIFILES` | `Q7AHIFILES` | `Q8AHIFILES` |
| `OS400-JOB_OWNER: Q7ABATCH` | `Q5ABATCH` | `Q7ABATCH` | `Q8ABATCH` |
| Cualquier `Q7A` o `Q8A` | `Q5A` | `Q7A` | `Q8A` |

## 🚀 Opciones de Despliegue

### Local (Para desarrollo)
```bash
python api_control_m.py
```
- ✅ Rápido para probar
- ❌ No accesible desde Jira Cloud

### Railway (Recomendado)
```bash
# Push a GitHub → Deploy en Railway
```
- ✅ Gratis
- ✅ Fácil de configurar
- ✅ HTTPS automático
- ✅ Perfecto para Jira Cloud

### Docker
```bash
docker-compose up -d
```
- ✅ Portable
- ✅ Fácil de escalar
- ✅ Aislamiento completo

### Servidor propio
```bash
gunicorn -w 4 api_control_m:app
```
- ✅ Control total
- ✅ En tu infraestructura
- ❌ Requiere configuración

## ✅ Checklist de Implementación

### Fase 1: Setup Local (30 minutos)
- [ ] Instalar Python y dependencias
- [ ] Ejecutar `start.bat` o `start.sh`
- [ ] Verificar `/health` funciona
- [ ] Ejecutar `test_api.py`
- [ ] Verificar que los tests pasan

### Fase 2: Configurar Jira (30 minutos)
- [ ] Crear campo "Ambiente" en Jira
- [ ] Obtener ID del custom field
- [ ] Crear regla de automation
- [ ] Configurar trigger
- [ ] Configurar action "Send web request"
- [ ] Configurar body con tu JSON

### Fase 3: Despliegue (20 minutos)
- [ ] Subir código a GitHub
- [ ] Crear proyecto en Railway
- [ ] Desplegar desde GitHub
- [ ] Obtener URL pública
- [ ] Actualizar URL en Jira

### Fase 4: Testing (10 minutos)
- [ ] Crear ticket de prueba con Q5
- [ ] Verificar que automation se ejecuta
- [ ] Revisar JSON modificado
- [ ] Probar con Q7 y Q8
- [ ] Verificar logs

### Fase 5: Producción (5 minutos)
- [ ] Configurar CORS correctamente
- [ ] Añadir autenticación (opcional)
- [ ] Configurar rate limiting (opcional)
- [ ] Documentar para el equipo
- [ ] Entrenar usuarios

## 🆘 Soporte

### Problemas más comunes:

1. **API no inicia**
   - Solución: Verificar que Python 3.8+ está instalado
   - Solución: `pip install -r requirements.txt`

2. **Jira no puede conectar**
   - Solución: La API debe estar en servidor público (no localhost)
   - Solución: Usar Railway o ngrok

3. **JSON no se modifica**
   - Solución: Verificar que el campo "environment" llega correctamente
   - Solución: Revisar logs de la API

4. **Error 401/403 en Jira**
   - Solución: Verificar configuración de CORS
   - Solución: Verificar headers de autenticación

### Logs útiles:

**Ver logs de la API:**
```bash
# Local
# Los logs aparecen en la consola

# Docker
docker logs -f control-m-api

# Railway
# Ver en dashboard → Logs
```

**Ver logs de Jira:**
- Ve al ticket → Menú → "View automation history"

## 📈 Próximas Mejoras Posibles

### Funcionalidades:
- [ ] Guardar historial de cambios
- [ ] Soporte para más ambientes (PROD, DEV, etc.)
- [ ] Validación de JSON de Control-M
- [ ] Integración directa con API de Control-M
- [ ] UI web para probar la API

### Seguridad:
- [ ] Autenticación con tokens
- [ ] Rate limiting
- [ ] Logging avanzado
- [ ] Auditoría de cambios

### DevOps:
- [ ] CI/CD pipeline
- [ ] Tests automatizados
- [ ] Monitoreo con Prometheus
- [ ] Alertas automáticas

## 🤝 Contribuir

Este proyecto fue creado específicamente para Coopeuch y sus necesidades de Control-M.

Si necesitas modificarlo:
1. Edita `api_control_m.py` para la lógica
2. Actualiza `requirements.txt` si añades librerías
3. Actualiza la documentación correspondiente
4. Prueba localmente con `test_api.py`

## 📝 Licencia

Uso interno de Coopeuch.

## 📞 Contacto

Para preguntas o soporte sobre este proyecto, contacta al equipo de DevOps de Coopeuch.

---

## 🎓 Recursos Adicionales

### Aprender más sobre:
- **Flask**: https://flask.palletsprojects.com/
- **Jira Automation**: https://www.atlassian.com/software/jira/automation
- **Control-M**: https://docs.bmc.com/docs/automation-api
- **Railway**: https://docs.railway.app/

### Herramientas útiles:
- **JSON Validator**: https://jsonlint.com/
- **Postman**: Para probar la API manualmente
- **ngrok**: Para exponer localhost a internet (testing)

---

**Versión**: 1.0.0  
**Fecha**: Octubre 2025  
**Autor**: Creado para Coopeuch Control-M Integration


