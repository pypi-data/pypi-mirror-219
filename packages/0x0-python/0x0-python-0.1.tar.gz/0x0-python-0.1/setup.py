from setuptools import setup
from markdown import markdown

with open('README.md', 'r', encoding='utf-8') as f:
    long_description_md = f.read()
    long_description_html = markdown(long_description_md, extensions=['markdown.extensions.fenced_code'])

setup(name='0x0-python',
      version='0.1',
      description='Библиотека для взаимодействия с 0x0 point через питон',
      long_description=long_description_html,
      long_description_content_type='text/markdown',
      author_email='neso_hoshi_official@mail.ru',
      zip_safe=False,
      author='Neso Hiroshi',
      classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
])