from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description_md = f.read()

setup(name='oxpy',
      version='1.2',
      description='Библиотека для взаимодействия с https://0x0.st через Python',
      long_description=long_description_md,
      long_description_content_type='text/markdown',
      author_email='neso_hoshi_official@mail.ru',
      zip_safe=False,
      author='Neso Hiroshi',
      classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
])