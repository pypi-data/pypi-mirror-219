from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ARIclicker',
    version='2.0.1',
    description="The best autoclicker in minecraft!",
    long_description=open('README.md').read() ,
    long_description_content_type="text/markdown",

    author='LIN,Zhe',
    author_email='2081812728@qq.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['autoclicker','minecraft-auto'],
    packages=find_packages(),
    requires=['pynput'],

)
