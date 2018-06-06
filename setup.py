from setuptools import setup

setup(
    name='devsearch',
    packages=['devsearch'],
    include_package_data=True,
    install_requires=[
        'flask==1.0.2',
        'python-dotenv==0.8.2',
        'flask-sqlalchemy==2.3.2',
        'mysqlclient==1.3.12',
        'flask-migrate==2.1.1',
    ],
)