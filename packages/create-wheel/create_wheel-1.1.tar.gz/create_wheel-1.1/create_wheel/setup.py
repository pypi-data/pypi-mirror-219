from setuptools import *
import os



proj_name_dir=os.getcwd()
proj_name=proj_name_dir.split("\\")[-1]
print("Your python package name is :",proj_name)
proj_version=str(input("Enter project version : "))
author_name= str(input("Enter author's name : "))
author_email_id = str(input("Enter e-mail address : "))

user_input = input('Would you like to add description (y/n): ')

if user_input.lower() == 'y':
    description= str(input("enter description : "))
elif user_input.lower() == 'n':
    description = ''
else:
    print('Type y or n')

user_input_pkg = input('Would you like to add include_package_data  (y/n): ')

if user_input_pkg.lower() == 'y':
    include_package_data=True
elif user_input_pkg.lower() == 'n':
    include_package_data = False
else:
    print('Type yes or no')
    
print("Creating requirment.txt this may take some time !!!!")

try:  
    os.system("pipreqs --force")

    print("requirment.txt is created")
except Exception as e:
    print(e)
    
with open("requirements.txt") as f:
    reqs_d = f.read().splitlines()
    
setup(
    name=proj_name,
    version=proj_version,
    author=author_name,
    author_email=author_email_id,
    description=description,
    # long_description_content_type='text/markdown',
    include_package_data=include_package_data,
    packages=find_packages(),
    install_requires=reqs_d,
    # license='MIT',
    
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    
    # url=URL,
    
    # extras_require=EXTRAS,
    
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    
    # cmdclass={
    #     'upload': UploadCommand,
    # },
    
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
)

