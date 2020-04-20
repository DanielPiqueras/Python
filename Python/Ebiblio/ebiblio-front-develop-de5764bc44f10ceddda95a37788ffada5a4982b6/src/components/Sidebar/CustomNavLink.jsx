/** Packages */
import Icon from '@material-ui/core/Icon';
import PropTypes from 'prop-types';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { NavLink } from 'react-router-dom';
import styled from 'styled-components';

/** Modules */
import Box from '../Box';

const StyledLink = styled(NavLink)`
  text-decoration: none;
  display: flex;
  justify-content: ${({ isOpen }) => (isOpen ? 'space-between' : 'center')};
  padding: 4px 8px;
  font-size: 13px;
  color: gray;
  cursor: pointer;
  transition: all 0.25s ease-out;
  &:hover {
    background: #333;
    transition: all 0.25s ease-out;
  }
`;

const FadeInOutWrapper = styled(Box)`
  display: ${({ isOpen }) => (isOpen ? 'block' : 'none')};
  width: ${({ isOpen }) => (isOpen ? '100%' : '0')};
  transition: all 0.2s ease-out;
`;

const CustomNavLink = ({
  isOpen, title, to, icon,
}) => {
  const { t } = useTranslation();
  const processedTitle = t(title);
  return (
    <Box my={8}>
      <StyledLink to={to} exact activeStyle={{ color: 'blue' }}>
        <FadeInOutWrapper isOpen={isOpen} fontSize="default">
          {processedTitle}
        </FadeInOutWrapper>
        <Icon title={processedTitle} alt={processedTitle} fontSize="small">
          {icon}
        </Icon>
      </StyledLink>
    </Box>
  );
};

CustomNavLink.displayName = 'CustomNavLink';

CustomNavLink.defaultProps = {
  isOpen: false,
};

CustomNavLink.propTypes = {
  isOpen: PropTypes.bool,
  title: PropTypes.string.isRequired,
  to: PropTypes.string.isRequired,
  icon: PropTypes.objectOf(PropTypes.any).isRequired,
};

/** Export */
export default CustomNavLink;
