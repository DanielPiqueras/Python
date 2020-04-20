import { append } from 'ramda';

import { historyBookConstants } from '../_constants';

const initialState = {
  error: false,
  loaded: false,
  requesting: false,
  creating: false,
  updating: false,
};

export function historyBooks(state = initialState, action) {
  switch (action.type) {
    case historyBookConstants.GETALL_REQUEST:
      return {
        ...state,
        requesting: true,
      };

    case historyBookConstants.GETALL_SUCCESS:
      return {
        ...state,
        loaded: true,
        requesting: false,
        items: action.payload,
      };

    case historyBookConstants.GETALL_FAILURE:
      return {
        ...state,
        loaded: true,
        error: true,
        requesting: false,
      };

    case historyBookConstants.CREATE_REQUEST:
      return {
        ...state,
        error: false,
        creating: true,
      };

    case historyBookConstants.CREATE_SUCCESS:
      return {
        ...state,
        creating: false,
        items: append(action.payload, state.items),
      };

    case historyBookConstants.CREATE_FAILURE:
      return {
        ...state,
        error: true,
        creating: false,
      };

    default:
      return state;
  }
}
