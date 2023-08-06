from unittest import TestCase
from time import sleep

import os
import unittest
import json
import string
import random
import re
import shutil

from blendedcli.helpers import *
from blendedUx.blended_flask.blended_hostlib.backend import FileSystemBackend
from blendedUx.blended_flask.blended_hostlib.network import Network
from blendedUx.blended_flask.blended_hostlib.controller import Controller
from blendedUx.blended_flask.blended_hostlib.exceptions import BlendedException, \
    PackageNameExistsException, AccountActivationException


blended_dir = get_blended_directory_path()
current_account = "sun72"
current_dir = os.path.join(blended_dir, current_account)
network = Network()
backend = FileSystemBackend(
                            current_dir, blended_dir=blended_dir,
                            current_account=current_account,
                            blended_directory_path=blended_dir)
controller = Controller(network, backend)



class NetworkTest(TestCase):
    """
    We are testing hub using hostlib_Network
    """
    def test_00_backend_intermediary(self):
        """
        get version from backend and save data on backend
        """
        try:
            package_obj = controller.get_package(package_name="sun72/business_theme", format='context', version="1.0")
        except OSError:
            package_obj = {} 
        self.assertIsInstance(package_obj, dict)

    def test_01_backend_intermediary(self):
        """
        get draft with dependencyies.
        """
        package_obj = controller.get_package(package_name="sun72/business_theme", format='context', version="draft")
        self.assertIsInstance(package_obj, dict)

    def test_02_backend_intermediary(self):
        """
        get version from backend and save data on backend
        """
        package_obj = controller.get_package(package_name="sun72/business_theme", format='context', version="1.0", dependency=True )
        self.assertIsInstance(package_obj, dict)

    def test_03_backend_intermediary_invalid_package(self):
        """
        get version from backend and save data on backend
        """
        try:
            package_obj = controller.get_package(package_name="sun72/business_theme_invalid", format='context', version="1.0", dependency=True )
        except BlendedException as exc:
            self.assertEqual(exc.args[0].args[0], {'status_code': 5008, 'message': 'Package does not exist.'})

    def test_04_backend_intermediary_invalid_version(self):
        """
        get version from backend and save data on backend
        """
        try:
            package_obj = controller.get_package(package_name="sun72/business_theme", format='context', version="1.45", dependency=True )
        except BlendedException as exc:
            self.assertEqual(exc.args[0].args[0], {'message': 'Version does not exist', 'status_code': 9999})

    def test_05_backend_intermediary(self):
        """
        get version from backend and save data on backend
        """
        package_obj = controller.get_package(package_name="sun72/business_theme", format='context', version="1.0")
        self.assertIsInstance(package_obj, dict)
        
if __name__ == '__main__':
    unittest.main()


