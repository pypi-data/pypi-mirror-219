from setuptools import setup

setup(
    name="pytorch-quantum",
    version="0.2",
    description="A PyTorch based library for Quantum Machine Learning",
    url="http://github.com/pytorch-quantum",
    author_email="contact@anuragsaharoy.me",
    include_package_data=True,
    packages=[
        "pytorch_quantum",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy",
        "scipy",
        "torch",
    ],
    python_requires=">=3.9",
)
