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

export type IMovieFromList = {
  id: number;
  title: string;
  overview: string;
  keywords: string;
  release_date: string;
  poster_path: string;
  vote_average: number;
  vote_count: number;
  latest_viewed_at?: string;
  explanation?: string;

  genres: IGenreWithoutMovies[];
  collections: ICollectionWithoutMovies[];
};

export type IMovie = IMovieFromList & {
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

export type IMoviesResponse = {
  movies: IMovieFromList[];
  totalCount: number;
};

export type IMoviesResultTypeEnum =
  | 'best_rating'
  | 'new'
  | 'popular_now'
  | 'continue_watching'
  | 'recommendations'
  | 'watch_later'
  | 'watched'
  | 'own_rating'
  | 'viewing_history';

export type IMoviesParams = {
  limit?: number;
  offset?: number;
  q?: string;
  year_min?: number;
  year_max?: number;
  genre_ids?: number[];
  result_type?: IMoviesResultTypeEnum;
};
