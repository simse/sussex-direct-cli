from setuptools import setup, find_packages

setup(
    name='sussex',
    version='0.6',
    license='MIT',
    author='Simon Sorensen',
    author_email='hello@simse.io',
    url='https://simse.io',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'BeautifulSoup4',
        'yaspin',
        'pickledb',
        'lxml',
        'tabulate'
    ],
    entry_points='''
        [console_scripts]
        sussex=sussex.cli:cli
    ''',
)