import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '@fontsource/inter';
import { BrowserRouter } from 'react-router-dom';
import { Provider as ChakraProvider } from '~/components/ui/provider';
import { Provider as ReduxProvider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { persistor, store } from './store/store';
import Loader from './components/Loader';
import { Toaster } from '~/components/ui/toaster';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
    <ChakraProvider>
      <ReduxProvider store={store}>
        <PersistGate loading={<Loader />} persistor={persistor}>
          <BrowserRouter>
            <App />
            <Toaster />
          </BrowserRouter>
        </PersistGate>
      </ReduxProvider>
    </ChakraProvider>
  </StrictMode>,
);
