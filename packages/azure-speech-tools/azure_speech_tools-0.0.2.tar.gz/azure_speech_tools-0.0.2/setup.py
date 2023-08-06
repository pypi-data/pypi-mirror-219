from setuptools import find_packages, setup

setup(
    name="azure_speech_tools",
    version="0.0.2",
    description="This is the Azure Speech Services tools package",
    packages=find_packages(),
    install_requires=[
        "azure-cognitiveservices-speech",
        "azure-storage-blob",
        "azure-identity",
    ],
    entry_points={
        "package_tools": ["my_tools = azure_speech_tools.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)