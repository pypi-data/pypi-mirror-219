from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='pyclockify',
    version='0.1.0',
    description='Python library for interacting with the Clockify API',
    author='Alejandro Santiago Félix',
    author_email='alex.0002002@gmail.com',
    packages=['clockify'],
    install_requires=['requests', 'attrs'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
