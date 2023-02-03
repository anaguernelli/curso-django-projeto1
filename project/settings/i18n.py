# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
from . import BASE_DIR

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

# caso não usar o site para outros idiomas
# pode colocar abaixo como False, melhora
# minimamente a rapidez do site, caso contrário, True
USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    # para passar o caminho das traduções
    BASE_DIR / 'locale'
]