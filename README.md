# Creado por Jeffrey Vargas

# Page 1

Conﬁdential – Oracle Internal 
Creación de Asistente Digital IA en OCI 
I. Crear política de IA en el tenant 
Navegamos a Identity & Security -> Policies 

![Image Page 1-1](./Images/page1_img1.png)

# Page 2

Conﬁdential – Oracle Internal 
Create Policy -> Crear una nueva política en el compartment root, 
Poner Nombre, Descripción y seleccionar Show manual editor 
Poner las siguientes instrucciones: 
Allow any-user to inspect buckets in tenancy 
Allow any-user to read objects in tenancy 
Allow any-user to use database-tools-connections in tenancy 
Allow any-user to read database-tools-family in tenancy 
Allow any-user to read secret-family in tenancy 
Allow any-user to {BUCKET_INSPECT, BUCKET_READ, OBJECT_INSPECT, 
OBJECT_READ, OBJECT_CREATE, OBJECT_OVERWRITE, PAR_MANAGE} in tenancy 

![Image Page 2-1](./Images/page2_img1.png)

# Page 3

Conﬁdential – Oracle Internal 
II. Creación de Compartment 
Navegamos a Identity & Security -> Compartments  
 
Create compartment -> Poner Nombre y Descripción, usar este compartment para crear 
todos los recursos de este laboratorio. 

![Image Page 3-1](./Images/page3_img1.png)

![Image Page 3-2](./Images/page3_img2.png)

# Page 4

Conﬁdential – Oracle Internal 
III. Creación de VCN 
Navegamos a Networking -> Virtual Cloud Networks 
 
Crear una nueva VCN a partir del Wizard y dejamos los valores por defecto 
 
Poner Nombre y crear. 

![Image Page 4-1](./Images/page4_img1.png)

![Image Page 4-2](./Images/page4_img2.png)

# Page 5

Conﬁdential – Oracle Internal 
Una vez creada la VCN entrar a la lista de seguridad de la sub red pública y habilitar los 
puertos TCP 80 y 8501 
 
IV. Creación del Bucket 
Navegamos a Storage -> Buckets 

![Image Page 5-1](./Images/page5_img1.png)

![Image Page 5-2](./Images/page5_img2.png)

# Page 6

Conﬁdential – Oracle Internal 
Create bucket -> La creación puede realizarse con los parámetros por defecto, solo se 
debe de agregar el nombre. 
Este Bucket contendrá el sitio web que descargaremos y subiremos posteriormente. 

![Image Page 6-1](./Images/page6_img1.png)

# Page 7

Conﬁdential – Oracle Internal 
V. Creación de Máquina Virtual en OCI 
Crear una máquina virtual con sistema operativo OL9, procesador Intel o AMD y en una 
subred pública que tenga salida a los puertos 80 y 8501 
Conﬁguración en la lista de seguridad de la subred pública: 
# Ingresar a la máquina virtual con el comando ssh 
ssh -i llave.key opc@PublicIP 
Realizar la instalación dentro de la maquina: 
Lo primero que realizaremos es la instalación y conﬁguración del OCI CLI 
Cualquier duda de instalación referenciar a este link:  
https://docs.oracle.com/es-ww/iaas/Content/API/SDKDocs/cliinstall.htm 
# Instalar CLI 
sudo dnf -y install oraclelinux-developer-release-el9 
sudo dnf install python39-oci-cli 
# Validamos la instalación: oci -v 
oci -v 
# Realizamos la conﬁguración: 
oci setup config 
# Probamos que traiga nuestro Object storage namespace 
oci os ns get 

# Page 8

Conﬁdential – Oracle Internal 
VI. Descargar el Sitio: 
Se identiﬁca la página web principal y a través del comando wget se descarga el sitio. 
Nota: Podría ser que el sitio este protegido en ese caso tendríamos que pensar en un plan 
B como descargar los archivos htmls y PDFs manualmente de las páginas de interés o 
modiﬁcar esta instrucción. 
Página de ejemplo: https://www.mycustomer.com 
cd $HOME 
wget --recursive --level=3 --no-parent --adjust-extension --convert-links --domains= 
www.grupomutual.fi.cr, grupomutual.fi.cr --
reject="jpg,jpeg,png,gif,svg,webp,ico,css,js,woff,woff2,ttf,mp4,avi,pdf" --header="Accept: 
text/html" --header="Accept-Language: es-CR,es;q=0.9,en;q=0.8" --user-agent="Mozilla/5.0 (Windows 
NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36" --execute 
robots=off --directory-prefix=html https://www.grupomutual.fi.cr/  
Notas:  
• Las partes marcadas en amarillo son las que deben ser sustituidas por el nuevo 
sitio web a trabajar. 
• El sitio quedara en la ruta /home/opc/html 

• Sacar una copia del index.html para ser modiﬁcada después y dejarlo en la ruta 
/home/opc/ 

![Image Page 8-1](./Images/page8_img1.png)

![Image Page 8-2](./Images/page8_img2.png)

# Page 9

Conﬁdential – Oracle Internal 
VII. Cargar sitio web al Bucket. 
El comando para cargar en modo bulk el sitio a OCI es: 
cd $HOME 
oci os object bulk-upload --bucket-name Bucket-MyCustomer --src-dir 
/home/opc/html/ --namespace axhxyz2qo8xt 
Notas:  
• Las partes marcadas en amarillo son las que deben ser sustituidas por los valores 
de su ambiente 
• Validar una vez terminado el comando que en el bucket los archivos hayan sido 
cargados exitosamente. 

# Page 10

Conﬁdential – Oracle Internal 
VIII. Creación del Knowledge Base para nuestro agente. 
Una vez que el sitio ya se encuentre cargado en nuestro Bucket procederemos a crear el 
Knowledge Base. 
Nota: Se puede dejar creando este componente y avanzar con el tutorial. 
Menu: Analytics & AI -> Generative AI Agents -> Knowledge Bases 

![Image Page 10-1](./Images/page10_img1.png)

![Image Page 10-2](./Images/page10_img2.png)

# Page 11

Conﬁdential – Oracle Internal 
 
En la creación debemos de introducir un nombre, importante que el Data storage type sea 
Object storage, marcar el check de Enable hybrid search y deﬁnir el data source 

![Image Page 11-1](./Images/page11_img1.png)

![Image Page 11-2](./Images/page11_img2.png)

# Page 12

Conﬁdential – Oracle Internal 
En el data source poner: 
Un nombre, habilitar Enable multi-modal parsing, seleccionar el Bucket creado 
anteriormente, habilitar Select all in bucket y crear 

![Image Page 12-1](./Images/page12_img1.png)

![Image Page 12-2](./Images/page12_img2.png)

# Page 13

Conﬁdential – Oracle Internal 
IX. Creación del Agente: 
Nota Importante: El Knowledge Bases no será relacionado al agente en este momento, ya 
que eso se hará a través del código al igual que las instrucciones del ruteo; Además, se 
puede dejar creando este componente y avanzar con el tutorial. 
En la primera página se debe de agregar el nombre y darle Next 

![Image Page 13-1](./Images/page13_img1.png)

# Page 14

Conﬁdential – Oracle Internal 
Segunda página dejarla así y Next 
 
Tercera página dejarla igual y Next 

![Image Page 14-1](./Images/page14_img1.png)

![Image Page 14-2](./Images/page14_img2.png)

# Page 15

Conﬁdential – Oracle Internal 
Cuarta página crear agente y aceptar política 

![Image Page 15-1](./Images/page15_img1.png)

![Image Page 15-2](./Images/page15_img2.png)

# Page 16

Conﬁdential – Oracle Internal 
X. Conﬁguración de la Aplicación  
Para esta parte nos devolvemos a la máquina virtual previamente creada 
# Ingresar a la máquina virtual con el comando ssh 
ssh -i llave.key opc@PublicIP 
#  Conﬁgurar Networking 
sudo firewall-cmd --permanent --add-port=8501/tcp 
sudo firewall-cmd --reload 
#  Descargar la aplicación desde github 
cd $HOME 
wget https://github.com/jevargascr/OCI_AI_Digital_Agent/archive/refs/heads/main.zip 
unzip main.zip -d temp 
mv temp/OCI_AI_Digital_Agent-main/* . 
rm -rf temp 
rm main.zip 
rm README.md 
Nuestro directorio $HOME se debería de ver así 
 
# Instalación de Python 11 
sudo dnf -y update 
sudo dnf install -y python3.11 python3.11-devel 
 
# Creación ambiente virtual 
cd $HOME 
cd Agente 
/usr/bin/python3.11 -m venv IA-VENV 
source IA-VENV/bin/activate 

![Image Page 16-1](./Images/page16_img1.png)

# Page 17

Conﬁdential – Oracle Internal 
# Validar que las versiones sean la 11 
python -V   
pip -V  
 
# Instalar actualizaciones y requisitos 
cd $HOME/Agente/ 
python -m pip install --upgrade pip 
pip install -r requirements.txt 
 
# Se debe de editar el archivo conﬁg_agent.py que se encuentra dentro de la carpeta UI 
para sustituir estos valores: 
knowledge_base_id= 
agent_endpoint_id= 

![Image Page 17-1](./Images/page17_img1.png)

![Image Page 17-2](./Images/page17_img2.png)

# Page 18

Conﬁdential – Oracle Internal 
Notas: 
El  knowledge_base_id es el OCID de nuestra base de datos de conocimiento y en OCI se 
encuentra en Menu: Analytics & AI -> Generative AI Agents -> Knowledge Bases -> OCID 

![Image Page 18-1](./Images/page18_img1.png)

# Page 19

Conﬁdential – Oracle Internal 
El  agent_endpoint_id es el OCID del Endpoint de nuestro agente y en OCI se encuentra en 
Menu: Analytics & AI -> Generative AI Agents -> Agents -> Endpoint -> OCID 

# Editar 
cd $HOME/Agente/UI/ 
vi config_agente.py 

![Image Page 19-1](./Images/page19_img1.png)

![Image Page 19-2](./Images/page19_img2.png)

# Page 20

Conﬁdential – Oracle Internal 
# Correr la aplicación y probar que el bot funciona 
Nota: Antes de ejecutar la app garantizarse que la creación del Agent y Knowledge base 
hayan ﬁnalizado y que se completara el proceso de carga de la base de datos de 
conocimiento (el Ingestion job debe de estar Completado). 
 
# Prueba Inicial 
cd $HOME/Agente/UI/ 
streamlit run app.py  
 
Abrir dirección Externa, se debería de ver así (inicia con un proceso de instalación tener 
paciencia) 

![Image Page 20-1](./Images/page20_img1.png)

![Image Page 20-2](./Images/page20_img2.png)

![Image Page 20-3](./Images/page20_img3.png)

# Page 21

Conﬁdential – Oracle Internal 
 
# Una vez que el Bot sea probado lo podemos correr y que se mantenga corriendo, aunque 
se termine la sesión, se deja un archivo de log que puede ser consultado después 
cd $HOME/Agente/UI/ 
nohup streamlit run app.py > streamlit.log 2>&1 & 
# En caso de necesitar matar el proceso 
cd $HOME/Agente/UI/ 
pkill -f "streamlit run app.py"    
rm streamlit.log  

# Page 22

Conﬁdential – Oracle Internal 
XI. Conﬁguración del Sitio Web 
La idea principal es poder embeber nuestro asistente digital en una copia local de la 
página principal de nuestro cliente, recordemos que en pasos anteriores habíamos 
realizado una copia en $HOME 
# Modiﬁcación del index.html 
Se debe de modiﬁcar el index.html 
cd $HOME 
vi index.html 
Agregar este código justo antes de cerrar el body, pero antes modiﬁcar lo que está en 
amarillo por la dirección publica de su máquina virtual. 
<!-- Estilos para el botón flotante y el panel --> 
  <style> 
    :root { 
        --asistente-scale: 0.9;  /* Escala general del botón y panel (ajústala libremente) */ 
    } 
 
    /* Contenedor del panel flotante (iframe) */ 
    #asistente-container { 
        display: none; 
        position: fixed; 
        right: calc(28px * var(--asistente-scale)); 
        bottom: calc(95px * var(--asistente-scale)); /* 🔹 Se coloca justo encima del botón */ 
        width: calc(450px * var(--asistente-scale)); /* ← ancho del iframe */ 
        height: calc(650px * var(--asistente-scale));  /* ← alto del iframe*/ 
        background: #fff; 
        border: 1px solid #ccc; 
        border-radius: 16px; 
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.25); 
        z-index: 2147483646; 
        overflow: hidden; 
    } 
 
    #asistente-iframe { 
        width: 100%; 
        height: 100%; 
        border: none; 
    } 
 
    /* Botón flotante */ 
    #asistente-launcher { 
        position: fixed; 

![Image Page 22-1](./Images/page22_img1.png)

# Page 23

Conﬁdential – Oracle Internal 
        bottom: calc(28px * var(--asistente-scale)); 
        right: calc(28px * var(--asistente-scale)); 
        z-index: 2147483647; 
        background: linear-gradient(145deg, #0055B8 0%, #0072E3 100%); 
        color: #fff; 
        font-weight: 700; 
        font-size: calc(18px * var(--asistente-scale)); 
        padding: calc(18px * var(--asistente-scale)) calc(30px * var(--asistente-scale)); 
        border: none; 
        border-radius: calc(50px * var(--asistente-scale)); 
        cursor: pointer; 
        box-shadow: 0 6px 20px rgba(0, 85, 184, 0.35); 
        transition: all 0.25s ease; 
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial; 
    } 
 
    #asistente-launcher:hover { 
        transform: scale(1.06); 
        box-shadow: 0 10px 25px rgba(0, 85, 184, 0.45); 
        background: linear-gradient(145deg, #0072E3 0%, #0093FF 100%); 
    } 
  </style> 
  <!-- Contenedor del iframe oculto --> 
  <div id="asistente-container"> 
    <iframe id="asistente-iframe" src=""></iframe> 
  </div> 
 
  <!-- Botón flotante (emoji correcto en UTF-8; alternativa con entity: &#129302;) --> 
  <button id="asistente-launcher" onclick="toggleAsistente()">🤖 Asistente Digital</button> 
  <!-- Lógica para mostrar/ocultar el iframe --> 
  <script> 
    function toggleAsistente() { 
      const container = document.getElementById("asistente-container"); 
      const iframe = document.getElementById("asistente-iframe"); 
      const visible = container.style.display !== "none" && container.style.display !== ""; 
      if (!visible) { 
        // Cambia la URL a tu destino (Open WebUI o tu runner embebido) 
        iframe.src = "http://localhost:8501"; 
        container.style.display = "block"; 
      } else { 
        container.style.display = "none"; 
        iframe.src = ""; // libera recursos 
      } 
    } 
  </script> 

![Image Page 23-1](./Images/page23_img1.png)

# Page 24

Conﬁdential – Oracle Internal 
# Habilitation de Networking 
sudo firewall-cmd --permanent --add-port=8080/tcp 
sudo firewall-cmd --permanent --add-service=http 
sudo firewall-cmd --reload 

# Page 25

Conﬁdential – Oracle Internal 
# Instalación de webserver nginx 
sudo dnf install -y nginx 
sudo systemctl enable --now nginx 
sudo mkdir -p /etc/nginx/conf.d 
# Copiar este comando como un solo bloque 
sudo tee /etc/nginx/conf.d/misitio.conf > /dev/null <<'NGINX' 
server { 
    listen 80; 
    server_name _; 
 
    root /var/www/misitio; 
    index index.html; 
 
    location / { 
        try_files $uri $uri/ =404; 
    } 
 
    # Proxy a Streamlit en /app/ 
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

# Page 26

Conﬁdential – Oracle Internal 
# Continuar con la conﬁguración 
sudo mkdir -p /var/www/misitio 
sudo cp index.html /var/www/misitio/index.html 
sudo semanage fcontext -a -t httpd_sys_content_t '/var/www/misitio(/.*)?' || true 
sudo restorecon -Rv /var/www/misitio 
sudo nginx -t 
sudo systemctl restart nginx 
sudo systemctl status nginx 
 
Probar con la IP publica: 
http://64.181.201.189 

![Image Page 26-1](./Images/page26_img1.png)
