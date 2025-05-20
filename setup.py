from setuptools import setup, find_packages

setup(
    name='data-science-project',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A data science project for web scraping, data analysis, and machine learning model evaluation.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
        'numpy',
        'pandas',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'requests',
        'beautifulsoup4',
        'jupyter'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)