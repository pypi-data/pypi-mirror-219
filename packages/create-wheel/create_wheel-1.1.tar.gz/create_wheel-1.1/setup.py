import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="create_wheel",
    version="1.1",
    author="Pankaj Kalal",
    author_email="pankajgkalal@gmail.com",
    description="Package to create wheel file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=["pipreqs","importlib-resources"
                      ],

    entry_points = {
        'console_scripts': [
            'create_wheel = create_wheel:create_wheel_function'
        ],
    },)
