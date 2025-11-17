import { Route, Routes, Navigate } from 'react-router-dom';
import MoviesPage from '~/pages/MoviePages/MoviesPages';
import MoviePage from '~/pages/MoviePages/MoviePage';
import ProtectedRoute from '~/components/ProtectedRoute';
import NotFound from '~/pages/NotFound/NotFound';
import { MOVIES_RESULT_TYPES } from '~/consts/movies';

const MoviesRoutes = () => (
  <Routes>
    <Route index element={<Navigate to="/" />} />
    <Route path="/best-rating" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.BEST_RATING} />} />
    <Route path="/new" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.NEW} />} />
    <Route path="/popular-now" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.POPULAR_NOW} />} />

    <Route element={<ProtectedRoute />}>
      <Route path="/continue-watching" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.CONTINUE_WATCHING} />} />
      <Route path="/recommendations" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.RECOMMENDATIONS} />} />
    </Route>

    <Route path="/:id" element={<MoviePage />} />
    <Route path="/*" element={<NotFound />} />
  </Routes>
);

export default MoviesRoutes;
