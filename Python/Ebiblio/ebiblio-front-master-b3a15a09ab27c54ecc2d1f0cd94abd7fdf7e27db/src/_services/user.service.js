import { buildHeaders } from '../_helpers';
import { defaultHeaders } from './constants';
import { mapObjectToSnakeCase } from '../utils';

const axios = require('axios');

const update = user => axios.put(`login/users/${user.pk}/`, mapObjectToSnakeCase(user), buildHeaders());

const getAll = () => axios.get('login/users/', buildHeaders());

const login = (username, password) => axios.post(
  'login/setLogin/',
  {
    username,
    password,
  },
  defaultHeaders,
);

function logout() {
  // remove user from local storage to log user out
  localStorage.removeItem('user');
}

const create = user => axios.post('login/users/', mapObjectToSnakeCase(user), buildHeaders());

export const userService = {
  login,
  logout,
  create,
  getAll,
  update,
};
