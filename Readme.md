# Sistema de Gestión de Chocolatería

## Descripción del Proyecto

Este proyecto es un sistema de gestión para una chocolatería que incluye módulos para la gestión de productos, reconocimiento de imágenes, gestión de pedidos, facturación y generación de estadísticas.

## Módulos del Sistema

### 1. Módulo de Gestión de Productos

#### Funcionalidades:

- **Crear Productos:**
  - **Inputs:** Nombre, descripción, precio unitario, imagen del producto.
  - **Proceso:** Almacenar la información en la base de datos.
  - **Outputs:** Confirmación de creación del producto.

- **Listas de Precios:**
  - **Inputs:** Lista de productos con precios.
  - **Proceso:** Actualizar la base de datos con los nuevos precios.
  - **Outputs:** Confirmación de actualización.

### 2. Módulo de Reconocimiento de Imágenes

#### Funcionalidades:

- **Almacenar Imágenes:**
  - **Inputs:** Imagen del producto.
  - **Proceso:** Asociar la imagen con el producto correspondiente en la base de datos.
  - **Outputs:** Confirmación de almacenamiento.

- **Reconocimiento de Productos:**
  - **Inputs:** Foto de la bandeja.
  - **Proceso:**
    - Utilizar modelos de visión por computadora (OpenCV, TensorFlow) para identificar productos.
    - Generar una lista de productos reconocidos con sus cantidades.
  - **Outputs:** Lista de productos y cantidades.

### 3. Módulo de Gestión de Pedidos

#### Funcionalidades:

- **Carga de Detalle de Pedidos:**
  - **Inputs:** Foto de la bandeja.
  - **Proceso:**
    - Reconocer productos en la imagen.
    - Permitir corrección manual por parte del empleado.
    - Calcular el total del pedido.
  - **Outputs:** Detalle del pedido y total a facturar.

- **Ingreso Manual:**
  - **Inputs:** Producto y cantidad.
  - **Proceso:** Actualizar el pedido con los datos ingresados manualmente.
  - **Outputs:** Confirmación de ingreso.

### 4. Módulo de Facturación

#### Funcionalidades:

- **Generar Código QR:**
  - **Inputs:** Detalle del pedido.
  - **Proceso:** Codificar la información del pedido en un QR.
  - **Outputs:** Código QR.

- **Emitir Comprobante:**
  - **Inputs:** Código QR.
  - **Proceso:** Leer el QR desde el sistema de facturación y generar el comprobante.
  - **Outputs:** Comprobante de pago.

### 5. Módulo de Estadísticas

#### Funcionalidades:

- **Estadísticas de Productos:**
  - **Inputs:** Datos de pedidos anteriores.
  - **Proceso:** Analizar y generar reportes estadísticos.
  - **Outputs:** Reportes sobre productos más vendidos, tendencias, etc.

## Tecnologías y Herramientas Sugeridas

- **Base de Datos:** MySQL o PostgreSQL para almacenar datos de productos, pedidos y estadísticas.
- **Backend:** Django (Python) para manejar la lógica del negocio y servir como API para el frontend.
- **Frontend:** HTML, CSS, JS en el mismo Django.
- **Visión por Computadora:** OpenCV y TensorFlow para el reconocimiento de productos en las imágenes.
- **Generación de QR:** Librerías como qrcode en Python para generar códigos QR.
- **Almacenamiento de Imágenes:** Amazon S3 para almacenamiento en la nube, o un sistema local si el volumen de imágenes es manejable.

## Flujo de Trabajo

1. **Creación y Gestión de Productos:**
   - El administrador puede agregar, actualizar y eliminar productos.
   - Las imágenes de los productos se almacenan y asocian con los datos correspondientes.

2. **Proceso de Pedido:**
   - El empleado toma una foto de la bandeja de chocolates.
   - El sistema procesa la imagen y reconoce los productos utilizando modelos entrenados de visión por computadora.
   - El empleado verifica y corrige, si es necesario, los productos reconocidos.
   - Se genera el detalle del pedido y se calcula el total.
   - Un código QR se genera con la información del pedido.

3. **Facturación:**
   - El sistema de facturación actual lee el código QR y genera el comprobante de pago.

4. **Generación de Estadísticas:**
   - El sistema analiza los datos de pedidos y genera reportes sobre las tendencias y productos más vendidos.
