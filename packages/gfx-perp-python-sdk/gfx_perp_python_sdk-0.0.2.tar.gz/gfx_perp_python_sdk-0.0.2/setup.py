from setuptools import setup, find_packages

setup(
    name='gfx_perp_python_sdk',
    version='0.0.2',
    url='https://github.com/GooseFX1/gfx-perp-python-sdk',
    author='Shashank Shekhar',
    author_email='shashank@goosefx.io',
    description='Perp python sdk',
    packages=find_packages(),    
    install_requires=[
        'pytest'
    ],
)