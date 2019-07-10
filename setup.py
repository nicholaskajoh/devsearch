from setuptools import setup


setup(
    name='devsearch',
    packages=['devsearch'],
    include_package_data=True,
    install_requires=[
        'flask==1.1.1',
        'python-dotenv==0.8.2',
        'click==6.7',
        'mongoengine==0.15.0',
        'scrapy==1.5.0',
        'lxml==4.2.1',
        'gunicorn==19.9.0',
    ],
)