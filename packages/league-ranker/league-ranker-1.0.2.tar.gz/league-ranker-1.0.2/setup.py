from setuptools import find_packages, setup


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='league-ranker',
    version='1.0.2',
    packages=find_packages(exclude=('tests',)),
    package_data={'league_ranker': ['py.typed']},
    url='https://ranker.readthedocs.io/en/latest/',
    project_urls={
        'Documentation': 'https://ranker.readthedocs.io/en/latest/',
        'Code': 'https://github.com/PeterJCLaw/ranker',
        'Issue tracker': 'https://github.com/PeterJCLaw/ranker/issues',
    },
    description="League ranking for arbitrary numbers of competitors.",
    long_description=long_description,
    author='Student Robotics Competition Software SIG',
    author_email='srobo-devel@googlegroups.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Typing :: Typed',
    ],
    python_requires='>=3.7',
    setup_requires=[
        'Sphinx >=1.8.5, <5',
    ],
    zip_safe=True,
)
