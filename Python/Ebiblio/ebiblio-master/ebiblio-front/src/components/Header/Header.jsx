/** Packages */
import Icon from '@material-ui/core/Icon';
import { MenuTwoTone, PowerSettingsNewOutlined } from '@material-ui/icons';
import PropTypes from 'prop-types';
import React, { useContext } from 'react';
import { ThemeContext } from 'styled-components';
/** Modules */
import Box from '../Box';
import Button from '../Button';
import Flex from '../Flex';
import StyledLink from '../StyledLink';

import { useTitlePage } from '../../misc';

const Header = ({ isMobileHandler }) => {
  const theme = useContext(ThemeContext);
  const { title } = useTitlePage();

  return (
    <Flex
      height={theme.sizes.headerHeight}
      width="100%"
      alignItems="center"
      borderBottom="tinGray"
      bg="white"
      px="lg"
      justifyContent="space-between"
    >
      <Button variant="normal" onClick={isMobileHandler} display={['block', 'block', 'none']}>
        <Icon title="Menú" fontSize="large">
          <MenuTwoTone fontSize="inherit" />
        </Icon>
      </Button>
      <Box fontSize="md">{title}</Box>

      <StyledLink variant="link" to="/logout">
        <Icon title="Cerrar sesión" fontSize="large">
          <PowerSettingsNewOutlined fontSize="inherit" />
        </Icon>
      </StyledLink>
    </Flex>
  );
};

export default React.memo(Header);

Header.propTypes = {
  isMobileHandler: PropTypes.func.isRequired,
};
