import React from 'react';
import { StaticRouter } from 'react-router-dom';
import { shallow } from 'enzyme';

import withTitlePage, {
  getCurrentTitle,
  ComposedCurrentTitlePage,
  EnhancedCurrentTitlePage,
} from './titlePages';
import { APP_NAME } from '../_constants';

describe('withTitlePage', () => {
  test('withTitlePage', () => {
    const Component = () => <div>Component</div>;
    const props = {
      test: true,
    };
    const wrapper = shallow(withTitlePage(Component)(props));
    expect(wrapper).toBeDefined();
  });

  test('EnhancedCurrentTitlePage', () => {
    const wrapper = shallow(
      <StaticRouter context={{}}>
        <EnhancedCurrentTitlePage />
      </StaticRouter>,
    );
    expect(wrapper).toBeDefined();
  });

  test('ComposedCurrentTitlePage', () => {
    const props = {
      Component: () => <div>Component</div>,
      location: {
        pathname: '/login',
      },
      test: true,
    };
    const wrapper = shallow(<ComposedCurrentTitlePage {...props} />);
    expect(wrapper).toBeDefined();
  });

  describe('getCurrentTitle', () => {
    test('Invalid values', () => {
      expect(getCurrentTitle(undefined)).toBe(APP_NAME);
      expect(getCurrentTitle(null)).toBe(APP_NAME);
      expect(getCurrentTitle(false)).toBe(APP_NAME);
      expect(getCurrentTitle(true)).toBe(APP_NAME);
      expect(getCurrentTitle('')).toBe(APP_NAME);
      expect(getCurrentTitle('undefined')).toBe(APP_NAME);
      expect(getCurrentTitle([])).toBe(APP_NAME);
      expect(getCurrentTitle({})).toBe(APP_NAME);
    });
    test('Valid values', () => {
      expect(getCurrentTitle('/')).toBe('pages:login');
      expect(getCurrentTitle('/profile')).toBe('pages:profile');
      expect(getCurrentTitle('/books')).toBe('pages:bookList');
      expect(getCurrentTitle('/admin/users')).toBe('pages:adminUserList');
    });
  });
});
