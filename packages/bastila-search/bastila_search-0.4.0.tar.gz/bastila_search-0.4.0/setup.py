from setuptools import setup

setup(
    name='bastila_search',
    version='0.4.0',
    description='A python script that catches commits that introduce predefined deprecated patterns',
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
            'bastila_run=bastla_search.bastila_search:main'
        ]
    },
    zip_safe=False
)
