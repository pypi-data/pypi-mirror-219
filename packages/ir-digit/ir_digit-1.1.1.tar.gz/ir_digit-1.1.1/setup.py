import setuptools


setuptools.setup(
    name="ir_digit",
    version="1.1.1",
    author="FKLiu",
    author_email="fkliu001@outlook.com",
    description="digit package",
    long_description="digit package 与 digit web 配套使用，下载其digit web中的数据资源并在本地运行",
    long_description_content_type="text",
    url="https://master--ir-digit-redocs.netlify.app/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires = [
        "gitpython",
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "jieba"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
            'console_scripts': [
                'digit=digit.scripts:main',
            ],
        },

)
