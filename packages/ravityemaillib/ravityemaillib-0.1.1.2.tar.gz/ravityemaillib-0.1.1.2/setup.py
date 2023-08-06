from setuptools import find_packages, setup
setup(
    name='ravityemaillib',
    packages=find_packages(),
    version='0.1.1.2',
    description='Ravity Custom Libraries',
    install_requires=['email','smtplib'],
    author='Me',
    license='MIT',
)