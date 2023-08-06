from setuptools import setup, find_packages

setup(
    name="pathgenmap",
    version="0.0.6",
    packages=find_packages(),
    scripts=["pathgenmap/PathGenMap.py"],  # make sure this is the correct path and name
    install_requires=["pandas>=1.1.0", "tqdm>=4.48.0"],
    author="Marcos Paulo Alves de Sousa",
    author_email="msousa@museu-goeldi.br",
    description="PathGenMap is a comprehensive Python application designed to integrate pathway, annotation, and species abundance data.",
    license="MIT",
    keywords="pathway annotation species abundance",
    url="http://github.com/marcos-de-sousa/pathgenmap",
)
