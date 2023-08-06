

## Development install

The commands below will install a development environment for
SMUnoSchedulerJupyterLabExtension locally. Before running these commands, you should ensure that NodeJS is
installed locally. The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the brazil workspace to your local environment
brazil ws create -n SMUnoSchedulerJupyterLabExtension && \
    cd SMUnoSchedulerJupyterLabExtension && \
    brazil ws use -p SMUnoSchedulerJupyterLabExtension --vs SMUnoSchedulerJupyterLabExtension/development

# Change dir to the source folder
cd src/SMUnoSchedulerJupyterLabExtension/

# Install the project in editable mode
pip install -e ".[dev]"

# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite

# Server extension must be manually installed in develop mode
jupyter server extension enable amazon_sagemaker_jupyter_scheduler

# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in
different terminals to watch for changes in the extension's source and
automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab --SchedulerApp.scheduler_class=amazon_sagemaker_jupyter_scheduler.scheduler.SageMakerScheduler --SchedulerApp.environment_manager_class=amazon_sagemaker_jupyter_scheduler.environments.SagemakerEnvironmentManager
```

With the `watch` command running, every file change will be built immediately
and made available in your running JupyterLab. Refresh JupyterLab to load the
change in your browser (you may need to wait several seconds for the extension
to be rebuilt).

## Development uninstall

```bash
pip uninstall amazon_sagemaker_jupyter_scheduler
```

## Host Region update

Run this command -`python build-tools/get_host_mapping.py` from root of the project to update the host_region_mapping.json file.
This will read the sagemaker latest pricing pages and update the host types. This should be run periodically until we get a dynamic api to get the host type for a region.
