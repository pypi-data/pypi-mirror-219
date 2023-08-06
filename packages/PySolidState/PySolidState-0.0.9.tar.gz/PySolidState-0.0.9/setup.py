import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="PySolidState",
    version="0.0.9",
    description="PySolidState is a library developed to facilitate the study of solid-state materials, ranging from crystal structures to tight-binding models. It provides a set of tools and functionalities that enable researchers and students to analyze and simulate various aspects of the solid-state physics.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/miguelta281/PySolidState",
    author="Jose Miguel Tarazona, Yerimi Gamboa Caballero, Felipe",
    author_email="makesens19@gmail.com",
    license="GNU General Public License v3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["PySolidState", "PySolidState.crystal_structure"],
    include_package_data=True,
    install_requires=["numpy", "matplotlib","mayavi"]
)