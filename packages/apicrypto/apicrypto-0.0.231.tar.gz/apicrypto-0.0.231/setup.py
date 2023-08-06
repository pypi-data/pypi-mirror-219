from setuptools import setup, find_packages


with open('README.md', encoding = 'utf-8') as f:
    long_description = f.read()

setup(
  name='apicrypto',
  version='0.0.231',
  author='Ivan Shapovalov',
  author_email='sartondev@gmail.com',
  description='Simple module for Crypto API',
  url='https://github.com/SartonDev/cryptoapi/',
  packages=find_packages(),
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  install_requires=['requests', 'hashlib', 'time', 'json'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='crypto cryptoapi vk vkontakte module simple apicrypto api',
  project_urls={
    'Documentation': 'https://github.com/SartonDev/cryptoapi/blob/main/README.md'
  },
  python_requires='>=3.9'
)