# template_pypackage_builder
A simple tool for packaging python
## Table of Contents
    
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Author](#author)
- [License](#license)
    
## Description
This tool walks you through the process of python packaging. Well it doesnot create actual package, more like a template with initial files to start with. The tool conatin following functions to help with package deployment.

* README maker
* LIcense creater
* setup file creater
* directory tree builder
* pip code generater to install package from subdirectory of github repo
* main function to initial package building from scratch 

## Installation

Install from pypi

```
pip install template-pypackage-builder 
```

Install from GitHub

```
pip install git+https://github.com/dipson94/packagemaker
```

#### Install requires

* pkg_resources
* pyperclip
* os

## Usage

Direct function from packages. Use main function to start initial package build.

```
import template_pypackage_builder as pb
pb.main()
```
Use pip_code() function to generate pip code to install package from subdirectory of github repo
```
import template_pypackage_builder as pb
pb.pip_code()
```
Alternatively use key words pysetup and gitpip directly in terminal to execute the main and pip_code functions respectively

@terminal
```
pysetup
```

@terminal
```
gitpip
```

### Additional notes on package Building
Additional info about package building

**including path**

To include path in package file use the following command
```
import pkg_resources
relative_path=pkg_resources.resource_filename("packagemaker", "types")
```
This command is used if you want to use the path inside package in site-packages folder. Otherwise the path will be relative to the directory where you imported the package (while programming after importing the module).
Here relative_path refers to the path to types folder inside installed package template_pypackage_builder.

**`__init__.py` file handeling**

The following is the tree structure of a package showing basic files and directories. From main package directory in source, each modules ( also directories) contain an `__init__.py` file.
```
└── package_name
    ├── License.txt
    ├── MANIFEST.in
    ├── README.md
    ├── setup.py
    └── src
        └── package_name
            ├── __init__.py
            ├── module_1
            │   ├── __init__.py
            │   └── module_1.py
            ├── module_2
            │   ├── __init__.py
            │   └── module_2.py
            └── module_3
                ├── __init__.py
                └── module_3.py
```


There are numberous ways to handel  `__init__.py` file

Rule of thumb : keep all  `__init__.py` files empty at first and then start addding data from main  `__init__.py` file.

Methods

* if you wish to include all the functions and classes in one file, then write all in main  `__init__.py` file and discard other sub-directories (modules).
* if you wish to follow the structure shown in the illustration then you can include those modules in main  `__init__.py` file by 
```
from . import (module_1,module_2,module_3)
__all__ = ["module_1","module_2","module_3"]

```
* Another approach
```
from .module_1 import (function_1,function_2,function_3)
from .module_2 import (function_1,function_2,function_3)
from .module_3 import (function_1,function_2,function_3)
```
Here we are importing functions directly to main `__init__.py` file, so the functions are readly availble when the main module is called (or imported).

**Final thoughts**

template_pypackage_builder only helps with making a template or initial structure of a package. For making better package, work on the files manually using the editor.

## Author

Dipson

## License

GNU GPL V3
