def license(x=None,*kwargs):
    intro="""
----------------------------License Maker-----------------------------------
    
Select the type of the license from the following
    
1. GNU General Public License (GPL): A copyleft license that requires
   derivative works to be distributed under the same license. It
   promotes software freedom and has different versions such as GPLv2
   and GPLv3.
2. MIT License: A permissive license that allows users to freely use,
   modify, and distribute the software with minimal restrictions. It
   is widely used and simple to understand.
3. Apache License 2.0: A permissive license that grants users the 
   freedom to use, modify, and distribute the software. It includes 
   patent grants and provides explicit permissions for contributors.
4. Mozilla Public License (MPL): A copyleft license that allows users
   to modify and distribute the software, even in proprietary projects.
   It requires source code changes to be shared under the MPL.
5. A license with no conditions whatsoever which dedicates works to 
   the public domain. Unlicensed works, modifications, and larger 
   works may be distributed under different terms and without source code. 
6. User-defined or other : Here use you can copy paste user-defined 
   or ther type of License.
   
-------------------------------------------------------------------------------
    
"""
    if x==None:
        x=int(input(intro))
        while x<1 or x>6:
        	x=int(input("""
        enter a value from 1-6  
        """))
    file=["GNU GPLv3","MIT License","Apache Version 2.0","Mozilla Public License 2.0","The Unlicense","user_defined"][x-1]
    import pkg_resources
    relativepath=pkg_resources.resource_filename("packagemaker", "types")
    path=relativepath+"/"+file+".txt"
    if x==6:
        path=str(input("enter path to custon License file : "))
    with open(path,"r") as template:
        content=template.read()
    name_author=year=name_program=note=0
    data=[name_author,year,name_program,note]
    for i,x in enumerate(kwargs):
    	data[i]=x
    if x in [1,2,3] and len(kwargs)<2:
        name_author=str(input("Enter the name of the author : "))
        year=str(input("Enter year of publication : "))
        if x==1:
            name_program=str(input("Enter the name of the program : "))
            note=str(input("Breif note about program : "))           
    if x==1 and len(kwargs)<4 and len(kwargs)>2:            
        name_program=str(input("Enter the name of the program : "))
        note=str(input("Breif note about program : "))

    content=content.replace("[name of copyright owner]","["+str(name_author)+"]")
    content=content.replace("[yyyy]","["+str(year)+"]")
    content=content.replace("[fullname]","["+str(name_author)+"]")
    content=content.replace("[year]","["+str(year)+"]")
    content=content.replace("<name of author>",""+str(name_author)+"")
    content=content.replace("<year>",""+str(year)+"")
    content=content.replace("<program>",""+str(name_program)+"")
    content=content.replace("<one line to give the program's name and a brief idea of what it does.>",""+str(note)+"")
            
    return content
"""
Template-----------------------------------------------------------------------
pip install git+https://github.com/username/repo.git@branch#subdirectory=folder
-------------------------------------------------------------------------------
"""
def pip_code():
    split=str(input("enter url to package : ")).split("/")
    from pyperclip import copy
    user=split[3]
    repo=split[4]
    branch=split[6]
    folder="/".join(split[7:])
    i="pip install git+https://github.com/"+user+"/"+repo+".git@"+branch+"#subdirectory="+folder
    copy(i)
    print("---> ",i)
    print("Also copied to clipboard")
def readme():
    print("\n----------------------------README Maker-----------------------------------\n")
    package_name=str(input("Enter package name : "))
    breif=str(input("Enter brief description in one line : "))
    note=str(input("Enter long description : "))
    install_description=str(input("Enter install pointers : "))
    install_cmd=str(input("Enter install command : "))
    install_require=[]
    while True:
        x=str(input("enter install requires : "))
        if x=="":
            break
        install_require.append(x)
    usage_note=[]
    usage_cmds=[]
    while True:
        n=str(input("enter usage description : "))
        if n=="":
            break
        c=str(input("enter usage command : "))
        if c=="":
            break
        usage_note.append(n)
        usage_cmds.append(c)
    author_name=str(input("Enter Author name : "))
    license=str(input("Enter License type : "))
    
    s="# "+package_name+"\n"+breif+"\n"
    s=s+"""## Table of Contents
    
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Author](#author)
- [License](#license)
    
## Description
    """+note+"\n## Installation\n"+install_description+"\n\n```\n"+install_cmd+"\n```\n#### Install requires\n\n"
    for i in install_require:
        s=s+i+"\n\n"
    s=s+"## Usage\n"
    for idx,x in enumerate(usage_cmds):
        s=s+usage_note[idx]+"\n\n"
        s=s+"```\n"+x+"\n```\n"
    s=s+"## Author\n"+author_name+"\n"+"## License\n"+license
    print("\n------------------------------------------------------------------\n") 
    return s

def setup():
    from pyperclip import copy
    print('''
    
    ----------------------------------------------------
    |                  Setupfile tool                  |
    ----------------------------------------------------
    | This tool will walk through the creation of the  |
    | setup.py file for the package deployment.        |
    | Leave blank (just press enter) when the value is |
    | optional or default.                             |
    ----------------------------------------------------
    
    ''')
    readme=str(input("\nenter path to readme file : \n(Dafault value : README.md) "))
    if readme=="":
        readme="README.md"
    name=""
    while name=="":
        name=str(input("enter name of the package *(must specify) : "))
    version=str(input("enter version of the package : \n(Dafault value : 0.1) "))
    if version=="":
        version="0.1"
    description=str(input("enter short description aboout package : \n(Dafault value : Initial deploy) "))
    if description=="":
        description="Initial deploy"
    packagedir=str(input("enter path to package directory : \n(Dafault value : src) "))
    if packagedir=="":
        packagedir="src"
    url=str(input("enter url to github (optional) : "))
    authorname=str(input("enter name of the author \n(Dafault value : Author): "))
    if authorname=="":
        authorname="Author"
    authoremail=str(input("enter e-mail of author (optional) : "))
    license=str(input("enter the type of license : \n(Dafault value : GNU GPL V3)"))
    if license=="":
        license="GNU GPL V3"
    print("\nenter the classifiers (optional) : ")
    print("""
    
    ----------------------------------------..
    | Example (enter each line one by one)   |
    ----------------------------------------..
    | License :: OSI Approved :: MIT License |
    | Programming Language :: Python :: 3.10 |
    | Operating System :: OS Independent     |
    ----------------------------------------..
    
    """)
    classifier=[]
    while True:
        x=str(input("enter classifier line :"))
        if x=="":
            break    
        classifier.append(x)
    print("\nenter install_requires packages (optional) : ")
    print("""
    
    ----------------------------------------
    | Example                              |
    ----------------------------------------
    | bson >= 0.5.10                       |
    ----------------------------------------
    | only add version if necessary        |
    ----------------------------------------
    
    """)
    installrequire=[]
    while True:
            x=str(input("enter package :"))
            if x=="":
                break
            installrequire.append(x)
    print("\nenter dev require packages (optional) : ")
    print("""

    ----------------------------------------
    | Example                              |
    ----------------------------------------
    | pytest >= 7.0                        |
    ----------------------------------------
    | only add version if necessary        |
    ----------------------------------------
    
    """)
    extrarequire=[]
    while True:
            x=str(input("enter package :"))
            if x=="":
                break
            extrarequire.append(x)
    print("\nenter python version requires (optional) : ")
    print("""

    ----------------------------------------
    | Example                              |
    ----------------------------------------
    | >=3.10                               |
    ----------------------------------------
    | only add version if necessary        |
    ----------------------------------------
    
    """)
    pythonrequires=str(input("enter version :"))
    
    s='''from setuptools import setup
    
    with open("'''
    s=s+readme+'''", "r") as f:
        long_description = f.read()
    
    setup(
        name="'''+name+'''",
        version="'''+version+'''",
        description="'''+description+'''",
        package_dir={"": "'''+packagedir+'''"},
        include_package_data=True,
        long_description=long_description,
        long_description_content_type="text/markdown",'''
    if url!="":
        s=s+'''
        url="'''+url+'''",'''
        
    s=s+'''
        author="'''+authorname+'''",'''
    if authoremail!="":
        s=s+'''
        author_email="'''+authoremail+'''",'''
        
    s=s+'''
        license="'''+license+'''",'''
    if len(classifier)!=0:
        s=s+'''
        classifiers='''
        c='['
        for i in classifier:
            c=c+'"'+i+'",'
        c=c[:-1]+']'
        s=s+c
    if len(installrequire)!=0:
        s=s+''',
        install_requires='''
        
        ir='['
        for i in installrequire:
            ir=ir+'"'+i+'",'
        ir=ir[:-1]+']'
        s=s+ir
    if len(extrarequire)!=0:
        s=s+''',
        extras_require={
                "dev": '''
        exr='['
        for i in extrarequire:
            exr=exr+'"'+i+'",'
        exr=exr[:-1]+']'
        s=s+exr+'''
                },'''
    if pythonrequires!="":
        s=s+'''
        python_requires="'''+pythonrequires+'''",'''
    s=s+'''    
    )'''
    max=0
    for i in  s.split("\n"):
        if len(i)>max:
            max=len(i)
    max=max+5
    p="-"*max+"----"+"\n"+"|"+" "*max+"  |\n"
    for i in  s.split("\n"):
        fill=" "*int(max-len(i))
        p=p+"|  "+str(i)+fill+"|\n"
    p=p+"|"+" "*max+"  |\n"+"-"*max+"----"+"\n"
    print("\n"+" "*int((len(p.split("\n")[0])-len("The setup.py codes"))/2)+"The setup.py codes"+"\n")
    print(p)
    copy(s)
    print("code is copied to clipboard................\n\n")
    print("\n------------------------------------------------------------------\n") 
    return s
def tree(setup="",readme="",license=""): 
    print("\n---------------------------- Tree -----------------------------------\n") 
    import os  
    package_name=str(input("Enter package name : "))
    sub_packages=[]
    while True:
        x=str(input("enter sub package name : "))
        if x=="":
            break
        if x in sub_packages:
            print("--- name exists ---")
            continue
        sub_packages.append(x)
    
    os.mkdir(package_name)
    os.chdir(package_name)
    with open("README.md","w") as rd:
        rd.write(readme)
        rd.close()
    with open("License.txt","w") as ls:
        ls.write(license)
        ls.close()
    with open("setup.py","w") as st:
        st.write(setup)
        st.close()
    with open("MANIFEST.in","w") as m:
        m.write("recursive-include src/"+package_name+" *")
        m.close()
    os.mkdir("src")
    os.chdir("src")
    os.mkdir(package_name)
    os.chdir(package_name)
    open("__init__.py","w")
    for i in sub_packages:
        os.mkdir(i)
        open(i+"/__init__.py","w")
        open(i+"/"+i+".py","w")
    print("\n------------------------------------------------------------------\n") 
def main():
    print("""

-----------------------------------------------------------------
|                                                               |
| ******************** Packagemaker - Main ******************** |
|                                                               |
|---------------------------------------------------------------|
|This function will walk you through complete packaging process |
| Including folder creation and file creation                   |
-----------------------------------------------------------------

""")
    if str(input("\nDo you wish to continue (y/n) ?"))!="y":
       return 0
    print("\n")
    ls=license()
    rd=readme()
    st=setup()
    tree(st,rd,ls)
        
