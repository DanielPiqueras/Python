import { append } from 'ramda';

import { userConstants } from '../_constants';

const initialState = {
  error: false,
  loaded: false,
  requesting: false,
  creating: false,
  updating: false,
};

export function users(state = initialState, action) {
  switch (action.type) {
    case userConstants.GETALL_REQUEST:
      return {
        ...state,
        requesting: true,
      };

    case userConstants.GETALL_SUCCESS:
      return {
        ...state,
        loaded: true,
        requesting: false,
        items: action.payload,
      };

    case userConstants.GETALL_FAILURE:
      return {
        ...state,
        loaded: true,
        error: true,
        requesting: false,
      };

    case userConstants.REGISTER_REQUEST:
      return {
        ...state,
        error: false,
        creating: true,
      };

    case userConstants.REGISTER_SUCCESS:
      return {
        ...state,
        creating: false,
        items: append(action.payload, state.items),
      };

    case userConstants.REGISTER_FAILURE:
      return {
        ...state,
        error: true,
        creating: false,
      };

    case userConstants.UPDATE_REQUEST:
      return {
        ...state,
        error: false,
        updating: true,
      };

    case userConstants.UPDATE_SUCCESS:
      return {
        ...state,
        updating: false,
        items: state.items.map(user => (user.pk === action.payload.pk ? action.payload : user)),
      };

    case userConstants.UPDATE_FAILURE:
      return {
        ...state,
        error: true,
        updating: false,
      };

    default:
      return state;
  }
}
