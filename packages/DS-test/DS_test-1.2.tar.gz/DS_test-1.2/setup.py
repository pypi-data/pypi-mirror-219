from setuptools import setup, find_packages
setup(
    name='DS_test',
    version='1.2',
    description='A sample Python project',
    author='wzq',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyyaml == 5.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)