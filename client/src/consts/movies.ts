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
