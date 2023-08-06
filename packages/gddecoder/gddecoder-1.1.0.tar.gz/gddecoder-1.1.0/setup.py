from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='gddecoder',
    version='1.1.0',
    author='LordNodus',
    author_email='LordNodus@mail.ru',
    description='Lib for work this Geometry Dash levels',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/NodusLorden/gddecoder',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='geometrydash python',
    project_urls={'Documentation': "https://github.com/NodusLorden/gddecoder"},
    python_requires='>=3.11'
)
