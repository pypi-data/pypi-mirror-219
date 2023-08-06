import os

kwargs = {}
if os.environ.get("CT_WHEEL") == "1":
    from setuptools import setup
else:
    from skbuild import setup

    cmake_args = []
    for key in ["CT_INSTRUCTIONS", "CT_CUBLAS"]:
        value = os.environ.get(key)
        if value:
            cmake_args.append(f"-D{key}={value}")
    if cmake_args:
        kwargs["cmake_args"] = cmake_args

with open("README.md") as f:
    long_description = f.read()

name = "ctransformers"

setup(
    name=f"{name}-langdash",
    version="0.2.11",
    description="Fork of CTransformers to support Langdash functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nana Mochizuki',
    author_email='nana@mysymphony.jp.net',
    url='https://git.mysymphony.jp.net/nana/ctransformers',
    license="MIT",
    packages=[name],
    #package_data={name: ["lib/*/*.so", "lib/*/*.dll", "lib/*/*.dylib"]},
    install_requires=[
        "huggingface-hub",
    ],
    extras_require={
        "tests": [
            "pytest",
        ],
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="{} transformers ai llm".format(name),
    **kwargs,
)
