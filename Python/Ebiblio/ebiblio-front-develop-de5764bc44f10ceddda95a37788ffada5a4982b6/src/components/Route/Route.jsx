import PropTypes from 'prop-types';
import { path as rPath } from 'ramda';
import React from 'react';
import { useSelector } from 'react-redux';
import { Redirect, Route } from 'react-router-dom';

const RedirectToLoggedRoot = () => <Redirect to="/books" />;
const RedirectToUnloggedRoot = () => <Redirect to="/" />;

const GenericRoute = ({
  path, hasAccess, FallbackComponent, component,
}) => {
  if (!hasAccess) return <FallbackComponent />;
  return <Route path={path} component={component} />;
};

GenericRoute.defaultProps = {
  path: '',
  hasAccess: false,
  FallbackComponent: RedirectToUnloggedRoot,
  component: React.Fragment,
};

GenericRoute.propTypes = {
  path: PropTypes.string,
  hasAccess: PropTypes.bool,
  FallbackComponent: PropTypes.func,
  component: PropTypes.oneOfType([PropTypes.func, PropTypes.object]),
};

export const AdminRoute = ({ ...props }) => {
  const isAdminSelector = rPath(['authentication', 'user', 'isStaff']);
  const isAdmin = useSelector(isAdminSelector);
  return <GenericRoute {...props} hasAccess={isAdmin} FallbackComponent={RedirectToLoggedRoot} />;
};

export const UserRoute = ({ ...props }) => {
  const isLoggedUserSelector = rPath(['authentication', 'loggedIn']);
  const isLoggedUser = useSelector(isLoggedUserSelector);
  return <GenericRoute {...props} hasAccess={isLoggedUser} />;
};

export const UnloggedRoute = ({ ...props }) => {
  const isLoggedUserSelector = rPath(['authentication', 'loggedIn']);
  const isUnloggedUser = !useSelector(isLoggedUserSelector);
  return (
    <GenericRoute {...props} hasAccess={isUnloggedUser} FallbackComponent={RedirectToLoggedRoot} />
  );
};

export default GenericRoute;
