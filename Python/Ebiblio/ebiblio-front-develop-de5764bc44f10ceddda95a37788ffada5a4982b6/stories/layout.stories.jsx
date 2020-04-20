/** Packages */
import { boolean, withKnobs } from '@storybook/addon-knobs';
import { storiesOf } from '@storybook/react';
import React from 'react';
import { Provider } from 'react-redux';
import { StaticRouter } from 'react-router-dom';
import configureStore from 'redux-mock-store';

/** Modules */
import { Header, Sidebar } from '../src/components';

const mockStore = configureStore([]);
const stories = storiesOf('Layout', module);

stories.addDecorator(withKnobs);

stories.add('header', () => {
  const store = mockStore({});

  return (
    <Provider store={store}>
      <StaticRouter context={{}}>
        <Header
          isSidebarExpanded={boolean('Is sidebar expanded', true)}
          isMobileHandler={() => ''}
        />
      </StaticRouter>
    </Provider>
  );
});

stories.add('sidebar', () => {
  const store = mockStore({
    authentication: {
      user: {
        isStaff: boolean('Is staff', false),
      },
    },
  });

  return (
    <Provider store={store}>
      <StaticRouter context={{}}>
        <Sidebar
          isMobileView={boolean('Is mobile view', false)}
          isSidebarExpanded={boolean('Is sidebar expanded', true)}
          isMobileHandler={() => ''}
          InOutHandler={() => ''}
        />
      </StaticRouter>
    </Provider>
  );
});
