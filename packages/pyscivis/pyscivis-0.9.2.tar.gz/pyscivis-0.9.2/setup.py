from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyscivis",
    version="0.9.2",
    author="Jannik Meinecke",
    #author_email="TODO",
    description="A visualization tool for ISMRMRD files. Can be used standalone or embedded into Jupyter Notebooks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/chi-imrt/pyscivis/pyscivis",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'bokeh==2.4.3',
        'tornado>=6.2',
        'ismrmrd>=1.12.0',
        'Pillow>=8.4.0',
        'numpy>=1.22.3',
        'numba>=0.55.2',
        'attr>=0.3.2',
        'desert>=2020.11.18',
        'toml>=0.10.2',
        'pptree>=3.1',
        'defusedxml>=0.7.1'
    ],
    extras_require={
        'testing': [
            'pytest>=6.2.4',
            'pytest-cov',
            'pytest-dependency'
        ]
    },
    project_urls={
        "Bug Tracker": "https://gitlab.com/chi-imrt/pyscivis/pyscivis/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['pyscivis = pyscivis.__main__:main']},
    python_requires=">=3.8",
)
