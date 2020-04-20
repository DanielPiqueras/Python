import PropTypes from 'prop-types';
import React from 'react';

import Flex from '../Flex';

const Main = ({ children }) => (
  <Flex justifyContent="center" width="100%" padding="xxl" overflow="auto" height="100%">
    {children}
  </Flex>
);

export default Main;

Main.propTypes = {
  children: PropTypes.node.isRequired,
};
