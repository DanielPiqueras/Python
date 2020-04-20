/** Packages */
import React, { Suspense } from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { I18nextProvider } from 'react-i18next';
import { ThemeProvider } from 'styled-components';

/** Modules */
import { Notifications, Loading } from './components';
import i18n from './i18n';
import Pages from './pages';
import theme, { GlobalStyle } from './theme';
import { store } from './_helpers';

/** Main component */
const App = (
  <I18nextProvider i18n={i18n}>
    <Suspense fallback={<Loading />}>
      <ThemeProvider theme={theme}>
        <Provider store={store}>
          <GlobalStyle />
          <BrowserRouter>
            <Pages />
          </BrowserRouter>
          <Notifications />
        </Provider>
      </ThemeProvider>
    </Suspense>
  </I18nextProvider>
);

/** Render main component */
const rootElement = document.querySelector('div#app-root');
render(App, rootElement);
