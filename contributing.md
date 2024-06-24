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
    <code>git clone https://github.com/Alvaro0219/Sistema-chocolateria.git</code>

- Navega al directorio del proyecto:
    <code>cd tu_repositorio</code>

### 2. Crear y Activar un Entorno Virtual

- Crear y Activar un Entorno Virtual:

<code>python -m venv venv</code>

<code>venv\Scripts\activate</code>

### 3. Instalar las Dependencias
<code> pip install -r requirements.txt</code>

### 4. Probar el Proyecto Django
- Asegúrate de estar en el directorio del proyecto y de que el entorno virtual esté activo.

<code>python manage.py migrate</code>

<code>python manage.py runserver</code>

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