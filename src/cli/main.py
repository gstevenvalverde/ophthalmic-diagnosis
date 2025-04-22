from src.models.diagnosis import Diagnosis
from src.services.diagnosis_service import DiagnosisService
from src.services.file_services import display_text_file_graphically
from src.services.image_service import display_image
from src.utils import (
    get_input_with_icon,
    get_gender_input,
    get_diagnosis_type,
    move_file_with_os,
    validate_file_exists,
    validate_file_extension,
)
import os


class App:

    def __init__(self, diagnosis_service: DiagnosisService, data_dir: str):
        self.diagnosis_service = diagnosis_service
        self.diagnosises = self.diagnosis_service.load_diagnosis_db()
        self.DATA_DIR = data_dir

    def home(self):
        try:
            while True:
                print("\n👁️‍🗨️ \033[1;36mEye Diagnosis App\033[0m 👁️‍🗨️")
                print("1. ➕ Añadir diagnóstico")
                print("2. 👀 Ver diagnósticos")
                print("3. ✏️ Editar diagnóstico")
                print("4. ❌ Eliminar diagnóstico")
                print("5. 🔴 Salir\n")
                opt = get_input_with_icon("🖥️ Elige opción: ", int)
                if opt == 1:
                    self.add_diagnosis_cli()
                elif opt == 2:
                    self.see_diagnosis_cli()
                elif opt == 3:
                    self.edit_diagnosis_cli()
                elif opt == 4:
                    self.delete_diagnosis_cli()
                elif opt == 5:
                    print("Close aplication...")
                    break
                else:
                    print("Opción no disponible.")
        except ValueError:
            print("Opción no válida.")

    def add_diagnosis_cli(self):
        print("\n✨ === AÑADIR NUEVO DIAGNÓSTICO === ✨")
        print("\n📝 DATOS DEL PACIENTE")
        patient_data = {
            "age": get_input_with_icon("👴 Edad del paciente: ", int),
            "gender": get_gender_input(),
            "diagnosis": get_diagnosis_type(),
        }
        self.diagnosis_service.add_diagnosis(
            age=patient_data["age"],
            gender=patient_data["gender"],
            diagnosis=patient_data["diagnosis"],
            diagnosises=self.diagnosises,
        )
        diagnosis_id = self.diagnosises[-1].diagnosis_id
        print(f"\n🆔 ID de diagnóstico asignado: {diagnosis_id}")
        for eye in ["OD", "OS"]:
            print(f"\n👁️ EXAMEN DEL OJO {eye}")
            eye_data = self._get_eye_exam_data(eye=eye, diagnosis_id=diagnosis_id)
            print(eye_data)
            self.diagnosis_service.add_eye(
                diagnosises=self.diagnosises,
                diagnosis_id=diagnosis_id,
                opt_eye=eye,
                **eye_data,
            )
            print(f"✅ Datos del ojo {eye} añadidos correctamente")

    def _get_eye_exam_data(self, eye: str, diagnosis_id: int):
        DESTINATIONS = {
            "path_retina_image": f"{self.DATA_DIR}/FundusImages",
            "path_contour_cup_exp1": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_contour_cup_exp2": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_contour_disc_exp1": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_contour_disc_exp2": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_retina_contours_image": f"{self.DATA_DIR}/ExpertsSegmentations/ImagesWithContours",
        }
        FILE_NAME_FORMAT = {
            "path_retina_image": f"RET{diagnosis_id:03d}{eye}.jpg",
            "path_contour_cup_exp1": f"RET{diagnosis_id:03d}{eye}_cup_exp1.txt",
            "path_contour_cup_exp2": f"RET{diagnosis_id:03d}{eye}cup_exp2.txt",
            "path_contour_disc_exp1": f"RET{diagnosis_id:03d}{eye}_disc_exp1.txt",
            "path_contour_disc_exp2": f"RET{diagnosis_id:03d}{eye}_disc_exp2.txt",
            "path_retina_contours_image": f"RET{diagnosis_id:03d}{eye}.jpg",
        }
        numeric_fields = {
            "dioptre_1": "🔸 Dioptría 1",
            "dioptre_2": "🔸 Dioptría 2",
            "astigmatism": "🔸 Astigmatismo",
            "phakic_pseudophakic": "🔸 Phakic/Pseudophakic [0/1]",
            "pneumatic": "🔸 Pneumatic",
            "perkins": "🔸 Perkins",
            "pachymetry": "🔸 Pachymetry",
            "axial_length": "🔸 Longitud axial",
            "vf_md": "🔸 VF MD",
        }
        path_fields = {
            "path_retina_image": "🖼️ Ruta imagen retina",
            "path_contour_cup_exp1": "📁 Ruta contorno copa 01",
            "path_contour_cup_exp2": "📁 Ruta contorno copa 02",
            "path_contour_disc_exp1": "📁 Ruta contorno disco 01",
            "path_contour_disc_exp2": "📁 Ruta contorno disco 02",
            "path_retina_contour_image": "🖼️ Ruta imagen retina con contornos",
        }
        eye_data = {}
        for field, label in numeric_fields.items():
            eye_data[field] = get_input_with_icon(
                f"{label}: ",
                (
                    float
                    if "dioptre" in field or field in ["axial_length", "vf_md"]
                    else int
                ),
            )
        for field, label in path_fields.items():
            while True:
                file_path = get_input_with_icon(f"{label} (ruta completa): ", str)
                exists, msg = validate_file_exists(file_path)
                if not exists:
                    print(f"❌ {msg}")
                    continue
                ext_valid, ext_msg = validate_file_extension(file_path, field)
                if not ext_valid:
                    print(f"❌ {ext_msg}")
                    continue
                dest_dir = DESTINATIONS[field]
                moved_path = move_file_with_os(file_path, dest_dir)
                if moved_path:
                    new_filename = FILE_NAME_FORMAT[field]
                    new_path = os.path.join(dest_dir, new_filename)
                    try:
                        os.rename(moved_path, new_path)
                        eye_data[field] = new_path
                        print(f"✅ Archivo procesado y renombrado: {new_path}")
                        break
                    except Exception as e:
                        print(f"❌ Error al renombrar archivo: {e}")
                        continue
                else:
                    print("⚠️ Intente nuevamente con otra ruta")
        return eye_data

    def see_diagnosis_cli(self):
        while True:
            self._display_diagnoses_menu()
            try:
                opt_see = int(input("👉 Elija una opción: "))
                if opt_see == len(self.diagnosises) + 1:
                    print("\n👋 Saliendo del visualizador...")
                    break
                self._show_diagnosis_details(opt_see)
            except (ValueError, IndexError):
                print("\n⚠️ Error: Opción no válida. Intente nuevamente.")

    def _display_diagnoses_menu(self):
        print("\n🔍 === LISTA DE DIAGNÓSTICOS ===")
        for i, diagnosis in enumerate(self.diagnosises, 1):
            print(
                f"{i} ▶ ID: #{diagnosis.diagnosis_id:03d} | Diagnóstico: {diagnosis.diagnosis}"
            )
        print(f"{len(self.diagnosises)+1} ❌ Salir")

    def _show_diagnosis_details(self, option):
        if 1 <= option <= len(self.diagnosises):
            diagnosis = self.diagnosises[option - 1]
            print(diagnosis)
            print("\n📋 === DETALLES COMPLETOS ===")
            print(f"🆔 ID: #{diagnosis.diagnosis_id:03d}")
            print(
                f"👤 Paciente: {diagnosis.patient.age} años | Género: {self._format_gender(diagnosis.patient.gender)}"
            )
            print(f"🏥 Diagnóstico principal: {diagnosis.diagnosis}")
            print("\n👁️ EXAMEN OCULAR OD:")
            self._print_eye_exam(diagnosis.eye_examination_od)
            print("\n👁️ EXAMEN OCULAR OS:")
            self._print_eye_exam(diagnosis.eye_examination_os)
        else:
            print("\n⚠️ Error: Número de diagnóstico no existe")

    def _print_eye_exam(self, exam):
        if not exam:
            print("🔴 Examen no registrado")
            return
        print("\n📊 DATOS CLÍNICOS:")
        print(f"  🔸 Dioptrías: {exam.dioptre_1}/{exam.dioptre_2}")
        print(f"  🔸 Astigmatismo: {exam.astigmatism}")
        print(
            f'  🔸 Tipo de lente: {"Phakic" if exam.phakic_pseudophakic == 0 else "Pseudophakic"}'
        )
        print(f"  � Pneumatic: {exam.pneumatic}")
        print(f"  📏 Perkins: {exam.perkins}")
        print(f"  📏 Pachymetry: {exam.pachymetry}")
        print(f"  📐 Longitud axial: {exam.axial_length}")
        print(f"  📈 VF MD: {exam.vf_md}")
        if exam.eye_image:
            print("\n🖼️ IMÁGENES:")
            print(
                f'  📁 Ver Retina y contornos: {exam.eye_image.path_retina_contours_image or "N/A"}'
            )
            if exam.eye_image.retina_image:
                print(
                    f'  🖼️ Ver Imagen retina: {exam.eye_image.retina_image.path_retina_image or "N/A"}'
                )
            if exam.eye_image.contours_layer:
                contours = exam.eye_image.contours_layer
                print("\n📐 CONTORNOS:")
                print(f'  🔵 Ver Copa Exp1: {contours.path_retina_cup_exp1 or "N/A"}')
                print(f'  🔵 Ver Copa Exp2: {contours.path_retina_cup_exp2 or "N/A"}')
                print(f'  🟡 Ver Disco Exp1: {contours.path_retina_disc_exp1 or "N/A"}')
                print(f'  🟡 Ver Disco Exp2: {contours.path_retina_disc_exp2 or "N/A"}')
                files_to_watch = [
                    exam.eye_image.path_retina_contours_image,
                    (
                        exam.eye_image.retina_image.path_retina_image
                        if exam.eye_image.retina_image
                        else None
                    ),
                    contours.path_retina_cup_exp1,
                    contours.path_retina_cup_exp2,
                    contours.path_retina_disc_exp1,
                    contours.path_retina_disc_exp2,
                ]
                valid_files = [
                    file for file in files_to_watch if file and isinstance(file, str)
                ]

                if not valid_files:
                    print("⚠️ No hay archivos válidos para visualizar.")
                    return
                valid_files = [
                    os.path.abspath(file) if not os.path.isabs(file) else file
                    for file in valid_files
                ]

                while True:
                    print("\n📂 Archivos disponibles:")
                    for i, file in enumerate(valid_files, start=1):
                        print(f"  {i}. {os.path.basename(file)}")
                    print(f"  {len(valid_files) + 1}. ❌ Salir")

                    option_to_watch = get_input_with_icon(
                        "Seleccione un archivo a visualizar (número): ", int
                    )

                    if option_to_watch == len(valid_files) + 1:
                        break
                    elif 1 <= option_to_watch <= len(valid_files):
                        selected_file = valid_files[option_to_watch - 1]

                        if not os.path.exists(selected_file):
                            print(f"❌ Error: El archivo no existe:\n{selected_file}")
                            continue
                        if selected_file.lower().endswith(
                            (".png", ".jpg", ".jpeg", ".webp")
                        ):
                            display_image(selected_file)
                        elif selected_file.lower().endswith(".txt"):
                            display_text_file_graphically(selected_file)
                        else:
                            print(
                                f"Formato no soportado: {os.path.basename(selected_file)}"
                            )
                    else:
                        print("❌ Opción inválida. Intente nuevamente.")

    def _format_gender(self, gender_code):
        return "Masculino" if gender_code == 0 else "Femenino"

    def edit_diagnosis_cli(self):
        while True:
            self._display_diagnoses_list()
            diagnosis_to_update = self._select_diagnosis()
            if diagnosis_to_update is None:
                break
            while True:
                choice = self._display_edit_menu()
                if choice == "1":
                    self._edit_patient_data(diagnosis_to_update)
                elif choice in ["2", "3"]:
                    eye_type = "OD" if choice == "2" else "OS"
                    self._edit_eye_data(diagnosis_to_update, eye_type)
                elif choice == "4":
                    break
                else:
                    print("Opción no válida. Intente nuevamente.")

    def _display_diagnoses_list(self):
        print("\nLista de Diagnósticos:")
        for i, diagnosis in enumerate(self.diagnosises, 1):
            print(f"{i}. ID: {diagnosis.diagnosis_id} - {diagnosis.diagnosis}")
        print(f"{len(self.diagnosises)+1}. Salir")

    def _select_diagnosis(self):
        try:
            opt = int(input("\nSeleccione un diagnóstico: "))
            if opt == len(self.diagnosises) + 1:
                return None
            if 1 <= opt <= len(self.diagnosises):
                return self.diagnosises[opt - 1]
            print("Opción no válida.")
            return None
        except ValueError:
            print("Por favor ingrese un número válido.")
            return None

    def _display_edit_menu(self):
        print("\nMenú de Edición:")
        print("1. Editar información del paciente")
        print("2. Editar examen del ojo OD")
        print("3. Editar examen del ojo OS")
        print("4. Volver")
        return input("Seleccione una opción: ").strip()

    def _edit_patient_data(self, diagnosis):
        print("\n📝 Editando información del paciente:")
        new_age = get_input_with_icon(
            f"👴 Edad actual ({diagnosis.patient.age}): ",
            int,
            default=diagnosis.patient.age,
        )
        new_gender = get_input_with_icon(
            f"🚻 Género actual ({self._format_gender(diagnosis.patient.gender)}): ",
            str,
            default=str(diagnosis.patient.gender),
            validation_func=lambda x: x in ["0", "1"],
            error_msg="⚠️ Solo se permite 0 (Masculino) o 1 (Femenino)",
        )
        new_diagnosis = get_input_with_icon(
            f"🏥 Diagnóstico actual ({diagnosis.diagnosis}): ",
            str,
            default=diagnosis.diagnosis,
        )
        self.diagnosis_service.update_diagnosis(
            age=new_age,
            gender=(
                int(new_gender) if new_gender is not None else diagnosis.patient.gender
            ),
            diagnosis=new_diagnosis,
            diagnosis_object=diagnosis,
        )
        self.diagnosis_service.update_diagnosis(
            age=new_age,
            gender=new_gender,
            diagnosis=new_diagnosis,
            diagnosis_object=diagnosis,
        )

    def _edit_eye_data(self, diagnosis, eye_type):
        print(f"\n👁️ EDITANDO EXAMEN DEL OJO {eye_type}")
        eye_exam = getattr(diagnosis, f"eye_examination_{eye_type.lower()}")
        DESTINATIONS = {
            "path_retina_image": f"{self.DATA_DIR}/FundusImages",
            "path_contour_cup_exp1": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_contour_cup_exp2": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_contour_disc_exp1": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_contour_disc_exp2": f"{self.DATA_DIR}/ExpertsSegmentations/Contours",
            "path_retina_contours_image": f"{self.DATA_DIR}/ExpertsSegmentations/ImagesWithContours",
        }
        FILE_NAME_FORMAT = {
            "path_retina_image": f"RET{diagnosis.diagnosis_id:03d}{eye_type}.jpg",
            "path_contour_cup_exp1": f"RET{diagnosis.diagnosis_id:03d}{eye_type}_cup_exp1.txt",
            "path_contour_cup_exp2": f"RET{diagnosis.diagnosis_id:03d}{eye_type}cup_exp2.txt",
            "path_contour_disc_exp1": f"RET{diagnosis.diagnosis_id:03d}{eye_type}_disc_exp1.txt",
            "path_contour_disc_exp2": f"RET{diagnosis.diagnosis_id:03d}{eye_type}_disc_exp2.txt",
            "path_retina_contours_image": f"RET{diagnosis.diagnosis_id:03d}{eye_type}.jpg",
        }
        numeric_fields = {
            "dioptre_1": ("🔸 Dioptría 1", float),
            "dioptre_2": ("🔸 Dioptría 2", float),
            "astigmatism": ("🔸 Astigmatismo", float),
            "phakic_pseudophakic": ("🔸 Tipo de lente [0-Phakic/1-Pseudophakic]", int),
            "pneumatic": ("📏 Pneumatic", float),
            "perkins": ("📏 Perkins", float),
            "pachymetry": ("📏 Pachymetry", float),
            "axial_length": ("📏 Longitud Axial", float),
            "vf_md": ("📊 VF MD", float),
        }
        path_fields = {
            "path_retina_contours_image": "🖼️ Ruta retina con contornos",
            "retina_image.path_retina_image": "🖼️ Ruta imagen retina",
            "contours_layer.path_retina_cup_exp1": "📁 Contorno copa Exp1",
            "contours_layer.path_retina_cup_exp2": "📁 Contorno copa Exp2",
            "contours_layer.path_retina_disc_exp1": "📁 Contorno disco Exp1",
            "contours_layer.path_retina_disc_exp2": "📁 Contorno disco Exp2",
        }
        numeric_values = {}
        path_values = {}
        for field, (label, input_type) in numeric_fields.items():
            current_value = getattr(eye_exam, field)
            numeric_values[field] = get_input_with_icon(
                f"{label} (actual: {current_value}): ",
                input_type=input_type,
                default=current_value,
                validation_func=lambda x, f=field: (
                    True if f != "phakic_pseudophakic" else x in ["0", "1"]
                ),
                error_msg=(
                    "⚠️ Solo 0 o 1 para tipo de lente"
                    if field == "phakic_pseudophakic"
                    else "⚠️ Valor inválido"
                ),
            )
        for field, label in path_fields.items():
            parts = field.split(".")
            current_obj = eye_exam.eye_image
            for part in parts[:-1]:
                current_obj = getattr(current_obj, part)
            current_value = getattr(current_obj, parts[-1])
            while True:
                new_path = get_input_with_icon(
                    f"{label} (actual: {current_value}): ",
                    input_type=str,
                    default=current_value,
                )
                if not new_path or new_path == current_value:
                    path_values[field.replace(".", "_")] = current_value
                    break
                exists, exists_msg = validate_file_exists(new_path)
                if not exists:
                    print(f"❌ {exists_msg}")
                    continue
                ext_valid, ext_msg = validate_file_extension(
                    new_path, field.split(".")[-1]
                )
                if not ext_valid:
                    print(f"❌ {ext_msg}")
                    continue
                dest_dir = DESTINATIONS[field]
                moved_path = move_file_with_os(new_path, dest_dir)
                if moved_path:
                    new_filename = FILE_NAME_FORMAT[field]
                    new_path_renamed = os.path.join(dest_dir, new_filename)
                    try:
                        os.rename(moved_path, new_path_renamed)
                        print(f"✅ Archivo procesado y renombrado: {new_path_renamed}")
                        path_values[field.replace(".", "_")] = new_path_renamed
                        break
                    except Exception as e:
                        print(f"❌ Error al renombrar archivo: {e}")
                        continue
                else:
                    print("⚠️ Intente nuevamente con otra ruta")
        self.diagnosis_service.update_eye(
            diagnosis=diagnosis,
            opt_eye=eye_type,
            dioptre_1=numeric_values["dioptre_1"],
            dioptre_2=numeric_values["dioptre_2"],
            astigmatism=numeric_values["astigmatism"],
            phakic_pseudophakic=numeric_values["phakic_pseudophakic"],
            pneumatic=numeric_values["pneumatic"],
            perkins=numeric_values["perkins"],
            pachymetry=numeric_values["pachymetry"],
            axial_length=numeric_values["axial_length"],
            vf_md=numeric_values["vf_md"],
            path_retina_image=path_values.get("retina_image_path_retina_image"),
            path_contour_cup_exp1=path_values.get(
                "contours_layer_path_retina_cup_exp1"
            ),
            path_contour_cup_exp2=path_values.get(
                "contours_layer_path_retina_cup_exp2"
            ),
            path_contour_disc_exp1=path_values.get(
                "contours_layer_path_retina_disc_exp1"
            ),
            path_contour_disc_exp2=path_values.get(
                "contours_layer_path_retina_disc_exp2"
            ),
            path_retina_contours_image=path_values.get("path_retina_contours_image"),
            eye_examination=eye_exam,
        )
        print(f"✅ Datos del ojo {eye_type} actualizados correctamente")

    def delete_diagnosis_cli(self):
        """Interfaz mejorada para eliminar diagnósticos"""
        while True:
            self._display_diagnoses_list()
            try:
                input_str = input(
                    "❌ Ingrese el número a eliminar (0 para cancelar): "
                ).strip()
                if not input_str:
                    print("🚫 Operación cancelada")
                    break
                opt_delete = int(input_str)
                if opt_delete == 0:
                    print("🚫 Operación cancelada")
                    break
                if 1 <= opt_delete <= len(self.diagnosises):
                    diagnosis = self.diagnosises[opt_delete - 1]
                    print(f"\n⚠️ ATENCIÓN: Está por eliminar:")
                    print(f"   🆔 ID: #{diagnosis.diagnosis_id:03d}")
                    print(f"   🏥 Diagnóstico: {diagnosis.diagnosis}")
                    print(f"   👤 Paciente: {diagnosis.patient.age} años")
                    confirm = input("¿Confirmar eliminación? (s/n): ").strip().lower()
                    while confirm not in ["s", "n"]:
                        print("⚠️ Ingrese 's' para sí o 'n' para no")
                        confirm = (
                            input("¿Confirmar eliminación? (s/n): ").strip().lower()
                        )
                    if confirm == "s":
                        self.diagnosis_service.delete_diagnosis(
                            diagnosis_to_delete=opt_delete - 1,
                            diagnosises=self.diagnosises,
                        )
                        print(
                            f"✅ Diagnóstico #{diagnosis.diagnosis_id} eliminado exitosamente"
                        )
                        break
                    else:
                        print("🚫 Eliminación cancelada")
                        break
                else:
                    print(
                        f"⚠️ Error: Debe ingresar un número entre 1 y {len(self.diagnosises)}"
                    )
            except ValueError:
                print("⚠️ Error: Debe ingresar un número entero válido")
            except Exception as e:
                print(f"⚠️ Error inesperado: {str(e)}")

# Ft. Deepseek and chatGPT
