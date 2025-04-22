from src.cli.main import App
from src.services.diagnosis_service import DiagnosisService
from config import setup_data_dir
import os


def main():
    DATA_DIR = setup_data_dir()
    print(f"📂 Directorio usable: {DATA_DIR}")
    excel_path = os.path.join(
        "data", "load_data", "ClinicalData", "diagnosis_data.xlsx"
    )
    diagnosis_service = DiagnosisService(excel_path=excel_path)
    cli = App(diagnosis_service=diagnosis_service, data_dir=DATA_DIR)
    cli.home()


if __name__ == "__main__":
    main()
