from setuptools import setup, find_packages
import pathlib
import subprocess
import distutils.cmd

# current directory

here = pathlib.Path(__file__).parent.resolve()

version_file = here / 'VERSION'

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


def format_git_describe_version(version):
    if '-' in version:
        splitted = version.split('-')
        tag = splitted[0]
        index = f"dev{splitted[1]}"
        return f"{tag}.{index}"
    else:
        return version

def get_version_from_git():
    try:
        process = subprocess.run(["git", "describe", "--tags"], cwd=str(here), check=True, capture_output=True)
        version = process.stdout.decode('utf-8').strip()
        version = format_git_describe_version(version)
        with version_file.open('w') as f:
            f.write(version)
        return version
    except subprocess.CalledProcessError:
        if version_file.exists():
            return version_file.read_text().strip()
        else:
            return '0.2.0'

version = get_version_from_git()

print(f"Detected version {version} from git describe")

class GetVersionCommand(distutils.cmd.Command):
    """A custom command to get the current project version inferred from git describe."""

    description = 'gets the project version from git describe'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


class GenerateProtoCommand(distutils.cmd.Command):
    description = 'generate the files from .proto'
    protoPath = "prolog_primitives/proto"
    generatedPath = "prolog_primitives/generatedProto"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass
    
    def run(self):
        import os
        if os.path.exists(self.generatedPath):
            import shutil
            shutil.rmtree(self.generatedPath)
        os.mkdir(self.generatedPath)
        
        subprocess.run(
            f"python -m grpc_tools.protoc -I {self.protoPath} " +
                f"--python_out={self.generatedPath} " +
                f"--pyi_out={self.generatedPath} " +
                f"--grpc_python_out={self.generatedPath} {self.protoPath}/*.proto",
            text=True, check=True, shell=True)
        
        import glob
        import re
        protoFiles = glob.glob(f'{self.generatedPath}/*.py',)
        for protoFile in protoFiles:
            with open(protoFile, 'r' ) as f:
                print(protoFile)
                content = f.read()
                content_new = re.sub('(^import.*pb2)', r'from . \1', content, flags = re.M)
            with open(protoFile, 'w') as file:
                file.write(content_new)
        with open(f"{self.generatedPath}/__init__.py", "w") as f:
            f.close()
        if os.path.exists(f"{self.generatedPath}/__init__.py"):
            print("Files successfully generated from .proto")
            
setup(
    name='prolog_primitives',  # Required
    version=version,
    description='description here',
    license='Apache 2.0 License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lorenzo-osimani/prolog_primitives/',
    author='Lorenzo Osimani',
    author_email='lorenzo.osimani@studio.unibo.it',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Prolog'
    ],
    keywords='aeuitas, horizon2020, xai, bias',  # Optional
    # package_dir={'': 'src'},  # Optional
    packages=find_packages(),  # Required
    include_package_data=True,
    python_requires='>=3.9.0, <=3.11.3',
    install_requires=[
        'scikit-learn>=1.0.2',
        'pandas>=1.4.2',
        'grpcio>=1.54.0',
        'grpcio-tools>=1.54.0',
        'pymongo>=4.3.3',
        'tensorflow>=2.12.0',
        'datasets>=2.12.0'
    ],  # Optional
    zip_safe = False,
    platforms = "Independant",
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/lorenzo-osimani/prolog_primitives/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/lorenzo-osimani/prolog_primitives/',
    },
    cmdclass={
        'get_project_version': GetVersionCommand,
        'generate_proto': GenerateProtoCommand
    },
)

