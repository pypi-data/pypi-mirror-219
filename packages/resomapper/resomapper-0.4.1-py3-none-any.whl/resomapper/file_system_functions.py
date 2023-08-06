import os
import shutil
import tkinter as tk
import warnings
from fnmatch import fnmatch
from pathlib import Path
from tkinter import filedialog

import pandas as pd
from bruker2nifti.converter import Bruker2Nifti

import resomapper.utils as ut
from resomapper.utils import Headermsg as hmg

warnings.filterwarnings("ignore")


def select_directory():
    """Allows selection of root directory showing a file explorer window.

    Returns:
        Path: full path to the selected directory."""

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    root.destroy()
    root.mainloop()

    return Path(file_path)


def select_file():
    """Allows selection of a file showing a file explorer window.

    Returns:
        Path: full path to the selected file.
    """

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    # root.mainloop()

    return Path(file_path)


def check_cwd(cwd: bool, return_cwd=True):
    """Checks if current work directory contains the studies.
    Otherwise, changes path.

    Args:
        cwd (bool): If True, it indicates that we are in the correct path. If False, it
            indicates that we are not in the correct path and a change of path
            is needed.
        return_cwd (bool, optional): Indicates whether to return the current working
            directory or not. Defaults to True.

    Returns:
        path-like or None: The current working directory if return_cwd is True,
        otherwise None (nothing is returned).
    """
    if not cwd:
        while True:
            data_path = input("¿Cuál es el directorio actual de los datos?\n")
            try:
                os.chdir(data_path)  # change cwd to a given path
                if return_cwd:
                    return Path(data_path)
                break
            except FileNotFoundError:
                print(f"{hmg.error}Por favor, introduce un directorio válido.")
    if return_cwd:
        return Path().cwd()


class FileSystemBuilder:
    """File and folder organization workflow."""

    def __init__(self, root_path) -> None:
        """Initialize a new instance of the FileSystemBuilder class.

        Args:
            root_path (str): The path of the working directory.
        """
        self.root_path = root_path

    def create_dir(self):
        """Create 'convertidos' and 'procesados' folders."""

        folders = ["convertidos", "procesados"]
        for folder_name in folders:
            if not (self.root_path / folder_name).exists():
                (self.root_path / folder_name).mkdir(parents=True)

    def get_studies(self):
        """Get only studies folders present in the working directory. Returns a list
        with the names of the studies folders.

        Returns:
            list: list of paths to the studies folders in the working directory.
        """

        not_studies = ["procesados", "convertidos", "supplfiles", ".DS_Store"]
        return [s for s in os.listdir(self.root_path) if s not in not_studies]

    def convert_bru_to_nii(self):
        """Convert all studies present in the workinf folder from Bruker to Niftii.
        Converted files will be stored in the 'convertidos' folder.
        """

        studies_names = self.get_studies()
        self.path_converted = self.root_path / "convertidos"
        converter = Bru2NiiConverter(self.root_path, self.path_converted, studies_names)
        converter.perform_conversion_bru2nii()

    def get_study_subfolders(self, directory: str):
        """Get subfolders of a directory located in root_path.

        Args:
            directory (str): Name of the directory.

        Returns:
            Generator: A generator that yields subfolder paths.
        """
        directory = self.root_path / directory
        return directory.glob("*/*")

    def rename_sutudies(self):
        """Rename studies located in 'convertidos' adding a
        prefix depending on their modality."""
        conv_study_subfolders = self.get_study_subfolders("convertidos")
        for subfolder in conv_study_subfolders:
            if subfolder.parts[-1].startswith("convertido"):
                self.add_method_to_subfolder(subfolder)

    def ask_preprocessing(self):
        """Select from a checklist those modalities to be processed.

        Returns:
            list: list of str with the selected modalities.
        """

        print(
            f"\n{hmg.ask}Marca qué modalidades deseas procesar en la ventana emergente."
        )

        # init tkinter
        root = tk.Tk()
        root.title("resomapper")

        row = 1
        selected_modals = []
        modalities = ["T1", "T2", "T2E", "DTI", "MT"]

        # add label
        tk.Label(root, text="Selecciona las modalidades que desees procesar.").grid(
            row=0, sticky="w"
        )

        # create checklist
        for modal in modalities:
            var = tk.IntVar()
            selected_modals.append(var)
            tk.Checkbutton(root, text=modal, variable=var).grid(row=row, sticky="w")
            row += 1

        # create button to close the window
        tk.Button(root, text="Aceptar", command=root.destroy).grid(
            row=6, sticky="w", pady=4
        )
        # tk.mainloop()
        root.mainloop()  # changed by raquel... not sure if necessary

        return [
            modalities[idx]
            for idx in range(len(modalities))
            if selected_modals[idx].get() == 1
        ]

    def get_converted_files(self, known_modals=False):
        """Get the files' names of those that we want to transfer from 'convertidos'
        to 'procesados' folder.

        Returns:
            list: a list including *method.txt, *.nii, *DwEffBval.txt and
                *DwGradVec.txt files.
        """

        # add an uderscore to distingish T2 from T2E and change DTI per DT
        modals = []
        method_files = []
        nii_files = []
        dti_files = []
        # ask user for which modalities are desired to be processed
        if known_modals is False:
            self.modals_to_process = self.ask_preprocessing()

            for modal in self.modals_to_process:
                if modal == "DTI":
                    modals.append("DT_")
                else:
                    modals.append(modal + "_")

            for modal in modals:
                method_files += list(
                    self.path_converted.glob(f"*/{modal}*/*method.txt")
                )
                nii_files += list(self.path_converted.glob(f"*/{modal}*/*.nii*"))
                dti_files += list(
                    self.path_converted.glob(f"*/{modal}*/*DwEffBval.txt")
                ) + list(self.path_converted.glob(f"*/{modal}*/*DwGradVec.txt"))

        else:
            for modal in known_modals:
                if modal == "DTI":
                    modals.append("DT_")
                else:
                    modals.append(modal + "_")

            for modal in known_modals:
                method_files += list(
                    self.path_converted.glob(f"*/{modal}*/*method.txt")
                )
                nii_files += list(self.path_converted.glob(f"*/{modal}*/*.nii*"))
                dti_files += list(
                    self.path_converted.glob(f"*/{modal}*/*DwEffBval.txt")
                ) + list(self.path_converted.glob(f"*/{modal}*/*DwGradVec.txt"))

        return method_files + nii_files + dti_files

    def transfer_files(self, src_paths=None, dst_paths=None):
        """Transfer files from 'convertidos' to 'procesados' folder.
        If folder alredy exists in destiny, it will not be overwritten.

        Args:
            src_paths (list(Path)): Paths to source folder.
                Defaults to None (automatically selected).
            dst_paths (list(Path)): Paths to destination folder.
                Defaults to None (automatically selected).
        """

        # replicate the file directory from 'convertidos' to 'procesados' taking
        # into account those modalities that user wants to process. Get the files
        # we want to mirror in 'procesados' folder.
        if src_paths is None:
            src_paths = self.get_converted_files()  # path of converted files
            dst_paths = [
                Path(
                    str(f)
                    .replace("convertidos", "procesados")
                    .replace("convertido", "procesado")
                )
                for f in src_paths
            ]

        # create directory tree at the destinatinon
        for src_path, dst_path in zip(src_paths, dst_paths):
            # if we have alredy processed a modality, it will not be trasferred
            if not dst_path.exists():
                sub_study_path = Path("/".join(dst_path.parts[:-1]))
                if not sub_study_path.exists():
                    sub_study_path.mkdir(parents=True)

                # copy files from source to destination
                try:
                    shutil.copy(src_path, dst_path)
                except Exception:
                    print(
                        f'{hmg.error}No se ha podido trasferir el \
                            archivo {src_path.split("/|//")[-1]}'
                    )

    # def add_method_to_subfolder2(self, study_subfolder: str):
    #     """Adds method (T1, T2, T2*, D, MTon, MToff) to study subfolder name.
    #     It discriminates by adquisition and method.

    #     Args:
    #         study_subfolder (str): Name or path of the study subfolder.

    #     The 'acquisition_method.txt' file located in the study subfolder to determine
    #     the acquisition method.

    #     The following acquisition methods are handled:
    #     - "RAREVTR": T1 modality.
    #     - "MGE": T2* modality.
    #     - "DtiEpi": Diffusion (DT) modality.
    #     - "MSME": T2, M0, or MT modality.

    #     For "MSME" acquisition method, it additionally reads the '*method.txt' file in
    #     the subfolder to determine the specific method.
    #     - If the method contains "EffectiveTE" and its length is greater than 35, the
    #       subfolder is renamed as T2.
    #     - If the method contains "MagTransOnOff = On", the subfolder is
    #       renamed as MTon.
    #     - If the method contains "MagTransOnOff = Off" and
    #       "DigFilter = Digital_Medium", the subfolder is renamed as MToff.
    #     """

    #     f_adq = "acquisition_method.txt"
    #     path_adq = study_subfolder / f_adq

    #     try:
    #         with open(path_adq, "r") as f:
    #             adq_lines = f.readlines()
    #     except FileNotFoundError:
    #         # patch to avoid 'variable referenced before assignment error'
    #         adq_lines = [""]

    #     # rename study subfolder
    #     if adq_lines[0] == "RAREVTR":  # T1
    #         r_study_subfolder = Path("/".join(study_subfolder.parts[:-1])) / (
    #             "T1_" + study_subfolder.parts[-1]
    #         )
    #         os.rename(study_subfolder, r_study_subfolder)

    #     elif adq_lines[0] == "MGE":  # T2STAR
    #         r_study_subfolder = Path("/".join(study_subfolder.parts[:-1])) / (
    #             "T2E_" + study_subfolder.parts[-1]
    #         )
    #         os.rename(study_subfolder, r_study_subfolder)

    #     elif adq_lines[0] == "DtiEpi":  # DIFFUSION
    #         r_study_subfolder = Path("/".join(study_subfolder.parts[:-1])) / (
    #             "DT_" + study_subfolder.parts[-1]
    #         )
    #         os.rename(study_subfolder, r_study_subfolder)

    #     elif adq_lines[0] == "MSME":  # T2, M0 or MT
    #         f_method = study_subfolder.parts[-1] + "_method.txt"
    #         path_met = study_subfolder / f_method  # path to *method.txt file

    #         try:
    #             with open(path_met, "r") as f:
    #                 met_lines = f.readlines()
    #         except FileNotFoundError:
    #             print(f"{hmg.error}Archivo no encontrado.")

    #         for line in met_lines:
    #             if not line.startswith("EffectiveTE"):
    #                 continue
    #             elif len(line) > 35:
    #                 r_study_subfolder = Path("/".join(study_subfolder.parts[:-1])) / (
    #                     "T2_" + study_subfolder.parts[-1]
    #                 )
    #                 os.rename(study_subfolder, r_study_subfolder)
    #                 return None
    #             else:
    #                 if "MagTransOnOff = On \n" in met_lines:
    #                     r_study_subfolder = Path(
    #                         "/".join(study_subfolder.parts[:-1])
    #                     ) / ("MT_" + study_subfolder.parts[-1])
    #                     os.rename(study_subfolder, r_study_subfolder)
    #                 elif ("MagTransOnOff = Off \n" in met_lines) and (
    #                     "DigFilter = Digital_Medium \n" in met_lines
    #                 ):
    #                     r_study_subfolder = Path(
    #                         "/".join(study_subfolder.parts[:-1])
    #                     ) / ("M0_" + study_subfolder.parts[-1])
    #                     os.rename(study_subfolder, r_study_subfolder)
    #                 return None

    def add_method_to_subfolder(self, study_subfolder: str):
        """Adds method (T1, T2, T2*, D, MTon, MToff) to study subfolder name.
        It discriminates by adquisition and method.

        Args:
            study_subfolder (str): Name or path of the study subfolder.

        The 'acquisition_method.txt' file located in the study subfolder to determine
        the acquisition method.

        The following acquisition methods are handled:
        - "RAREVTR": T1 modality.
        - "MGE": T2* modality.
        - "DtiEpi": Diffusion (DT) modality.
        - "MSME": T2, M0, or MT modality.

        For "MSME" acquisition method, it additionally reads the '*method.txt' file in
        the subfolder to determine the specific method.
        - If the method contains "EffectiveTE" and its length is greater than 35, the
          subfolder is renamed as T2.
        - If the method contains "MagTransOnOff = On", the subfolder is renamed as MTon.
        - If the method contains "MagTransOnOff = Off" and "DigFilter = Digital_Medium",
          the subfolder is renamed as MToff.
        """

        f_adq = "acquisition_method.txt"
        path_adq = study_subfolder / f_adq

        try:
            with open(path_adq, "r") as f:
                adq_lines = f.readlines()
        except FileNotFoundError:
            # patch to avoid 'variable referenced before assignment error'
            adq_lines = [""]

        acquisition_method = adq_lines[0].strip()

        new_prefix = None

        # Rename study subfolder based on acquisition method
        if acquisition_method == "RAREVTR":  # T1
            new_prefix = "T1_"
        elif acquisition_method == "MGE":  # T2STAR
            new_prefix = "T2E_"
        elif acquisition_method == "DtiEpi":  # DIFFUSION
            new_prefix = "DT_"
        elif acquisition_method == "MSME":  # T2, M0 or MT
            f_method = study_subfolder.parts[-1] + "_method.txt"
            path_met = study_subfolder / f_method  # path to *method.txt file

            try:
                with open(path_met, "r") as f:
                    met_lines = f.readlines()
            except FileNotFoundError:
                print(f"{hmg.error}Archivo no encontrado.")
                return None

            for line in met_lines:
                if line.startswith("EffectiveTE") and len(line) > 35:
                    new_prefix = "T2_"
                    break
                elif line == "MagTransOnOff = On \n":
                    new_prefix = "MT_"
                    break
                elif (
                    line == "MagTransOnOff = Off \n"
                    and "DigFilter = Digital_Medium \n" in met_lines
                ):
                    new_prefix = "M0_"
                    break

        if new_prefix:
            r_study_subfolder = Path("/".join(study_subfolder.parts[:-1])) / (
                new_prefix + study_subfolder.parts[-1]
            )
            os.rename(study_subfolder, r_study_subfolder)

    def get_modality(self, study_subfolder_path: str):
        """Returns the modality of a subfolder path such as
        "C:// * //T2_convertidos*"

        Args:
            study_subfolder_path (str): Path to the subfolder.

        Returns:
            str: The modality of the subfolder.
        """
        if study_subfolder_path.parts[-1][:3] == "T1_":
            return "T1"
        elif study_subfolder_path.parts[-1][:3] == "T2_":
            return "T2"
        elif study_subfolder_path.parts[-1][:3] == "T2E":
            return "T2E"
        elif study_subfolder_path.parts[-1][:3] == "DT_":
            return "DT"
        elif study_subfolder_path.parts[-1][:3] == "MT_":
            return "MT"
        else:
            return "M0"

    def get_selected_studies(self):
        """Returns those studies that will be processed. Checks if a modality
        has alredy been processed. In that case gives two options:
            - Remove it and process it again.
            - Do not process it again.

        Returns:
            subfolders_paths (list): Paths to modality subfolders to be processed.
            modals_to_process (list): Modalities present in the studies to process.
        """

        self.proc_study_subfolders = self.get_study_subfolders("procesados")

        subfolders_paths = []
        if "DTI" in self.modals_to_process:
            self.modals_to_process[self.modals_to_process.index("DTI")] = "DT"

        for subfolder in self.proc_study_subfolders:
            # check if a modality has to be processed
            processed_modal = self.get_modality(subfolder)
            for modal in self.modals_to_process:
                if modal == processed_modal:
                    if (
                        (("ADC_map.nii" in os.listdir(subfolder)) and modal == "DT")
                        or (("mapas" in os.listdir(subfolder)) and fnmatch(modal, "T*"))
                        or ("MT_map" in str(list(os.walk(subfolder))) and modal == "MT")
                    ):
                        patient = "_".join(subfolder.parts[-2].split("_")[1:])
                        msg = (
                            f"La modalidad {processed_modal} del estudio {patient} ya "
                            "ha sido procesada.\n¿Desea volver a procesarla?"
                        )
                        process_again = ut.ask_user(msg)
                        if process_again:  # if process again
                            ready = ""
                            while ready != "y":
                                msg = (
                                    f"\n{hmg.warn}El resultado del procesamiento "
                                    f"anterior de {processed_modal} del estudio "
                                    f"{patient} no se conservará.\n"
                                    f"\n{hmg.ask}Si desea guardarlo debe hacerlo ahora."
                                    f' Pulse "y" para continuar.\n{hmg.pointer}'
                                )
                                ready = input(msg)
                                ready = ready.lower()
                    else:
                        process_again = True

                    if process_again:
                        # remove folder and files contained in it
                        shutil.rmtree(str(subfolder))
                        # create folder again
                        # src_path = Path(
                        #     str(subfolder)
                        #     .replace("procesados", "convertidos")
                        #     .replace("procesado", "convertido")
                        # )
                        files_to_transfer = self.get_converted_files([processed_modal])
                        dst_paths = [
                            Path(
                                str(f)
                                .replace("convertidos", "procesados")
                                .replace("convertido", "procesado")
                            )
                            for f in files_to_transfer
                        ]
                        self.transfer_files(files_to_transfer, dst_paths)
                        subfolders_paths.append(subfolder)

        return subfolders_paths, self.modals_to_process


###############################################################################
# From Bruker to Nifti format
###############################################################################


class Bru2NiiConverter:
    """Conversion from Bruker files to NIfTI files workflow."""

    def __init__(self, root_path: str, converted_path: str, studies: list) -> None:
        """Initialize a new instance of the Bru2NiiConverter class.

        Args:
            root_path (str): Path of the working directory.
            converted_path (str): Path of the output folder ('convertidos').
            studies (list): List of paths to the studies folders in the working dir.
        """
        self.root_path = root_path
        self.converted_path = converted_path
        self.studies = studies

    def convert_bru_2_nii(self, study):
        """Convert Bruker files of one study to NIfTI.

        Args:
            study (str): Name of the study to convert.

        Note:
            To understand the Bruker2Nifti converter, you can check a example in:
            https://github.com/SebastianoF/bruker2nifti/wiki/
            Setting get_method or save_human_readable to False is
            extremely not recommended
        """
        pfo_study_in = str(self.root_path / study)
        pfo_study_out = str(self.root_path / "convertidos")

        # instantiating the converter
        study_name = "convertido_" + study
        bru = Bruker2Nifti(pfo_study_in, pfo_study_out, study_name=study_name)
        bru.verbose = 0
        bru.correct_slope = True  # grayscale correction based on slope
        bru.get_acqp = False
        bru.get_method = True
        bru.get_reco = False
        bru.nifti_version = 1
        bru.qform_code = 1
        bru.sform_code = 2
        bru.save_human_readable = True  # stores parameters in a .txt
        bru.save_b0_if_dwi = False

        # perform conversion
        bru.convert()

    def perform_conversion_bru2nii(self):
        """Check if any studies have already been converted and convert those that
        haven't or those that the user wants to reconvert.

        Three cases:
        1. No study has been converted
        2. All studies have been converted
        3. Some studies have been converted
        """
        conv_f = os.listdir(self.converted_path)  # converted folder
        # 1. If list is empty converts all raw data folders from bruker to nii
        if not conv_f:
            conv_studies = []
            for study in self.studies:
                self.convert_bru_2_nii(study)
                conv_studies.append(study)
            # df_conv_studies = pd.DataFrame(conv_studies)
            print(f"\n{hmg.info}Ya se han convertido todos los estudios.")

        else:
            alredy_conv = []
            not_conv = []
            for study in self.studies:
                if "convertido_" + study in conv_f:
                    alredy_conv.append(study)
                else:
                    not_conv.append(study)

            df_conv = pd.DataFrame(alredy_conv, columns=["Estudios"])
            df_not_conv = pd.DataFrame(not_conv, columns=["Estudios"])

            if not_conv:
                # 2. Some studies converted
                print(
                    f"\n{hmg.info}Ya se habían convertido los siguientes \
                        estudios: \n {df_conv}\n"
                )
                print(
                    f"\n{hmg.info}Estos estudios no están convertidos:   \
                        \n {df_not_conv} \n"
                )

                perform_conv = ut.ask_user("¿Desea convertirlos?")
                if perform_conv:
                    for nc_study in not_conv:
                        self.convert_bru_2_nii(nc_study)
                print(
                    f"{hmg.info}Ya se han convertido todos los \
                    estudios, que son los siguientes:\n"
                    f"{pd.concat([df_conv, df_not_conv], ignore_index=True)}"
                )
            else:
                # 3. All studies converted
                print(f"\n{hmg.info}Ya se han convertido todos los estudios.")
