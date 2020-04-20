/** Packages */
import { LibraryBooksRounded } from '@material-ui/icons';
import { mount } from 'enzyme';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';

/** Modules */
import CustomNavLink from './CustomNavLink';

describe('CustomNavLink', () => {
  test('Component should be mount correctly', () => {
    const mock = {
      to: 'toFake',
      title: 'titleFake',
      icon: <LibraryBooksRounded fontSize="inherit" />,
    };
    const wrapper = mount(
      <MemoryRouter>
        <CustomNavLink {...mock} />
      </MemoryRouter>,
    );
    expect(wrapper).toBeDefined();
    expect(wrapper).toMatchSnapshot();
  });
});
