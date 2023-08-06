from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyfilters_lib',
    version='1.0.1',
    py_modules=['filters_lib.filter_types', 'filters_lib.filters_sdk'],
    packages=['filters_lib'],
    url='https://gitlab.com/neurosdk2/neurosamples/-/tree/main/python',
    license='MIT',
    author='Brainbit Inc.',
    author_email='support@brainbit.com',
    description='Python wrapper for Filters library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={"filters_lib": ['libs\\windows-x64\\filters.dll', 
                               'libs\\windows-x86\\filters.dll']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7',
)