from typing import List, Optional, Union
from pydantic import BaseModel, Field, computed_field, field_validator
from pathlib import Path
from utils import get_config

class Show(BaseModel):
    name: str
    year: int = Field(gt=1880, lt=9999)

    @property
    def folder(self):
        return f'{self.name} ({self.year})'


class Episode(BaseModel):
    number: int = Field(gt=0, lt=100)
    name: str

    @property
    def episode_nbr(self):
        return str(self.number).zfill(2)


class Season(BaseModel):
    number: int = Field(gt=0, lt=100)
    episodes: List[Episode]

    @property
    def season_nbr(self):
        return str(self.number).zfill(2)

    @property
    def folder(self):
        return f'Season {str(self.number).zfill(2)}'

    @property
    def episode_count(self):
        return len(self.episodes)


class TvShow(BaseModel):
    show: Show
    seasons: List[Season]

    @property
    def season_count(self):
        return len(self.seasons)

    @property
    def root_path(self):
        return Path(get_config('tv_show_dir'))

    def get_season(self, season_nbr: int):
        return next(season for season in self.seasons if season.number == season_nbr)

    def get_episode(self, season_nbr: int, episode_nbr: int):
        season = self.get_season(season_nbr)
        return next(episode for episode in season.episodes if episode.number == episode_nbr)

    def get_episode_filename(self, season_nbr: int, episode_nbr: int):
        season = self.get_season(season_nbr)
        episode = self.get_episode(season_nbr, episode_nbr)
        return f'{self.show.name} - s{season.season_nbr}e{episode.episode_nbr} - {episode.name}'

    def get_episode_filepath(self, season_nbr: int, episode_nbr: int):
        filename = self.get_episode_filename(season_nbr, episode_nbr)
        return self.root_path / self.show.folder / self.get_season(season_nbr).folder / filename


if __name__ == '__main__':
    show = Show(name='Breaking Bad', year=2008)

    episode1 = Episode(number=1, name='Pilot')
    episode2 = Episode(number=2, name="Cat's in the Bag...")
    episode3 = Episode(number=3, name="...And the Bag's in the River")

    season1 = Season(number=1, episodes=[episode1, episode2, episode3])

    episode1 = Episode(number=1, name='No Mas')
    episode2 = Episode(number=2, name='Caballo Sin Nombre')

    season2 = Season(number=2, episodes=[episode1, episode2])

    tv_show = TvShow(show=show, seasons=[season1, season2])

    print(f'Show folder: {tv_show.show.folder}')

    season = tv_show.get_season(1)
    print(f'Season folder: {season.folder}')

    episode = tv_show.get_episode(1, 1)
    print(f'Episode filename: {tv_show.get_episode_filename(1, 1)}')
    print(f'Episode filepath: {tv_show.get_episode_filepath(1, 1)}')
