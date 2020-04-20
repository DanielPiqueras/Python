import { append } from 'ramda';

import { bookConstants } from '../_constants';

const initialState = {
  error: false,
  loaded: false,
  requesting: false,
  creating: false,
  updating: false,
};

export function books(state = initialState, action) {
  switch (action.type) {
    case bookConstants.GETALL_REQUEST:
      return {
        ...state,
        requesting: true,
      };

    case bookConstants.GETALL_SUCCESS:
      return {
        ...state,
        loaded: true,
        requesting: false,
        items: action.payload,
      };

    case bookConstants.GETALL_FAILURE:
      return {
        ...state,
        loaded: true,
        error: true,
        requesting: false,
      };

    case bookConstants.CREATE_REQUEST:
      return {
        ...state,
        error: false,
        creating: true,
      };

    case bookConstants.CREATE_SUCCESS:
      return {
        ...state,
        creating: false,
        items: append(action.payload, state.items),
      };

    case bookConstants.CREATE_FAILURE:
      return {
        ...state,
        error: true,
        creating: false,
      };

    case bookConstants.UPDATE_REQUEST:
      return {
        ...state,
        error: false,
        updating: true,
      };

    case bookConstants.UPDATE_SUCCESS:
      return {
        ...state,
        updating: false,
        items: state.items.map(book => (book.uuidBook === action.payload.uuidBook ? action.payload : book)),
      };

    case bookConstants.UPDATE_FAILURE:
      return {
        ...state,
        error: true,
        updating: false,
      };

    case bookConstants.DELETE_REQUEST:
      return {
        ...state,
        error: false,
        deleting: true,
      };

    case bookConstants.DELETE_SUCCESS:
      return {
        deleting: false,
        items: state.items.map(book => (book.uuidBook === action.payload.uuidBook ? { ...book, deletedBook: true } : book)),
      };

    case bookConstants.DELETE_FAILURE:
      return {
        ...state,
        error: true,
        deleting: false,
      };

    default:
      return state;
  }
}
