from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='crawler-telefone-PT-BR-version',
    version=1.0,
    description='Crawler para pegar telefones em sites. Totalmente amador e apenas de TESTE.',
    long_description=Path('README.md').read_text(),
    author='Gabriel',
    author_email='gabrielmarquessant062@gmail.com',
    keywords=['crawler', 'telefone'],
    packages=find_packages()
)
