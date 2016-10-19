from setuptools import setup


setup(
    name="ImageStego",
    scripts=['ImageStego.py'],
    version="0.0.1",
    author="Kevin Almansa",
    author_email="kevin.almansa@gmail.com",
    description="An LSB Steganography Demonstration",
    license="MIT",
    keywords="stego stegano steganography lsb LSB",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['StegoImage'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Security"
    ],
    install_requires=['bitstring', 'Pillow']
)
