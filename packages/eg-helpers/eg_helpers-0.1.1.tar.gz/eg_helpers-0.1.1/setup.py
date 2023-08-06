from setuptools import setup

setup(
    name='eg_helpers',
    version='0.1.1',    
    description='Just some helper functions I use in my projects',
    url='https://github.com/Talla/eg_helpers',  
    author='Eduard Germis',
    author_email='edugermis@gmail.com',
    license='MIT',
    packages=['eg_helpers'],
    install_requires=[
        'pandas>=2.0.1',
        'pytz>=2023.3',
        'regex>=2022.10.31',
        'tiktoken>=0.4.0'
    ],
)