from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='aikopanel-bot',
    version='1.2',
    author='AikoCute',
    author_email='aiko@aikocute.tech',
    description='Description of the aikopanel-bot project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Github-Aiko/AikoPanel-bot',
    packages=find_packages(),
    install_requires=[
        'DBUtils==3.0.2',
        'pandas==1.4.2',
        'PyMySQL==1.0.2',
        'python-telegram-bot==20.0a4',
        'PyYAML==6.0',
        'requests==2.27.1',
        'sshtunnel==0.4.0',
        'qrcode==7.4.2'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
