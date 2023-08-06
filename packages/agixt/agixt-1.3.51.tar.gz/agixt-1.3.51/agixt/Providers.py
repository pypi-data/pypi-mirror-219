import importlib
import subprocess
import pkg_resources
import glob
import os
import inspect


def get_providers():
    providers = []
    for provider in glob.glob("providers/*.py"):
        if "__init__.py" not in provider:
            providers.append(os.path.splitext(os.path.basename(provider))[0])
    return providers


def get_provider_options(provider_name):
    provider_name = provider_name.lower()
    module = importlib.import_module(f"providers.{provider_name}")
    provider_class = getattr(module, f"{provider_name.capitalize()}Provider")
    signature = inspect.signature(provider_class.__init__)
    options = {
        name: param.default if param.default is not inspect.Parameter.empty else None
        for name, param in signature.parameters.items()
        if name != "self" and name != "kwargs"
    }
    options["provider"] = provider_name
    return options


class Providers:
    def __init__(self, name, **kwargs):
        try:
            module = importlib.import_module(f"providers.{name}")
            provider_class = getattr(module, f"{name.capitalize()}Provider")
            self.instance = provider_class(**kwargs)

            # Install the requirements if any
            self.install_requirements()

        except (ModuleNotFoundError, AttributeError) as e:
            raise AttributeError(f"module {__name__} has no attribute {name}") from e

    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def get_providers(self):
        providers = []
        for provider in glob.glob("providers/*.py"):
            if "__init__.py" not in provider:
                providers.append(os.path.splitext(os.path.basename(provider))[0])
        return providers

    def install_requirements(self):
        requirements = getattr(self.instance, "requirements", [])
        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        for requirement in requirements:
            if requirement.lower() not in installed_packages:
                subprocess.run(["pip", "install", requirement], check=True)


def __getattr__(name):
    return Providers(name)
