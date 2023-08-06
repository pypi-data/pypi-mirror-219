from setuptools import setup

setup(
    name='hedgesql',
    version='1.3.1',
    description='Convenient work with sqlite3 and aiosqlite',
    url='https://github.com/I-HedgeDev/litesqlite',
    author='HedgeDev',
    author_email='hedge_dev@mail.ru',
    packages=['hedgesql'],
    install_requires=[
        'aiosqlite'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)
