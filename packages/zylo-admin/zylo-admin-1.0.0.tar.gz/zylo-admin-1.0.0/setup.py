from setuptools import setup, find_packages

setup(
    name='zylo-admin',
    version='1.0.0',
    author='Pawan Kumar',
    author_email='control@vvfin.in',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'zylo-admin = zyloAdmin.main:main',
        ],
    },
)