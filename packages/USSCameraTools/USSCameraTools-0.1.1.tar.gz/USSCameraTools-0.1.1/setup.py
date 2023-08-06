from setuptools import setup

setup(
    name='USSCameraTools',
    version='0.1.1',
    description='USSCamera: Python package for interacting with GigE cameras using the Harvesters library',
    long_description='USSCamera is a Python package that provides functionality to interact with GigE cameras using the Harvesters library. It allows you to easily connect to cameras, capture images, trigger the camera, and retrieve camera attributes.',
    long_description_content_type='text/markdown',
    author='USSVision',
    author_email='bhelfer@ussvision.com',
    packages=['USSCameraTools'],
    install_requires=[
        'harvesters',
        'opencv-python',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
