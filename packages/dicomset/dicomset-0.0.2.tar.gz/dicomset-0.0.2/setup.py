import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name = 'dicomset',
  packages = setuptools.find_packages(),
  version = '0.0.2',
  description = 'Python library for DICOM processing and analysis',
  long_description = long_description,
  author = 'Brett Clark',
  author_email = 'clarkbab@gmail.com',
  url = 'https://github.com/clarkbab/dicomset',
  keywords = ['python', 'DICOM', 'processing', 'analysis', 'medical imaging'],
  classifiers = []
)