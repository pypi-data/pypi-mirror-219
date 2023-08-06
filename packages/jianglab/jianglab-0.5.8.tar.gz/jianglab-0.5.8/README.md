conda install treelib

** In your package's root directory, create a setup.py file. **



1. Update your package version:
In your `setup.py` file, increment the version number. For example, if the current version is `0.1`, you can update it to `0.1.1` or `0.2`:
```python
setup(
    name="my-package",
    version="0.1.1",  # Increment the version number here
    ...
)



1. Rebuild your package:
Remove the existing `dist` directory to clear out old build files:
```bash
rm -rf dist

```

Rebuild your package using the following command:
```bash
python setup.py sdist bdist_wheel

```
This command will create a new `dist` directory with the updated package files.
dist, build and *.egg-info should be in root when created


1. Upload the new version:
Now you can upload the new version of your package to PyPI using twine:

```bash
twine upload dist/*1.7*

```
Since the version number has been incremented, you should not encounter the "file already exists" error, and your package should be uploaded successfully. Users can now install the new version of your package using pip.



To use video output. 
```bash
pip install PyQt5
conda install -c conda-forge ffmpeg
```
