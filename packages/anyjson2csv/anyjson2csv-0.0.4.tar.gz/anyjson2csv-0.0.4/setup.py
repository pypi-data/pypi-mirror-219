from distutils.core import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="anyjson2csv",  # How you named your package folder (MyLib)
    version="0.0.4",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="JSON flatten for Python",  # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="BrainsLogic",  # Type in your name
    author_email="info@brainslogic.com",  # Type in your E-Mail
    url="https://github.com/mehdiabidi/json2csv",
    python_requires=">=3.7",
    # Keywords that define your package best
    install_requires=[  # I get to this in a second
        "pandas",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
    ],
)
