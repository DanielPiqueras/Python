import { bookConstants } from '../_constants';

const initialState = {
  loading: false,
  error: false,
};

export function bookInfo(state = initialState, action) {
  switch (action.type) {
    case bookConstants.CLEAR_INFO:
      return initialState;

    case bookConstants.GETINFO_REQUEST:
      return {
        loading: true,
        error: false,
      };

    case bookConstants.GETINFO_SUCCESS:
      return {
        ...state,
        loading: false,
        error: false,
        items: action.payload,
      };

    case bookConstants.GETINFO_FAILURE:
      return { ...initialState, error: true, items: {} };

    default:
      return state;
  }
}
