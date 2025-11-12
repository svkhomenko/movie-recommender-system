import { Route, Routes } from 'react-router-dom';
import PageLayout from './components/PageLayout';
import Home from './pages/Home/Home';
import NotFound from './pages/NotFound/NotFound';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import EmailConfirmation from './pages/Auth/EmailConfirmation';
import SendPasswordConfirmation from './pages/Auth/SendPasswordConfirmation';
import PasswordReset from './pages/Auth/PasswordReset';
import ProtectedRoute from './components/ProtectedRoute';
import ProfileRoutes from './routes/ProfileRoutes';

function App() {
  return (
    <Routes>
      <Route element={<PageLayout />}>
        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/confirm-email" element={<EmailConfirmation />} />
        <Route path="/confirm-password-reset" element={<SendPasswordConfirmation />} />
        <Route path="/password-reset" element={<PasswordReset />} />

        <Route element={<ProtectedRoute />}>
          <Route path="profile/*" element={<ProfileRoutes />} />
        </Route>

        <Route path="/*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
