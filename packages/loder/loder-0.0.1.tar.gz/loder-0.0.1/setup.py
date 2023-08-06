import setuptools
import sys

pkg_vars = dict()
with open("loder/_version.py") as f:
    exec(f.read(), pkg_vars)

package_version = pkg_vars["__version__"]
minimum_python_version_required = pkg_vars["__version_minimum_python__"]

# check Python version
if sys.version_info < tuple(map(int, minimum_python_version_required.split("."))):
    sys.exit(f"This package requires Python >= {minimum_python_version_required}")


with open("requirements.txt", "r", encoding="utf8") as reqs:
    required_packages = reqs.read().splitlines()

with open("README.md") as f:
    readme = f.read()

setuptools.setup(
    name="loder",
    version=package_version,
    author="Joey Greco",
    author_email="joeyagreco@gmail.com",
    description="Env vars made easy.",
    long_description_content_type="text/markdown",
    long_description=readme,
    license="MIT",
    url="https://github.com/joeyagreco/loder",
    packages=setuptools.find_packages(exclude=("test", "doc", "example", "img", ".github")),
    install_requires=required_packages,
    include_package_data=True,
    python_requires=f">={minimum_python_version_required}",
    keywords="env vars environment variables easy",
)
