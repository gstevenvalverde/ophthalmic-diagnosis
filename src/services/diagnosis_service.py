from src.models.diagnosis import Diagnosis
from src.models.patient import Patient
from src.models.eye_examination import EyeExamination
from src.models.eye_image import EyeImage
from src.models.retina import Retina
from src.models.contours import Contours
import pandas as pd
import os


class DiagnosisService:

    # os.path.join('data', 'load_data', 'ClinicalData', 'diagnosis_data.xlsx')
    def __init__(self, excel_path: str):
        self.excel_path = excel_path

    # Carga los datos de los archivos Excel a la Estructura de Clases creada
    def load_diagnosis_db(self) -> list:
        df = self.convert_xls_to_df("OD")
        diagnosises = self.load_data(df)
        df_os = self.convert_xls_to_df("OS")
        self.add_diagnosises_os(diagnosises=diagnosises, df_entry_os=df_os)
        print("...Data loaded.")
        return diagnosises

    # Convierte el excel recibido en un DataFrame de pandas
    def convert_xls_to_df(self, sheet: str) -> pd.DataFrame:
        df = pd.read_excel(self.excel_path, sheet_name=sheet)
        df_optimazing = self.optimazing_df(df)
        return df_optimazing

    # Realiza la limpieza del código ID a formato int y aplica tipo de dato a las columnas del DataFrame
    def optimazing_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(subset=["ID"])
        df["ID"] = df["ID"].str.replace("#", "").astype("int")
        df["Age"] = df["Age"].astype("Int8")
        df["Gender"] = df["Gender"].astype("category")
        df["Diagnosis"] = df["Diagnosis"].astype("category")
        df["dioptre_1"] = df["dioptre_1"].astype("Float32")
        df["dioptre_2"] = df["dioptre_2"].astype("Float32")
        df["astigmatism"] = df["astigmatism"].astype("Float32")
        df["Phakic/Pseudophakic"] = df["Phakic/Pseudophakic"].astype("category")
        df["Pneumatic"] = df["Pneumatic"].astype("Float32")
        df["Perkins"] = df["Perkins"].astype("Float32")
        df["Pachymetry"] = df["Pachymetry"].astype("Float32")
        df["Axial_Length"] = df["Axial_Length"].astype("Float32")
        df["VF_MD"] = df["VF_MD"].astype("Float32")
        return df

    # Carga los datos de patient, diagnosis, EyeExamination (OD), EyeImage (OD), Contours (OD), Retina (OD). De df_entry_od a la lista diagnosises[]
    def load_data(self, df_entry_od: str) -> list:
        try:
            diagnosises = []
            for index, row in df_entry_od.iterrows():
                diagnosis = Diagnosis(
                    diagnosis_id=row["ID"],
                    diagnosis=row["Diagnosis"],
                )
                patient = Patient(age=row["Age"], gender=row["Gender"])
                diagnosis.add_patient(patient=patient)
                eye_examination = EyeExamination(
                    dioptre_1=row["dioptre_1"],
                    dioptre_2=row["dioptre_2"],
                    astigmatism=row["astigmatism"],
                    phakic_pseudophakic=row["Phakic/Pseudophakic"],
                    pneumatic=row["Pneumatic"],
                    perkins=row["Perkins"],
                    pachymetry=row["Pachymetry"],
                    axial_length=row["Axial_Length"],
                    vf_md=row["VF_MD"],
                )
                diagnosis.add_eye_examination_od(eye_examination_od=eye_examination)
                eye_image = EyeImage(
                    path_retina_contours_image=os.path.join(
                        "data",
                        "load_data",
                        "ExpertsSegmentations",
                        "ImagesWithContours",
                        f"Opht_cont_RET{row['ID']:03d}OD.jpg",
                    ),
                )
                retina_image = Retina(
                    path_retina_image=os.path.join(
                        "data", "load_data", "FundusImages", f"RET{row['ID']:03d}OD.jpg"
                    )
                )
                contours_layers = Contours(
                    path_retina_cup_exp1=os.path.join(
                        "data",
                        "load_data",
                        "ExpertsSegmentations",
                        "Contours",
                        f"RET{row['ID']:03d}OD_cup_exp1.txt",
                    ),
                    path_retina_cup_exp2=os.path.join(
                        "data",
                        "load_data",
                        "ExpertsSegmentations",
                        "Contours",
                        f"RET{row['ID']:03d}OD_cup_exp2.txt",
                    ),
                    path_retina_disc_exp1=os.path.join(
                        "data",
                        "load_data",
                        "ExpertsSegmentations",
                        "Contours",
                        f"RET{row['ID']:03d}OD_disc_exp1.txt",
                    ),
                    path_retina_disc_exp2=os.path.join(
                        "data",
                        "load_data",
                        "ExpertsSegmentations",
                        "Contours",
                        f"RET{row['ID']:03d}OD_disc_exp2.txt",
                    ),
                )
                eye_examination.add_eye_image(eye_image=eye_image)
                eye_image.add_retina_image(retina_image=retina_image)
                eye_image.add_contours_layer(contours_layer=contours_layers)
                diagnosises.append(diagnosis)
        except Exception as e:
            print(e)
        else:
            return diagnosises

    # Agrega EyeExamination (OS), EyeImage (OS), Contours (OS), Retina (OS). De df_entry_os a la lista diagnosises[]
    def add_diagnosises_os(
        self, diagnosises: list[Diagnosis], df_entry_os: pd.DataFrame
    ):
        for index, row_os in df_entry_os.iterrows():
            for diagnosis in diagnosises:
                if row_os["ID"] == diagnosis.diagnosis_id:
                    eye_examination = EyeExamination(
                        dioptre_1=row_os["dioptre_1"],
                        dioptre_2=row_os["dioptre_2"],
                        astigmatism=row_os["astigmatism"],
                        phakic_pseudophakic=row_os["Phakic/Pseudophakic"],
                        pneumatic=row_os["Pneumatic"],
                        perkins=row_os["Perkins"],
                        pachymetry=row_os["Pachymetry"],
                        axial_length=row_os["Axial_Length"],
                        vf_md=row_os["VF_MD"],
                    )
                    diagnosis.add_eye_examination_os(eye_examination_os=eye_examination)
                    eye_image = EyeImage(
                        path_retina_contours_image=os.path.join(
                            "..",
                            "data",
                            "load_data",
                            "ExpertsSegmentations",
                            "ImagesWithContours",
                            f"Opht_cont_RET{row_os['ID']:03d}OS.jpg",
                        ),
                    )
                    retina_image = Retina(
                        path_retina_image=os.path.join(
                            "..",
                            "data",
                            "load_data",
                            "FundusImages",
                            f"RET{row_os['ID']:03d}OS.jpg",
                        )
                    )
                    contours_layers = Contours(
                        path_retina_cup_exp1=os.path.join(
                            "..",
                            "data",
                            "load_data",
                            "ExpertsSegmentations",
                            "Contours",
                            f"RET{row_os['ID']:03d}OS_cup_exp1.txt",
                        ),
                        path_retina_cup_exp2=os.path.join(
                            "..",
                            "data",
                            "load_data",
                            "ExpertsSegmentations",
                            "Contours",
                            f"RET{row_os['ID']:03d}OS_cup_exp2.txt",
                        ),
                        path_retina_disc_exp1=os.path.join(
                            "..",
                            "data",
                            "load_data",
                            "ExpertsSegmentations",
                            "Contours",
                            f"RET{row_os['ID']:03d}OS_disc_exp1.txt",
                        ),
                        path_retina_disc_exp2=os.path.join(
                            "..",
                            "data",
                            "load_data",
                            "ExpertsSegmentations",
                            "Contours",
                            f"RET{row_os['ID']:03d}OS_disc_exp2.txt",
                        ),
                    )
                    eye_examination.add_eye_image(eye_image=eye_image)
                    eye_image.add_retina_image(retina_image=retina_image)
                    eye_image.add_contours_layer(contours_layer=contours_layers)

    def add_diagnosis(
        self, age: int, gender: int, diagnosis: int, diagnosises: list[Diagnosis]
    ):
        patient = Patient(age=age, gender=gender)
        id = int(diagnosises[-1].diagnosis_id + 1)
        diagnosis = Diagnosis(diagnosis_id=id, diagnosis=diagnosis)
        diagnosis.add_patient(patient=patient)
        diagnosises.append(diagnosis)
        self.save_diagnosis_to_excel(diagnosis=diagnosis)

    def update_diagnosis(
        self, age: int, gender: int, diagnosis: int, diagnosis_object: Diagnosis
    ):
        diagnosis_object.patient.update_age(age=age)
        diagnosis_object.patient.update_gender(gender=gender)
        diagnosis_object.update_diagnosis(diagnosis=diagnosis)
        self.save_diagnosis_to_excel(diagnosis=diagnosis_object)

    def save_diagnosis_to_excel(self, diagnosis: Diagnosis):
        sheets = ["OD", "OS"]
        for sheet_name in sheets:
            try:
                df = pd.read_excel(
                    self.excel_path,
                    sheet_name=sheet_name,
                    dtype={"ID": str, "Age": int, "Gender": int, "Diagnosis": int},
                )
                diagnosis_id_str = f"#{diagnosis.diagnosis_id:03d}"
                mask = df["ID"] == diagnosis_id_str
                if mask.any():
                    df.loc[mask, "ID"] = diagnosis_id_str
                    df.loc[mask, "Age"] = int(diagnosis.patient.age)
                    df.loc[mask, "Gender"] = int(diagnosis.patient.gender)
                    df.loc[mask, "Diagnosis"] = int(diagnosis.diagnosis)
                    action = "Actualizados"
                else:
                    new_row = pd.DataFrame(
                        [
                            {
                                "ID": diagnosis_id_str,
                                "Age": int(diagnosis.patient.age),
                                "Gender": int(diagnosis.patient.gender),
                                "Diagnosis": int(diagnosis.diagnosis),
                            }
                        ]
                    )
                    for col in ["Age", "Gender", "Diagnosis"]:
                        new_row[col] = new_row[col].astype(int)
                    df = pd.concat([df, new_row], ignore_index=True)
                    action = "Agregados"
                with pd.ExcelWriter(
                    self.excel_path,
                    engine="openpyxl",
                    mode="a",
                    if_sheet_exists="replace",
                ) as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"Datos {action} correctamente en la hoja {sheet_name}")

            except Exception as e:
                print(f"Error al guardar en Excel (hoja {sheet_name}): {str(e)}")
                # Opcional: imprime el traceback completo para diagnóstico
                import traceback

                traceback.print_exc()

    def delete_diagnosis(self, diagnosis_to_delete: int, diagnosises: list[Diagnosis]):
        try:
            del diagnosises[diagnosis_to_delete]
            data_od = []
            data_os = []
            for d in diagnosises:
                row_od = {
                    "ID": f"#{d.diagnosis_id:03d}",
                    "Age": d.patient.age,
                    "Gender": d.patient.gender,
                    "Diagnosis": d.diagnosis,
                    "dioptre_1": getattr(
                        getattr(d, "eye_examination_od", None), "dioptre_1", None
                    ),
                    "dioptre_2": d.eye_examination_od.dioptre_2,
                    "astigmatism": d.eye_examination_od.astigmatism,
                    "Phakic/Pseudophakic": d.eye_examination_od.phakic_pseudophakic,
                    "Pneumatic": d.eye_examination_od.pneumatic,
                    "Perkins": d.eye_examination_od.perkins,
                    "Pachymetry": d.eye_examination_od.pachymetry,
                    "Axial_Length": d.eye_examination_od.axial_length,
                    "VF_MD": d.eye_examination_od.vf_md,
                }
                row_os = {
                    "ID": f"#{d.diagnosis_id:03d}",
                    "Age": d.patient.age,
                    "Gender": d.patient.gender,
                    "Diagnosis": d.diagnosis,
                    "dioptre_1": getattr(
                        getattr(d, "eye_examination_os", None), "dioptre_1", None
                    ),
                    "dioptre_2": d.eye_examination_os.dioptre_2,
                    "astigmatism": d.eye_examination_os.astigmatism,
                    "Phakic/Pseudophakic": d.eye_examination_os.phakic_pseudophakic,
                    "Pneumatic": d.eye_examination_os.pneumatic,
                    "Perkins": d.eye_examination_os.perkins,
                    "Pachymetry": d.eye_examination_os.pachymetry,
                    "Axial_Length": d.eye_examination_os.axial_length,
                    "VF_MD": d.eye_examination_os.vf_md,
                }
                data_od.append(row_od)
                data_os.append(row_os)
            df_od = pd.DataFrame(data_od)
            df_os = pd.DataFrame(data_os)
            with pd.ExcelWriter(self.excel_path, engine="openpyxl", mode="w") as writer:
                df_od.to_excel(writer, sheet_name="OD", index=False)
                df_os.to_excel(writer, sheet_name="OS", index=False)
            print("Delete Diagnosis: ", diagnosis_to_delete)
        except Exception as e:
            print(f"Error to eliminate Diagnosis: {str(e)}")

    def add_eye(
        self,
        diagnosis_id: int,
        dioptre_1: float,
        dioptre_2: float,
        astigmatism: float,
        phakic_pseudophakic: int,
        pneumatic: float,
        perkins: float,
        pachymetry: float,
        axial_length: float,
        vf_md: float,
        path_retina_image: str,
        path_contour_cup_exp1: str,
        path_contour_cup_exp2: str,
        path_contour_disc_exp1: str,
        path_contour_disc_exp2: str,
        path_retina_contour_image: str,
        diagnosises: list[Diagnosis],
        opt_eye: str,
    ):
        diagnosis = None
        for d in diagnosises:
            if d.diagnosis_id == diagnosis_id:
                diagnosis = d
                print(f"El diagnosis es:  {diagnosis}")
        if diagnosis:
            eye_examination = EyeExamination(
                dioptre_1=dioptre_1,
                dioptre_2=dioptre_2,
                astigmatism=astigmatism,
                phakic_pseudophakic=phakic_pseudophakic,
                pneumatic=pneumatic,
                perkins=perkins,
                pachymetry=pachymetry,
                axial_length=axial_length,
                vf_md=vf_md,
            )
            eye_image = EyeImage(path_retina_contours_image=path_retina_contour_image)
            retina_image = Retina(path_retina_image=path_retina_image)
            contours_layer = Contours(
                path_retina_cup_exp1=path_contour_cup_exp1,
                path_retina_cup_exp2=path_contour_cup_exp2,
                path_retina_disc_exp1=path_contour_disc_exp1,
                path_retina_disc_exp2=path_contour_disc_exp2,
            )
            eye_examination.add_eye_image(eye_image=eye_image)
            eye_image.add_retina_image(retina_image=retina_image)
            eye_image.add_contours_layer(contours_layer=contours_layer)
            if opt_eye == "OD":
                diagnosis.add_eye_examination_od(eye_examination_od=eye_examination)
                self.save_eye_to_excel(diagnosis=diagnosis, sheet_name=opt_eye)
            elif opt_eye == "OS":
                diagnosis.add_eye_examination_os(eye_examination_os=eye_examination)
                self.save_eye_to_excel(diagnosis=diagnosis, sheet_name=opt_eye)
            else:
                print("Eye no valid.")

    def update_eye(
        self,
        diagnosis: Diagnosis,
        dioptre_1: float,
        dioptre_2: float,
        astigmatism: float,
        phakic_pseudophakic: int,
        pneumatic: float,
        perkins: float,
        pachymetry: float,
        axial_length: float,
        vf_md: float,
        path_retina_image: str,
        path_contour_cup_exp1: str,
        path_contour_cup_exp2: str,
        path_contour_disc_exp1: str,
        path_contour_disc_exp2: str,
        path_retina_contours_image: str,
        eye_examination: EyeExamination,
        opt_eye: str,
    ):
        eye_examination.update_dioptre_1(dioptre_1=dioptre_1)
        eye_examination.update_dioptre_2(dioptre_2=dioptre_2)
        eye_examination.update_astigmatism(astigmatism=astigmatism)
        eye_examination.update_phakic_pseudophakic(
            phakic_pseudophakic=phakic_pseudophakic
        )
        eye_examination.update_pneumatic(pneumatic=pneumatic)
        eye_examination.update_perkins(perkins=perkins)
        eye_examination.update_pachymetry(pachymetry=pachymetry)
        eye_examination.update_axial_length(axial_length=axial_length)
        eye_examination.update_vf_md(vf_md=vf_md)
        eye_examination.eye_image.update_path_retina_contours_image(
            path_retina_contours_image=path_retina_contours_image
        )
        eye_examination.eye_image.retina_image.update_path_retina_image(
            path_retina_image=path_retina_image
        )
        eye_examination.eye_image.contours_layer.update_path_retina_cup_exp1(
            path_retina_cup_exp1=path_contour_cup_exp1
        )
        eye_examination.eye_image.contours_layer.update_path_retina_cup_exp2(
            path_retina_cup_exp2=path_contour_cup_exp2
        )
        eye_examination.eye_image.contours_layer.update_path_retina_disc_exp1(
            path_retina_disc_exp1=path_contour_disc_exp1
        )
        eye_examination.eye_image.contours_layer.update_path_retina_disc_exp2(
            path_retina_disc_exp2=path_contour_disc_exp2
        )
        self.save_eye_to_excel(diagnosis=diagnosis, sheet_name=opt_eye)

    def save_eye_to_excel(self, diagnosis: Diagnosis, sheet_name: str):
        try:
            df = pd.read_excel(self.excel_path, sheet_name=sheet_name)
            mask = df["ID"] == f"#{diagnosis.diagnosis_id:03d}"
            if sheet_name == "OD":
                eye_examination = diagnosis.eye_examination_od
            elif sheet_name == "OS":
                eye_examination = diagnosis.eye_examination_os
            else:
                print("Invalid sheet_name parameter.")
            if mask.any():
                df.loc[
                    mask,
                    [
                        "dioptre_1",
                        "dioptre_2",
                        "astigmatism",
                        "Phakic/Pseudophakic",
                        "Pneumatic",
                        "Perkins",
                        "Pachymetry",
                        "Axial_Length",
                        "VF_MD",
                    ],
                ] = [
                    eye_examination.dioptre_1,
                    eye_examination.dioptre_2,
                    eye_examination.astigmatism,
                    eye_examination.phakic_pseudophakic,
                    eye_examination.pneumatic,
                    eye_examination.perkins,
                    eye_examination.pachymetry,
                    eye_examination.axial_length,
                    eye_examination.vf_md,
                ]
                action = "actualizados"
                with pd.ExcelWriter(
                    self.excel_path,
                    engine="openpyxl",
                    mode="a",
                    if_sheet_exists="replace",
                ) as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(
                    f"Datos {action} correctamente en la hoja {sheet_name} para ID {diagnosis.diagnosis_id}"
                )
        except Exception as e:
            print(f"Error al guardar en Excel: {str(e)}")
            raise
