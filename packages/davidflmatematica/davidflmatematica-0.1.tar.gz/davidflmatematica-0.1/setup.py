
from setuptools import setup, find_packages

setup(
    name="davidflmatematica",
    version="0.1",
    packages=['matematica'],
    include_package_data=True,
    description = "Libería Matemática para la clase de python avanzado",
    author = "David Alonso",
    author_email="david.alonso@factorlibre.com",
    license="MIT",
    url="https://www.factorlibre.com/",
    python_requires=">=3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ]
)
