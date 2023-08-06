from setuptools import setup, find_packages

setup(
    name='Test-User-Generator',
    version='1.0.0',
    description='A Package user to create a new user. created for making test users',
    author='Gokul Dev P',
    author_email='gokuldev.p123@gmail.com',
    packages=find_packages(),
    install_requires=[
        # List the dependencies required by your package
        'pytest',
    ],
    license='MIT',
)