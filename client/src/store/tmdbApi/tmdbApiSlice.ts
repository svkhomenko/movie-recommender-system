import { createApi } from '@reduxjs/toolkit/query/react';
import tmdbBaseQuery from './tmdbBaseQuery';

export const tmdbApiSlice = createApi({
  reducerPath: 'tmdbApi',
  baseQuery: tmdbBaseQuery,
  tagTypes: ['MoviePoster'],
  endpoints: (_builder) => ({}),
});
