MarkovPy
========
MarkovPy is a modular MarkovChain-Implementation for Python.::

  from markov import MarkovPy
  from markov.stores import Store

  m = MarkovPy(store=Store())
  m.learn('hello, world!')
  m.reply('hello,', min_length=2)
  # hello, world!


Contents:

.. toctree::
   :maxdepth: 2

   stores
   api
