export type IGenreWithoutMovies = {
  id: string;
  name: string;
};

export type ICollectionWithoutMovies = {
  id: string;
  name: string;
};

export type IMovieCrewRoleEnum = 'cast' | 'director';

export type ICrewWithoutMovies = {
  id: string;
  movie_id: string;
  crew_id: string;
  full_name: string;
  role: IMovieCrewRoleEnum;
};

export type IMovie = {
  id: string;
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
  id: string;
  poster_path: string;
};
