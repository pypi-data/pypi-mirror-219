from setuptools import setup, find_packages

readme_path = 'README.md'
# PACKAGE_NAME主要在使用的时候用到 pkg_resources.resource_filename('log_translate', 'res/log_logo.ico')
PACKAGE_NAME = 'log_translate'
# 需要写清楚路径
ICON_PATH = 'res/*.ico'

setup(
    name='LogTranslate',
    version='1.2.6',
    author='5hmlA',
    author_email='jonas.jzy@gmail.com',
    # 指定运行时需要的Python版本
    python_requires='>=3.6',
    # 找到当前目录下有哪些包 当前(setup.py)目录下的文件夹 当前目录的py不包含 打包的是把所有代码放一个文件夹下文件名为库名字
    packages=find_packages(),
    # 配置readme
    long_description=open(readme_path, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT Licence",
    # 配置要打包的文件
    package_data={PACKAGE_NAME: [ICON_PATH]},
    # 手动指定
    # packages=['log_translate', 'log_translate/business'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        # 只包含包名。 这种形式只检查包的存在性，不检查版本。 方便，但不利于控制风险。
        'PyQt6',
        'PySide6',
        'rx',
        'typer',
        'keyboard',
        # 'setuptools==38.2.4'，指定版本。 这种形式把风险降到了最低，确保了开发、测试与部署的版本一致，不会出现意外。 缺点是不利于更新，每次更新都需要改动代码
    ],
    keywords='tools log translate',
    url='https://github.com/5hmlA/PyTools',
    description='A Python library for translate log from log files'
)

# python -m pip install --upgrade twine
# pip install wheel setuptools
# python setup.py sdist bdist_wheel

# 发布到测试地址
# twine upload --repository testpypi dist/*
# twine upload dist/*
