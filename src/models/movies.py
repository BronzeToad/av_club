from pathlib import Path

from pydantic import BaseModel, Field, computed_field

from utils import create_folder, get_config


class Movie(BaseModel):
    name: str
    year: int = Field(gt=1880, lt=9999)

    @property
    def filename(self) -> str:
        return f'{self.name} ({self.year})'

    @property
    def folder(self) -> str:
        return f'{self.name} ({self.year})'

    def create_movie_folder(self):
        movie_dir = Path(get_config('movie_dir'))
        create_folder(self.folder, path=movie_dir)


if __name__ == '__main__':
    # Create a Movie instance
    movie = Movie(name='The Matrix', year=1999)

    # Check model
    print(movie.model_dump())
