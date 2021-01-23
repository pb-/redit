from setuptools import find_packages, setup

setup(
    name='redit',
    version='1.0.0',
    author='Paul Baecher',
    description='Preview recently edited notes and launch editor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pb-/redit',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'redit = redit.main:run',
        ],
    },
)
