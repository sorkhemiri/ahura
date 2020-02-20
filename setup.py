from distutils.core import setup


long_description  = "Ahura
=======

a God like Serializer for God like Developers.

Getting Started
---------------

just clone the project or use pip to install ahura and there should be no problem using it. ahura is available as django model seriliazer for now but it is goning to be a general python seriliazer very soon. feel free to contribute.

Prerequisites
-------------

Ahura is a Django Model Seriliazer for now so you must have django installed and use Django ORM. 

Installing
----------

For using Ahura you just need to install it using pip.

.. code-block:: console
    
    $pip install ahura

or clone the project.then import the Seriliazer and use it like the example below.


.. code-block:: python

    >>> from ahura import Seriliazer
    >>> from myapp.models import MyModel
    >>> my_objects = MyModel.objects.all()
    >>> s = Seriliazer(exclude=["password"], date_format="%Y-%m-%d")
    >>> data = s.serialize(my_objects)


Contributing
------------

Please read `CONTRIBUTING.md`_ for details on our code of conduct, and the process for submitting pull requests to us.

Authors
-------
* **Mahdi Sorkhemiri**  - *Initial work* - `Sorkhemiri`_
* **Mohammad Rabetian**  - *Initial work* - `Rabetian`_

See also the list of `contributors`_ who participated in this project.

License
-------

This project is licensed under the MIT License - see the `LICENSE.md`_ file for details


.. _CONTRIBUTING.md: https://github.com/sorkhemiri/ahura/blob/master/CONTRIBUTING.md
.. _Sorkhemiri: https://github.com/sorkhemiri
.. _Rabetian: https://github.com/mohammadrabetian
.. _contributors: https://github.com/sorkhemiri/ahura/graphs/contributors
.. _LICENSE.md: https://github.com/sorkhemiri/ahura/blob/master/LICENSE.md
"

setup(
  name = 'ahura',
  packages = ['ahura'],
  version = '0.1.5',
  license='MIT',
  description = 'A God Like Serializer For God Like Developers.',
  long_description=long_description,
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