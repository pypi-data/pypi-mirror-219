from setuptools import setup, find_packages

DESCRIPTION = "A package that allows to sync tickets from Zendesk to ClickUp."

# Read the contents of the README.md file
with open("README.md", "r", encoding="utf-8") as f:
    md_long_description = f.read()

# Setting up
setup(
    name="syncticketstoclickup",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="abrahamprz (Abraham Perez)",
    author_email="fcoabrahamprz@gmail.com",
    description=DESCRIPTION,
    long_description=md_long_description,  # Use the contents of README.md as the long description
    long_description_content_type="text/markdown",  # Specify the content type as Markdown
    packages=find_packages(),
    install_requires=["requests", "tqdm", "python-dotenv"],
    keywords=["python", "zendesk", "clickup", "ticket", "task", "sync", "requests"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    # entry_points={
    #     'console_scripts': [
    #         'sync-zendesk-to-clickup=syncticketstoclickup.main:main'
    #     ]
    # },
)
