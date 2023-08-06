from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='mysqlbuilder',
    version='1.0.1',
    author='Santu Sarkar',
    author_email='santusarkar2020@gmail.com',
    description='This is a simple mysql builder design to easiy query & get data from your database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dip20/mysqlbuilder',
    packages=find_packages(),
    install_requires=[
         # Add any dependencies required by your package
    ]
)
