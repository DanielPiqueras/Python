import { generateActions } from './utils';

/** Action types */
export const NOTIFICATIONS_NEW_INFO = 'NOTIFICATIONS/NEW_INFO';
export const NOTIFICATIONS_NEW_SUCCESS = 'NOTIFICATIONS/NEW_SUCCESS';
export const NOTIFICATIONS_NEW_ERROR = 'NOTIFICATIONS/NEW_ERROR';
export const NOTIFICATIONS_CLEAR_ALL = 'NOTIFICATIONS/CLEAR_ALL';
export const NOTIFICATIONS_CLEAR_BY_ID = 'NOTIFICATIONS/CLEAR_BY_ID';

/** Actions to dispatch */
export const [
  notificationsNewInfo,
  notificationsNewSuccess,
  notificationsNewError,
  notificationsClearAll,
  notificationsClearById,
] = generateActions(
  NOTIFICATIONS_NEW_INFO,
  NOTIFICATIONS_NEW_SUCCESS,
  NOTIFICATIONS_NEW_ERROR,
  NOTIFICATIONS_CLEAR_ALL,
  NOTIFICATIONS_CLEAR_BY_ID,
);
