from app.core.config import Settings


def test_database_url_preserves_special_characters_and_hides_password() -> None:
    password = "fictitious:p@ss/%word"
    settings = Settings(_env_file=None, postgres_password=password)

    assert settings.database_url.password == password
    assert settings.database_url.drivername == "postgresql+psycopg"
    assert password not in str(settings.database_url)
    assert password not in repr(settings)
