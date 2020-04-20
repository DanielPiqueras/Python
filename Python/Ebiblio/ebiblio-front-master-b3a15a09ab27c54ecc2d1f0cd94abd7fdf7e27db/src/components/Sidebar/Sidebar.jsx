/** Packages */
import { KeyboardArrowLeftTwoTone, KeyboardArrowRightTwoTone } from '@material-ui/icons';
import PropTypes from 'prop-types';
import { path } from 'ramda';
import React, { useContext } from 'react';
import { useSelector } from 'react-redux';
import { ThemeContext } from 'styled-components';

/** Modules */
import Box from '../Box';
import Flex from '../Flex';
import LanguageSelector from '../LanguageSelector';
import Logo from '../Logo';

import { adminNavLinks, userNavLinks } from '../../_constants';
import MenuSection from './MenuSection';

/** Selectors */
const isAdminSelector = path(['authentication', 'user', 'isStaff']);

/** Component */
export const SidebarComponent = ({
  isMobileView,
  isMobileHandler,
  isSidebarExpanded,
  InOutHandler,
}) => {
  const theme = useContext(ThemeContext);

  const isAdmin = useSelector(isAdminSelector);

  return (
    <Flex
      borderRight="tinGray"
      flexDirection="column"
      height="100vh"
      bg="white"
      position="relative"
      width={
        isSidebarExpanded || isMobileView
          ? theme.sizes.menuWidthExpanded
          : theme.sizes.menuWidthCollapsed
      }
      style={{ transition: 'all 0.35s' }}
    >
      <Flex justifyContent="center">
        <Flex height="xxl" alignItems="center" my="lg">
          <Logo
            width="50px"
            color="black"
            withTitle={isSidebarExpanded || isMobileView}
          />
        </Flex>
      </Flex>

      <Box height="100%" overflow={['auto', 'auto', 'none']}>
        <MenuSection subsections={userNavLinks} isOpen={isSidebarExpanded || isMobileView} />
        {isAdmin && (
          <MenuSection subsections={adminNavLinks} isOpen={isSidebarExpanded || isMobileView} />
        )}
        <Flex justifyContent="center" my="xl">
          <LanguageSelector isLabelVisible={isSidebarExpanded || isMobileView} />
        </Flex>
      </Box>

      <Box
        bg="#ebeced"
        width="lg"
        position="absolute"
        py="xxl"
        top="40%"
        right="-25px"
        opacity="0.45"
        onClick={() => {
          if (isMobileView) isMobileHandler();
          InOutHandler();
        }}
        display={['none', 'none', 'block']}
      >
        {isSidebarExpanded || isMobileView ? (
          <KeyboardArrowLeftTwoTone />
        ) : (
          <KeyboardArrowRightTwoTone />
        )}
      </Box>
    </Flex>
  );
};

SidebarComponent.displayName = 'SidebarComponent';

SidebarComponent.defaultProps = {
  isMobileView: false,
  isSidebarExpanded: false,
};

SidebarComponent.propTypes = {
  isMobileView: PropTypes.bool,
  isMobileHandler: PropTypes.func.isRequired,
  isSidebarExpanded: PropTypes.bool,
  InOutHandler: PropTypes.func.isRequired,
};

export default React.memo(SidebarComponent);
