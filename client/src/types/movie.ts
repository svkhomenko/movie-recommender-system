export type IGenreWithoutMovies = {
  id: number;
  name: string;
};

export type ICollectionWithoutMovies = {
  id: number;
  name: string;
};

export type IMovieCrewRoleEnum = 'cast' | 'director';

export type ICrewWithoutMovies = {
  id: number;
  movie_id: number;
  crew_id: number;
  full_name: string;
  role: IMovieCrewRoleEnum;
};

export type IMovie = {
  id: number;
  title: string;
  overview: string;
  keywords: string;
  release_date: string;
  poster_path: string;
  vote_average: number;
  vote_count: number;
  latest_viewed_at?: Date;

  genres: IGenreWithoutMovies[];
  collections: ICollectionWithoutMovies[];

  rating?: number;
  watch_later?: boolean;
  watched?: boolean;

  casts: ICrewWithoutMovies[];
  directors: ICrewWithoutMovies[];
};

export type IMoviePoster = {
  id: number;
  poster_path: string;
};

export type IRating = {
  rating: number;
};
