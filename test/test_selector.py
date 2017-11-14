from unittest import TestCase
import os

from file_selector import generate

class TestFileSelector(TestCase):

    def setUp(self):
        import shutil
        def touch(fname, times=None):
            with open(fname, 'a'):
                os.utime(fname, times)

        self.test_dir = os.getcwd() + "\\foo"

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

        os.makedirs(self.test_dir)
        path1 = self.test_dir + "\\path1"
        path2 = self.test_dir + "\\path2"
        path3 = self.test_dir + "\\path3"
        os.makedirs(path1)
        os.makedirs(path2)
        os.makedirs(path3)

        def touch(fname, times=None):
            with open(fname, 'a'):
                os.utime(fname, times)

        touch(path1 + "\\file1.1")
        touch(path1 + "\\file1.2")
        touch(path1 + "\\file1.3")
        touch(path2 + "\\file2.1")
        touch(path2 + "\\file2.2")
        touch(path2 + "\\file2.3")
        touch(path3 + "\\file1.1")
        touch(path3 + "\\file2.2")
        touch(path3 + "\\file3.3")

        self.files_list = self.test_dir + "\\files_list"
        touch(self.files_list)
        file = open(self.files_list, "w")
        file.writelines("path1/file1.1" + "\n")
        file.writelines("path1/file1.3" + "\n")
        file.writelines("path1/file2.2" + "\n")
        file.writelines("path1/file3.1" + "\n")
        file.writelines("path1/file3.2" + "\n")
        file.close()

        expected_dir = self.test_dir + "\\expected_dir"
        os.makedirs(expected_dir)

        touch(expected_dir + "\\file1.1")
        touch(expected_dir + "\\file1.3")
        touch(expected_dir + "\\file2.2")
        touch(expected_dir + "\\file3.1")
        touch(expected_dir + "\\file3.2")



    def testGenerate(self)
        output_dir = self.test_dir + ""
        pass