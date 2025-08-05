# App Installation

To add Apps you will need to build a custom container with the App(s) installed.  There are multiple ways to add an App to your environment but this document will show the standard method pulling from PyPI.

## Getting Started Using Apps

1. Follow the steps in the README to create your Poetry environment and ensure you can build a container.
2. There are two methods by which to add a specific App to your environment with Poetry:

- Use the `poetry add` command.

For example, to add the Device Onboarding App you would do the following:

```bash
poetry add nautobot-device-onboarding
```

This command should automatically trigger Poetry to see the versions you've specified for Nautobot and your other dependencies in the `pyproject.toml` file and find the most compatible version that is within the limits of the versions defined in your `pyproject.toml`.

- To specify a particular version you can append that to the command like so:

```bash
poetry add nautobot-device-onboarding==3.0.1
```

If for some reason this version doesn't conform to the limits set in your `pyproject.toml` you will need to modify the versions specified by your other dependencies. Poetry should provide some feedback at the command prompt once you've issued the add command if there are limits that restrict you from using that version. Poetry should also update your `poetry.lock` file with the specific pinned version of that App.

3. Once your `poetry.lock` file is updated by Poetry you will need to update the file `config/nautobot_config.py` settings of `PLUGINS` and `PLUGINS_CONFIG` to match your configuration updates for the plugins (PLUGINS_CONFIG is optional, if not adjusting from the default settings). See the [example PLUGIN configuration](#nautobot-configuration).

```bash
vi config/nautobot_config.py
```

4. Finally, you should simply need to rebuild your containers with an `invoke build --no-cache` to build the new custom container.

```bash
invoke build --no-cache
```

5. Once your new containers are built you should simply need to start them if not already started, or restart them with the following:

```bash
invoke stop start
```

## Nautobot Configuration

The configuration file is the same file that is used by the Dockerfile in the Nautobot repo. This file should be updated to match what is required for each of the Apps. An example update for the Onboarding App looks like:

```python
# Enable installed Apps. Add the name of each App to the list.
PLUGINS = ["nautobot_device_onboarding"]

# App configuration settings. These settings are used by various Apps that the user may have installed.
# Each key in the dictionary is the name of an installed App and its value is a dictionary of settings.
PLUGINS_CONFIG = {}
```
