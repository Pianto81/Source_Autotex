import os
import subprocess as sp

class Autotex():
    '''
    Transforme une image de texture en vtf.

    Paramètres
    --------

    folder: `str` -> le chemin d'accès vers le dossier à scanner pour trouver des textures

    output: `str` -> le chemin d'accès vers le dossier de sortie
    '''


    def __init__(self, folder:str, output:str):
        if not os.path.isdir(folder):
            os.mkdir(folder)
        if not os.path.isdir(output):
            os.mkdir(output)
        self.folder = folder
        self.output = output
        self.texfiles = []
    
    def convert_to_dtx5_vtf(self, name:str, pbr:bool, file_format='png', vtf_format='dxt5'):
        '''Convertit les textures du dossier en vtf.

        name: `str` -> le nom de la texture en sortie

        pbr: `bool` -> indique si le dossier est composé de 3 textures, pour le rennomage avec préfixe

        file_format: `str` -> le format des textures d'origine
        '''

        path = f"{self.folder}\*.{file_format}"

        if pbr:
            sp.run(f".//bin//VTFCmd.exe -folder {path} -output {self.output} -format {vtf_format}")
            self.rename_pbr(name)
        else:
            sp.run(f".//bin//VTFCmd.exe -folder {path} -output {self.output} -format {vtf_format} -prefix RENAMETHIS")
            self.rename(name)

    
    def rename_pbr(self, name:str):
        file_type = ''
        for file in os.listdir(self.output):

            if file[-3:] == 'vtf' and '0' in file:
                for char in file:
                    if char == '0':
                         break
                    file_type += char

                if file_type == "basecolor":
                    file_type = "diff"

                if file_type in ["diff", "normal", "phong"]:
                    os.rename(f"{self.output}/{file}", f"{self.output}/{name}_{file_type}.vtf")
                    file_type = ''

    def rename(self, name:str):
        for file in os.listdir(self.output):
            if file[-3:] == 'vtf' and "RENAMETHIS" in file:
                os.rename(f"{self.output}/{file}", f"{self.output}/{name}.vtf")