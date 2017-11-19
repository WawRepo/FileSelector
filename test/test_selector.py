from unittest import TestCase
import os

from error_classes import FileExistsErrorNoConfig\
    , FileExistsErrorNoOutputFolder\
    , FileExistsErrorNoRoot\
    , FileExistsErrorFileAlreadyExist

from file_selector import generate, extract_file_name

class TestFileSelector(TestCase):

    def touch(self, fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    def setUp(self):
        import shutil

        self.test_dir = os.getcwd() + "\\foo"

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

        os.makedirs(self.test_dir)
        path1 = self.test_dir + "\\folder1"
        path2 = self.test_dir + "\\folder2"
        path3 = self.test_dir + "\\folder3"
        os.makedirs(path1)
        os.makedirs(path2)
        os.makedirs(path3)

        self.touch(path1 + "\\file1.1")
        self.touch(path1 + "\\file1.2")
        self.touch(path1 + "\\file1.3")
        self.touch(path2 + "\\file2.1")
        self.touch(path2 + "\\file2.2")
        self.touch(path2 + "\\file2.3")
        self.touch(path3 + "\\file3.1")
        self.touch(path3 + "\\file3.2")
        self.touch(path3 + "\\file3.3")
        self.touch(self.test_dir + "\\file0.1")

        # self.files_list = self.test_dir + "\\files_list"
        # touch(self.files_list)
        # file = open(self.files_list, "w")
        # file.writelines("path1/file1.1" + "\n")
        # file.writelines("path1/file1.3" + "\n")
        # file.writelines("path1/file2.2" + "\n")
        # file.writelines("path1/file3.1" + "\n")
        # file.writelines("path1/file3.2" + "\n")
        # file.close()

        self.expected_dir = self.test_dir + "\\expected_dir"
        os.makedirs(self.expected_dir)

        self.touch(self.expected_dir + "\\file1.1")
        self.touch(self.expected_dir + "\\file1.3")
        self.touch(self.expected_dir + "\\file2.2")
        self.touch(self.expected_dir + "\\file3.1")
        self.touch(self.expected_dir + "\\file3.2")
        self.touch(self.expected_dir + "\\file0.1")

        from shutil import copyfile
        copyfile(os.getcwd() + "\\fileList.gen", self.expected_dir + "\\fileList.gen" )

    def testRaiseExeptionWhenRootFolderNotExist(self):
        self.assertRaises(FileExistsErrorNoConfig, lambda: generate("x","X","x"))

    def testRaiseExeptionWhenConfigFileNotExist(self):
        self.assertRaises(FileExistsErrorNoOutputFolder, lambda: generate(os.getcwd(),"X","x"))

    def testRaiseExeptionWhenOutputFolderNotExist(self):
        self.assertRaises(FileExistsErrorNoRoot,
                          lambda: generate(os.getcwd(), os.getcwd() + "\\fileList.gen", "x"))

    def testGenerate(self):
        output_dir = self.test_dir + "\\generated"
        config_file = os.getcwd() + "\\fileList.gen"
        os.makedirs(output_dir)
        generate(self.test_dir, config_file, output_dir)
        self.assertListEqual(os.listdir(self.expected_dir),os.listdir(output_dir))

    def _testGenerateFileNotExistInFolderStructure(self):
        pass

    def testGenerateFileExistTwiceInConfigFile(self):

        config_list = open("fileList.gen", 'r').read()
        config_list = config_list + "\n" + config_list.split("\n")[-2]
        file_name_with_duplicate = self.test_dir + "\\" + "file_list_with_duplicate.gen"

        self.touch(file_name_with_duplicate)
        open( file_name_with_duplicate,'w').writelines(config_list)

        output_dir = self.test_dir + "\\generated"
        os.makedirs(output_dir)

        self.assertRaises(FileExistsErrorFileAlreadyExist,
                          lambda: generate(self.test_dir
                                           , file_name_with_duplicate
                                           , self.test_dir + "\\generated" ))

    def testExtractFileName(self):
        self.assertEqual(extract_file_name("aa\\bb\\file1"), "file1")
        self.assertEqual(extract_file_name("file1"), "file1")



