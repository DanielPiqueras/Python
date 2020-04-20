import { shallow } from 'enzyme';
import React from 'react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';

import Sidebar from './Sidebar';

describe('Sidebar', () => {
  test('Should be mount correctly', () => {
    const mockStore = configureStore([]);
    const stateStore = {
      authentication: {
        user: {
          isStaff: true,
        },
      },
    };
    const store = mockStore(stateStore);
    const wrapper = shallow(
      <Provider store={store}>
        <Sidebar />
      </Provider>,
    );
    expect(wrapper).toBeDefined();
  });
});
