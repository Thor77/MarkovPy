API
***

MarkovPy
========

.. autoclass:: markov.MarkovPy
  :members:

Prepare
=======

.. autofunction:: markov.markov.is_smiley

.. autofunction:: markov.markov.prepare_line

Stores
======

.. autoclass:: markov.stores.Store
  :members:

  .. automethod:: markov.stores.Store.__len__
  .. automethod:: markov.stores.Store.__contains__

.. autoclass:: markov.stores.Pickle

  .. automethod:: markov.stores.Pickle.__init__


.. autoclass:: markov.stores.Redis

  .. automethod:: markov.stores.Redis.__init__
