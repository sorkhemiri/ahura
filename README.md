# Ahura

a God like Serializer for God like Developers.

## Getting Started

just clone the project or use pip to install ahura and there should be no problem using it. ahura is available as django model seriliazer for now but it is goning to be a general python seriliazer very soon. feel free to contribute.

### Prerequisites

Ahura is a Django Model Seriliazer for now so you must have django installed and use Django ORM. 

### Installing

For using Ahura you just need to install it using pip.

```
pip install ahura
```

or clone the project.
then import the Seriliazer and use it like the example below.
```pycon
>>> from ahura import Seriliazer
>>> from myapp.models import MyModel
>>> my_objects = MyModel.objects.all()
>>> s = Seriliazer(exclude=["password"], date_format="%Y-%m-%d")
>>> data = s.serialize(my_objects)
```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/sorkhemiri/ahura/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Mahdi Sorkhemiri** - *Initial work* - [Sorkhemiri](https://github.com/sorkhemiri)
* **Mohammad Rabetian** - *Initial work* - [Rabetian](https://github.com/mohammadrabetian)

See also the list of [contributors](https://github.com/sorkhemiri/ahura/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/sorkhemiri/ahura/blob/master/LICENSE.md) file for details
