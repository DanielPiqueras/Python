/** Packages */
import { path } from 'ramda';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';
import { object } from 'yup';

/** Modules */
import {
  Box, Button, Flex, LanguageSelector, Loading, Logo, MyForm,
} from '../../components';
import { userActions } from '../../_actions';

export const LoginComponent = () => {
  const { t } = useTranslation();

  const loggingIn = useSelector(path(['authentication', 'loggingIn']));

  const dispatch = useDispatch();
  const handleSubmit = values => dispatch(userActions.login(values.username, values.password));

  const fields = [
    {
      name: 'username',
      type: 'username',
      label: 'login:username',
      required: true,
    },
    {
      name: 'password',
      type: 'password',
      label: 'login:password',
      required: true,
    },
  ];
  const initialValues = { username: '', password: '' };
  const SignInSchema = object().shape({});

  return (
    <Flex
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      height="80vh"
      padding="md"
    >
      <Flex alignItems="center">
        <Logo width="70" color="black" />
      </Flex>
      <Box width={['100%', '50%', '30%', '25%']} mt="md">
        <MyForm
          initialValues={initialValues}
          fields={fields}
          handleSubmit={handleSubmit}
          validationSchema={SignInSchema}
          formKey="loginForm"
        >
          <Flex justifyContent="space-between" my="md">
            <LanguageSelector />
            <Box>
              <Button type="submit" variant="primary">
                {!loggingIn && t('login:loggingIn')}
                {loggingIn && <Loading color="white" width="50px" height="25px" />}
              </Button>
            </Box>
          </Flex>
        </MyForm>
      </Box>
    </Flex>
  );
};

LoginComponent.displayName = 'LoginComponent';

export default LoginComponent;
