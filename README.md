Enrique Gómez Fernández y Daniel Birsan
G2321 - PSI-10

---

Se pone a su disposicion un .env para exportar todo lo necesario para desplegar localmente, dentro de mychess/.
El superusuario es creado al ejecutar 'python3.11 manage.py superuser --noinput' y se crea el user: alumnodb , password: alumnodb (si se ha exportado el .env)
Si lo prefiere, puede ejecutar 'sh build.sh' para crear el superusuario y desplegar la aplicación localmente.

---

- API desplegada en: https://mychess-dbmi.onrender.com
- App Vue desplegada en: https://mychess-vue-zq5z.onrender.com

La aplicación usa una BBDD en neon-tech si se despliega desde render, de lo contrario, usará la default con Django, al igual que se hizo en las entregas anteriores.

- BBDD neon: https://console.neon.tech/app/projects/little-hall-03076215
