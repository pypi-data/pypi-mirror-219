import setuptools

setuptools.setup(
    name="streamlit-binary-tree",
    version="0.2.1",
    author="Abhishek Sharma",
    author_email="abhishek1995sharma@gmail.com",
    description="Interactive Binary Tree as a Streamlit component",
    long_description="Interactive Binary Tree as a Streamlit component",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
        "scikit-learn >= 1.3.0",
        "numpy",
    ],
)
