import { object, ref, string } from 'yup';

export const UserUpdateSchema = object().shape({
  username: string().required('users:usernameMessage'),
  firstName: string().required('users:firstNameMessage'),
  lastName: string().required('users:lastNameMessage'),
  email: string().required('users:emailMessage'),
  password: string()
    .trim()
    .oneOf([ref('repeatPassword')], 'users:repeatPasswordMessage'),
  repeatPassword: string()
    .trim()
    .oneOf([ref('password')], 'users:repeatPasswordMessage'),
});
