/** Packages */
import PropTypes from 'prop-types';
import { prop } from 'ramda';
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Redirect } from 'react-router-dom';

/** Modules */
import { useTitlePage } from '../../../misc';
import { Loading } from '../../../components';
import { userActions } from '../../../_actions';
import UserForm from './UserForm';

export const UserUpdateComponent = ({ match }) => {
  const dispatch = useDispatch();
  const { setTitleValues } = useTitlePage();
  const handleGetAllUsers = () => dispatch(userActions.getAll());

  const users = useSelector(prop('users'));

  if (!users.loaded && !users.requesting) handleGetAllUsers();

  const myUser = users && users.items ? users.items.find(user => user.pk.toString() === match.params.id) : {};
  React.useEffect(() => {
    if (myUser && myUser.firstName && myUser.lastName) {
      setTitleValues({ name: `${myUser.firstName} ${myUser.lastName}` });
    }
  });

  return (
    <>
      {!users.loaded && users.requesting && <Loading />}
      {users.loaded && !users.requesting && !myUser && <Redirect to="/admin/users" />}
      {users.loaded && myUser && <UserForm user={myUser} />}
    </>
  );
};

UserUpdateComponent.displayName = 'UserUpdateComponent';

UserUpdateComponent.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      id: PropTypes.string.isRequired,
    }).isRequired,
  }).isRequired,
};

export default UserUpdateComponent;
