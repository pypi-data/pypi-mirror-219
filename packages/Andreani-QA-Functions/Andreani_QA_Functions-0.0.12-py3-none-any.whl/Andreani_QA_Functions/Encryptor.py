# -*- coding: utf-8 -*-
import bz2
import os
import xml.etree.ElementTree as Et
from cryptography.fernet import Fernet


class Encryptor:
    def __init__(self, father_attribute, attribute_to_search, data_find, data_inner_key, enviroment_var,
                 environment_back_up_file_name, environment_proj_file_path, xml_en_consola=False):
        self.ENVIROMENT_VAR = enviroment_var
        self.ENVIRONMENT_BACKUP_FILE_NAME = environment_back_up_file_name
        self.ENVIROMENT_PROJ_FILE_PATH = environment_proj_file_path
        self.father_attribute = father_attribute
        self.atribute_to_search = attribute_to_search
        self.data_find = data_find
        self.data_inner_key = data_inner_key
        self.key = self.get_enviroment_key_from_file()
        self.encriptor = Fernet(self.key)
        self.xml_en_consola = xml_en_consola

    def main(self):
        data_returned = None
        # Proceso:
        # 1 Si el archivo del proyecto existe
        if self.project_file_exists() is True:
            print("Archivo del proyecto encontrado!")
            data_returned = self.get_data_from_proj_file(self.father_attribute,
                                                         self.atribute_to_search,
                                                         self.data_find,
                                                         self.data_inner_key)
            # Si la información obtenida del archivo del proyecto no existe
            if data_returned is None:
                print(f"Parace que el archivo no contiene la información buscada: {self.data_inner_key}")
                print(f"Buscando {self.data_inner_key} ahora en el archivo BackUp")
                # reviso que el archivo backup exista
                if self.backup_file_exists() is True:
                    print("Archivo BackUp encontrado!")
                    # obtengo el dato si existe, desde el archivo backup
                    data_returned = self.get_data_from_backup_file(self.father_attribute,
                                                                   self.atribute_to_search,
                                                                   self.data_find,
                                                                   self.data_inner_key)
                    # Si el dato existe
                    if data_returned is not None:
                        print("Se a encontrado el dato buscado, pero este se encuentra en el archivo BackUp")
                        print(f"Copiando [{self.father_attribute};{self.atribute_to_search}] al archivo del "
                              f"proyecto actual")
                        # Agrego la información faltante desde el archivo backup, al archivo del proyecto
                        self.add_data_to_proj_file(self.father_attribute, self.atribute_to_search, self.data_find)
                        print("La información fué agregada al archivo del proyecto actual correctamente!")
                    # Si el dato NO existe
                    else:
                        # Skiptest para implementación
                        print("Parace que ninguno de los archivos contiene la información buscada")
                else:
                    # Si el archivo backup no existe
                    # Lo creo vacio
                    # Skiptest para implementación
                    print("Archivo BackUp no encontrado!")
                    print("Creando archivo BackUp con template base para futuras ejecuciones")
                    self.create_backup_file()
                    print("Archivo BackUp creado con éxito!")
        else:
            print("Archivo del proyecto no encontrado!")
            # 2 - Si el archivo del proyecto NO existe, reviso que el archivo backup exista
            if self.backup_file_exists() is True:
                print("Archivo BackUp encontrado!")
                # Si el archivo backup existe, crea un template en la ubicación del proyecto
                print("Creando archivo de proyecto actual con template base para futuras ejecuciones")
                self.create_project_file()
                print("Archivo del proyecto creado con éxito!")
                self.add_data_to_proj_file(self.father_attribute, self.atribute_to_search, self.data_find)
                print("Data transferida al archivo del proyecto actual")
                # Corro el proceso otra vez
                data_returned = Core(self.father_attribute, self.atribute_to_search, self.data_find,
                                     self.data_inner_key).main()
            # Si no existe el archivo del proyecto y tampoco existe el archivo backup
            else:
                # Skiptest para implementación
                print("No se puede continuar sin la presencia de al menos uno de los archivos environment_access.xml")
        return data_returned

    def project_file_exists(self):
        project_exists = False
        if os.path.exists(self.ENVIROMENT_PROJ_FILE_PATH) is True:
            project_exists = True
        return project_exists

    def backup_file_exists(self):
        ignored_exists = False
        # Si existe el archivo ignorado ubicado en testing-Automation devuelve True, sino existe False
        if os.path.exists(self.ENVIRONMENT_BACKUP_FILE_NAME):
            ignored_exists = True
        return ignored_exists

    ####################################################################################################################
    #                                           ENCRYPTOR FUNCTIONS                                                    #
    ####################################################################################################################

    def get_enviroment_key_from_file(self):

        """

            Description:
                Obtiene la key (bytes) de la variable de entorno "PYBOT_KEY".

            Returns:
                Devuelve la key en bytes.

        """

        key = ""
        enviroment_key = os.getenv(self.ENVIROMENT_VAR)
        if enviroment_key is not None:
            try:
                with open(enviroment_key, 'rb') as file:
                    key = file.read()
            except FileNotFoundError:
                print(f"No existe el archivo '{enviroment_key}'")
        else:
            print(f"No se encuentra cargada correctamente la variable de entorno f{self.ENVIROMENT_VAR}")
        return key

    # Decript
    def decompress_and_deencrypt_xml(self, read_file):
        if self.is_file_encrypted(read_file) is True:
            try:
                with open(read_file, 'rb') as file:
                    data = file.read()
                deencrypted_data = self.encriptor.decrypt(data)
                decompressed_data = bz2.decompress(deencrypted_data)
                file.close()
                os.remove(read_file)
                with open(read_file, 'wb') as output_file:
                    output_file.write(decompressed_data)
            except FileNotFoundError:
                print("El archivo buscado no existe en el directorio especificado.")
        else:
            print(f"No se puede desencryptar el archivo, ya que este es su estado actual -> {read_file}")

    # Encript
    def compress_and_encrypt_xml(self, read_file):
        if self.is_file_encrypted(read_file) is not True:
            try:
                with open(read_file, 'rb') as file:
                    data = file.read()
                compressed_data = bz2.compress(data)
                encrypted_data = self.encriptor.encrypt(compressed_data)
                file.close()
                os.remove(read_file)
                with open(read_file, 'wb') as output_file:
                    output_file.write(encrypted_data)
            except FileNotFoundError:
                print("El archivo buscado no existe en el directorio especificado.")
        else:
            print(f"No se puede encryptar el archivo, ya que este es su estado actual -> {read_file}")

    # obtener data requerida desde el archivo
    def get_data_from_proj_file(self, father_attribute, atribute_to_search, dato_a_buscar, inner_search):
        return_data = None
        try:
            read_xml_file, project_tree = self.get_xml_root(self.ENVIROMENT_PROJ_FILE_PATH)
            for element in read_xml_file.findall(f"./{father_attribute}[@{atribute_to_search}='{dato_a_buscar}']/"):
                if element.tag == inner_search and (element.text is not None or element.text != ""
                                                    or element.text != " "):
                    return_data = element.text
        except Exception:
            print("Ha Ocurrido un Error en el Tiempo de Ejecución -> ERROR CODE 204 (Encriptor)")

        return return_data

    def get_data_from_backup_file(self, father_attribute, atribute_to_search, dato_a_buscar, inner_search):
        return_data = None
        try:
            read_xml_file, backup_tree = self.get_xml_root(self.ENVIRONMENT_BACKUP_FILE_NAME)
            for element in read_xml_file.findall(f"./{father_attribute}[@{atribute_to_search}='{dato_a_buscar}']/"):
                if element.tag == inner_search and (element.text is not None or element.text != ""
                                                    or element.text != " "):
                    return_data = element.text
        except Exception:
            raise "Ha Ocurrido un Error en el Tiempo de Ejecución -> ERROR CODE 204 (Encriptor)"

        return return_data

    # Actualizar data
    def add_data_to_proj_file(self, father_attribute, atribute_to_search, dato_a_buscar):
        # Necesito:
        #   *   Ahora que sé que el dato existe en el archivo backup, obtenerlo con su bloque de información.
        #   *   VALIDAR MEDIANTE TAG SI ESTE ELEMENTO EXISTE EN EL ARCHIVO
        backup_xml, backup_tree = self.get_xml_root(self.ENVIRONMENT_BACKUP_FILE_NAME)
        project_xml, project_tree = self.get_xml_root(self.ENVIROMENT_PROJ_FILE_PATH)
        self.validate(project_xml)
        # Create a new CLAVES element
        new_claves = Et.Element('CLAVES')
        new_claves.set(atribute_to_search, dato_a_buscar)
        # Create sub-elements for the new CLAVES
        port = Et.SubElement(new_claves, 'PORT')
        ip = Et.SubElement(new_claves, 'IP')
        environment = Et.SubElement(new_claves, 'ENVIRONMENT')
        base = Et.SubElement(new_claves, 'BASE')
        user = Et.SubElement(new_claves, 'USER')
        password = Et.SubElement(new_claves, 'PASS')
        # Append the new CLAVES element to the root
        project_xml.append(new_claves)
        for element in backup_xml.findall(f"./{father_attribute}[@{atribute_to_search}='{dato_a_buscar}']/"):
            if element.tag == "PORT":
                port.text = element.text
            if element.tag == "IP":
                ip.text = element.text
            if element.tag == "ENVIRONMENT":
                environment.text = element.text
            if element.tag == "BASE":
                base.text = element.text
            if element.tag == "USER":
                user.text = element.text
            if element.tag == "PASS":
                password.text = element.text
        Et.indent(project_xml, "   ")
        project_tree.write(self.ENVIROMENT_PROJ_FILE_PATH)
        self.compress_and_encrypt_xml(self.ENVIROMENT_PROJ_FILE_PATH)
        if self.xml_en_consola is True:
            Et.dump(project_xml)
            print("---------------------")
            Et.dump(backup_xml)

    def create_backup_file(self):
        xml_body = b'<?xml version="1.0" encoding="UTF-8" ?> ' \
                   b'<root>' \
                   b'<!--<CLAVES id="Test_Id">-->' \
                   b'<!--<PORT>9999</PORT>-->' \
                   b'<!--<IP>255.255.255.255</IP>-->' \
                   b'<!--<ENVIRONMENT>Test</ENVIRONMENT>-->' \
                   b'<!--<BASE>SQL_BASE</BASE>-->' \
                   b'<!--<USER>Test_User</USER>-->' \
                   b'<!--<PASS>Test_Password</PASS>-->' \
                   b'<!--</CLAVES>-->' \
                   b'</root>'
        # Formateo del archivo output
        compressed_data = bz2.compress(xml_body)
        encripted_xml = self.encriptor.encrypt(compressed_data)
        with open(self.ENVIRONMENT_BACKUP_FILE_NAME, 'wb') as output_file:
            output_file.write(encripted_xml)
        output_file.close()

    def create_project_file(self):
        with open(rf"{self.ENVIROMENT_PROJ_FILE_PATH}", "wb") as env_file:
            env_file.write(b'<root>\n')
            env_file.write(b'</root>\n')
        tree = Et.parse(self.ENVIROMENT_PROJ_FILE_PATH)
        root = tree.getroot()
        Et.indent(root, "   ")
        tree.write(self.ENVIROMENT_PROJ_FILE_PATH)
        self.compress_and_encrypt_xml(self.ENVIROMENT_PROJ_FILE_PATH)

    def get_xml_root(self, file_loc):
        self.decompress_and_deencrypt_xml(file_loc)
        tree = Et.parse(file_loc)
        current_root = tree.getroot()
        self.compress_and_encrypt_xml(file_loc)
        return current_root, tree

    def is_file_encrypted(self, file_path):
        try:
            # Intentar analizar el archivo XML
            Et.parse(file_path)
            return False
        except Et.ParseError:
            # Si se produce un error al analizar, se considera que el archivo está encriptado
            return True

    def validate(self, root_tree):
        elemento_prueba = root_tree.find(f'.//*[@{self.atribute_to_search}="{self.data_find}"]')
        if elemento_prueba is not None:
            root_tree.remove(elemento_prueba)
