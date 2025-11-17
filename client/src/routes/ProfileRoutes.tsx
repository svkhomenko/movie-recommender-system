import { Route, Routes } from 'react-router-dom';
import ProfilePage from '~/pages/Profile/ProfilePage';
import MoviesPage from '~/pages/MoviePages/MoviesPages';
import NotFound from '~/pages/NotFound/NotFound';
import { MOVIES_RESULT_TYPES } from '~/consts/movies';

const ProfileRoutes = () => (
  <Routes>
    <Route index element={<ProfilePage />} />

    <Route path="/watch-later" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.WATCH_LATER} />} />
    <Route path="/watched" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.WATCHED} />} />
    <Route path="/own-rating" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.OWN_RATING} />} />
    <Route path="/viewing-history" element={<MoviesPage headingType={MOVIES_RESULT_TYPES.VIEWING_HISTORY} />} />

    <Route path="/*" element={<NotFound />} />
  </Routes>
);

export default ProfileRoutes;
