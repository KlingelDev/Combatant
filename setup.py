import re
from setuptools import setup
from os import path

DEFAULT_BRANCH = "main"
BASE_GITHUB_URL = "https://github.com/Klingel-Dev/Combatant"

MARKUP_LINK_REGEX = r"\[([^]]+)\]\(([\w]+\.md)\)"
FILE_DIR = path.dirname(path.abspath(path.realpath(__file__)))


with open(path.join(FILE_DIR, 'README.md')) as f:
    readme_contents = f.read()
    markup_link_substitution = '[\\1](%s/%s/\\2)' % (BASE_GITHUB_URL,
                                                     DEFAULT_BRANCH)
    README = re.sub(MARKUP_LINK_REGEX, markup_link_substitution,
                    readme_contents, flags=re.MULTILINE)

with open(path.join(FILE_DIR, 'requirements.txt')) as f:
    INSTALL_PACKAGES = f.read().splitlines()

with open(path.join(FILE_DIR, 'combatant', 'version.py')) as f:
    VERSION = re.match(r"^COMBATANT = \'([\w\.-]+)\'$", f.read().strip())[1]

setup(
    name='combatant',
    packages=['combatant'],
    description="Terminal interface for TimeWarrior.",
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    version=VERSION,
    url='https://github.com/Klingel-Dev/Combatant',
    author='Karl-Heinz Ruskowski',
    author_email='khruskowski@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Topic :: Office/Business',
        'Topic :: Utilities'
    ],
    keywords=[
        'timewarrior',
        'console',
        'tui',
        'text-user-interface',
    ],
    tests_require=[
    ],
    entry_points = {
        'console_scripts': [
            'combatant=combatant.command_line:main',
            'comba=combatant.command_line:main',
        ],
    },
    include_package_data=True,
    python_requires='>=3.7',
    zip_safe=False
)
