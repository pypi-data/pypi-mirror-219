from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zylo',
    version='2.0.2',
    description='A lightweight web framework made with love',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pawan kumar',
    author_email='control@vvfin.in',
    url='https://github.com/E491K7/zylo',
    packages=find_packages(),
    install_requires=['werkzeug', 'jinja2', 'cryptography', 'zylo-admin', 'itsdangerous'],  
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
