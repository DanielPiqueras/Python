/** Packages */
import React from 'react';
import { Redirect } from 'react-router-dom';
import { useDispatch } from 'react-redux';

/** Modules */
import { authLogout as authLogoutAction, notificationsClearAll } from '../../_actions';

/** Utils */
const clearUserInLocalStorage = () => localStorage.removeItem('user');

/** Component */
const LogoutComponent = () => {
  /** Clear user in local storage */
  clearUserInLocalStorage();

  /** Dispatch logout and clear all notifications */
  const dispatch = useDispatch();

  dispatch(authLogoutAction());
  dispatch(notificationsClearAll());

  return <Redirect to="/" />;
};

/** Export */
LogoutComponent.displayName = 'LogoutComponent';

export default LogoutComponent;
