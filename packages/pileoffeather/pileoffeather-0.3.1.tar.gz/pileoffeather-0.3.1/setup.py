import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
    name='pileoffeather',
    version='0.3.1',
    license='MIT',
    url = 'https://github.com/usedToBeTomas/pile-of-feather',
    author='Daniele Tomaselli',
    description='Lightweight and easy to use ml library for small projects, create a neural network in minutes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pileoffeather'],
    python_requires='>=3.6',
    keywords = ['neural network', 'ml', 'ai', 'machine learning','simple','nn'],
    install_requires=[
        'opencv-python',
        'numpy'
    ]
)
