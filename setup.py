from setuptools import setup

setup(
    name='MarkovPy',
    version='0.4.0',
    description='A simple Markovchain-Implementation',
    author='Thor77',
    author_email='thor77@thor77.org',
    url='https://github.com/Thor77/MarkovPy',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Chat',
        'Topic :: Database',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='markovpy markov ai',
    packages=['markov', 'markov.stores']
)
