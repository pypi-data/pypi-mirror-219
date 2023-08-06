import twine
from setuptools import setup, find_packages

# reading long description from file
with open('docs/index.rst') as file:
	long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = [
    'numpy',
    'qiskit',
    'pennylane',
    'scikit-learn',
    'arduino',
    'serial'
]
setup(
    name='amin_qvm',
    version='1.0.8',
    author='Amin Alogaili',
    author_email='aminalogai@aol.com',
    description='Amin-QVM: Quantum Computing Library',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://pypi.org/project/amin-qvm/',
    packages=['amin_qvm'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='quantum computing library simulation amin alogaili QVM aminalogaili',
    install_requires=REQUIREMENTS,
    python_requires='>=3.8',
)
