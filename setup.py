from setuptools import setup, find_packages

__version__ = "0.0.1"

setup(
    name="bully-backend",
    version=__version__,
    python_requires='>3.8.0',
    packages=find_packages(exclude=[]),
    install_requires=[
        "flask",
        "Flask-Admin",
        "flask-cors",
        "flask-sqlalchemy",
        "flask-restful",
        "Flask-Login",
        "flask-migrate",
        "flask-marshmallow",
        "flask-wtf",
        "marshmallow-sqlalchemy",
        "python-dotenv",
        "psycopg2",
        "requests"
    ],
    entry_points={
        "console_scripts": [""]
    },
)
