import os
from setuptools import setup


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def package_data_dirs(root, data_dirs):
    data_dirs_path = [x + "/*" for x in data_dirs]
    for data_dir in data_dirs:
        data_dirs_path += [x.replace(f"{root}/", "") + "/*" for x in fast_scandir(f"{root}/{data_dir}")]

    return {root: data_dirs_path}


requirements = [
    # config
    "dynaconf>=3.1.11",
    # HTTP clients
    "requests>=2.28.1",
]

with open("requirements.txt", "w") as file1:
    for requirement in requirements:
        file1.write(f"{requirement}\n")

setup(
    name="rds-core",
    version="0.2.2",
    description="Framework para serviços do Rede de Dados em Saúde do LAIS",
    long_description="É uma biblioteca pública em Python que condensa um conjunto de boas práticas para o"
    " desenvolvimento das aplicações que compõem a Rede da Dados em Saúde (RDS) RDS do Laboratório de"
    " Inovação Tecnológica em Saúde (LAIS) e dos parceiros que contam com o LAIS para fazer suas próprias"
    " RDS, a exemplo RDS-RN e RDS-ES.",
    author="Kelson da Costa Medeiros",
    author_email="kelson.medeiros@lais.huol.ufrn.br",
    keywords=["rds", "cache", "config", "helper", "searchengine"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    packages=[
        "rds",
        "rds.core",
        "rds.core.cache",
        "rds.core.config",
        "rds.core.helpers",
        "rds.core.searchengine",
        "rds.core.transformers",
        "rds.core.transformers.fields",
        "rds.core.transformers.models",
        "rds.core.types",
        "rds.core.validators",
        "rds.contrib",
        "rds.contrib.datasus",
        "rds.contrib.datasus.transformers",
        "rds.contrib.datasus.transformers.fields",
    ],
    package_dir={"rds": "rds"},
    package_data=package_data_dirs("rds.core", []),
    download_url="https://github.com/lais-huol/rds-core/tags",
    url="https://github.com/lais-huol/rds-core",
)
