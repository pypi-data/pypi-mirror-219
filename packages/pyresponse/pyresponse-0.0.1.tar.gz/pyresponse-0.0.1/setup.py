from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()

setup(
    name='pyresponse',
    version='0.0.1',
    description='Package for creating success and error responses in Python Projects',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    author='Ibrahim Oluwapeluwa',
    author_email='ipeluwa@gmail.com',
    packages=find_packages(),
    install_requires=[
        'rollbar',
        'sentry-sdk',
        'python-dotenv',
        'pydantic',
        'marshmallow'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
