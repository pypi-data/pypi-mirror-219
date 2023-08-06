import setuptools, os

with open('README.md', "r") as f:
    long_description = f.read()
    
print('Thank you for installing version 3 of this library ❤')
    
def find_packages(path='.'):
    ret = []
    for root, dirs, files in os.walk(path):
        if '__init__.py' in files:
            package_name = root.replace('/', '.').lstrip('.\\')
            ret.append(package_name)
    return ret

setuptools.setup(
    name=f"Req_http_vpn",
    version=f"4.5.0",
    author=f"Amin Rngbr",
    author_email=f"rngbramin@gmail.com",
    description=f"A simple and optimized library for sending HTTP requests to closed or filtered sites (:",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LICENSE',
    url=f"https://github.com/aminrngbr1122",
    keywords=f"http",
    packages=find_packages(),
    install_requires=['colorter', 'requests'],
)
                                     