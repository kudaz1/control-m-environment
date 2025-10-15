# ⚡ Inicio Rápido

Guía de 5 minutos para poner en marcha la API Control-M.

## 🎯 Objetivo

Crear una API que reciba el ambiente (Q5, Q7, Q8) desde Jira y modifique automáticamente tu JSON de Control-M.

## 🚀 Pasos Rápidos

### 1. Instalar dependencias (1 minuto)

**Windows:**
```bash
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
pip3 install -r requirements.txt
```

### 2. Iniciar la API (30 segundos)

**Windows:**
```bash
python api_control_m.py
```

**Linux/Mac:**
```bash
python3 api_control_m.py
```

O simplemente ejecuta el script de inicio:
- Windows: Doble clic en `start.bat`
- Linux/Mac: `./start.sh`

### 3. Probar que funciona (30 segundos)

Abre tu navegador en:
```
http://localhost:5000/health
```

Deberías ver:
```json
{"status": "ok", "message": "API Control-M está funcionando correctamente"}
```

### 4. Probar con tu JSON (2 minutos)

Ejecuta el script de pruebas:
```bash
python test_api.py
```

Esto probará automáticamente:
- ✅ Health check
- ✅ Reemplazo de Q7A por Q5A
- ✅ Reemplazo de Q7A por Q8A
- ✅ Formato Jira

## 🔗 Integrar con Jira (5 minutos)

### Opción A: Testing local (para pruebas)

Si solo quieres probar desde tu máquina:

1. Usa **ngrok** para exponer tu localhost:
   ```bash
   ngrok http 5000
   ```

2. Anota la URL que te da (ej: `https://abc123.ngrok.io`)

3. En Jira Automation, usa esa URL:
   ```
   https://abc123.ngrok.io/api/replace-environment-from-jira
   ```

### Opción B: Despliegue en Railway (para producción)

1. Sube tu código a GitHub
2. Ve a https://railway.app/
3. "New Project" → "Deploy from GitHub"
4. Selecciona tu repositorio
5. Espera 2-3 minutos
6. Copia la URL generada

7. En Jira Automation, usa:
   ```
   https://tu-proyecto.railway.app/api/replace-environment-from-jira
   ```

## 📝 Configurar Jira Automation

### 1. Crear campo "Ambiente"

1. Configuración → Problemas → Campos personalizados
2. Crear campo → Select List
3. Nombre: "Ambiente"
4. Opciones: Q5, Q7, Q8

### 2. Crear regla de automatización

1. Proyecto → Automation → Crear regla
2. **Trigger**: "Issue created" o "Field value changed"
3. **Action**: "Send web request"
   - URL: `https://tu-api.com/api/replace-environment-from-jira`
   - Method: POST
   - Headers: `Content-Type: application/json`
   - Body: Ver archivo `EJEMPLO_JIRA_WEBHOOK.json`

4. **Action**: "Add comment" (para ver el resultado)
   - Body: `{{webResponse.body}}`

5. Guardar y activar la regla

## 🧪 Probar la integración

1. Crea un ticket en Jira
2. En el campo "Ambiente", selecciona "Q5"
3. Guarda el ticket
4. Ve al ticket y busca el comentario con el JSON modificado
5. Verifica que todas las referencias Q7A y Q8A se cambiaron a Q5A

## ✅ Verificación

Revisa que se hayan cambiado estos campos:
- `RunAs`: Q7ABATCH → Q5ABATCH
- `OS400-CURLIB`: Q7AHIFILES → Q5AHIFILES  
- `OS400-JOB_OWNER`: Q7ABATCH → Q5ABATCH

## 📚 ¿Necesitas más detalles?

- **Configuración completa de Jira**: Ver `CONFIGURACION_JIRA.md`
- **Opciones de despliegue**: Ver `DEPLOYMENT.md`
- **Documentación de la API**: Ver `README.md`

## 🆘 Problemas comunes

### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
Otro programa está usando el puerto 5000. Ciérralo o cambia el puerto en `api_control_m.py`.

### Jira no puede conectar a localhost
Necesitas desplegar la API en un servidor público (Railway, Heroku, etc.) o usar ngrok para pruebas.

## 💡 Tips

1. **Para desarrollo**: Usa el script `test_api.py` antes de probar con Jira
2. **Para producción**: Despliega en Railway (gratis y fácil)
3. **Para debugging**: Revisa los logs de la API y de Jira Automation
4. **Para seguridad**: Añade autenticación en producción (ver README.md)

## 🎉 ¡Listo!

Tu API está funcionando y lista para recibir requests desde Jira Automation.

### Próximos pasos:

- [ ] API funcionando localmente
- [ ] Tests pasando correctamente  
- [ ] Desplegada en servidor público
- [ ] Integrada con Jira Automation
- [ ] Probada con tickets reales
- [ ] Documentada para tu equipo

---

**¿Preguntas?** Revisa la documentación completa en los otros archivos .md


