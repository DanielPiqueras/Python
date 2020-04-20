import { mount } from 'enzyme';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';

import { adminNavLinks } from '../../_constants';
import MenuSection from './MenuSection';

describe('MenuSection', () => {
  test('Component should be mount correctly', () => {
    const wrapper = mount(
      <MemoryRouter>
        <MenuSection subsections={adminNavLinks} />
      </MemoryRouter>,
    );
    expect(wrapper).toBeDefined();
    expect(wrapper).toMatchSnapshot();
  });
});
