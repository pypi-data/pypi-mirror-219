from pathlib import Path
from tempfile import NamedTemporaryFile

import nox
from nox_poetry import Session
from nox_poetry import session

nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ['format_check', 'lint', 'type_check', 'test', 'docs']


@session(python=['pypy-3.10', '3.10', '3.11'])
def test(s: Session) -> None:
    s.install('.', 'pytest', 'pytest-cov')
    s.run(
        'python',
        '-m',
        'pytest',
        '--cov=no_name',
        '--cov-report=html',
        '--cov-report=lcov',
        '--cov-report=xml',
        '--cov-report=term-missing',
        'tests',
        *s.posargs,
    )


# For some sessions, set venv_backend="none" to simply execute scripts within the existing Poetry
# environment. This requires that nox is run within `poetry shell` or using `poetry run nox ...`.
@session(venv_backend='none')
def format(s: Session) -> None:
    s.run('ruff', 'check', '.', '--select', 'I', '--fix')
    s.run('black', '.')


@session(venv_backend='none')
def format_check(s: Session) -> None:
    s.run('ruff', 'check', '.', '--select', 'I')
    s.run('black', '--check', '.')


@session(venv_backend='none')
def lint(s: Session) -> None:
    s.run('ruff', 'check', '.')


@session(venv_backend='none')
def lint_fix(s: Session) -> None:
    s.run('ruff', 'check', '.', '--fix')


@session(venv_backend='none')
def type_check(s: Session) -> None:
    s.run('mypy', 'src', 'tests', 'noxfile.py')


@session(venv_backend='none')
def docs(s: Session) -> None:
    s.run(
        'sphinx-build',
        '--color',
        '-W',
        '-b',
        'html',
        'docs/source',
        'docs/build',
    )


@session(venv_backend='none')
def docs_check_urls(s: Session) -> None:
    s.run('sphinx-build', '--color', '-W', '-b', 'linkcheck')


@session(venv_backend='none')
def docs_test(s: Session) -> None:
    s.run('sphinx-build', '--color', '-W', '-b', 'doctest')


# Note: This reuse_venv does not yet have affect due to:
#   https://github.com/wntrblm/nox/issues/488
@session(reuse_venv=False)
def licenses(s: Session) -> None:
    # Generate a unique temporary file name. Poetry cannot write to the temp file directly on
    # Windows, so only use the name and allow Poetry to re-create it.
    with NamedTemporaryFile() as t:
        requirements_file = Path(t.name)

    # Install dependencies without installing the package itself:
    #   https://github.com/cjolowicz/nox-poetry/issues/680
    s.run_always(
        'poetry',
        'export',
        '--without-hashes',
        f'--output={requirements_file}',
        external=True,
    )
    s.install('pip-licenses', '-r', str(requirements_file))
    s.run(
        'pip-licenses',
        '--from=all',
        '--no-version',
        '--format=html',
        '--output-file=licenses-summary.html',
        *s.posargs,
    )
    requirements_file.unlink()
