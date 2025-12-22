import { apiSlice } from './apiSlice';
import type { IMovie, IRating, IMoviesResponse, IMoviesParams, IMovieFromList } from '~/types/movie';
import { prepareSearchParams } from './prepareSearchParams';

export const extendedApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMovies: builder.query<IMoviesResponse, IMoviesParams>({
      query: (queryParams) => ({
        url: '/movies',
        params: prepareSearchParams(queryParams),
      }),
      transformResponse(movies: IMovieFromList[], meta: any) {
        return { movies, totalCount: Number(meta.response.headers.get('X-Total-Count')) };
      },
      providesTags: (result) => {
        const movies = result?.movies || [];
        return ['Movie', ...movies.map(({ id }: Pick<IMovie, 'id'>) => ({ type: 'Movie' as const, id }))];
      },
    }),
    getMovie: builder.query<IMovie, number>({
      query: (id) => `/movies/${id}`,
      providesTags: (_result, _error, arg) => [{ type: 'Movie' as const, id: arg }],
    }),
    addMovieToWatchLater: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watch_later`,
        method: 'POST',
      }),
      invalidatesTags: (_result, _error, arg) => ['Movie', { type: 'Movie' as const, id: arg }],
    }),
    removeMovieFromWatchLater: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watch_later`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, arg) => ['Movie', { type: 'Movie' as const, id: arg }],
    }),
    addMovieToWatched: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watched`,
        method: 'POST',
      }),
      invalidatesTags: (_result, _error, arg) => ['Movie', { type: 'Movie' as const, id: arg }],
    }),
    removeMovieFromWatched: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watched`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, arg) => ['Movie', { type: 'Movie' as const, id: arg }],
    }),
    createrMovieRating: builder.mutation<void, IRating & Pick<IMovie, 'id'>>({
      query: ({ id, ...body }) => ({
        url: `/movies/${id}/rating`,
        method: 'POST',
        body,
      }),
      invalidatesTags: (_result, _error, arg) => ['Movie', { type: 'Movie' as const, id: arg.id }],
    }),
    deleteMovieRating: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/rating`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, arg) => ['Movie', { type: 'Movie' as const, id: arg }],
    }),
    removeMovieFromViewingHistory: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/viewing_history`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, arg) => ['Movie', { type: 'Movie' as const, id: arg }],
    }),
  }),
});

export const {
  useGetMoviesQuery,
  useGetMovieQuery,
  useAddMovieToWatchLaterMutation,
  useRemoveMovieFromWatchLaterMutation,
  useAddMovieToWatchedMutation,
  useRemoveMovieFromWatchedMutation,
  useCreaterMovieRatingMutation,
  useDeleteMovieRatingMutation,
  useRemoveMovieFromViewingHistoryMutation,
} = extendedApiSlice;
