from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'From Image of a curve/graph, extract and store the cordinates pairs in a 2D array, Github link (https://github.com/kumarUjjawal3621/mypython_lib)'
LONG_DESCRIPTION = """ 
How to use:
    1. import graph_cordinates.graph_cordinates as gc
    2. gc.get_graphcordinates(image_path,x_range,y_range,background_value)
    3. Will return an array of 2D cordinates: [[x1,y1], [x2,y2], .......n-points] ; n=pixel width of Image
    
How to pass arguments-
    1. image_path == path to a graph image
    2. x_range == [Value of left most point on graph's x-axis, Value of right most point on graph's x-axis]
    3. y_range == [Value of bottom most point on graph's y-axis, Value of top most point on graph's y-axis]
    4. background_value == 0 or 1 
        0: When the graph's background color is relatively darker than the curve 
        1: Otherwise

Caution- Try to pass the Image by erasing the axes
"""
# Setting up

setup(
    name="graph_cordinates",
    version=VERSION,
    author="Ujjawal Kumar (India)",
    author_email="<kumarujjawal3621@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['stock price','Python', 'Cordinates', 'Image', '2D Curve'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)