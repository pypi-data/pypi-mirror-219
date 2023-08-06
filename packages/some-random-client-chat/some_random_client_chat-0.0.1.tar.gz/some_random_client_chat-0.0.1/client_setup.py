from setuptools import setup, find_packages

setup(name="some_random_client_chat",
      version="0.0.1",
      description="some_random_client_chat",
      author="Artur B.",
      author_email="ex1le@hotbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
