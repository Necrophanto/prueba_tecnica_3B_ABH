# Prueba técnica para 3B

Este es un breve documento para explicar la prueba técnica

### Instalar paquetes
Antes de intentar ejecutar el proyecto, asegúrese de instalar las dependencias con el comando `pip install -r requirements.txt`, para ello cerciórese de estar en el path raíz de la aplicación y después ejecute dicho comando.

### Endpoints & Documentación
Se realizaron los endpoints acorde a las instrucciones y se anexa la documentacion de los mismos en la colección de Postman anexa al proyecto, intenté agregar el swagger de DRF, pero me obligaba a retrabajar parte de la lógica para integrar los serrializadores que completaran el swagger con los bodies de petición, por lo que el swagger de DRF está disponible, pero incompleto, bajo las URL: swagger/  y redoc/

### Pruebas
Se agregaron las pruebas en el archivo `tests.py` dentro de la app llamada `api`

### Job para alertar de bajo stock
Como menciono en el archivo de `models.py`, preferí hacer un ajuste sobre la función `save()`, y aquí replico lo que expliqué en ese archivo:
```
Aunque se pide generar un job para hacer esta alerta, me pareció más 
directo modificar la función save para que dispare el logger en lugar de 
poner a correr un job, incluso se podría agregar un mensajero para mandar el mismo mensaje ya sea a un correo de administrador o por SMS; incluso otra opción sería crear un cronjob en el servidor donde se monte esto y que revise cada X minutos el stock, pero eso generaría una consulta innecesaria en la BD, reduciendo su desempeño.
```
Básicamente siendo Django sería más eficiente liberar una consulta SQL innecesaria cada determinado tiempo.

### Encapsulación en contenedor Docker
Debido a la premura con la que estoy realizando la prueba, preferí no encapsular el proyecto en una imagen Docker, ya que siendo opcional no lo ví escencial, sin embargo debo comentar que en caso de haberlo hecho agregaría el archivo de variables tanto para el proyecto Django, como para las variables de entorno necesarias: DB user, password, DB IP, puerto y clave del pryecto Django, así como su user y password de la consola admin (la cual no activé)


Sin más por el momento espero sus comentarios y retroalimentación.