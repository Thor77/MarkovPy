Stores
******
MarkovPy is using a modular approach for storage of the MarkovChain: Stores.
Stores should inherit from :py:class:`markov.stores.Store`

Pickle
======
:py:class:`markov.stores.Pickle` has no requirements other than read- and write-access to the filesystem.

Redis
=====
:py:class:`markov.stores.Redis` requires :py:mod:`redis` and a running redis(-compatible) server.
The store needs access to these commands: ``KEYS`` [#f1]_, ``EXISTS``, ``HMSET``, ``HINCRBY``, ``HLEN`` and ``HGETALL``.

.. rubric:: Footnotes

.. [#f1] Just required for looking up the database-size (not used by :py:class:`~markov.MarkovPy`)
