/** Packages */
import { path } from 'ramda';
import React from 'react';
import { useSelector } from 'react-redux';

/** Modules */
import UserForm from './UserForm';

export const UserProfileComponent = () => {
  const user = useSelector(path(['authentication', 'user']));

  return <UserForm user={user} updateProfile />;
};

UserProfileComponent.displayName = 'UserProfileComponent';

export default UserProfileComponent;
