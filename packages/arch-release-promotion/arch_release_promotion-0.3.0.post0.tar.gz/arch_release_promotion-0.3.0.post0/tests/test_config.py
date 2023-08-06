import random
import tempfile
from contextlib import nullcontext as does_not_raise
from pathlib import Path
from string import ascii_letters, ascii_uppercase
from typing import ContextManager, List, Optional
from unittest.mock import patch

from pydantic import ValidationError
from pytest import mark, raises

from arch_release_promotion import config


@mark.parametrize(
    "gpgkey, packager, private_token, expectation",
    [
        (
            "".join(random.choice(ascii_uppercase) for x in range(40)),
            "Foobar McFoo <foobar@archlinux.org>",
            "".join(random.choice(ascii_letters) for x in range(20)),
            does_not_raise(),
        ),
        (
            "".join(random.choice(ascii_uppercase) for x in range(40)),
            "Foobar McFoo <foobar@archlinux.org>",
            None,
            does_not_raise(),
        ),
        (
            "".join(random.choice(ascii_uppercase) for x in range(40)),
            "",
            "".join(random.choice(ascii_letters) for x in range(20)),
            raises(ValueError),
        ),
        (
            "".join(random.choice(ascii_uppercase) for x in range(40)),
            "Foobar McFoo <foobar@archlinux.org>",
            "".join(random.choice(ascii_letters) for x in range(10)),
            raises(ValueError),
        ),
        (
            "".join(random.choice(ascii_uppercase) for x in range(40)),
            "Foobar McFoo",
            "".join(random.choice(ascii_letters) for x in range(20)),
            raises(ValueError),
        ),
        (
            "".join(random.choice(ascii_uppercase) for x in range(40)),
            "<foobar@archlinux.org>",
            "".join(random.choice(ascii_letters) for x in range(20)),
            raises(ValueError),
        ),
        (
            "".join(random.choice(ascii_uppercase) for x in range(40)),
            "Foobar McFoo <foobar@mc.fooface>",
            "".join(random.choice(ascii_letters) for x in range(20)),
            raises(ValueError),
        ),
        (
            "".join(random.choice(ascii_uppercase) for x in range(10)),
            "Foobar McFoo <foobar@archlinux.org>",
            "".join(random.choice(ascii_letters) for x in range(20)),
            raises(ValueError),
        ),
    ],
)
def test_settings(
    gpgkey: str,
    packager: str,
    private_token: Optional[str],
    expectation: ContextManager[str],
) -> None:
    conf = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".conf", delete=False)
    conf.write(f"GPGKEY='{gpgkey}'\n")
    conf.write(f"PACKAGER='{packager}'\n")
    if private_token:
        conf.write(f"PRIVATE_TOKEN={private_token}\n")
    conf.close()

    with patch("arch_release_promotion.config.MAKEPKG_CONFIGS", [Path(conf.name)]):
        with expectation:
            assert config.Settings()  # type: ignore[call-arg]
    Path(conf.name).unlink()


@mark.parametrize(
    "create_config, config_rows, name, expectation",
    [
        (
            True,
            [
                "[[projects]]",
                'name = "foo/bar"',
                'job_name = "build"',
                'metrics_file = "metrics.txt"',
                'output_dir = "output"',
                'releases = [{name = "test",version_metrics = ["bar"],extensions_to_sign = [".baz"]}]',
            ],
            "foo/bar",
            does_not_raise(),
        ),
        (
            True,
            [
                "[sync_config]",
                'directory = "foo"',
                "backlog = 2",
                "[[projects]]",
                'name = "foo/bar"',
                'job_name = "build"',
                'metrics_file = "metrics.txt"',
                'output_dir = "output"',
                'releases = [{name = "test",version_metrics = ["bar"],extensions_to_sign = [".baz"]}]',
            ],
            "foo/bar",
            does_not_raise(),
        ),
        (
            True,
            [
                "[[projects]]",
                'name = "foo/bar"',
                'job_name = "build"',
                'metrics_file = "metrics.txt"',
                'output_dir = "output"',
                'releases = [{name = "test",version_metrics = ["bar"],extensions_to_sign = [".baz"]}]',
                "[projects.sync_config]",
                'directory = "foo"',
                "sync_backlog = 2",
            ],
            "foo/bar",
            does_not_raise(),
        ),
        (
            True,
            [
                "[[projects]]",
                'name = "foo/bar"',
                'job_name = "build"',
                'metrics_file = "metrics.txt"',
                'output_dir = "output"',
                'releases = [{name = "test",version_metrics = ["bar"],extensions_to_sign = [".baz"]}]',
            ],
            "foo/baz",
            raises(RuntimeError),
        ),
        (
            True,
            [
                "[[projects]]",
                'name = "foo/bar"',
                'job_name = "build"',
                'metrics_file = "metrics.txt"',
                'output_dir = "output"',
                "releases = [",
                '  {name = "test", extensions_to_sign = [".baz"]},',
                '  {name = "test", extensions_to_sign = [".bar"]},',
                "]",
            ],
            "foo/bar",
            raises(ValidationError),
        ),
        (
            False,
            [],
            "",
            raises(RuntimeError),
        ),
        (
            True,
            [],
            "",
            raises(RuntimeError),
        ),
    ],
)
def test_projects(
    create_config: bool,
    config_rows: List[str],
    name: str,
    expectation: ContextManager[str],
) -> None:
    if create_config:
        conf = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".conf", delete=False)
        for row in config_rows:
            conf.write(f"{row}\n")
        conf.close()

        with patch("arch_release_promotion.config.PROJECTS_CONFIGS", [Path(conf.name)]):
            with expectation:
                projects = config.Projects()  # type: ignore[call-arg]
                assert projects
                assert isinstance(projects.get_project(name=name), config.ProjectConfig)

        Path(conf.name).unlink()
    else:
        with patch("arch_release_promotion.config.PROJECTS_CONFIGS", [Path("foo.bar")]):
            with expectation:
                assert config.Projects()  # type: ignore[call-arg]
