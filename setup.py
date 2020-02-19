from distutils.core import setup
setup(
  name = 'ahura',
  packages = ['ahura'],
  version = '0.1',
  license='MIT',
  description = 'A God Like Serializer For God Like Developers.',
  author = 'Mahdi Sorkhemiri',
  author_email = 'sorkhemiri@gmail.com',
  url = 'https://github.com/sorkhemiri/ahura',
  download_url = 'https://github.com/sorkhemiri/ahura/archive/0.1.tar.gz',
  keywords = ['python', 'django', 'serializer', 'json', 'model', 'orm'],
  install_requires=[
          'django',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)