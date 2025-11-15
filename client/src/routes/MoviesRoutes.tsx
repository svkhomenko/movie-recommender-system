import { Route, Routes, Navigate } from 'react-router-dom';
import MoviePage from '~/pages/MoviePages/MoviePage';
import NotFound from '~/pages/NotFound/NotFound';

const MoviesRoutes = () => (
  <Routes>
    <Route index element={<Navigate to="/" />} />
    <Route path="/:id" element={<MoviePage />} />
    <Route path="/*" element={<NotFound />} />
  </Routes>
);

export default MoviesRoutes;
