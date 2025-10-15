# 🚀 Guía de Despliegue

Esta guía te muestra cómo desplegar la API en diferentes entornos.

## 📋 Tabla de Contenidos

1. [Despliegue Local](#despliegue-local)
2. [Despliegue con Docker](#despliegue-con-docker)
3. [Despliegue en Railway](#despliegue-en-railway)
4. [Despliegue en Heroku](#despliegue-en-heroku)
5. [Despliegue en servidor propio](#despliegue-en-servidor-propio)

---

## 🖥️ Despliegue Local

### Windows

1. **Instalar Python** (si no lo tienes)
   - Descarga desde: https://www.python.org/downloads/
   - Versión mínima: 3.8

2. **Abrir terminal en la carpeta del proyecto**
   - Haz clic derecho en la carpeta
   - "Abrir PowerShell aquí" o "Abrir terminal aquí"

3. **Ejecutar el script de inicio**
   ```bash
   start.bat
   ```

   O manualmente:
   ```bash
   pip install -r requirements.txt
   python api_control_m.py
   ```

4. **Verificar que funciona**
   - Abre el navegador en: http://localhost:5000/health
   - Deberías ver: `{"status": "ok", ...}`

### Linux/Mac

1. **Instalar Python** (si no lo tienes)
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip
   
   # Mac (con Homebrew)
   brew install python3
   ```

2. **Dar permisos al script**
   ```bash
   chmod +x start.sh
   ```

3. **Ejecutar el script**
   ```bash
   ./start.sh
   ```

   O manualmente:
   ```bash
   pip3 install -r requirements.txt
   python3 api_control_m.py
   ```

4. **Verificar que funciona**
   ```bash
   curl http://localhost:5000/health
   ```

---

## 🐳 Despliegue con Docker

### Prerrequisitos
- Docker instalado: https://www.docker.com/get-started

### Opción 1: Docker solo

1. **Construir la imagen**
   ```bash
   docker build -t control-m-api .
   ```

2. **Ejecutar el contenedor**
   ```bash
   docker run -d -p 5000:5000 --name control-m-api control-m-api
   ```

3. **Verificar logs**
   ```bash
   docker logs control-m-api
   ```

4. **Detener el contenedor**
   ```bash
   docker stop control-m-api
   ```

### Opción 2: Docker Compose

1. **Iniciar todo**
   ```bash
   docker-compose up -d
   ```

2. **Ver logs**
   ```bash
   docker-compose logs -f
   ```

3. **Detener todo**
   ```bash
   docker-compose down
   ```

---

## 🚂 Despliegue en Railway

Railway es gratuito y muy fácil de usar para despliegues rápidos.

### Paso 1: Preparar el repositorio

1. **Crear repositorio en GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/control-m-api.git
   git push -u origin main
   ```

### Paso 2: Desplegar en Railway

1. Ve a: https://railway.app/
2. Clic en **"Start a New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza Railway a acceder a tu GitHub
5. Selecciona tu repositorio
6. Railway detectará automáticamente que es Python y Flask
7. Espera a que termine el despliegue (2-3 minutos)

### Paso 3: Configurar

1. En Railway, ve a tu proyecto
2. Clic en **"Settings"**
3. En **"Environment Variables"**, añade (si es necesario):
   ```
   PORT=5000
   ```
4. En **"Networking"**, haz clic en **"Generate Domain"**
5. Anota tu URL: `https://tu-proyecto.railway.app`

### Paso 4: Probar

```bash
curl https://tu-proyecto.railway.app/health
```

### Paso 5: Usar en Jira

En tu Jira Automation, usa la URL:
```
https://tu-proyecto.railway.app/api/replace-environment-from-jira
```

---

## 🟣 Despliegue en Heroku

### Prerrequisitos
- Cuenta en Heroku: https://heroku.com
- Heroku CLI instalado: https://devcenter.heroku.com/articles/heroku-cli

### Paso 1: Login

```bash
heroku login
```

### Paso 2: Crear aplicación

```bash
heroku create control-m-api
```

### Paso 3: Desplegar

```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Paso 4: Verificar

```bash
heroku open /health
```

### Paso 5: Ver logs

```bash
heroku logs --tail
```

---

## 🖥️ Despliegue en Servidor Propio (Linux)

Para un servidor de producción real en tu infraestructura.

### Prerrequisitos
- Servidor Linux (Ubuntu 20.04+ recomendado)
- Acceso SSH
- Dominio o IP pública

### Paso 1: Conectar al servidor

```bash
ssh usuario@tu-servidor.com
```

### Paso 2: Instalar dependencias

```bash
# Actualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar Python y pip
sudo apt install python3 python3-pip python3-venv -y

# Instalar Nginx (para proxy reverso)
sudo apt install nginx -y
```

### Paso 3: Crear usuario para la aplicación

```bash
sudo useradd -m -s /bin/bash controlm
sudo su - controlm
```

### Paso 4: Clonar el proyecto

```bash
cd /home/controlm
git clone https://github.com/tu-usuario/control-m-api.git
cd control-m-api
```

### Paso 5: Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 6: Crear servicio systemd

Como root, crea el archivo `/etc/systemd/system/control-m-api.service`:

```ini
[Unit]
Description=Control-M API
After=network.target

[Service]
Type=notify
User=controlm
WorkingDirectory=/home/controlm/control-m-api
Environment="PATH=/home/controlm/control-m-api/venv/bin"
ExecStart=/home/controlm/control-m-api/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 api_control_m:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Paso 7: Iniciar el servicio

```bash
sudo systemctl daemon-reload
sudo systemctl start control-m-api
sudo systemctl enable control-m-api
sudo systemctl status control-m-api
```

### Paso 8: Configurar Nginx

Crea el archivo `/etc/nginx/sites-available/control-m-api`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;  # Cambia esto

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar el sitio:

```bash
sudo ln -s /etc/nginx/sites-available/control-m-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 9: Configurar SSL (HTTPS) con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

### Paso 10: Verificar

```bash
curl https://tu-dominio.com/health
```

---

## 🔒 Seguridad en Producción

### 1. Configurar HTTPS
Siempre usa HTTPS en producción (certificado SSL).

### 2. Limitar CORS
En `api_control_m.py`, cambia:
```python
CORS(app)  # Permite todo
```

Por:
```python
CORS(app, origins=["https://tu-jira.atlassian.net"])
```

### 3. Añadir autenticación (Opcional)

Añade un token de autenticación:

```python
from functools import wraps
from flask import request

API_TOKEN = "tu-token-super-secreto"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {API_TOKEN}":
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/replace-environment', methods=['POST'])
@require_auth
def replace_environment_endpoint():
    # ... resto del código
```

Luego en Jira, añade el header:
```
Authorization: Bearer tu-token-super-secreto
```

### 4. Rate Limiting

Instala Flask-Limiter:
```bash
pip install Flask-Limiter
```

Añade al código:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/replace-environment', methods=['POST'])
@limiter.limit("10 per minute")
def replace_environment_endpoint():
    # ... resto del código
```

---

## 📊 Monitoreo

### Ver logs en servidor Linux

```bash
sudo journalctl -u control-m-api -f
```

### Ver logs en Docker

```bash
docker logs -f control-m-api
```

### Ver logs en Railway/Heroku

- Railway: Pestaña "Logs" en el dashboard
- Heroku: `heroku logs --tail`

---

## 🆘 Solución de Problemas

### La API no inicia

1. Verifica los logs
2. Verifica que el puerto 5000 esté libre
3. Verifica que todas las dependencias estén instaladas

### Error de permisos

```bash
sudo chown -R controlm:controlm /home/controlm/control-m-api
```

### Nginx no puede conectar

Verifica SELinux (en RHEL/CentOS):
```bash
sudo setsebool -P httpd_can_network_connect 1
```

### La API es muy lenta

Aumenta los workers en gunicorn:
```bash
gunicorn -w 8 -b 0.0.0.0:5000 api_control_m:app
```

---

## ✅ Checklist de Despliegue

- [ ] API funciona localmente
- [ ] Tests pasan correctamente
- [ ] Repositorio en GitHub/GitLab
- [ ] Servicio desplegado y accesible
- [ ] HTTPS configurado (en producción)
- [ ] CORS configurado correctamente
- [ ] Logs configurados
- [ ] Monitoreo activo
- [ ] URL añadida a Jira Automation
- [ ] Pruebas realizadas desde Jira

¡Tu API está lista para producción! 🎉


