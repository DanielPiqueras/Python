/** Packages */
import { withInfo } from '@storybook/addon-info';
import { setOptions } from '@storybook/addon-options';
import { addDecorator, configure } from '@storybook/react';
import React from 'react';
import { ThemeProvider } from 'styled-components';

/** Modules */
import theme, { GlobalStyle } from '../src/theme';

// automatically import all files ending in *.stories.js
const req = require.context('../stories', true, /\.stories\.(js|jsx)$/);
function loadStories() {
  req.keys().forEach(filename => req(filename));
}

addDecorator(withInfo);
const initializeStorybook = () => {
  addDecorator(story => {
    localStorage.setItem('i18nextLng', 'es-ES');

    return (
      <ThemeProvider theme={theme}>
        <>
          {story()}
          <GlobalStyle />
        </>
      </ThemeProvider>
    );
  });

  setOptions({
    name: 'E-biblio',
    url: `/`,
    sidebarAnimations: true,
  });

  configure(loadStories, module);
};

initializeStorybook();
