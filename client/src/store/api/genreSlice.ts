import { apiSlice } from './apiSlice';
import type { IGenreWithoutMovies } from '~/types/movie';

export const extendedApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getGenres: builder.query<IGenreWithoutMovies[], void>({
      query: () => `/genres`,
      providesTags: (result) => {
        const genres = result || [];
        return ['Genre', ...genres.map(({ id }: Pick<IGenreWithoutMovies, 'id'>) => ({ type: 'Genre' as const, id }))];
      },
    }),
  }),
});

export const { useGetGenresQuery } = extendedApiSlice;
