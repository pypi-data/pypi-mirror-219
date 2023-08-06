# jupyterlab-hide-cells

A [JupyterLab](https://jupyterlab.readthedocs.io/en/latest/) [extension](https://jupyterlab.readthedocs.io/en/latest/user/extensions.html).

Add metadata `jupyterlab-hide-cells:hidden` to cells to either hide or show these.

Toggle this option via right click on cell and click on "Show this cell" / "Hide this cell".

Two view mode: Standard Mode hide all cells with corresponding metadata. To also show hidden cells go to View => View All Cells (incl. Hidden Cells). Within this mode, the background of the cell is light purple to show that they are normally hidden.

![preview](./documentation/JupyterLabHideCode.gif)

## Requirements

- JupyterLab >= 3.0
- Tested on JupyterLab 3.2.0
- Node (for installation via repository clone)

## Install

### (Un-)Installation via pip directly

To install the extension, execute:

```bash
pip install jupyterlab-hide-cells
```

To remove the extension, execute:

```bash
pip uninstall jupyterlab-hide-cells
```

## Contributing

### (Un-)Installation via Repository Clone

#### Installation via pip

```bash
pip install "."
```

**_Development Installation_**

```bash
# Clone the repo to your local environment
# Change directory to the jupyterlab-hide-cells directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

**_Development Uninstallation_**

```bash
pip uninstall jupyterlab-hide-cells
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `jupyterlab-hide-cells` within that folder.

#### Installation via jlpm

```bash
root@device:~/jupyterlab-hide-cells$ jlpm
# expected output:
yarn install v1.21.1
[1/4] Resolving packages...
success Already up-to-date.
Done in 0.76s.
root@device:~/jupyterlab-hide-cells$ jlpm build:lib:prod
# expected output
yarn run v1.21.1
$ tsc
Done in 11.77s.
root@device:~/jupyterlab-hide-cells$ jupyter labextension install .
# expected output:
Building jupyterlab assets (build:dev:minimize)
```



T.B.D.

### Packaging the extension

See [RELEASE](RELEASE.md)
