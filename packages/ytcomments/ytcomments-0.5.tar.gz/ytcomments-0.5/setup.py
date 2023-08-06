from setuptools import setup
    
with open("README.md", "r") as f:
	long_description = f.read()

setup(
name="ytcomments",
version="0.5",
description="python package to retreive youtube comments and translate them",
package_dir={"": "src"},
include_package_data=True,
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/dipson94/yt-comments",
author="Dipson",
author_email="dipson94.coding@gmail.com",
license="GNU GPL V3",
classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)","Programming Language :: Python :: 3.10","Operating System :: OS Independent"],
install_requires=["pyperclip >= 1.8.2","tqdm >= 4.65.0","getch >= 1.0","youtube_comment_downloader >= 0.1.68","beautifulsoup4","webencodings","packaging>=21.3","numpy>=1.4","scipy!=1.9.2,>=1.4","importlib-metadata>=3.6","keyring>=15.1","requests-toolbelt!=0.9.0,>=0.8.0","ipython>=7.23.1","matplotlib-inline>=0.1"],
extras_require={
        "dev": ["pytest >= 7.0"]
        },
entry_points={
'console_scripts': ['ytcmts=ytcomments:main',],},
python_requires=">=3.10",    
)
