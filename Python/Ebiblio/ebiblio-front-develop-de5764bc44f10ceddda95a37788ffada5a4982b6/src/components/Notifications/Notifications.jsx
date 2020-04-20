/** Packages */
import { prop } from 'ramda';
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';

/** Modules */
import { notificationsClearById as notificationsClearByIdAction } from '../../_actions';
import Notification from './Notification';
import { StyledNotifications } from './styles';

/** Constants */
const TIME_LIFE = 5 * 1000;

/** Utils */
const notificationsSelector = prop('notifications');
const getNotifications = (notifications = [], clearNotification) => notifications.map(({ id = null, message = '', type = null }) => {
  if (!type) return null;
  setTimeout(clearNotification, TIME_LIFE, id);
  return (
    <Notification
      key={id}
      onClick={() => clearNotification(id)}
      id={id}
      message={message}
      type={type}
    />
  );
});

/** Notifications container component */
const Notifications = () => {
  const notificationsStack = useSelector(notificationsSelector);
  const dispatch = useDispatch();
  const clearNotification = id => dispatch(notificationsClearByIdAction(id));
  const notificationProcessed = getNotifications(notificationsStack, clearNotification);
  return <StyledNotifications>{notificationProcessed}</StyledNotifications>;
};

/** Export */
export default Notifications;
