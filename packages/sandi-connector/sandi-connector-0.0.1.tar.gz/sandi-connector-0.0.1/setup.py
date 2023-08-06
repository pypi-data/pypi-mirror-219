from setuptools import setup, find_packages

setup(
    name='sandi-connector',
    version='0.0.1',
    author='Luis Gonzalez',
    author_email='luis.gonzalez.pi@usach.cl',
    description='Library for connecting devices to the SANDI project',
    long_description='SANDI connect is a python library available from pypi, which allows the connection of a PMU or device that allows the transmission of data under the IEEE C37.118 standard.',
    long_description_content_type='text/markdown',
    url='https://github.com/C-SESLAB/sandi-connector',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='mqtt websocket library',
    install_requires=[
        'paho-mqtt',
        'keyboard',
        'crcmod'
    ],
)
