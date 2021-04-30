from distutils.core import setup

VERSION = '1.0.2'

setup(
    name='KT_image_scrape',
    version=VERSION,
    author='Josh Prakke',
    author_email='joshprakke@ktperformance.net',
    url='https://github.com/JPrakke/kt-image-scrape',
    install_requires=[
        'beautifulsoup4==4.8.1',
        'certifi==2019.9.11',
        'chardet==3.0.4',
        'idna==2.8',
        'requests==2.22.0',
        'soupsieve==1.9.4',
        'urllib3==1.25.8',],
    packages=['scraper,],
    license='MIT License',
    description='scrapes site for thumbnails by part number',
    long_description=open('README.txt').read(),
    entry_points = {
        'console_scripts':[
            'KT_scraper=scraper.scrape:run'
        ]
    }
)