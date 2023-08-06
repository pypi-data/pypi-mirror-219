from setuptools import setup, find_packages

import setuptools

setuptools.setup(
    name="neonelly.core",
    version="0.0.4",
    description="Class library",
    packages=find_packages(),
    install_requires=[],  # Aquí van las dependencias de tu paquete, si las hay
    author="Edi ROsuna",
    author_email="edi.rosuna@gmail.com",
    url="https://github.com/Edi1012/NeoNelly.Core",  # Si tienes un repositorio para tu paquete
    #packages=find_packages(),
    setup_requires=['wheel']
)
