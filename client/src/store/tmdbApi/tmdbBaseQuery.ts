import { fetchBaseQuery } from '@reduxjs/toolkit/query';

const tmdbBaseQuery = fetchBaseQuery({
  baseUrl: import.meta.env.VITE_TMDB_BASE_URL,
  prepareHeaders: (headers) => {
    const token = import.meta.env.VITE_TMDB_TOKEN;
    headers.set('authorization', `Bearer ${token}`);
    return headers;
  },
});

export default tmdbBaseQuery;
