from app.db.models import Language
from app.schemas.language import LanguageResponse, LanguageVersionResponse


def fetch_languages(db_session):
    languages = db_session.query(Language).all()
    response = []

    for language in languages:
        language_versions = [
            LanguageVersionResponse(version=version.version, id=version.id)
            for version in language.versions
        ]
        language_data = LanguageResponse(
            name=language.name,
            uuid=language.uuid,
            versions=language_versions
        )

        response.append(language_data)

    return response
