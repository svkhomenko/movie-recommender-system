import { apiSlice } from './apiSlice';
import type { IMovie } from '~/types/movie';

export const extendedApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMovie: builder.query<IMovie, number>({
      query: (id) => `/movies/${id}`,
      providesTags: (_result, _error, arg) => [{ type: 'Movie' as const, id: arg }],
    }),
  }),
});

export const { useGetMovieQuery } = extendedApiSlice;
