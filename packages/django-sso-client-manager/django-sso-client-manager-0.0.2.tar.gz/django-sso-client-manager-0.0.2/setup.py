import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'readme.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sso-client-manager',
    version='0.0.2',
    packages=['sso_client_manager'],
    include_package_data=True,
    license='MIT License',
    description='A Django app for the managing sso client that have login, logout and set code a in cookies.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/rjnp2/django-sso-client-manager',
    author='rjnp2',
    author_email='rjnp2@outlook.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.10",
    install_requires=[
        'cryptography>=1.0.1',
        'requests>=2.31.0',
    ],
    extras_require={
        "dev": ['twine>=4.0.2',]
    }
)
