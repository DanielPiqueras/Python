/** Packages */
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';

/** Modules */
import Box from '../Box';
import Flex from '../Flex';

import { APP_NAME } from '../../_constants';

const LogoShape = styled(Flex)`
  transition: all 0.2s ease-out;
  cursor: default;
`;

const LogoTxt = styled(Box)`
    width : ${({ isRolled }) => (isRolled ? '100%' : '2px')}
    opacity : ${({ isRolled }) => (isRolled ? '1' : '0')}
    overflow: hidden;
    transition: all .2s ease-out;
  `;

const Logo = ({ color, width, withTitle }) => (
  <>
    <LogoShape justifyContent="center" width={width} pr="xs">
      <img src="favicon.png" alt="Logo" />
    </LogoShape>
    {withTitle && (
      <LogoTxt fontSize="md" isRolled={withTitle} color={color} fontWeight="bold">
        <b>{APP_NAME}</b>
      </LogoTxt>
    )}
  </>
);

Logo.defaultProps = {
  width: '200px',
  color: '#61DAFB',
  withTitle: true,
};

Logo.propTypes = {
  width: PropTypes.string,
  color: PropTypes.string,
  withTitle: PropTypes.bool,
};

export default Logo;
