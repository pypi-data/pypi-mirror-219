from setuptools import setup, find_packages

setup(
    name='iotboard',
    version='1.0.0',
    description='Your SDK description',
    author='Your Name',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=[
        'paho-mqtt'
        # 添加其他依赖库
    ],
)
