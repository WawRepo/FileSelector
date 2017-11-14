import os

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
        raise FileExistsError("Specified root does not exist")

    if not os.path.isfile(file_config):
        raise FileExistsError("Specified file config does not exist")

    if not os.path.exists(output_directory):
        raise FileExistsError("Specified output folder does not exist")