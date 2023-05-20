from setuptools import setup

setup(
    name='mfinance',
    version='0.1.0',
    description='Library for accessing financial data of Moroccan stock exchange companies',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/mfinance',
    packages=['mfinance'],
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        # Add any other dependencies required by your library
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
