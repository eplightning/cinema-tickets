from setuptools import setup

setup(
    name='cinema-tickets',
    packages=['cinema-tickets'],
    include_package_data=True,
    install_requires=[
        'flask',
        'cassandra-driver',
    ],
)

