"""
This module contains an example of both methods of adding commands to su6.
"""
import typing

from su6.plugins import PluginConfig, register, run_tool

from .helpers import chdir, find_project_root


@register
class PrettierPluginConfig(PluginConfig):
    """
    Config without state, loads [tool.su6.demo] from pyproject.toml into self.
    """

    target: str = "."
    node_modules: str = "./node_modules"


config = PrettierPluginConfig()


@register
def install_prettier(target_dir: str = None) -> int:
    """
    Install the svelte-check tool using npm.
    """
    config.update(target=target_dir)

    with chdir(config.target):
        return run_tool("npm", "install", "prettier")


@register(add_to_all=True, add_to_fix=True)
def prettier(target: typing.Optional[str] = None, fix: bool = False, node_modules: str = None) -> int:
    """
    Run the svelte-check tool.
    """
    config.update(target=target, node_modules=node_modules)

    root, _ = find_project_root((config.node_modules,))
    executable = str(root / "node_modules/prettier/bin/prettier.cjs")

    args = [config.target]

    if fix:
        args.append("--write")
    else:
        args.append("--check")

    return run_tool(executable, *args)
