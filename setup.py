from setuptools import setup


setup(
    name='devsearch',
    packages=['devsearch'],
    include_package_data=True,
    install_requires=[
        'flask==1.1.1',
        'python-dotenv==0.10.3',
        'click==7.0',
        'mongoengine==0.15.0',
        'scrapy==1.6.0',
        'lxml==4.3.4',
        'gunicorn==19.9.0',
    ],
)