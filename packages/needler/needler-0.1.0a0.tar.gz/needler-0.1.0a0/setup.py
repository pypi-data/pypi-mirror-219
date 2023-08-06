import setuptools
from needler import __version__

LONG_DESCRIPTION = """
# Needler: TBD
"""

def setup_package():
    setuptools.setup(
        name="needler",
        version=__version__,
        author="Tonio Lora",
        author_email="tonio.lora@microsoft.com",
        description="A python package",
        long_description_content_type="text/markdown",
        # url="https://github.com/wjohnson/pyapacheatlas",
        packages=setuptools.find_packages(),
        install_requires=[],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        long_description=LONG_DESCRIPTION
    )

if __name__ == "__main__":
    setup_package()