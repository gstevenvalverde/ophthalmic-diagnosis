import shutil
import os
import os.path
from pathlib import Path


def get_input_with_icon(
    prompt,
    input_type=str,
    default=None,
    validation_func=None,
    error_msg="⚠️ Valor inválido",
):
    """
    Obtiene input con validación mejorada
    Args:
        prompt: Texto mostrado al usuario (con emoji)
        input_type: Tipo de dato esperado (int, float, str)
        default: Valor por defecto si se presiona Enter
        validation_func: Función para validación adicional
        error_msg: Mensaje personalizado para errores
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value and default is not None:
                return default

            converted = input_type(value)

            if validation_func and not validation_func(value):
                raise ValueError(error_msg)

            return converted

        except ValueError as e:
            print(f"{error_msg}: {e}")


def get_gender_input():
    while True:
        gender = input("🚻 Género (0-Masculino, 1-Femenino): ")
        if gender in ["0", "1"]:
            return int(gender)
        print("⚠️ Error: Ingrese 0 o 1")


def get_diagnosis_type():
    while True:
        diagnosis = input("🏥 Tipo de diagnóstico (0-2): ")
        if diagnosis in ["0", "1", "2"]:
            return int(diagnosis)
        print("⚠️ Error: Ingrese un valor entre 0 y 2")


import os
import shutil
from pathlib import Path


def move_file_with_os(src_path: str, dest_dir: str) -> str:
    """
    Mueve un archivo de manera segura, con verificación de permisos y rutas.

    Args:
        src_path: Ruta absoluta del archivo origen.
        dest_dir: Directorio destino (se creará si no existe).

    Returns:
        str: Ruta del archivo movido, o None si falla.
    """
    try:
        # Verifica que el archivo origen exista (usa Path para robustez)
        src = Path(src_path)
        if not src.is_file():
            print(f"❌ Error: {src_path} no existe o no es un archivo")
            return None

        # Prepara directorio destino (con Path para manejo multiplataforma)
        dest_dir_path = Path(dest_dir)
        dest_dir_path.mkdir(parents=True, exist_ok=True)

        # Construye ruta destino
        dest_path = dest_dir_path / src.name

        # Verifica si el destino ya existe (opcional: manejar colisiones)
        if dest_path.exists():
            print(f"⚠️ Advertencia: {dest_path} ya existe. Sobrescribiendo...")

        # Mueve el archivo (SOLO shutil.move, no os.rename)
        shutil.move(
            str(src), str(dest_path)
        )  # str() para compatibilidad con Python <3.6
        print(f"✅ Archivo movido a: {dest_path}")
        return str(dest_path)

    except PermissionError as e:
        print(f"❌ Error de permisos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    return None


def validate_file_exists(file_path: str) -> tuple:
    if not file_path:
        return False, "La ruta no puede estar vacía"
    try:
        if not os.path.exists(file_path):
            return False, f"El archivo no existe en: {file_path}"
        if not os.path.isfile(file_path):
            return False, f"La ruta no es un archivo válido: {file_path}"
        if not os.access(file_path, os.R_OK):
            return False, f"No se tienen permisos de lectura para: {file_path}"
        return True, f"Archivo válido: {file_path}"
    except Exception as e:
        return False, f"Error validando archivo: {str(e)}"


def validate_file_extension(file_path: str, field_name: str) -> tuple:
    VALID_EXTENSIONS = {
        "path_retina_image": [".jpg", ".jpeg", ".png", ".tiff", ".bmp"],
        "path_contour_cup_exp1": [".txt"],
        "path_contour_cup_exp2": [".txt"],
        "path_contour_disc_exp1": [".txt"],
        "path_contour_disc_exp2": [".txt"],
        "path_retina_contour_image": [".jpg", ".jpeg", ".png", ".tiff", ".bmp"],
    }

    file_ext = Path(file_path).suffix.lower()
    allowed_exts = VALID_EXTENSIONS.get(field_name, [])

    if not allowed_exts:
        return False, f"Campo {field_name} no tiene extensiones configuradas"

    if file_ext not in allowed_exts:
        return False, (
            f"Extensión inválida para {field_name}: {file_ext}. "
            f"Permitidas: {', '.join(allowed_exts)}"
        )

    return True, f"Extensión válida para {field_name}: {file_ext}"
