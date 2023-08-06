from setuptools import find_packages, setup

with open("app/README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name="chatting_with_pdfs",
    version="0.0.10",
    description="Load a PDF file and ask questions via llama_index and GPT.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Morne",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
