"""
The setup.py file for QVSED.
"""
from setuptools import setup, find_packages

setup(
    name='qvsed',
    version='1.5.3',
    author='Arsalan Kazmi',
    description='Qt-Based Volatile Small Editor',
    long_description="""QVSED is a volatile and small text editor.

"Volatile" means that QVSED is entirely stateless - once you open a file, QVSED doesn't store any file paths or any other data other than the text contents of the file you loaded.
Additionally, QVSED won't prompt you if you're about to potentially lose an unsaved file, since it doesn't know of any file metadata.
You may be prompted if you're about to overwrite a file, but that's up to your OS, not QVSED.
    
QVSED follows the philosophy of ultra-minimalism, with its heavy emphasis on just editing text and nothing more.
QVSED's editing style is text-based, not file-based like basically every other editor out there.
Text goes in, from a file, and then text later comes out, into another or perhaps the same file.

QVSED can be used as a simple scratchpad or throwaway editor, as well as a general editing software application, since it won't prompt you if you do anything destructive.
It stays out of your way on many occasions. Whether or not that's a good thing is up to you.""",
    packages=find_packages(),
    license="GPL-3.0-or-later",
    url='https://github.com/That1M8Head/QVSED/',
    include_package_data=True,
    install_requires=[
        'PyQt5'
    ],
    entry_points={
        'gui_scripts': [
            'qvsed = qvsed.qvsed:main',
        ],
    },
    package_data={'qvsed': ['qvsed.ui', 'qvsed_dialog.ui']},
)
