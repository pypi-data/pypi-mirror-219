from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ArucoScanner',
  version='0.0.2',
  description='Simplicity for Aruco code',
  long_description=open('README.txt').read(),
  url='https://pypi.org/project/ArduinoScanner/',  
  author='Julien Serbanescu',
  author_email='julien.serbanescu@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='aruco', 
  packages=find_packages(),
  install_requires=['opencv-python', 'numpy'] 
)
