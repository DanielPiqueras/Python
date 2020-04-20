/** Packages */
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import TextField from '@material-ui/core/TextField';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { Field } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch } from 'react-redux';

/** Modules */
import {
  Box, Button, Flex, MyForm,
} from '../../../components';
import { userActions } from '../../../_actions';
import { UserUpdateSchema } from './validationSchema';

export const UserFormComponent = ({ user, updateProfile }) => {
  const { t } = useTranslation();
  const dispatch = useDispatch();

  const handleSubmit = (userData) => {
    const updateUser = { ...user, ...userData };
    if (updateProfile) {
      return dispatch(userActions.updateProfile(updateUser));
    }
    return dispatch(userActions.update(updateUser));
  };

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
  ];

  const passwordFields = [
    {
      name: 'oldPassword',
      type: 'password',
      label: 'users:oldPassword',
    },
    {
      name: 'password',
      type: 'password',
      label: 'users:password',
    },
    {
      name: 'repeatPassword',
      type: 'password',
      label: 'users:repeatPassword',
    },
  ];

  const initialValues = {
    username: user.username,
    firstName: user.firstName,
    lastName: user.lastName,
    email: user.email,
  };

  return (
    <Box width={['100%', '85%', '70%']}>
      <MyForm
        initialValues={initialValues}
        fields={fields}
        handleSubmit={handleSubmit}
        validationSchema={UserUpdateSchema}
        formKey="profileForm"
      >
        <Box my="md">
          <ExpansionPanel style={{ backgroundColor: '#f1f1f157' }}>
            <ExpansionPanelSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1a-content"
              id="panel1a-header"
            >
              {t('users:changePassword')}
            </ExpansionPanelSummary>
            <ExpansionPanelDetails>
              <Box width="100%">
                {passwordFields.map(field => (
                  <Field
                    name={field.name}
                    key={`profileForm${field.name}`}
                    render={({ field: formData }) => (
                      <TextField
                        label={t(field.label)}
                        id={field.name}
                        name={field.name}
                        type={field.type}
                        autoComplete="off"
                        fullWidth
                        variant="outlined"
                        margin="normal"
                        {...formData}
                      />
                    )}
                  />
                ))}
              </Box>
            </ExpansionPanelDetails>
          </ExpansionPanel>
        </Box>
        <Flex justifyContent="center" my="md" width="100%">
          <Button type="submit" variant="primary">
            {t('common:save')}
          </Button>
        </Flex>
      </MyForm>
    </Box>
  );
};

UserFormComponent.defaultProps = {
  updateProfile: false,
};

UserFormComponent.propTypes = {
  updateProfile: PropTypes.bool,
  user: PropTypes.shape({
    pk: PropTypes.number.isRequired,
    isStaff: PropTypes.bool,
    isActive: PropTypes.bool,
    firstName: PropTypes.string,
    lastName: PropTypes.string,
    username: PropTypes.string.isRequired,
    email: PropTypes.string,
  }).isRequired,
};

export default UserFormComponent;
