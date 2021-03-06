import os
import argparse
from error_classes import FileExistsErrorNoConfig,\
    FileExistsErrorNoOutputFolder,\
    FileExistsErrorNoRoot,\
    FileExistsErrorFileAlreadyExist


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def not_comment_line(line, comment_identifier="#"):
    """
    :param line:
    :param comment_identifier:
    :return:
    """
    return not line.startswith(comment_identifier)


def extract_file_name(sub_path):
    """
    :param sub_path: full file path. Ex. c:\home\ user\1.txt
    :return: filename. Ex. 1.txt
    """

    if sub_path.rfind("\\") > 0:
        return sub_path[sub_path.rfind("\\") + 1:]
    return sub_path


def generate(root_catalogue, file_config, output_directory):
    """
    :param root_catalogue: root catalogue that is used as a starting  point to
    select all files from config file
    :param file_config: file that includes all files required from directory
     root
    :param output_directory: path where all files specified in config file
    :return:
    """

    if not os.path.exists(root_catalogue):
        raise FileExistsErrorNoConfig("Specified root does not exist")

    if not os.path.isfile(file_config):
        raise FileExistsErrorNoOutputFolder("Specified file config "
                                            "does not exist")

    if not os.path.exists(output_directory):
        raise FileExistsErrorNoRoot("Specified output folder does not exist")

    with open(file_config) as files:
        files_to_lookup = [file.rstrip() for file in files
                           if not_comment_line(file.rstrip())]
        files.close()

    from shutil import copyfile
    for file in files_to_lookup:
        file_name_to_copy = extract_file_name(file)
        if os.path.isfile(output_directory + "\\" + file_name_to_copy):
            raise FileExistsErrorFileAlreadyExist("File already exists")
        copyfile(root_catalogue + "\\"
                 + file, output_directory + "\\" + file_name_to_copy)

    copyfile(file_config,
             output_directory + "\\" + extract_file_name(file_config))


def aggregate(file_config, directory_with_generated_files,
              delimiter="\ngo\ncommit\ngo\n"):
    """
    :param file_config:
    :param directory_with_generated_files:
    :param delimiter:
    :return:
    """

    aggregate_file_name = directory_with_generated_files \
                          + "\\" + extract_file_name(file_config) + ".agg"
    touch(aggregate_file_name)

    with open(file_config) as files:
        files_to_lookup = [extract_file_name(file.rstrip()) for file in files
                           if not_comment_line(file.rstrip())]
        files.close()

    with open(aggregate_file_name, "w") as file_output:
        for f in files_to_lookup:
            with open(directory_with_generated_files + "\\" + f, "r") \
                    as file_input:
                for line in file_input:
                    file_output.write(line)
                file_input.close()
            file_output.writelines(delimiter)
            # file_ouput.writelines("\ngo\n")
        file_output.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('root_catalogue',
                   help='root folder that is added as prefix'
                        ' to files from file config')
    p.add_argument('file_config',
                   help='path to file with list of files to be generated')
    p.add_argument('output_directory', help='output directory to be created')
    p.add_argument('--aggregation_delimiter', '-a', default=r"\ngo\ncommit\ngo")

    arguments = p.parse_args()

    import shutil
    if os.path.exists(arguments.output_directory):
        shutil.rmtree(arguments.output_directory, ignore_errors=True)

    os.mkdir(arguments.output_directory)

    generate(arguments.root_catalogue, arguments.file_config,
             arguments.output_directory)
    aggregate(arguments.file_config, arguments.output_directory)

if __name__ == '__main__':
    main()
