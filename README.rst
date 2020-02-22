Ahura
=======

**a God like Serializer for God like Developers.**
 | Ahura is an Automatic easy to use Django serializer. it comes With diverse features designed to fit in all different occasions. Feel free to contribute in case of detecting issues or if any new ideas came to your mind.


Prerequisites
-------------

Ahura is a Django model serializer for now, so you must have Django installed and use Django ORM. 

Installing
----------

For using Ahura you just need to install it using pip.

.. code-block:: console
    
    $pip install ahura

or clone the project. then import the Serializer and use it like the example 
below.


.. code-block:: python

    >>> from ahura import Serializer
    >>> from myapp.models import MyModel
    >>> my_objects = MyModel.objects.all()
    >>> s = Serializer(exclude=["password"], date_format="%Y-%m-%d")
    >>> data = s.serialize(my_objects)


Getting Started
---------------
using ahura is easy as you can see above while it gives you many different options
to modify your model's json. let's go through some of these options.

*this  part is not complete but we will add the documention very soon*



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
