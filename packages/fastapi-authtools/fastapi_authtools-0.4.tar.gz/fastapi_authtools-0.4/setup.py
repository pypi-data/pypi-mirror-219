from setuptools import setup, find_packages

setup(
    name='fastapi_authtools',
    version='0.4',
    url='https://github.com/michael7nightinglae/fastapi_authtools',
    install_requires=[
        "fastapi", "python-jose"
    ],
    license='MIT',
    author='Michael Nightingale',
    author_email='suslanchikmopl@gmail.com',
    description='Simple and comfortable FastAPI JWT authentication.',
    packages=find_packages(exclude=['tests', "templates", "app.py"]),
    long_description=open('README.md').read(),
    zip_safe=False
)
