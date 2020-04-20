import PropTypes from 'prop-types';
import React from 'react';
import Button from './Button';

export const ConditionalButton = ({ condition, children, ...props }) => {
  if (!condition) return null;
  return <Button {...props}>{children}</Button>;
};

ConditionalButton.displayName = 'ConditionalButton';

ConditionalButton.propTypes = {
  condition: PropTypes.bool.isRequired,
  children: PropTypes.node.isRequired,
};
