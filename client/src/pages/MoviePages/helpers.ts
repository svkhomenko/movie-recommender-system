import { type IGenreWithoutMovies, type ICollectionWithoutMovies, type ICrewWithoutMovies } from '~/types/movie';

export const getRealiseDate = (date: string) => {
  return new Date(date).toLocaleDateString();
};

export const getGenres = (genres: IGenreWithoutMovies[]) => {
  const genresNames = genres.map((genre) => genre.name.toLowerCase());
  return genresNames.join(', ');
};

export const getCollections = (collections: ICollectionWithoutMovies[]) => {
  const collectionsNames = collections.map((collection) => collection.name);
  return collectionsNames.join(', ');
};

export const getCrewNames = (crew: ICrewWithoutMovies[]) => {
  const crewNames = crew.map((crewMember) => crewMember.full_name);
  return crewNames.join(', ');
};
