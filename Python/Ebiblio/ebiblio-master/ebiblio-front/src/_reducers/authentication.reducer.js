/** Packages */
import { pipe, when, defaultTo } from 'ramda';

/** Modules */
import { isTruthy } from '../utils';

import { userConstants } from '../_constants';
import { AUTH_LOGOUT } from '../_actions';

/** Utils */
const userFromLocalStorage = pipe(
  when(isTruthy, JSON.parse),
  defaultTo(null),
)(localStorage.getItem('user'));

/** Initial state */
const initialState = userFromLocalStorage ? { loggedIn: true, user: userFromLocalStorage } : {};

/** Reducer */
const reducer = (state = initialState, action) => {
  switch (action.type) {
    case userConstants.LOGIN_REQUEST:
      return {
        loggingIn: true,
        loggingError: false,
        user: action.payload,
      };
    case userConstants.LOGIN_SUCCESS:
      return {
        loggedIn: true,
        loggingError: false,
        user: action.payload,
      };
    case userConstants.LOGIN_FAILURE:
      return {
        loggingError: true,
      };
    case AUTH_LOGOUT:
      return {};
    default:
      return state;
  }
};

/** Export */
export default reducer;
