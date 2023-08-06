import setuptools

setuptools.setup(
    name="streamlit-cropperjs",
    version="0.0.3",
    author="erjieyong",
    author_email="erjieyong@gmail.com",
    description="A streamlit module integrating cropperjs",
    long_description="""
    # streamlit-cropperjs

    Integrating the amazing [cropperjs](https://github.com/fengyuanchen/cropperjs) with streamlit. 

    This streamlit module is primarily built with mobile usage in mind.

    ## Features
    - Crop and return image data
    - Supports touch (mobile)
    - Supports cropping on demand with a button
    """,
    long_description_content_type="text/plain",
    url="https://github.com/erjieyong/streamlit-cropperjs",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
