import os
from error_classes import FileExistsErrorNoConfig\
    , FileExistsErrorNoOutputFolder\
    , FileExistsErrorNoRoot\
    , FileExistsErrorFileAlreadyExist

def extract_file_name(sub_path):
    """
    :param sub_path: full file path. Ex. c:\home\user\1.txt
    :return: filename. Ex. 1.txt
    """
    if sub_path.rfind("\\") > 0:
        return sub_path[sub_path.rfind("\\") + 1:]
    return sub_path


def generate(root_catalogue, file_config, output_directory):
    """
    :param root_catalogue: root catalogue that is used as a starting  point to
    select all files from config fils
    :param file_config: file that includes all files required from directory
     root
    :param output_directory: path where all files specified in config file
    :return:
    """

    if not os.path.exists(root_catalogue):
        raise FileExistsErrorNoConfig("Specified root does not exist")

    if not os.path.isfile(file_config):
        raise FileExistsErrorNoOutputFolder("Specified file config does not exist")

    if not os.path.exists(output_directory):
        raise FileExistsErrorNoRoot("Specified output folder does not exist")

    files_to_lookup = [file.rstrip() for file in open(file_config)]

    from shutil import copyfile
    for file in files_to_lookup:
        file_name_to_copy = extract_file_name(file)
        if os.path.isfile(output_directory + "\\" + file_name_to_copy):
            raise FileExistsErrorFileAlreadyExist("File already exists")
        copyfile(root_catalogue + "\\" + file, output_directory + "\\" + file_name_to_copy)

    copyfile(file_config,
             output_directory + "\\" + extract_file_name(file_config))
