from setuptools import setup, find_packages

setup(name='tasks_generator_new',
      version='0.0.1',
      url='https://github.com/XxXDeathmatchXxX/tasks_generator.git',
      license='MIT',
      author='Kirill Kudinov',
      author_email='dr.kireal@yandex.ru',
      description='Add static script_dir() method to pathlib.Path',
      packages=find_packages(exclude=['random, math']),
      long_description=open('README.md').read(),
      zip_safe=False)