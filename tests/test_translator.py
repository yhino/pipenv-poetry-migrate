from pipenv_poetry_migrate.translator import translate_properties


def test_translate_properties() -> None:
    original = {
        "git": "https://github.com/yhino/pipenv_poetry_migrate.git",
        "ref": "develop",
        "editable": True,
    }

    translated = translate_properties(original)
    assert translated == {
        "git": "https://github.com/yhino/pipenv_poetry_migrate.git",
        "rev": "develop",
        "develop": True,
    }
