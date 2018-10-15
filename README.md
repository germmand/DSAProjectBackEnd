# DSAProject - Back-end

DSAProject es un proyecto para la asignatura de Desarrollo de Software Avanzado de la Universidad de Oriente.

## Requisitos para instalación:
- [x] Python 3.5.2 o superior.
- [x] Pip 8.1.1 o superior (Python 3).
- [x] PostgreSQL 10.5 o superior.
- [x] Git 2.7.4 o superior.


## Instalación.

1. **Clonar el repositorio.**
 - Desde la terminal ejecutar:
   
   `$ git clone https://github.com/germmand/DSAProjectBackEnd.git`
  
 - Moverse a la carpeta clonada:
   
   `$ cd DSAProjectBackEnd/`


2. **Crear ambiente virtual de Python.**

 - Instalar [virtualenv](https://python-guide-cn.readthedocs.io/en/latest/dev/virtualenvs.html) con el manejador de paquetes de Python.
   
   `$ pip install virtualenv`
 
 - Crear carpeta del ambiente virtual con virtualenv.
 
   `$ virtualenv venv`
 
 - Activar ambiente virtual (UNIX-like).
   
   `$ source ./venv/bin/activate`
   
 - Si se trabaja en Windows, moverse a la carpeta `./venv/bin/` desde la terminal y iniciar `activate`.


3. **Instalar las dependencias.**

 - En la carpeta raíz del proyecto ejecutar desde la terminal:
 
   `$ pip install -r requirements.txt`


4. **Configurar archivos de configuración de la aplicación.**

 - En la carpeta `./dsabackend/config/` hacer una copia de los archivos:
   * `db_config-TEMPLATE.py`
   * `jwt_config-TEMPLATE.py`

 - Remover el sufijo `-TEMPLATE` quedando de la forma:
   * `db_config.py`
   * `jwt_config.py`

 - Actualizar en `db_config.py` la propiedad `DATABASE_URI` con las respectivas credenciales de PostgreSQL.
   * Nombre de usuario.
   * Contraseña.
   * Host.
   * Puerto.
   * Nombre de la base de datos.

 - Actualizar en `jwt_config.py` la llave para los tokens de acceso y de refreso (propiedad `JWT_SECRET`) con cualquier llave de preferencia.


5. **Actualizar base de datos por migraciones y hacer _seeding_ para agregar datos de prueba.**

 - Ejecutar desde la raíz del proyecto:
   `$ python run.py db upgrade`

 - Finalmente agregamos datos de prueba con:
 
   `$ python run.py seed`


6. **Iniciar el servidor.**

 - Ejecutar:
 
   `$ python run.py runserver`.


:+1:
