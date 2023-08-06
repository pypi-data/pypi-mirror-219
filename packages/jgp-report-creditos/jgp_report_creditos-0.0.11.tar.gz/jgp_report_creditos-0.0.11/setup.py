import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.11' 
PACKAGE_NAME = 'jgp_report_creditos' 
AUTHOR = 'JGP Dev' 
AUTHOR_EMAIL = 'jgpdev20@gmail.com' 
URL = 'https://gitlab.com/develop-team-jdgp/jgp-report-creditos.git'

LICENSE = 'MIT' 
DESCRIPTION = 'Librería con funciones y herramientas útiles exclusivas para jgp'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"


INSTALL_REQUIRES = [
      #'locale'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['resources/img/*']},
    keywords=['python', 'primer paquete jgp'],
)