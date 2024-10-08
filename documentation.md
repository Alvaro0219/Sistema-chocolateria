# Delicias ChocolaterIA - Documentación

# Seccion 'Core'

## Templates

### 1. 'core/home.html'

#### Descripción
El template `home.html` es la página principal de bienvenida del sitio web de Delicias ChocolaterIA. Presenta una tarjeta central que muestra el logotipo de la empresa con un efecto interactivo que, al pasar el cursor, revela el nombre y una breve descripción del negocio.

### 2.'core/base.html'

#### Descripción
El template base.html es el layout base para la aplicación Django. Define la estructura general del sitio web, incluyendo la barra de navegación y el pie de página. Otros templates extienden este archivo para mantener la coherencia en el diseño de la aplicación.

## LOGIN
El flujo sería así:

1. El usuario intenta acceder a una URL que requiere autenticación (como /productos/).
2. Django detecta que el usuario no está autenticado y lo redirige a /accounts/login/.
3. Django utiliza la vista LoginView para procesar la solicitud.
4. La vista LoginView utiliza el archivo 'login.html' para mostrar el formulario de inicio de sesión.
5. Cuando el usuario envía el formulario (nombre de usuario y contraseña) y la autenticación es correcta, Django lo redirige a la página de inicio (o la página que el usuario estaba intentando acceder originalmente).

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