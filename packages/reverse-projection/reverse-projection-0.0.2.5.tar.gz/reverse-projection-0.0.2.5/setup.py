from setuptools import setup, find_packages

setup(
    name='reverse-projection',
    version='0.0.2.5',
    description=(
        'reverse-projection'
    ),
    author='luktian',
    author_email='luktian05@gmail.com',
    maintainer='luktian',
    maintainer_email='luktian@gmail.com',
    license='BSD License',
    packages=find_packages(exclude=[
        "__pycache__",
        ]),
    data_files=[

        ],
    platforms=["windows"],
    python_requires=">=3.6",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'hyperopt',
        'numpy',
        'scikit-learn',
        'pandas',
        'scipy',
        'flask',
        'flask_cors',
        'cachelib',
        'openpyxl',
        "xlrd",
        "xlwt",
        "flask_mail",
    ],
    include_package_data=True
)