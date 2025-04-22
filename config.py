import os
import stat
from pathlib import Path


def setup_data_dir():
    """Configura permisos para la estructura compleja de carpetas"""
    base_dir = Path(__file__).parent / "data" / "load_data"
    folders = [
        "ClinicalData",
        "FundusImages",
        "ExpertsSegmentations/Contours",
        "ExpertsSegmentations/ImagesWithContours",
    ]
    for folder in folders:
        full_path = base_dir / folder
        full_path.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            try:
                os.chmod(
                    full_path,
                    stat.S_IRWXU
                    | stat.S_IRGRP
                    | stat.S_IXGRP
                    | stat.S_IROTH
                    | stat.S_IXOTH,
                )
                print(f"✅ Configurado: {full_path}")
            except Exception as e:
                print(f"⚠️ Error en {full_path}: {e}")
    return base_dir
