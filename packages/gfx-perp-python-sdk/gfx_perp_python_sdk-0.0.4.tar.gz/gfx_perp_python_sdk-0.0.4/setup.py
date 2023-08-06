from setuptools import setup, find_packages

setup(
    name='gfx_perp_python_sdk',
    version='0.0.4',
    url='https://github.com/GooseFX1/gfx-perp-python-sdk',
    author='Shashank Shekhar',
    author_email='shashank@goosefx.io',
    description='Perp python sdk',
    py_modules=['my_project'],
    packages=find_packages(),    
    install_requires=[
        'pytest'
    ],
)