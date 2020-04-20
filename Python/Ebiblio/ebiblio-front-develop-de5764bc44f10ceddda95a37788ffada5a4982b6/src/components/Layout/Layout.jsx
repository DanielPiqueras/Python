/** Packages */
import PropTypes from 'prop-types';
import { path } from 'rambda';
import React, { useState } from 'react';
import { shallowEqual, useSelector } from 'react-redux';
import styled from 'styled-components';

/** Modules */
import Box from '../Box';
import Flex from '../Flex';
import Header from '../Header';
import Main from '../Main';
import Sidebar from '../Sidebar';

const AnimatedBox = styled(Box)`
  transform: translateX(
    ${({ isOpen, theme }) => (isOpen ? '0' : `-${theme.sizes.menuWidthExpanded}`)}
  );
  transition: transform 0.35s ease-in-out;

  @media (min-width: ${({ theme }) => theme.breakpointsFormated.md}) {
    right: auto;
    transform: translateX(0);
  }
`;

const StyledBg = styled(Box)`
  display: none;
  opacity: 0;

  @media (max-width: ${({ theme }) => theme.breakpointsFormated.md}) {
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: black;
    opacity: 0.2;
  }
`;

const Layout = ({
  sideBar, centerTop, centerMain, children,
}) => {
  const isLoggedUser = useSelector(path('authentication.loggedIn'), shallowEqual);

  const [isMobileView, setIsMobileViewState] = useState(false);
  const isMobileViewHandler = () => setIsMobileViewState(state => !state);

  const [isSidebarExpanded, setIsExpandedState] = useState(true);
  const InOutHandler = () => setIsExpandedState(state => !state);

  return isLoggedUser ? (
    <Flex
      height="100vh"
      position="relative"
      overflow="hidden"
      flexDirection={['column', 'column', 'row']}
      width="100%"
    >
      <AnimatedBox
        position={['fixed', 'fixed', 'relative']}
        isOpen={isMobileView}
        zIndex="3"
        overflow="none"
      >
        {sideBar && (
          <Sidebar
            isMobileView={isMobileView}
            isMobileHandler={isMobileViewHandler}
            isSidebarExpanded={isSidebarExpanded}
            InOutHandler={InOutHandler}
          />
        )}
      </AnimatedBox>
      <Flex flexDirection="column" width="100%" minHeight="100%" bg="lightGray" overflow="hidden">
        {isMobileView && <StyledBg onClick={isMobileViewHandler} zIndex="2" />}
        {centerTop && (
          <Header
            isMobileView={isMobileView}
            isMobileHandler={isMobileViewHandler}
            isSidebarExpanded={isSidebarExpanded}
          />
        )}

        {centerMain && <Main>{children}</Main>}
      </Flex>
    </Flex>
  ) : (
    children
  );
};

Layout.displayName = 'Layout';

Layout.defaultProps = {
  sideBar: false,
  centerTop: false,
  centerMain: false,
};

Layout.propTypes = {
  sideBar: PropTypes.bool,
  centerTop: PropTypes.bool,
  centerMain: PropTypes.bool,
  children: PropTypes.node.isRequired,
};

export default Layout;
