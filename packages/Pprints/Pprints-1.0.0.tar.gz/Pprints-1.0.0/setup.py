import setuptools, os

with open('README.md', "r") as f:
    long_description = f.read()
    
print('Thank you for installing version 1 of this library ❤')
    
def find_packages(path='.'):
    ret = []
    for root, dirs, files in os.walk(path):
        if '__init__.py' in files:
            package_name = root.replace('/', '.').lstrip('.\\')
            ret.append(package_name)
    return ret

setuptools.setup(
    name=f"Pprints",
    version=f"1.0.0",
    author=f"Amin Rngbr",
    author_email=f"rngbramin@gmail.com",
    description=f"A library for printing Persian text in color and without color (:",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url=f"https://github.com/aminrngbr1122",
    keywords=f"Print,print,persian,Persian,PP,iran,Iran,Arab,arab,jiji,ColorTER,Pprints,PPRINTs,PPrints",
    packages=find_packages(),
    install_requires=['colorter', 'arabic_reshaper'],
)
                                    
# python -m twine upload --repository pypi dist/*