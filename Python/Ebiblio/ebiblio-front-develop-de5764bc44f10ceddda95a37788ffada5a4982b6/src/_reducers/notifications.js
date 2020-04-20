/** Packages */
import { prepend, filter } from 'ramda';
import uuid from 'uuid/v4';

/** Modules */
import {
  NOTIFICATIONS_NEW_INFO,
  NOTIFICATIONS_NEW_SUCCESS,
  NOTIFICATIONS_NEW_ERROR,
  NOTIFICATIONS_CLEAR_ALL,
  NOTIFICATIONS_CLEAR_BY_ID,
} from '../_actions';
import { notificationsTypes } from '../_constants';

/** Utils */
const getNotification = (type, message = '') => ({ type, message, id: uuid() });

/** Reducer */
const initialState = [];
const reducer = (state = initialState, action) => {
  switch (action.type) {
    case NOTIFICATIONS_NEW_INFO:
      return prepend(getNotification(notificationsTypes.INFO, action.payload), state);
    case NOTIFICATIONS_NEW_SUCCESS:
      return prepend(getNotification(notificationsTypes.SUCCESS, action.payload), state);
    case NOTIFICATIONS_NEW_ERROR:
      return prepend(getNotification(notificationsTypes.ERROR, action.payload), state);
    case NOTIFICATIONS_CLEAR_BY_ID:
      return filter(({ id }) => id !== action.payload, state);
    case NOTIFICATIONS_CLEAR_ALL:
      return initialState;
    default:
      return state;
  }
};

export default reducer;
