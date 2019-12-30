from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='Mancala',
      version='0.1',
      description='Command line implementation of the Mancala game',
      long_description=readme(),
      url='http://github.com/kyokley/Mancala',
      author='Kevin Yokley',
      author_email='kyokley2@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['blessings',
                        'tabulate'],
      zip_safe=False)
