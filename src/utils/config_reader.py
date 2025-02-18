from pydantic import SecretStr, model_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv
from src.utils.checkers import is_valid_filename

class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: int
    database_type: str
    database_file: str | None = None
    job_database_file: str | None = None

    model_config = SettingsConfigDict(env_file=find_dotenv('.env'), env_file_encoding='utf-8')

    #TODO: rewrite to sqlite only, it looks horrible
    @model_validator(mode='after')
    def check_config_data(self):
        if self.database_type == 'sqlite' and not is_valid_filename(self.database_file):
            raise ValueError('When using SQLite you must specify DATABASE_FILE parameter\n'
                             f'Value provided: {self.database_file}')
        return self

    @computed_field
    @property
    def database_url_async(self) -> str:
        return f'sqlite+aiosqlite:///{self.database_file}'

    @computed_field
    @property
    def database_url_sync(self) -> str:
        return f'sqlite:///{self.database_file}'

app_config = Settings()
