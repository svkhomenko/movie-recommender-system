import { Route, Routes } from 'react-router-dom';
import ProfilePage from '~/pages/Profile/ProfilePage';
import NotFound from '~/pages/NotFound/NotFound';

const ProfileRoutes = () => (
  <Routes>
    <Route index element={<ProfilePage />} />
    <Route path="/*" element={<NotFound />} />
  </Routes>
);

export default ProfileRoutes;
