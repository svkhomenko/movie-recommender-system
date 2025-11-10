import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '@fontsource/inter';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from '~/components/ui/provider';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
    <Provider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  </StrictMode>,
);
