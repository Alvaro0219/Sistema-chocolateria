# Delicias ChocolaterIA - Documentación

# Seccion 'Core'

## Templates

### 1. 'core/home.html'

#### Descripción
El template `home.html` es la página principal de bienvenida del sitio web de Delicias ChocolaterIA. Presenta una tarjeta central que muestra el logotipo de la empresa con un efecto interactivo que, al pasar el cursor, revela el nombre y una breve descripción del negocio.

### 2.'core/base.html'

#### Descripción
El template base.html es el layout base para la aplicación Django. Define la estructura general del sitio web, incluyendo la barra de navegación y el pie de página. Otros templates extienden este archivo para mantener la coherencia en el diseño de la aplicación.

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
ProductoForm se encarga de la entrada para agregar nuevos productos. Incluye campos para los detalles del producto, pero gestiona las cargas de imágenes por separado en la vista.

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
- **Propósito** : Gestionar la creación de un nuevo producto y guardarlo en la base de datos junto con sus imágenes.
- **Parámetros** :
    - request:El objeto de solicitud HTTP.
- **Comportamiento**  :
    - Si el método de solicitud es POST, la vista procesa los datos del formulario enviado, guarda el producto y carga las imágenes.
    - Si el formulario es válido, se guarda el producto y sus imágenes y se redirige al usuario al listado de productos.
    - Si el método de solicitud no es POST, la vista muestra un formulario vacío para crear un nuevo producto.
- **Devuelve**  : Representa la agg_productos.html plantilla con el contexto del formulario.

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