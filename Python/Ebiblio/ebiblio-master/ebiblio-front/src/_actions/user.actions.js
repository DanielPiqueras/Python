import { mapObjectToCamelCase } from '../utils';
import { userConstants } from '../_constants';
import { userService } from '../_services';
import {
  notificationsNewSuccess as notificationsNewSuccessAction,
  notificationsNewError as notificationsNewErrorAction,
} from './notifications';

const updateProfile = (userData) => {
  const request = () => ({ type: userConstants.UPDATE_REQUEST });
  const success = userResponse => ({
    type: userConstants.LOGIN_SUCCESS,
    payload: mapObjectToCamelCase(userResponse),
  });
  const failure = error => ({ type: userConstants.UPDATE_FAILURE, payload: error });

  return (dispatch) => {
    dispatch(request());

    userService
      .update(userData)
      .then((userResponse) => {
        const processedUser = mapObjectToCamelCase(userResponse.data);
        localStorage.setItem('user', JSON.stringify(processedUser));
        dispatch(success(userResponse.data));
        dispatch(notificationsNewSuccessAction('Tu perfil ha sido actualizado correctamente.'));
      })
      .catch((error) => {
        dispatch(failure(error.response.data));
        dispatch(notificationsNewErrorAction(error.response.data));
      });
  };
};

const update = (user) => {
  const request = () => ({ type: userConstants.UPDATE_REQUEST });
  const success = userResponse => ({
    type: userConstants.UPDATE_SUCCESS,
    payload: mapObjectToCamelCase(userResponse),
  });
  const failure = error => ({ type: userConstants.UPDATE_FAILURE, payload: error });

  return (dispatch) => {
    dispatch(request());

    userService
      .update(user)
      .then((result) => {
        dispatch(success(result.data));
        dispatch(notificationsNewSuccessAction('El usuario ha sido actualizado correctamente.'));
      })
      .catch((error) => {
        dispatch(failure(error.response.data));
        dispatch(notificationsNewErrorAction(error.response.data));
      });
  };
};

const getAll = () => {
  const request = () => ({ type: userConstants.GETALL_REQUEST });
  const success = userResponse => ({
    type: userConstants.GETALL_SUCCESS,
    payload: mapObjectToCamelCase(userResponse),
  });
  const failure = error => ({ type: userConstants.GETALL_FAILURE, payload: error });

  return (dispatch) => {
    dispatch(request());

    userService
      .getAll()
      .then((users) => {
        dispatch(success(JSON.parse(users.request.response)));
      })
      .catch((error) => {
        dispatch(failure(error.response.data));
        dispatch(notificationsNewErrorAction(error.response.data));
      });
  };
};

const login = (username, password) => {
  const request = () => ({ type: userConstants.LOGIN_REQUEST });
  const success = userResponse => ({
    type: userConstants.LOGIN_SUCCESS,
    payload: mapObjectToCamelCase(userResponse),
  });
  const failure = error => ({ type: userConstants.LOGIN_FAILURE, payload: error });

  return (dispatch) => {
    dispatch(request());

    userService
      .login(username, password)
      .then((userResponse) => {
        const processedUser = mapObjectToCamelCase(userResponse.data);
        localStorage.setItem('user', JSON.stringify(processedUser));
        dispatch(success(userResponse.data));
      })
      .catch((error) => {
        dispatch(failure(error.response.data));
        dispatch(notificationsNewErrorAction(error.response.data));
      });
  };
};

export const create = (user) => {
  const request = () => ({ type: userConstants.REGISTER_REQUEST });
  const success = userResponse => ({
    type: userConstants.REGISTER_SUCCESS,
    payload: mapObjectToCamelCase(userResponse),
  });
  const failure = error => ({ type: userConstants.REGISTER_FAILURE, payload: error });

  return (dispatch) => {
    dispatch(request());

    userService.create(user).then(
      (users) => {
        dispatch(success(users.data));
        dispatch(notificationsNewSuccessAction('El usuario ha sido creado correctamente.'));
      },
      (error) => {
        dispatch(failure(error));
        dispatch(notificationsNewErrorAction(error.response.data));
      },
    );
  };
};

export default {
  login,
  getAll,
  update,
  updateProfile,
  create,
};
