import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsc-crawler",
    version="0.1",
    author="Long Nguyễn",
    author_email="longnp@dc-labs.io",
    description="A package for crawling and processing audio, caption from Youtube, Bilibili, niconico",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zldzmfoq12/aud-crawler",
    keywords=['aud_crawler'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "pydub", "tqdm", "youtube_dl", "youtube_transcript_api"],
    python_requires='==3.6',
)