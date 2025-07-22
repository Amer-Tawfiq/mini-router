from setuptools import setup,find_packages

setup(
    name="minidrf",
    version='0.1.0',
    description="Minimal and flexible router for Django REST Framework",
    author="Eng: Amer Al-Jabri",
    author_email = "amerprogrammer85@gmail.com",
    url='https://github.com/Amer-Tawfiq/mini-router',
    packages=find_packages(),
    install_requires = [
        'djangorestframework>=3.14',
        'Django>=3.2',
        'inflect>=7.4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)