import { defaultHeaders } from '../_services/constants';

const authHeader = () => {
  // return authorization header with jwt token
  const user = JSON.parse(localStorage.getItem('user'));

  if (user && user.token) {
    return { Authorization: `Token ${user.token}` };
  }
  return {};
};

export default () => ({
  ...defaultHeaders,
  headers: authHeader(),
});
