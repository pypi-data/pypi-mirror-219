import setuptools

setuptools.setup(
    name = 'litesvg',
    version = '0.1.0',
    author = 'Make for art and science - Thierry Dassé',
    url = 'https://framagit.org/makeforartandscience/litesvg',
    license = 'MIT License',
    description = 'This package provides tools to make svg objects (file or in a web page) with rectangles, ellipses, polygons and texts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['litesvg'],
    install_requires=['classattr'],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
