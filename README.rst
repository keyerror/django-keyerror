keyerror.com Django client
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the Django client for the `KeyError <http://keyerror.com/>`_ error
service.

Installation
------------

1. Install the ``keyerror_django_client`` package, eg. via `pip`::

    $ pip install git+git://github.com/keyerror/keyerror-django-client.git

2. Check if installation was successful::

    $ ./manage.py shell
    Python 2.6.6 (r266:84292, Dec 26 2010, 22:31:48) 
    [GCC 4.4.5] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> import keyerror_django_client
    >>> 

   If you don't see any errors here, installation was succesful.

3. Add ``'keyerror_django_client'`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # [...]
        'keyerror_django_client',
        # [...]
    ]

4. Add your KeyError secret key to your ``settings.py``::

    KEYERROR_SECRET_KEY = '<..secret..>'
