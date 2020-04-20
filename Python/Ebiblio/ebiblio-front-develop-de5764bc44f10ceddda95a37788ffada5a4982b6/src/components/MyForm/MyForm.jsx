import TextField from '@material-ui/core/TextField';
import { Field, Form, Formik } from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import { useTranslation } from 'react-i18next';

const MyForm = ({
  initialValues, validationSchema, handleSubmit, fields, children, formKey,
}) => {
  const { t } = useTranslation();
  return (
    <Formik
      autoComplete="off"
      initialValues={initialValues}
      onSubmit={handleSubmit}
      validationSchema={validationSchema}
    >
      {({ errors, touched }) => (
        <Form>
          {fields.map(field => (
            <Field
              name={field.name}
              key={formKey + field.name}
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
                  helperText={
                    errors[field.name] && touched[field.name] ? t(errors[field.name]) : null
                  }
                  error={errors[field.name] && touched[field.name]}
                  required={field.required}
                  multiline={field.multiline}
                  rows={5}
                  {...formData}
                />
              )}
            />
          ))}
          {children}
        </Form>
      )}
    </Formik>
  );
};

export default MyForm;

MyForm.defaultProps = {
  fields: [
    {
      required: false,
    },
  ],
};

MyForm.propTypes = {
  initialValues: PropTypes.shape().isRequired,
  validationSchema: PropTypes.objectOf(PropTypes.any).isRequired,
  fields: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired,
      required: PropTypes.bool,
    }),
  ),
  handleSubmit: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired,
  formKey: PropTypes.string.isRequired,
};
