from setuptools import setup, find_packages

setup(
    name='lord-of-the-rings-sdk-seanmavley',
    version='1.0.0',
    author='Rexford',
    author_email='seanmavley@gmail.com',
    description='SDK for the Lord of the Rings API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seanmavley/lord-of-the-rings-sdk',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
