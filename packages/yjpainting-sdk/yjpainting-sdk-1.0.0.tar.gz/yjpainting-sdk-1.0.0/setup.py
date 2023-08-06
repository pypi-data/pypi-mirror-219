from setuptools import setup

setup(
    name='yjpainting-sdk',
    version='1.0.0',
    author='ricky_yang',
    author_email='biteasquirrel@gmail.com',
    description='A Python SDK for yjpainting API',
    packages=['openapi'],
    install_requires=[
        'requests',
    ],
)

