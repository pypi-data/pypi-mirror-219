from setuptools import setup, find_packages

setup(
  name = 'memorizing-transformers-pytorch',
  packages = find_packages(exclude=[]),
  version = '0.4.1',
  license='MIT',
  description = 'Memorizing Transformer - Pytorch',
  long_description_content_type = 'text/markdown',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/memorizing-transformers-pytorch',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'transformers',
    'memory',
    'retrieval'
  ],
  install_requires=[
    'einops>=0.6',
    'filelock',
    'joblib',
    'faiss-gpu',
    'numpy',
    'torch>=1.6',
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
