/** Packages */
import Switch from '@material-ui/core/Switch';
import { Field } from 'formik';
import { path } from 'ramda';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

/** Modules */
import {
  Button, Box, Flex, MyForm, Loading,
} from '../../../components';
import { userActions } from '../../../_actions';
import { UserCreateSchema } from './validationSchema';

export const UserCreateComponent = () => {
  const { t } = useTranslation();
  const dispatch = useDispatch();

  const isCreating = useSelector(path(['users', 'creating']));
  const handleSubmit = user => dispatch(userActions.create(user));

  const fields = [
    {
      name: 'username',
      type: 'username',
      label: 'users:username',
      required: true,
    },
    {
      name: 'firstName',
      type: 'text',
      label: 'users:firstName',
      required: true,
    },
    {
      name: 'lastName',
      type: 'text',
      label: 'users:lastName',
      required: true,
    },
    {
      name: 'email',
      type: 'email',
      label: 'users:email',
      required: true,
    },
    {
      name: 'password',
      type: 'password',
      label: 'users:password',
      required: true,
    },
    {
      name: 'repeatPassword',
      type: 'password',
      label: 'users:repeatPassword',
      required: true,
    },
  ];

  const initialValues = {
    username: '',
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    repeatPassword: '',
  };

  return (
    <Box width={['100%', '85%', '70%']}>
      <MyForm
        initialValues={initialValues}
        fields={fields}
        handleSubmit={handleSubmit}
        validationSchema={UserCreateSchema}
        formKey="userCreateForm"
      >
        <Box mt="md">
          <Field
            name="isStaff"
            key="userCreateFormIsStaff"
            render={({ field: formData }) => (
              <>
                <Switch color="primary" {...formData} />
                {t('users:isStaff')}
              </>
            )}
          />
        </Box>
        <Flex justifyContent="center" my="md" width="100%">
          <Button type="submit" variant="primary">
            {isCreating ? <Loading color="white" width="40px" height="40px" /> : t('common:save')}
          </Button>
        </Flex>
      </MyForm>
    </Box>
  );
};

UserCreateComponent.displayName = 'UserCreateComponent';

export default UserCreateComponent;
