# Delicias ChocolaterIA - Documentación

# Seccion 'Core'

## Templates

### home.html

#### Descripción
El template `home.html` es la página principal de bienvenida del sitio web de Delicias ChocolaterIA. Presenta una tarjeta central que muestra el logotipo de la empresa con un efecto interactivo que, al pasar el cursor, revela el nombre y una breve descripción del negocio.

### base.html

#### Descripción
El template base.html es el layout base para la aplicación Django. Define la estructura general del sitio web, incluyendo la barra de navegación y el pie de página. Otros templates extienden este archivo para mantener la coherencia en el diseño de la aplicación.

## LOGIN
El flujo sería así:

1. El usuario intenta acceder a una URL que requiere autenticación (como /productos/).
2. Django detecta que el usuario no está autenticado y lo redirige a /accounts/login/.
3. Django utiliza la vista LoginView para procesar la solicitud de inicio de sesion.
4. La vista LoginView utiliza el archivo 'login.html' para mostrar el formulario de inicio de sesión.
5. Cuando el usuario envía el formulario (nombre de usuario y contraseña) y la autenticación es correcta, Django lo redirige a la página de inicio (o la página que el usuario estaba intentando acceder originalmente).

## Restricción de Acceso a Vistas por Tipos de Usuarios
*Para controlar qué partes del sistema pueden acceder los usuarios administradores y empleados, hemos implementado una serie de decoradores y funciones de utilidad en el archivo utils.py. El objetivo es permitir a los administradores el acceso completo al sistema, mientras que los empleados tienen acceso restringido.*

# Seccion 'Productos'
*La sección “Productos” de la aplicación Django Delicias ChocolaterIA permite a los usuarios visualizar, buscar y agregar productos al sistema. Esto incluye mostrar una lista de productos, una barra de búsqueda para filtrar productos y un formulario para agregar nuevos productos con detalles e imágenes.*

## Modelos
### Producto
*El modelo Producto almacena detalles del producto como:*

- nombre : El nombre del producto.
- codigo : Un código único para el producto.
- precio : El precio del producto.
- descripcion : Una descripción del producto.

### ProductoImagen
*El modelo ProductoImagen almacena imágenes relacionadas con un producto:*

- producto : Una clave externa que vincula la imagen a un producto específico.
- imagen : El archivo de imagen.

## Formulario
### ProductoForm
*Gestiona tanto la entrada de datos como la validación necesaria antes de la creación del producto.*

- **Clase**: ProductoForm
- **Campos**: 
  - nombre: Campo de texto para el nombre del producto (debe ser único).
  - codigo: Campo de texto para el código del producto (debe ser único).
  - precio: Campo numérico para el precio del producto.
  - descripcion: Campo de texto para la descripción del producto.
- **Validación personalizada**:
  - La clase incluye un método clean que valida la presencia de al menos una imagen subida a través de request.FILES.
  - Si no se suben imágenes, se genera un error que impide la validación del formulario.
  - Verifica que no existan duplicados de nombre o codigo antes de permitir la creación del producto.

## Vistas
### productos
*maneja la visualización de la lista de productos.*

- **Función** :productos
- **Propósito** : Mostrar una lista de todos los productos.
- **Parámetros** :
    - request:El objeto de solicitud HTTP.
- **Return** : Representa la productos.htmlplantilla con el contexto que contiene la lista de productos.

### agg_productos
*maneja el formulario para agregar nuevos productos.*

- **Función** :agg_productos
- **Propósito** : Gestionar la creación de un nuevo producto y sus imágenes, asegurando la validación de los datos antes de guardarlos en la base de datos.
- **Parámetros** :
    - request:El objeto de solicitud HTTP.
- **Comportamiento**  :
    - Si el método de solicitud es POST, la vista procesa los datos del formulario enviados, incluyendo la validación de la existencia de imágenes y la verificación de duplicados de nombre o código.
    - Si el formulario es válido y no hay errores de duplicados o falta de imágenes:
      - Se guarda el nuevo producto en la base de datos.
      - Se guardan las imágenes asociadas al producto.
      - Se muestra un mensaje de éxito ("Producto agregado exitosamente") y se redirige al usuario al listado de productos.
    - Si el formulario no es válido o si hay duplicados de nombre o código:
      - Se muestran mensajes de error específicos, indicando si el nombre o código ya están en uso, si faltan imágenes o si hay otros errores en el formulario.
    - Si el método de solicitud no es POST, la vista muestra un formulario vacío para crear un nuevo producto.
- **Devuelve**  : Renderiza la plantilla agg_productos.html con el contexto del formulario y los posibles mensajes de error.

### detalle_producto

*La vista `detalle_producto` maneja la visualización de los detalles del producto.*

- **Función**: `detalle_producto`
- **Finalidad**: Mostrar los detalles de un producto específico.
- **Parámetros**: 
  - request`: el objeto de solicitud HTTP.
  - `pk`: La clave principal del producto que se mostrará.
- **Devoluciones**: Renderiza la plantilla `detalle_producto.html` con el contexto que contiene los detalles del producto.

### editar_producto

*La vista `editar_producto` maneja el formulario para editar un producto existente.*

- **Función**: `editar_producto`
- **Propósito**: Manejar la edición de un producto existente y actualizar la base de datos.
- **Parámetros**: 
  - `request`: el objeto de solicitud HTTP.
  - `pk`: La clave principal del producto a editar.
- **Comportamiento**:
  - Si el método de solicitud es "POST", la vista procesa los datos del formulario enviado y actualiza el producto.
  - Si el formulario es válido, se actualiza el producto y se redirige al usuario a la vista de detalle del producto.
  - Si el método de solicitud no es "POST", la vista muestra el formulario precargado con los detalles del producto.
- **Devoluciones**: Renderiza la plantilla `editar_producto.html` con el contexto del formulario.

### eliminar_producto

*La vista `eliminar_producto` maneja la confirmación y eliminación de un producto.*

- **Función**: `eliminar_producto`
- **Propósito**: Mostrar una página de confirmación para eliminar un producto y gestionar la eliminación.
- **Parámetros**: 
  - `request`: el objeto de solicitud HTTP.
  - `pk`: La clave principal del producto que se va a eliminar.
- **Comportamiento**:
  - Si el método de solicitud es `POST`, la vista elimina el producto y redirige a la lista de productos.
  - Si el método de solicitud no es "POST", la vista muestra una página de confirmación para eliminar el producto.
- **Devoluciones**: 
  - Para solicitudes GET: Renderiza la plantilla `eliminar_producto.html` con el contexto que contiene los detalles del producto.
  - Para solicitudes POST: Elimina el producto y redirige a la lista de productos.

## Plantillas
### productos.html
- **Propósito** : Muestra una lista de productos con una barra de búsqueda y un botón "Agregar Producto".
- **Características** :
    - Encabezado con el título de la página y botón “Agregar Producto”.
    - Barra de búsqueda para filtrar productos.
    - Tabla que enumera todos los productos con columnas para imagen, nombre, código y precio.

### agg_productos.html
- **Propósito** : Muestra un formulario para agregar un nuevo producto.
- **Características** :
    - Campos de formulario para nombre de producto, código, precio, descripción e imágenes.
    - Botón “Guardar Producto” para enviar el formulario.

### detalle_producto.html

- **Propósito**: Muestra información detallada sobre el producto, incluidas imágenes, y proporciona botones para editar o eliminar el producto.
- **Características**:
  - Visualización del nombre del producto, código, precio y descripción.
  - Visualización de imágenes asociadas.
  - Botones para editar y eliminar el producto.

### editar_producto.html

- **Propósito**: Muestra un formulario precargado con la información del producto, lo que permite al usuario editar y guardar cambios.
- **Características**:
  - Campos de formulario precargados con detalles del producto.
  - Botón "Guardar Cambios" para enviar el formulario.

### eliminar_producto.html

- **Propósito**: Confirma la intención del usuario de eliminar el producto y brinda opciones para cancelar o continuar con la eliminación.
- **Características**:
  - Mensaje de confirmación preguntando si el usuario está seguro de eliminar el producto.
  - Botón "Eliminar" para confirmar la eliminación.
  - Botón "Cancelar" para cancelar la eliminación y volver a los detalles del producto.

# Seccion 'Empleados'

La funcionalidad de creación de empleados permite que los administradores puedan registrar nuevos usuarios empleados en el sistema. Los empleados se añaden al grupo "Empleados", lo que les otorga permisos específicos que pueden ser gestionados a través del sistema de grupos y permisos de Django.

## Vistas

### crear_empleado()

- **Propósito**: Permitir a los administradores agregar nuevos empleados al sistema.
- **Características**:
  - Carga un formulario para registrar un nuevo empleado.
  - Verifica que los datos sean válidos antes de guardar al nuevo empleado.
  - Asigna automáticamente el nuevo empleado al grupo correspondiente en la base de datos.
  - Muestra mensajes de éxito o error en función del resultado de la operación.

### lista_empleados()

- **Propósito**: Listar todos los empleados registrados en el sistema para los administradores.
- **Características**:
  - Muestra una tabla con el nombre de usuario de cada empleado.
  - Incluye opciones para editar o eliminar cada empleado.
  - Permite a los administradores agregar nuevos empleados a través de un botón visible en la interfaz.

### editar_empleado()

- **Propósito**: Permitir a los administradores actualizar la información de un empleado existente.
- **Características**:
  - Carga un formulario pre-llenado con los datos actuales del empleado.
  - Actualiza la información del empleado si los datos nuevos son válidos.
  - Redirige a la lista de empleados después de una edición exitosa.
  - Gestiona la validación para evitar errores comunes como duplicados de nombres.

### eliminar_empleado()

- **Propósito**: Facilitar la eliminación de un empleado del sistema.
- **Características**:
  - Muestra una confirmación antes de realizar la eliminación.
  - Elimina el empleado de la base de datos si se confirma la acción.
  - Redirige a la lista de empleados después de eliminar.

## Plantillas

### crear_empleado.html

- **Propósito**: Mostrar un formulario para que los administradores puedan crear nuevos empleados.
- **Características**:
  - Contiene campos de entrada para el nombre de usuario, contraseña y otros detalles necesarios.
  - Incluye un botón Guardar para enviar el formulario.
  - Muestra mensajes de éxito o error según el resultado de la operación.
  - Permite regresar a la lista de empleados a través de un enlace destacado.
  - Diseño adaptado para ser visualmente limpio y funcional, facilitando la creación de nuevos empleados sin complicaciones.

### lista_empleados.html

- **Propósito**: Mostrar una lista de todos los empleados registrados en el sistema.
- **Características**:
  - Presenta una tabla con los nombres de usuario de cada empleado y acciones para editar o eliminar.
  - Incluye un botón Agregar Empleado en la parte superior que redirige al formulario para crear un nuevo empleado.

### editar_empleado.html

- **Propósito**: Mostrar un formulario para que los administradores puedan actualizar la información de un empleado existente.
- **Características**:
  - Similar al formulario de creación, pero pre-llenado con los datos actuales del empleado.
  - Permite a los administradores cambiar el nombre de usuario, contraseña y otros detalles del empleado.
  - Incluye botones para Guardar los cambios o Cancelar y regresar a la lista de empleados.
  - Muestra mensajes de éxito o error en función del resultado de la operación.

### eliminar_empleado.html

- **Propósito**: Mostrar una confirmación para que los administradores puedan decidir si realmente quieren eliminar un empleado del sistema.
- **Características**:
  - Muestra el nombre de usuario del empleado que se va a eliminar, asegurando que el administrador sepa cuál es el usuario afectado.
  - Incluye un botón Confirmar para proceder con la eliminación, y un botón Cancelar para regresar sin realizar ninguna acción.

## Formularios

### EmpleadoForm

- **Propósito**: Gestionar la creación y edición de cuentas de empleados en el sistema de Django utilizando el modelo de usuario estándar (User) de Django.
- **Características**:
  Campos:
    - username (Nombre de usuario): Campo obligatorio que identifica al empleado en el sistema. Debe ser único.
    - first_name (Nombre): Campo opcional para el nombre del empleado.
    - last_name (Apellido): Campo opcional para el apellido del empleado.
    - email: Campo opcional para el correo electrónico del empleado.
    - password: Campo obligatorio para establecer la contraseña del empleado. Se utiliza un widget especial (PasswordInput) para ocultar la entrada de texto.
