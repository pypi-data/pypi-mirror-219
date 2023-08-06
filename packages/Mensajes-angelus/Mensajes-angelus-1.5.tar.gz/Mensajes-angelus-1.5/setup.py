from struct import pack
from setuptools import setup, find_packages

setup(
    name = 'Mensajes-angelus',
    version = '1.5',
    description = 'Paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'angelus',
    author_email = 'cloud.angelus@gmail.com',
    url = 'https://github.com/angelus',
    license_files=['LICENSE'],
    packages = find_packages(),
    scripts = [],
    test_suite='tests',
    install_requires=[paquete.strip()
                      for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Topic :: Utilities'
    ]
)