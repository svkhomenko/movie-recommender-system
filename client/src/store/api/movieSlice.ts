import { apiSlice } from './apiSlice';
import type { IMovie } from '~/types/movie';

export const extendedApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMovie: builder.query<IMovie, number>({
      query: (id) => `/movies/${id}`,
      providesTags: (_result, _error, arg) => [{ type: 'Movie' as const, id: arg }],
    }),
    addMovieToWatchLater: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watch_later`,
        method: 'POST',
      }),
      invalidatesTags: (_result, _error, arg) => [{ type: 'Movie' as const, id: arg }],
    }),
    removeMovieFromWatchLater: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watch_later`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, arg) => [{ type: 'Movie' as const, id: arg }],
    }),
    addMovieToWatched: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watched`,
        method: 'POST',
      }),
      invalidatesTags: (_result, _error, arg) => [{ type: 'Movie' as const, id: arg }],
    }),
    removeMovieFromWatched: builder.mutation<void, number>({
      query: (id) => ({
        url: `/movies/${id}/watched`,
        method: 'DELETE',
      }),
      invalidatesTags: (_result, _error, arg) => [{ type: 'Movie' as const, id: arg }],
    }),
  }),
});

export const {
  useGetMovieQuery,
  useAddMovieToWatchLaterMutation,
  useRemoveMovieFromWatchLaterMutation,
  useAddMovieToWatchedMutation,
  useRemoveMovieFromWatchedMutation,
} = extendedApiSlice;
