from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='bastila_search',
    version='0.5.0',
    description='A python script that catches commits that introduce predefined deprecated patterns',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/GetBastila/bastila-hook',
    author='Bastila',
    author_email='hello@bastila.app',
    license='MIT',
    packages=['bastila_search'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'bastila_setup=bastila_search.setup_config:main',
            'bastila_run=bastila_search.bastila_search:main'
        ]
    },
    zip_safe=False
)
