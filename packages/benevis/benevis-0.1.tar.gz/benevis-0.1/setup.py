from setuptools import setup

setup(
    name="benevis",
    version="0.1",
    py_modules=["run"],
    entry_points="""
        [console_scripts]
        benevis=run:main
    """,
)
