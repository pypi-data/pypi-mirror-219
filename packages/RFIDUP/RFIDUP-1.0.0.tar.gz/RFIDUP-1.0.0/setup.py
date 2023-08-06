#Developer name:liuyuchen
#Developer email:liuyuchen032901@outlook.com
#@2023-2024 nfcup
from io import open
from setuptools import setup, find_packages

setup(
    name='RFIDUP',
    version='1.0.0',
    description='nfc',
    long_description='In order to make it easier for developers to develop hardware programs, we have developed this library. This is the first version of this library. There are only nfcsb functions.',
    author='liuyuchen',
    author_email='liuyuchen032901@outlook.com',
    license='',
    url='https://github.com/liuyuchen012/NFCUP',
    download_url='https://github.com/liuyuchen012/NFCUP/NFCUP.zip',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools',
        'django>=2',
        'django-crispy-forms>=1.6.0',
        'django-reversion>=2.0.0',
        'django-formtools>=1.0',
        'django-import-export>=0.5.1',
        'httplib2==0.9.2',
        'future',
        'six'
    ]
)
