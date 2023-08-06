from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil

# copy the readme file to publish as long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    

# custom installation commands
# we will create a congif file in users root directory 
class CustomInstallCommand(install):
    def run(self):
        install.run(self)

    
        # Get the project's root directory
        project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

        # Create the file in the project's root directory
        file_path = os.path.join(project_root, '.mysqlbuilder.conf')
        with open(file_path, 'w') as file:
            file.write('MYSQL_DEFAULT_DATABASE = "your_database_name" \n MYSQL_USERNAME = "root" \n MYSQL_PASSWORD = ""')
                
                
                
setup(
    name='mysqlbuilder',
    version='1.0.14',
    author='Santu Sarkar',
    author_email='santusarkar2020@gmail.com',
    description='This is a simple mysql builder design to easiy query & get data from your database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dip20/mysqlbuilder',
    packages=find_packages(),
    install_requires=[
         # Add any dependencies required by your package
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
