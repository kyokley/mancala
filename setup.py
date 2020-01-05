from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Mancala',
    version='0.1',
    description='Command line implementation of the Mancala game',
    long_description=readme(),
    url='http://github.com/kyokley/Mancala',
    author='Kevin Yokley',
    author_email='kyokley2@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['blessings', 'tabulate'],
    tests_require=['pytest', 'black', 'bpython', 'isort'],
    entry_points={'console_scripts': ['mancala=src.game:main']},
    zip_safe=False,
)
