import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mastodon_2_album",
    version="0.0.9",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Return photo list and caption (markdown format) from mastodon.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/mastodon_2_album",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'telegram_util',
        'bs4',
    ],
    python_requires='>=3.0',
)