import random
from typing import Optional
import barcode
# from barcode.writer import ImageWriter
from io import BytesIO
# from PIL import Image

def generar_codigo_producto(longitud: int = 4) -> str:
    """
    Genera un código interno de producto necesario para crear el código de barras completo.
    
    Args:
        longitud: Dígitos para el código (default 4)
    
    Returns:
        Código generado (ej. '1234' o '5678')
    """
    return ''.join(random.choices('0123456789', longitud))


def code_product_format(code_product: str ='123', longitud: int = 5) -> str:
    """
    Genera un código interno de producto necesario para crear el código de barras completo rellenando con 0 a la izquierda en caso de que falten dígitos.

    Args:
        longitud: Dígitos para el código (default 5)
        code_product: Código interno del producto para su registro
    
    Returns:
        Código generado (ej. '01234' o '06789')

    """
    if len(code_product) > longitud:
        raise ValueError("El codígo interno de producto debe ser de 5 dígitos")
    elif len(code_product) == 0:
        code_product = 0
        
    try:
        code_product = int(code_product)
    except ValueError as e:
        raise ValueError("El código ingresado contiene caracteres invalidos, favor de verificar")
    except Exception as e:
        raise Exception(f"No fue porible generar el código de producto, verificar: {e}")
    return f"{code_product:05d}"  # Rellena con ceros a la izquierda
  

def generar_codigo_ean13(
    codigo_producto: str = "1234",
    clave_pais: int = 750,
    empresa_id: str = "99999",  # ID genérico para pruebas
    longitud: int = 5
) -> str:
    """
    Genera código EAN-13 a partir de código de producto.
    
    Args:
        clave_pais: Código del pais de 3 dígitos (ej. '750' para méxico )
        codigo_producto: Código interno de 4 dígitos (ej. '4927')
        empresa_id: ID GS1 de la empresa (default '99999' para pruebas)
        longitud: tamaño del código interno permitido (ej. 5)
    
    Returns:
        Código EAN-13 completo (13 dígitos)
    
    Raises:
        ValueError: Si no recibe exactamente 4 dígitos
    """
    # Validar que sean exactamente 4 dígitos
    if not (codigo_producto.isdigit() and len(codigo_producto) == longitud):
        raise ValueError(f"El código de producto debe tener exactamente {longitud} dígitos")
    
    # Estructura completa:
    # 3 dígitos país + 5 dígitos empresa + 4 dígitos producto + 1 dígito verificador
    codigo_base = f"{clave_pais}{empresa_id[:5].zfill(5)}{codigo_producto}"
    
    # Calcular dígito verificador
    suma = sum(int(codigo_base[i]) * (3 if i % 2 == 0 else 1) 
             for i in range(12))
    digito_verificador = (10 - (suma % 10)) % 10
    
    return f"{codigo_base}{digito_verificador}"




# def generar_imagen_ean13(codigo: str, guardar_path: str = None) -> BytesIO:
#     """
#     Genera imagen de código de barras EAN-13 con especificaciones comerciales.
    
#     Args:
#         codigo: Código EAN-13 válido (13 dígitos)
#         guardar_path: Opcional - path para guardar la imagen
    
#     Returns:
#         BytesIO con la imagen PNG (300dpi, tamaño estándar)
#     """
#     # Validación estricta
#     if len(codigo) != 13 or not codigo.isdigit():
#         raise ValueError("Código EAN-13 debe tener 13 dígitos numéricos")
    
#     # Configuración profesional para impresión
#     writer_options = {
#         'module_width': 0.33,  # mm (estándar GS1)
#         'module_height': 25.93, # mm
#         'font_size': 12,
#         'text_distance': 5.0,
#         'quiet_zone': 7.5,      # Zona silenciosa mínima
#         'background': 'white',
#         'foreground': 'black',
#         'write_text': True,     # Mostrar números
#         'dpi': 300             # Resolución para impresión
#     }
    
#     # Generar código
#     ean = barcode.get('ean13', codigo, writer=ImageWriter())
    
#     # Guardar opcional
#     if guardar_path:
#         full_path = ean.save(guardar_path, options=writer_options)
#         print(f"Imagen guardada en: {full_path}")
    
#     # Devolver en memoria
#     buffer = BytesIO()
#     ean.write(buffer, options=writer_options)
#     buffer.seek(0)
#     return buffer