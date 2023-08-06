from setuptools import setup, find_packages
from setuptools.dist import Distribution


def parse_requirements(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if not line.startswith('#')]


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False


def incrementar_fix_version(file_path):
    try:
        # Abrir el archivo version.txt y leer la versión actual
        with open(file_path, 'r') as file:
            version_str = file.read().strip()

        # Parsear la versión en formato SemVer
        version_pattern = r'^(\d+\.\d+\.\d+)$'
        match = re.match(version_pattern, version_str)
        if not match:
            raise ValueError(
                f'El contenido del archivo {file_path} no está en formato de versión SemVer.')

        # Incrementar en 1 el número de versión de revisión (fix)
        version_parts = match.group(1).split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version_str = '.'.join(version_parts)

        # Actualizar el archivo version.txt con la nueva versión
        with open(file_path, 'w') as file:
            file.write(new_version_str)

        return new_version_str
    except Exception as e:
        print(f'Error: {str(e)}')
        return None


README_FILE = 'README.md'
REQUIREMENTS_FILE = 'requirements.txt'

setup(
    name='pyfrobot',
    version=incrementar_fix_version('version.txt'),
    author='alpeza',
    author_email='alvaroperi.06@gmail.com',
    description='Descripción de mi librería',
    long_description=open(README_FILE).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/mi_libreria',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=parse_requirements(REQUIREMENTS_FILE)
)
