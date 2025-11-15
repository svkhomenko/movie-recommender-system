import { tmdbApiSlice } from './tmdbApiSlice';
import type { IMoviePoster } from '~/types/movie';

export const extendedApiSlice = tmdbApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getMoviePosterPath: builder.query<IMoviePoster, number>({
      query: (id) => ({
        url: `/movie/${id}`,
        params: {
          language: 'en-US',
        },
      }),
      providesTags: (_result, _error, arg) => [{ type: 'MoviePoster' as const, id: arg }],
    }),
  }),
});

export const { useGetMoviePosterPathQuery } = extendedApiSlice;
