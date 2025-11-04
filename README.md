# 🧠 Creación de Asistente Digital IA en OCI  
## 👨‍💻 **Creado por Jeffrey Vargas**

---

## 📌 **Cheat Sheet — Comandos Clave**

| Acción | Comando |
|---|---|
Conectarse a VM | `ssh -i llave.key opc@PublicIP` |
Instalar repositorio OL dev | `sudo dnf -y install oraclelinux-developer-release-el9` |
Instalar OCI CLI | `sudo dnf install python39-oci-cli` |
Configurar OCI CLI | `oci setup config` |
Validar CLI | `oci -v` |
Obtener Namespace | `oci os ns get` |
Descargar sitio web | `wget …` *(ver sección)* |
Crear venv Python 3.11 | `/usr/bin/python3.11 -m venv IA-VENV` |
Activar venv | `source IA-VENV/bin/activate` |
Instalar requisitos | `pip install -r requirements.txt` |
Ejecutar UI | `streamlit run app.py` |
Ejecución persistente | `nohup streamlit run app.py > streamlit.log 2>&1 &` |
Detener app | `pkill -f "streamlit run app.py"` |

---

## 🚀 **Guía paso a paso con comandos**

### 1️⃣ Conectarse a la VM
```bash
ssh -i llave.key opc@PublicIP
```

---

### 2️⃣ Instalar OCI CLI
```bash
sudo dnf -y install oraclelinux-developer-release-el9
sudo dnf install python39-oci-cli
oci -v
oci setup config
oci os ns get
```

---

### 3️⃣ Descargar el sitio web
```bash
cd $HOME

wget --recursive --level=3 --no-parent --adjust-extension --convert-links --domains=www.grupomutual.fi.cr,grupomutual.fi.cr --reject="jpg,jpeg,png,gif,svg,webp,ico,css,js,woff,woff2,ttf,mp4,avi,pdf" --header="Accept:text/html" --header="Accept-Language: es-CR,es;q=0.9,en;q=0.8" --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36" --execute robots=off --directory-prefix=html https://www.grupomutual.fi.cr/
```

Copiar index:
```bash
cp ~/html/index.html ~/
```

---

### 4️⃣ Subir sitio al bucket OCI
```bash
cd $HOME

oci os object bulk-upload --bucket-name Bucket-MyCustomer --src-dir /home/opc/html/ --namespace axhxyz2qo8xt
```

---

### 5️⃣ Descargar la aplicación del agente
```bash
cd $HOME
wget https://github.com/jevargascr/OCI_AI_Digital_Agent/archive/refs/heads/main.zip
unzip main.zip -d temp
mv temp/OCI_AI_Digital_Agent-main/* .
rm -rf temp main.zip README.md
```

---

### 6️⃣ Instalar Python 3.11
```bash
sudo dnf -y update
sudo dnf install -y python3.11 python3.11-devel
```

---

### 7️⃣ Crear ambiente virtual
```bash
cd $HOME/Agente
/usr/bin/python3.11 -m venv IA-VENV
source IA-VENV/bin/activate
```

Validar:
```bash
python -V
pip -V
```

Instalar requisitos:
```bash
cd $HOME/Agente/
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 8️⃣ Configurar IDs del agente en OCI
```bash
cd $HOME/Agente/UI/
vi config_agente.py
```

---

### 9️⃣ Ejecutar aplicación
```bash
cd $HOME/Agente/UI/
streamlit run app.py
```

---

### 🔟 Mantener ejecución
```bash
nohup streamlit run app.py > streamlit.log 2>&1 &
```

Detener:
```bash
pkill -f "streamlit run app.py"
rm streamlit.log
```

---

### 1️⃣1️⃣ Configurar NGINX para servir Web + Bot
```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

Instalar:
```bash
sudo dnf install -y nginx
sudo systemctl enable --now nginx
sudo mkdir -p /etc/nginx/conf.d
```

Proxy config:
```bash
sudo tee /etc/nginx/conf.d/misitio.conf > /dev/null <<'NGINX'
server {
    listen 80;
    server_name _;
    root /var/www/misitio;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
    location /app/ {
        proxy_pass http://127.0.0.1:8501/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_read_timeout 86400;
    }
}
NGINX
```

Mover web:
```bash
sudo mkdir -p /var/www/misitio
sudo cp index.html /var/www/misitio/index.html
sudo semanage fcontext -a -t httpd_sys_content_t '/var/www/misitio(/.*)?' || true
sudo restorecon -Rv /var/www/misitio
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
```

---

🎯 **Listo! README Final para tu repositorio.**
