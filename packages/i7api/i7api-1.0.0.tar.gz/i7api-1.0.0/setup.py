import setuptools

setuptools.setup(
    name="i7api",
    version="1.0.0",
    author="Ojas Gupta",
    description="API Wrapper for i7StorageEngine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["i7api"],
    package_dir={'i7api':'i7api'},  # Replace 'path_to_source_code_directory' with the actual path
    install_requires=["requests"]
)
