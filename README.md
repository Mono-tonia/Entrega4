# Diseño y Construcción de Soluciones No Monolíticas
# Entrega 4 - Prueba de Concepto

En este repositorio se puede ver el proyecto que construimos para Entregas de Los Alpes, con el objetivo de cumplir con tres escenarios de calidad relacionados a tres atributos de calidad distintos.
- Disponibilidad
- Escalabilidad
- Modificabilidad

Para ello, implementamos una solución basada en microservicios usando el patrón Event Sourcing, teniendo en cuenta el uso de seedworks con el objetivo de facilitar la modificabilidad del código con respecto a cambios en el futuro. Adicionalmente, utilizamos MySQL para tener una base de datos escalable.

## Estructura del proyecto

El repositorio está construido a patir de 3 microservicios principales, distribuidos dentro de tres módulos distintos.
### Productos:
- El archivo **src/entregasDeLosAlpes/modulos/productos/dominio/entidades.py** describe el microservicio relacionado con el manejo de las **Ordenes** dentro de Entregas de los Alpes.
### Bodegas:
- El archivo **src/entregasDeLosAlpes/modulos/bodegas/dominio/entidades.py** describe el microservicio relacionado con la distribución del inventario para el **Almacenamiento** dentro de Entregas de los Alpes.
### Vehículos:
- El archivo **src/entregasDeLosAlpes/modulos/vehiculos/dominio/entidades.py** describe el microservicio correspondiente al **Transporte** de productos dentro de Entregas de los Alpes.
### Especificaciones:
- El archivo **src/entregasDeLosAlpes/modulos/vuelos/infraestructura/proyecciones.py** ahora incluye una unidad de trabajo para Pulsar, esta nos va ayudar a mantener la consistencia transaccional en el servicio usando Apache Pulsar como nuestro Event Store.
- El archivo **src/entregasDeLosAlpes/modulos/vuelos/infraestructura/proyecciones.py** cuenta con las diferentes formas en que podemos hacer proyección de nuestros datos. Una de las proyecciones tiene propósitos analíticos y la otra transaccionales.
- El archivo **src/entregasDeLosAlpes/modulos/vuelos/infraestructura/vistas.py** cuenta con el modelo de vistas que podemos exponer a nuestro clientes. Como se puede observar, este es un modelo bastante genérico definido en el seedwork (pero usted puede hacerlo mucho más complejo).
- Los archivos **src/entregasDeLosAlpes/seedwork/infraestructura/proyecciones.py** y **src/aeroalpes/seedwork/infraestructura/vistas.py** proveen las interfaces y definiciones genéricas para las proyecciones, handlers y vistas.

## EntregasDeLosAlpes
### Ejecutar Base de datos
Desde el directorio principal ejecute el siguiente comando.

```bash
docker-compose --profile db up
docker-compose --profile pulsar up
```

Este comando descarga las imágenes e instala las dependencias de la base datos.

### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/entregasDeLosAlpes/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/entregasDeLosAlpes/api --debug run
```

### Ejecutar pruebas

```bash
coverage run -m pytest
```

### Ver reporte de covertura
```bash
coverage report
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f entregas_de_los_alpes.Dockerfile -t entregasDeLosAlpes/flask
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 entregasDeLosAlpes/flask
```

## Sidecar/Adaptador
### Instalar librerías

En el mundo real es probable que ambos proyectos estén en repositorios separados, pero por motivos pedagógicos y de simpleza, 
estamos dejando ambos proyectos en un mismo repositorio. Sin embargo, usted puede encontrar un archivo `sidecar-requirements.txt`, 
el cual puede usar para instalar las dependencias de Python para el servidor y cliente gRPC.

```bash
pip install -r sidecar-requirements.txt
```

### Ejecutar Servidor

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/main.py 
```

### Ejecutar Cliente

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/cliente.py 
```

### Compilación gRPC

Desde el directorio `src/sidecar` ejecute el siguiente comando.

```bash
python -m grpc_tools.protoc -Iprotos --python_out=./pb2py --pyi_out=./pb2py --grpc_python_out=./pb2py protos/vuelos.proto
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f adaptador.Dockerfile -t entregasDeLosAlpes/adaptador
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 50051:50051 aeroalpes/adaptador
```

## Microservicio Notificaciones
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/notificaciones/main.py
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f notificacion.Dockerfile -t entregasDeLosAlpes/notificacion
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run aeroalpes/notificacion
```

## UI Websocket Server
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/ui/main.py
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f ui.Dockerfile -t aeroalpes/ui
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run aeroalpes/ui
```

## CDC & Debezium

**Nota**: Antes de poder ejectuar todos los siguientes comandos DEBE tener la base de datos MySQL corriendo.

### Descargar conector de Debezium

```
wget https://archive.apache.org/dist/pulsar/pulsar-2.10.1/connectors/pulsar-io-debezium-mysql-2.10.1.nar
```

### Ejecutar Debezium
Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:
```bash
./bin/pulsar-admin source localrun --source-config-file /pulsar/connectors/debezium-mysql-source-config.yaml --destination-topic-name debezium-mysql-topic
```

### Consumir eventos Debezium

Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-client consume -s "sub-datos" public/default/aeroalpesdb.reservas.usuarios_legado -n 0
```

### Consultar tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin topics list public/default
```

### Cambiar retención de tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```
Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1
```

Para poder ver que los cambios fueron efectivos ejecute el siguiente comando:

```bash
./bin/pulsar-admin namespaces get-retention public/default
```

**Nota**: Esto nos dejará con una retención infinita. Sin embargo, usted puede cambiar la propiedad de `size` para poder usar [Tiered Storage](https://pulsar.apache.org/docs/2.11.x/concepts-tiered-storage/)

### Instrucciones oficiales

Para seguir la guía oficial de instalación y uso de Debezium en Apache Pulsar puede usar el siguiente [link](https://pulsar.apache.org/docs/2.10.x/io-cdc-debezium/)


## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

## Comandos útiles

### Listar contenedoras en ejecución
```bash
docker ps
```

### Listar todas las contenedoras
```bash
docker ps -a
```

### Parar contenedora
```bash
docker stop <id_contenedora>
```

### Eliminar contenedora
```bash
docker rm <id_contenedora>
```

### Listar imágenes
```bash
docker images
```

### Eliminar imágenes
```bash
docker images rm <id_imagen>
```

### Acceder a una contendora
```bash
docker exec -it <id_contenedora> sh
```

### Kill proceso que esta usando un puerto
```bash
fuser -k <puerto>/tcp
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|aeroalpes|ui|notificacion> up
```
