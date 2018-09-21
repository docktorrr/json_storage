from setuptools import setup

version = '0.0.4'

setup(
    name='json_storage',
    version=version,
    author='',
    author_email='nikolay.kovalenko@gmail.com',
    include_package_data=True,
    packages=['json_storage'],
    url='',
    download_url='',
    description="JSON storage",
    long_description="JSON storage",
    python_requires='>=3.5',
    install_requires=[
        'jsonschema==2.6.0'
    ]
)
