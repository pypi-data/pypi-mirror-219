from setuptools import setup, find_packages

setup(name="mess_server_proj_timur",
      version="0.0.1",
      description="mess_server_proj_timur",
      author="Timur Vodovozov",
      author_email="vodovozzz@inbox.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )