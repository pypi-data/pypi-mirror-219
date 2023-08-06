from setuptools import setup, find_packages
import re
from pathlib import Path

long_description = '이 설명은 최신 버전이 아닐 수 있습니다. 만약 최신 버전을 확인하고 싶으시다면 [여기](https://github.com/ilotoki0804/pyfilename)를 참고하세요.\n'
long_description += Path('README.md').read_text(encoding='utf-8')
# 사진 대체
repl = r'![\g<1>](https://raw.githubusercontent.com/ilotoki0804/pyfilename/master/\g<2>)'
long_description = re.sub(r'!\[(.+?)\]\((images\/.+?)\)', repl, long_description)

setup(
    name='pyfilename',
    version='0.1.0',
    description='filename utility',
    author='ilotoki0804',
    author_email='ilotoki0804@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/ilotoki0804/pyfilename',
    install_requires=Path('requirements.txt').read_text().split(),
    packages=find_packages(exclude=[]),
    keywords=['filename'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
