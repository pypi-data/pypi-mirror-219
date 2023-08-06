from setuptools import setup, find_packages

setup(
  name='pythonqs',
  version="0.0.10",
  description="A program that asks the user/learner to predict the behavior of Python in an interpreter. Accessed through the console.",
  package_dir={"": "src"},
  packages=find_packages(where="src"),
  author="UC Berkeley CS61A, modified by Albany HS CS",
  extra_require={"dev": ["twine>=4.0.2", "pytest >= 7.4.0"]},
  python_requires=">=3.10"
)