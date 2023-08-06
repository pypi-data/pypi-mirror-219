from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='signmeup',
    version='0.0.1',
    author='Your Name',
    author_email='yourname@example.com',
    description='Sign Me Up API Package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/signmeup',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'asgiref==3.7.2',
        'Django==4.2.2',
        'django-cors-headers==4.1.0',
        'djangorestframework==3.14.0',
        'Pillow==10.0.0',
        'psycopg2==2.9.6',
        'python-dotenv==1.0.0',
        'pytz==2023.3',
        'sqlparse==0.4.4',
        'typing_extensions==4.6.3',
        'tzdata==2023.3',
    ],
    entry_points={
        'console_scripts': [
            'signmeup-postinstall = post_install.py:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        #'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
