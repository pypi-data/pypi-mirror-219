import shutil
from pathlib import Path

from su6 import app
from plumbum import local
from typer.testing import CliRunner

from src.su6_plugin_prettier.helpers import chdir

runner = CliRunner(mix_stderr=False)


def prepare_env():
    with chdir("./pytest_examples"):
        local["npm"]("install", "prettier")


def test_install():
    target_dir = Path("pytest_examples/node_modules")

    if target_dir.exists():
        shutil.rmtree(target_dir)

    result = runner.invoke(app, ["install-prettier", "--target-dir", "./pytest_examples"])

    assert not Path("node_modules").exists()
    assert Path("pytest_examples/node_modules/prettier/bin/prettier.cjs").exists()

    assert result.exit_code == 0

    result = runner.invoke(app, ["install-prettier", "--target-dir", "./non/existent/folder"])

    assert result.exit_code == 1


def test_check():
    prepare_env()

    FILES = Path("pytest_examples/code")
    BAD_CODE = FILES / "ugly.js"
    FIXME = FILES / "fixme.js"

    result = runner.invoke(app, ["prettier", "--target", FILES / "pretty.js"])
    assert result.exit_code == 0

    shutil.copyfile(BAD_CODE, FIXME)

    result = runner.invoke(app, ["prettier", "--target", FIXME])
    assert result.exit_code == 1

    result = runner.invoke(app, ["prettier", "--target", FIXME, "--fix"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["prettier", "--target", FIXME])
    assert result.exit_code == 0

    # assume original unchanged:
    result = runner.invoke(app, ["prettier", "--target", BAD_CODE])
    assert result.exit_code == 1
