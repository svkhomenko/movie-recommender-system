import type { IMoviesResultTypeEnum } from '~/types/movie';

export const MOVIES_RESULT_TYPES = {
  BEST_RATING: 'best_rating' as IMoviesResultTypeEnum,
  NEW: 'new' as IMoviesResultTypeEnum,
  POPULAR_NOW: 'popular_now' as IMoviesResultTypeEnum,
  CONTINUE_WATCHING: 'continue_watching' as IMoviesResultTypeEnum,
  RECOMMENDATIONS: 'recommendations' as IMoviesResultTypeEnum,
  WATCH_LATER: 'watch_later' as IMoviesResultTypeEnum,
  WATCHED: 'watched' as IMoviesResultTypeEnum,
  OWN_RATING: 'own_rating' as IMoviesResultTypeEnum,
  VIEWING_HISTORY: 'viewing_history' as IMoviesResultTypeEnum,
};

export const HEADING_MAP = {
  [MOVIES_RESULT_TYPES.BEST_RATING]: 'Top Rated Movies',
  [MOVIES_RESULT_TYPES.NEW]: 'New Movies',
  [MOVIES_RESULT_TYPES.POPULAR_NOW]: 'Popular Now Movies',
  [MOVIES_RESULT_TYPES.CONTINUE_WATCHING]: 'Continue Watching Collection',
  [MOVIES_RESULT_TYPES.RECOMMENDATIONS]: 'Recommended Movies',
  [MOVIES_RESULT_TYPES.WATCH_LATER]: 'Watch Later Movies',
  [MOVIES_RESULT_TYPES.WATCHED]: 'Watched Movies',
  [MOVIES_RESULT_TYPES.OWN_RATING]: 'Rated Movies',
  [MOVIES_RESULT_TYPES.VIEWING_HISTORY]: 'Viewing History',
};
