from setuptools import setup, find_packages

setup(
    name='asgiproxify',
    version='0.0.1',
    description='An ASGI middleware for dynamic reverse proxy',
    author='William Goodspeed',
    author_email='goodspeed@fsfans.club',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.0.0,<4.0.0',
    ],
)
