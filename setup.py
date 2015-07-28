from setuptools import setup, find_packages

setup(
    name='PyAI',
    version='0.0.1',
    description='Markov-implementation with redis-database',
    author='Thor77',
    author_email='thor77@thor77.org',
    url='https://github.com/Thor77/PyAI',
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
    keywords='pyai markov ai',
    py_modules=['pyai'],
    install_requires=['redis']
)
