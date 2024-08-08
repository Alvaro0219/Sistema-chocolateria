# ChocoProject

## Prerrequisitos

- Tener instalado Git.
- Tener instalado Python (preferentemente la versión 3.7 o superior).
- Tener instalado pip (viene con Python 3.4+).

## Instrucciones de Instalación

### 1. Clonar el Repositorio

- Abre una terminal o línea de comandos.

- Navega al directorio donde quieres clonar el repositorio.

- Clona el repositorio usando el siguiente comando:
    ```bash
    git clone https://github.com/Alvaro0219/Sistema-chocolateria.git

- Navega al directorio del proyecto:
    ```bash
    cd Sistema-chocolateria

### 2. Crear y Activar un Entorno Virtual

- Crear y Activar un Entorno Virtual:
    ```bash
    python -m venv venv
    venv/Scripts/activate

### 3. Instalar las Dependencias
- Instalar dependencias:
    ```bash
    pip install -r requirements.txt

### 4. Probar el Proyecto Django
- Asegúrate de estar en el directorio del proyecto y de que el entorno virtual esté activo.
    ```bash
    python manage.py migrate
    python manage.py runserver

# Normas de Contribución

## Estándar de Código

Para asegurar consistencia y calidad en el código, seguimos las convenciones de PEP 8 para Python. A continuación, se detallan las principales reglas y prácticas recomendadas.

### Nomenclatura

- **Variables y funciones:** Usar snake_case
  ```python
  variable_name = 42
  def function_name():
    pass

- **Clases:** Usar CamelCase
    ```python
    class MyClass:
        pass

- **Constantes:**  Usar UPPER_SNAKE_CASE
    ```python
    MAX_VALUE = 100

## Contribuir al Proyecto

1. Clonar el Repositorio:
    ```bash
    git clone https://github.com/Alvaro0219/Sistema-chocolateria.git
    cd Sistema-chocolateria

2. Crear una Rama:
    ```bash
    git checkout -b feature/nueva-funcionalidad

3. Hacer Commit de tus Cambios:
    ```bash
    git add .
    git commit -m "Descripción de los cambios"

4. Enviar tus Cambios:
    ```bash
    git push origin feature/nueva-funcionalidad

5. Crear un Pull Request:
- Ir a la página del repositorio en GitHub.
- Crear un nuevo Pull Request desde tu rama.

# Codigo

## Flujo django
1. Crear app para el modulo
2. Instalar app en settings.py
2. Crear vistas en app/views.py
3. Crear archivo urls.py en app
4. Crear urls (path)
5. Agregar path de url al 'urls.py' del proyecto

## Enrutamiento entre apps
1. Definir Vistas: Crear funciones o clases en views.py que manejen solicitudes.
    ```bash
    def my_view(request):
        return render(request, 'myapp/my_template.html')
2. Configurar URLs en Aplicaciones: Definir patrones de URL en urls.py de cada aplicación.
    ```bash
    urlpatterns = [
    path('', my_view, name='my_view'),
    ]
3. Incluir URLs en el Proyecto Principal: Usar include() en el urls.py del proyecto principal para incluir las rutas de las aplicaciones.
    ```bash
    urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
    ]
4. Usar URLs Dinámicas en Templates: Utilizar {% url 'name' %} en los templates para crear enlaces dinámicos.
    ```bash
    <a href="{% url 'my_view' %}">Go to My View</a>
