ForgeryPy
=========

ForgeryPy is an easy to use forged data generator. It's a (somewhat incomplete)
port of `forgery Ruby gem <http://rubygems.org/gems/forgery>`_.


Example usage
-------------

>>> import forgery_py
>>> forgery_py.address.street_address()
u'4358 Shopko Junction'
>>> forgery_py.basic.hex_color()
'3F0A59'
>>> forgery_py.currency.description()
u'Slovenia Tolars'
>>> forgery_py.date.date()
datetime.date(2012, 7, 27)
>>> forgery_py.internet.email_address()
u'brian@zazio.mil'
>>> forgery_py.lorem_ipsum.title()
u'Pretium nam rhoncus ultrices!'
>>> forgery_py.name.full_name()
u'Mary Peters'
>>> forgery_py.personal.language()
u'Hungarian'


Credits
-------

The project uses dictionary files from `forgery Ruby gem <https://github.com/sevenwire/forgery>`_.


License
-------

MIT-style, see LICENSE

