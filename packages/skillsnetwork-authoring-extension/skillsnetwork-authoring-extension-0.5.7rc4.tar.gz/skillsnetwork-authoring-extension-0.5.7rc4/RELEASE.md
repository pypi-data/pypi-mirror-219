# Making a new release of skillsnetwork-authoring-extension

The extension can be published to `PyPI` and `npm` manually or using the [Jupyter Releaser](https://github.com/jupyter-server/jupyter_releaser).


## Automatic release using Github Actions

Whenever a new release is created in Github, Github actions are triggered to create two releases for npm and PyPI respectively.

### NOTE
When creating a release tag for a package, it is important to ensure that the base version of the tag (i.e., x.x.x) matches the version specified in the package.json file. If there is a mismatch between these versions, the action will be terminated with an error message indicating a release and package version mismatch. This is done intentionally to prevent the publishing of a version that differs from the one specified in package.json.

However, you can still add a release candidate suffix (-rc*) to the end of the release tag without any issues, as long as the base version matches the version specified in package.json. This allows for the testing of pre-release versions without affecting the stable release and the Github Actions are designed to handle this use case without any issues.

## Manual release

### Python package

This extension can be distributed as Python
packages. All of the Python
packaging instructions in the `pyproject.toml` file to wrap your extension in a
Python package. Before generating a package, we first need to install `build`.

```bash
pip install build twine
```

To create a Python source package (`.tar.gz`) and the binary package (`.whl`) in the `dist/` directory, do:

```bash
python -m build
```

> `python setup.py sdist bdist_wheel` is deprecated and will not work for this package.

Then to upload the package to PyPI, do:

```bash
twine upload dist/*
```

### NPM package

To publish the frontend part of the extension as a NPM package, do:

```bash
npm login
npm publish --access public
```

## Automated releases with the Jupyter Releaser

The extension repository should already be compatible with the Jupyter Releaser.

Check out the [workflow documentation](https://github.com/jupyter-server/jupyter_releaser#typical-workflow) for more information.

Here is a summary of the steps to cut a new release:

- Fork the [`jupyter-releaser` repo](https://github.com/jupyter-server/jupyter_releaser)
- Add `ADMIN_GITHUB_TOKEN`, `PYPI_TOKEN` and `NPM_TOKEN` to the Github Secrets in the fork
- Go to the Actions panel
- Run the "Draft Changelog" workflow
- Merge the Changelog PR
- Run the "Draft Release" workflow
- Run the "Publish Release" workflow

## Publishing to `conda-forge`

If the package is not on conda forge yet, check the documentation to learn how to add it: https://conda-forge.org/docs/maintainer/adding_pkgs.html

Otherwise a bot should pick up the new version publish to PyPI, and open a new PR on the feedstock repository automatically.
