from setuptools import setup
with open("README.md", "r") as f:
    long_description = f.read()
setup(
    name="template_pypackage_builder",
    version="0.9",
    description="A simple tool for packaging python",
    package_dir={"": "src"},
    include_package_data=True,
    url="https://github.com/dipson94/packagemaker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dipson",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=['pyperclip'],
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'pysetup=template_pypackage_builder:main','gitpip=template_pypackage_builder:pip_code',
        ],
    },
)
