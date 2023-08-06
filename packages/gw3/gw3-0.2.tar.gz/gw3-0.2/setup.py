from setuptools import setup, find_packages

setup(
    name='gw3',
    version='0.2',
    description='A Python client for the Gateway3 API',
    keywords=["gw3", "ipfs", "gateway3"],
    author='photon team',
    author_email='admin@photon.storage',
    url='https://github.com/photon-storage/gw3-sdk-python',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7, <4',
)