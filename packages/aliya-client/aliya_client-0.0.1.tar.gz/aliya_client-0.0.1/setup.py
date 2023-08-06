from setuptools import setup, find_packages

setup(name="aliya_client",
      version="0.0.1",
      description="aliya_client",
      author="Kalimullina Aliya",
      author_email="pu_49@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
