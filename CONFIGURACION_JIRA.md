# 📘 Guía Detallada: Configuración de Jira Automation

Esta guía te ayudará paso a paso a configurar Jira Automation para llamar a la API y modificar los JSONs de Control-M según el ambiente.

## 🎯 Objetivo

Cuando se crea o modifica un ticket en Jira con un campo de ambiente (Q5, Q7, Q8), automáticamente:
1. Jira llamará a la API
2. La API modificará el JSON de Control-M
3. El JSON modificado se podrá usar para desplegar en Control-M

---

## 📋 Parte 1: Crear Campo Personalizado en Jira

### Paso 1: Acceder a la configuración

1. Haz clic en el ícono de ⚙️ **Configuración** (arriba a la derecha)
2. Selecciona **Problemas**
3. En el menú izquierdo, selecciona **Campos personalizados**

### Paso 2: Crear el campo

1. Haz clic en **Crear campo personalizado**
2. Selecciona el tipo:
   - **Opción recomendada**: `Select List (single choice)` - Para lista desplegable
   - **Opción alternativa**: `Text Field (single line)` - Para texto libre
3. Haz clic en **Siguiente**

### Paso 3: Configurar el campo

1. **Nombre**: `Ambiente`
2. **Descripción**: `Ambiente donde se ejecutará la malla (Q5, Q7 o Q8)`

3. Si elegiste **Select List**, añade las opciones:
   - Opción 1: `Q5`
   - Opción 2: `Q7`
   - Opción 3: `Q8`

4. Haz clic en **Crear**

### Paso 4: Asociar a pantallas

1. Selecciona en qué pantallas aparecerá el campo
2. Marca las pantallas relevantes:
   - ✓ Default Screen
   - ✓ Workflow Screen (si existe)
   - ✓ Cualquier otra pantalla de tu proyecto

3. Haz clic en **Actualizar**

### Paso 5: Obtener el ID del campo

**IMPORTANTE**: Necesitas saber el ID del campo personalizado.

1. Ve a **Configuración** → **Problemas** → **Campos personalizados**
2. Busca tu campo "Ambiente"
3. Haz clic en el ícono de engranaje → **Ver configuración**
4. En la URL verás algo como: `.../customfield_10050`
5. **Anota ese ID**: `customfield_10050` (tu número será diferente)

---

## 🤖 Parte 2: Configurar Automation Rule

### Paso 1: Crear nueva regla

1. Ve a tu proyecto en Jira
2. Clic en **Configuración del proyecto** (menú lateral)
3. Selecciona **Automation** en el menú
4. Clic en **Crear regla**

### Paso 2: Configurar el TRIGGER (Disparador)

Elige cuándo se ejecutará la automatización:

**Opción A: Cuando se crea un problema**
1. Busca y selecciona: `Issue created`
2. Haz clic en **Guardar**

**Opción B: Cuando cambia el campo de ambiente**
1. Busca y selecciona: `Field value changed`
2. En "Field": Selecciona tu campo `Ambiente`
3. Haz clic en **Guardar**

**Opción C: Trigger manual**
1. Busca y selecciona: `Manual trigger`
2. Esto te permitirá ejecutarlo cuando quieras desde el ticket

### Paso 3: Añadir CONDICIÓN (Opcional)

Si quieres que solo se ejecute bajo ciertas condiciones:

1. Clic en **➕ Añadir componente**
2. Selecciona **Condition** → **Advanced compare condition**
3. Ejemplo de condición:
   ```
   {{issue.Ambiente}} != null
   ```
4. Esto asegura que solo se ejecuta si el campo Ambiente tiene valor

### Paso 4: Añadir ACCIÓN - Send Web Request

Esta es la parte más importante:

1. Clic en **➕ Añadir componente**
2. Selecciona **Action** → **Send web request**

#### Configuración del Web Request:

**A. URL de la API**
```
https://tu-servidor.com/api/replace-environment-from-jira
```

⚠️ **IMPORTANTE**: 
- Si estás probando localmente: `http://localhost:5000/api/replace-environment-from-jira`
- En producción: Usa la URL real donde desplegaste la API
- Debe ser HTTPS en producción por seguridad

**B. HTTP Method**
```
POST
```

**C. Web request body**
Selecciona: `Custom data`

**D. Custom data** (Aquí va el JSON que enviarás):

```json
{
    "environment": "{{issue.Ambiente}}",
    "json_data": {
        "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
            "Type": "SimpleFolder",
            "ControlmServer": "COOPEUCH",
            "OrderMethod": "Manual",
            "CC1040P2": {
                "Type": "Job:OS400:Full:CommandLine",
                "CommandLine": "CALL PGM(RBIENVFCL)  PARM('CTINTDEM' 'NEXDEM')",
                "SubApplication": "GENER_NEXUS-DEMOGRAFICO-CARLOS",
                "Priority": "Very Low",
                "FileName": "CC1040P2",
                "Confirm": true,
                "Host": "ibsqa",
                "FilePath": "CC1040P2",
                "CreatedBy": "emuser",
                "Description": "NEXUS-DEMOGRAFICO",
                "RunAs": "Q7ABATCH",
                "Application": "GENER_NEXUS-DEMOGRAFICO-CARLOS",
                "Variables": [
                    {"tm": "%%TIME"},
                    {"HHt": "%%SUBSTR %%tm  1 2"},
                    {"MMt": "%%SUBSTR %%tm  3 2"},
                    {"SSt": "%%SUBSTR %%tm  5 2"},
                    {"HORA": "%%HHt:%%MMt:%%SSt"},
                    {"OS400-AEV_LEN": "4000"},
                    {"OS400-JOB_NAME": "CC1040P2"},
                    {"OS400-MEM_NAME": "CC1040P2"},
                    {"OS400-MEM_LIB": "CC1040P2"},
                    {"OS400-JOBD": "*USRPRF"},
                    {"OS400-CURLIB": "Q7AHIFILES"},
                    {"OS400-JOB_OWNER": "Q7ABATCH"}
                ],
                "RerunLimit": {
                    "Units": "Minutes",
                    "Every": "0"
                },
                "When": {
                    "WeekDays": ["MON", "TUE", "WED", "THU", "FRI"],
                    "MonthDays": ["NONE"],
                    "FromTime": "2000",
                    "DaysRelation": "OR",
                    "ConfirmationCalendars": {
                        "Calendar": "Cal_Habil"
                    }
                },
                "JobAFT": {
                    "Type": "Resource:Pool",
                    "Quantity": "1"
                },
                "eventsToWaitFor": {
                    "Type": "WaitForEvents",
                    "Events": [
                        {"Event": "PRECIERRE-EODAY-NEXUS-001-IBS-DIA"}
                    ]
                }
            }
        }
    }
}
```

**E. Headers**

Añade estos headers:

```
Content-Type: application/json
```

Si tu API requiere autenticación, añade también:
```
Authorization: Bearer TU_TOKEN_AQUI
```

**F. Configuración adicional**

- **Delay execution**: 0 seconds (o el que necesites)
- **Timeout**: 10 seconds (ajusta según necesidad)
- **Fail on error**: ✓ Marcado (para que falle si la API no responde)

5. Haz clic en **Guardar**

### Paso 5: Añadir acción para capturar la respuesta (Opcional)

Si quieres ver el JSON modificado en el ticket:

1. Clic en **➕ Añadir componente**
2. Selecciona **Action** → **Add comment**
3. En el comentario, usa:

```
JSON modificado para ambiente: {{issue.Ambiente}}

Respuesta de la API:
{{webResponse.body}}

Status: {{webResponse.status}}
```

Esto añadirá un comentario en el ticket con el JSON modificado.

### Paso 6: Nombrar y guardar la regla

1. Arriba a la izquierda, ponle un nombre a la regla:
   ```
   Control-M: Modificar JSON según ambiente
   ```

2. Haz clic en **Activar** (Turn on)

---

## ✅ Parte 3: Probar la Configuración

### Prueba 1: Crear un ticket de prueba

1. Crea un nuevo ticket en tu proyecto
2. En el campo **Ambiente**, selecciona `Q5`
3. Completa los otros campos requeridos
4. Crea el ticket

### Prueba 2: Verificar ejecución

1. Ve al ticket recién creado
2. En el menú superior, haz clic en **⋯** (más opciones)
3. Selecciona **View automation history**
4. Deberías ver tu regla ejecutándose

### Prueba 3: Verificar resultado

Si añadiste la acción de comentario:
1. Verifica que haya un comentario con el JSON modificado
2. Busca las referencias de ambiente y verifica que cambien correctamente:
   - Si elegiste Q5: Deberían aparecer `Q5ABATCH`, `Q5AHIFILES`, etc.

---

## 🔍 Solución de Problemas

### ❌ Error: "Connection timeout"

**Causa**: La API no es accesible desde Jira

**Solución**:
- Verifica que la URL de la API sea correcta
- Si es localhost, no funcionará (Jira Cloud necesita una URL pública)
- Despliega la API en un servidor accesible públicamente

### ❌ Error: "401 Unauthorized" o "403 Forbidden"

**Causa**: Problemas de autenticación

**Solución**:
- Verifica los headers de autenticación
- Asegúrate de que la API permita CORS
- Verifica que el token sea válido

### ❌ Error: "Invalid JSON"

**Causa**: El JSON en el Custom data tiene errores

**Solución**:
- Verifica que el JSON sea válido (usa un validador online)
- Asegúrate de usar comillas dobles `"` no simples `'`
- Verifica que las variables de Jira estén correctas: `{{issue.Ambiente}}`

### ❌ La regla no se ejecuta

**Causa**: El trigger no está configurado correctamente

**Solución**:
- Verifica que el trigger sea el correcto
- Revisa las condiciones (puede que las condiciones impidan la ejecución)
- Mira el **Audit log** de la regla

### ❌ El campo Ambiente no aparece

**Causa**: El campo no está asociado a la pantalla correcta

**Solución**:
- Ve a **Configuración** → **Problemas** → **Pantallas**
- Encuentra la pantalla que usa tu proyecto
- Añade el campo "Ambiente" a esa pantalla

---

## 📊 Variante Avanzada: Leer JSON desde archivo

Si tu JSON está en un archivo adjunto en Jira o en un repositorio:

### Opción A: JSON en campo de texto

1. Crea un campo personalizado tipo "Text Field (multi-line)"
2. Llámalo "JSON Control-M"
3. En la regla de automation, usa:
   ```json
   {
       "environment": "{{issue.Ambiente}}",
       "json_data": {{issue.JSON_Control-M}}
   }
   ```

### Opción B: JSON en repositorio Git

1. Añade una acción **Send web request** adicional ANTES de la llamada a la API
2. Llama a la API de GitHub/GitLab para obtener el archivo
3. Guarda la respuesta en una variable
4. Usa esa variable en la segunda llamada a tu API

---

## 🎓 Consejos Adicionales

### 1. Logging y Debugging

Añade acciones de log para depurar:
```
Action: Add comment (internal)
Comentario: "Ambiente seleccionado: {{issue.Ambiente}}"
```

### 2. Notificaciones

Añade notificaciones cuando termine:
```
Action: Send email
To: tu-equipo@coopeuch.cl
Subject: JSON de Control-M actualizado para {{issue.key}}
Body: El JSON fue modificado para ambiente {{issue.Ambiente}}
```

### 3. Validaciones

Añade validaciones antes de llamar a la API:
```
Condition: {{issue.Ambiente}} matches "Q[5-8]"
```

### 4. Manejo de errores

Añade una rama "else" para manejar errores:
```
If: webResponse.status == 200
  Then: Add comment con éxito
Else:
  Then: Add comment con error + notificar al equipo
```

---

## 📞 Contacto y Soporte

Si tienes dudas sobre la configuración:
1. Revisa los logs de Jira Automation
2. Revisa los logs de la API
3. Contacta al administrador de Jira de tu organización

---

## ✅ Checklist Final

Antes de dar por terminada la configuración, verifica:

- [ ] Campo personalizado "Ambiente" creado y visible
- [ ] API desplegada y accesible desde Jira
- [ ] Regla de automation creada y activada
- [ ] Trigger configurado correctamente
- [ ] Web request con la URL correcta
- [ ] Custom data con JSON válido
- [ ] Headers configurados (Content-Type)
- [ ] Probado con un ticket de prueba
- [ ] Respuesta de la API verificada
- [ ] JSON modificado correctamente

¡Listo! Tu integración Jira + API Control-M está configurada. 🎉


