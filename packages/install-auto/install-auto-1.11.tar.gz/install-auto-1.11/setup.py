from setuptools import setup, find_packages

setup(
    name="install-auto",
    version='1.11',
    packages=find_packages(),
    package_data={'utils': ['*']},
    install_requires=[
    'click==8.1.4',
    'colorama==0.4.6',
    'importlib-metadata==6.7.0',
    'pip==23.1.2',
    'prompt-toolkit==1.0.14',
    'Pygments==2.15.1',
    'PyInquirer==1.0.3',
    'pytz==2023.3',
    'regex==2023.6.3',
    'setuptools==47.1.0',
    'six==1.16.0',
    'typer==0.9.0',
    'typing_extensions==4.7.1',
    'wcwidth==0.2.6',
    'zipp==3.15.0',
],

    entry_points='''
    [console_scripts]
    gen=main:app
''',
)