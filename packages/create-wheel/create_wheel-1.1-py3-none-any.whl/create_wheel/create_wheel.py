import os

import importlib_resources
pkg = importlib_resources.files("create_wheel")
pkg_data_file = pkg /"setup.py"


def create_wheel_function():
    try:
        
        os.system(f"python {pkg_data_file} bdist_wheel")
        print("Wheel file is created pls check your package/dist folder ")
    except Exception as e:
        print(e)