import os
import sys
import errno
import pathlib
import tempfile
import unittest
import time
import shutil
import subprocess
from inspect import signature
from subprocess import Popen, PIPE
from tempfile import TemporaryDirectory
from multiprocessing.dummy import Pool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from poppdf import (
    image_from_path,
    xml_from_path,
    text_from_path
)
from poppdf.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFPopplerTimeoutError,
)

from functools import wraps

PROFILE_MEMORY = os.environ.get('PROFILE_MEMORY', False)

try:
    subprocess.call(
        ["pdfinfo", "-h"], stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w")
    )
    POPPLER_INSTALLED = True
except OSError as e:
    if e.errno == errno.ENOENT:
        POPPLER_INSTALLED = False




def get_poppler_path():
    return pathlib.Path(
        Popen(["which", "pdftoppm"], stdout=PIPE).communicate()[0].strip().decode()
    ).parent


class PDFConversionMethods(unittest.TestCase):

    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_xml_conversion_from_path(self):
        start_time = time.time()
        xml_file_from_path = xml_from_path("./tests/test.pdf")
        self.assertTrue(len(xml_file_from_path) == 1)
        print("test_conversion_from_path: {} sec".format(time.time() - start_time))

    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_text_conversion_from_path(self):
        start_time = time.time()
        text = text_from_path("./tests/test.pdf")
        self.assertTrue(text.strip()=="TEST TEST TEST")
        print("test_conversion_from_path: {} sec".format(time.time() - start_time))


    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path(self):
        start_time = time.time()
        images_from_path = image_from_path("./tests/test.pdf")
        self.assertTrue(len(images_from_path) == 1)
        print("test_conversion_from_path: {} sec".format(time.time() - start_time))


    
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = image_from_path("./tests/test.pdf", output_folder=path)
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir: {} sec".format(
                time.time() - start_time
            )
        )


    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_not_pdf(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            image_from_path("./tests/test.jpg")
        print("test_empty_if_not_pdf: {} sec".format(time.time() - start_time))

    
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_file_not_found(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            image_from_path("./tests/totally_a_real_file_in_folder.xyz")
        print("test_empty_if_file_not_found: {} sec".format(time.time() - start_time))

    
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_corrupted_pdf(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            image_from_path("./tests/test_corrupted.pdf")
        print("test_empty_if_corrupted_pdf: {} sec".format(time.time() - start_time))

    ## Test first page


    ## Test output as jpeg


    
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_jpeg_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = image_from_path(
                "./tests/test.pdf", output_folder=path, fmt="jpeg"
            )
            self.assertTrue(images_from_path[0].format == "JPEG")
            [im.close() for im in images_from_path]
        print(
            "test_conversion_to_jpeg_from_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )


    
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_png_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = image_from_path(
                "./tests/test.pdf", output_folder=path, fmt="png"
            )
            self.assertTrue(images_from_path[0].format == "PNG")
            [im.close() for im in images_from_path]
        print(
            "test_conversion_to_png_from_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )


    
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_cropbox(self):
        start_time = time.time()
        images_from_path = image_from_path("./tests/test.pdf", use_cropbox=True)
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_using_cropbox: {} sec".format(
                time.time() - start_time
            )
        )


    ## Tests multithreading

    
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_with_4_threads(self):
        start_time = time.time()
        images_from_path = image_from_path("./tests/test_14.pdf", thread_count=4)
        self.assertTrue(len(images_from_path) == 14)
        print(
            "test_conversion_from_path_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )


    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_xml_conversion_from_path_14_with_4_threads(self):
        start_time = time.time()
        images_from_path = xml_from_path("./tests/test_14.pdf", thread_count=4)
        self.assertTrue(len(images_from_path) == 14)
        print(
            "test_conversion_from_path_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )


    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_text_conversion_from_path_14_with_4_threads(self):
        start_time = time.time()
        images_from_path = text_from_path("./tests/test_14.pdf", thread_count=4)
        self.assertTrue(len(images_from_path) == 14)
        print(
            "test_conversion_from_path_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )


    # Testing custom exceptions

    @unittest.skipIf(POPPLER_INSTALLED, "Poppler is installed, skipping.")
    def test_pdfinfo_not_installed_throws(self):
        start_time = time.time()
        try:
            images_from_path = image_from_path("./tests/test_14.pdf")
            raise Exception("This should not happen")
        except PDFInfoNotInstalledError as ex:
            pass

        print(
            "test_pdfinfo_not_installed_throws: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_missingfonterror_throws(self):
        start_time = time.time()
        try:
            images_from_path = image_from_path("./tests/test_strict.pdf", strict=True)
            raise Exception("This should not happen")
        except PDFSyntaxError as ex:
            pass

        print("test_syntaxerror_throws: {} sec".format(time.time() - start_time))



if __name__ == "__main__":
    unittest.main()
