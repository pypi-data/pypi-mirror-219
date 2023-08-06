from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='InfSumate',
    version='0.0.1',
    description='finds sums and partial sums of geometric series',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Elijah Phifer',
    author_email='ephifer21@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Geometric',
    packages=find_packages(),
    install_requires=['']
)
