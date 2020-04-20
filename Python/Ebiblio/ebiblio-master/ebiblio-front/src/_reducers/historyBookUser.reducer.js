import { historyBookConstants } from '../_constants';

const initialState = {
  error: false,
  loaded: false,
  requesting: false,
};

export function historyBookUser(state = initialState, action) {
  switch (action.type) {
    case historyBookConstants.GETALL_USER_REQUEST:
      return {
        ...state,
        requesting: true,
      };

    case historyBookConstants.GETALL_USER_SUCCESS:
      return {
        ...state,
        loaded: true,
        requesting: false,
        items: action.payload,
      };

    case historyBookConstants.GETALL_USER_FAILURE:
      return {
        ...state,
        loaded: true,
        error: true,
        requesting: false,
      };

    default:
      return state;
  }
}
