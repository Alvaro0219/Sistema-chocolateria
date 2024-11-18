import cv2
import numpy as np
from productos.models import ProductoImagen
from collections import Counter

def visualizar_puntos_clave(imagen, keypoints, output_path):
    """
    Visualiza los puntos clave detectados en la imagen y los guarda.
    """
    imagen_con_kp = cv2.drawKeypoints(imagen, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite(output_path, imagen_con_kp)

def preprocesar_imagen(imagen_path):
    """
    Preprocesa la imagen para optimizar la detección de características.
    """
    imagen = cv2.imread(imagen_path)
    if imagen is None:
        raise ValueError("Error al cargar la imagen.")

    # Convertir a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Reducción de ruido
    imagen_gris = cv2.GaussianBlur(imagen_gris, (3, 3), 0)

    return imagen_gris

def reconocer_productos_por_segmento(imagen_cargada_path, visualizar=False):
    """
    Detecta productos en una imagen cargada utilizando SIFT y coincidencias globales.
    """
    sift = cv2.SIFT_create()
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    umbral_min_coincidencias = 15

    # Preprocesar la imagen cargada
    try:
        imagen_gris = preprocesar_imagen(imagen_cargada_path)
    except ValueError as e:
        print(e)
        return {}

    productos_detectados = []
    kp1, des1 = sift.detectAndCompute(imagen_gris, None)

    if des1 is None or len(kp1) < 50:
        print("Pocas características detectadas. Probablemente no sea posible detectar productos.")
        return {}

    # Guardar visualización de puntos clave
    if visualizar:
        visualizar_puntos_clave(imagen_gris, kp1, "puntos_clave_imagen_pedido.jpg")

    # Comparar con imágenes de productos
    for producto_imagen in ProductoImagen.objects.all():
        imagen_producto = cv2.imread(producto_imagen.imagen.path, cv2.IMREAD_GRAYSCALE)
        if imagen_producto is None:
            print(f"Error: No se pudo cargar la imagen del producto {producto_imagen.producto.nombre}.")
            continue

        # Detectar características de la imagen del producto
        kp2, des2 = sift.detectAndCompute(imagen_producto, None)
        if des2 is None:
            continue

        # Coincidencias con FLANN
        matches = flann.knnMatch(des1, des2, k=2)
        good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

        # Umbral de coincidencias
        if len(good_matches) > umbral_min_coincidencias:
            productos_detectados.append(producto_imagen.producto)

            # Guardar visualización de coincidencias
            if visualizar:
                imagen_matches = cv2.drawMatches(imagen_gris, kp1, imagen_producto, kp2, good_matches, None, flags=2)
                cv2.imwrite(f"coincidencias_{producto_imagen.producto.codigo}.jpg", imagen_matches)

    # Consolidar detecciones
    productos_detectados_unicos = Counter(productos_detectados)
    return productos_detectados_unicos
