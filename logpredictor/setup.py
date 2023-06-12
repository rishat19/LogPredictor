from setuptools import setup


setup(name='logpredictor',
      version='1.0.0',
      url='http://github.com/rishat19/LogPredictor',
      author='Rishat Ganiev',
      author_email='rishat.ganiev.9@gmail.com',
      packages=['datasets', 'parsers', 'predictor', 'report_generator', 'tmp', 'utils', 'visualizer', ''],
      install_requires=['boto3>=1.4.0'],
      entry_points={
          'console_scripts': [
              'logpredictor = log_predictor:main'
          ],
      },
      classifiers=[
          'Intended Audience :: Developers',
          'Environment :: Console',
          'Programming Language :: Python'
      ],
      zip_safe=True)
