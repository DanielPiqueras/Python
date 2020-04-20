/** Packages */
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';

/** Modules */
import Box from '../Box';
import Flex from '../Flex';

export const TableHeader = ({ children }) => (
  <Flex bg="black" display={['none', 'none', 'flex']}>
    {children}
  </Flex>
);

const StyledRow = styled(Flex)`
  transition: all 0.2s ease-out;
  cursor: default;
  &:hover {
    box-shadow: 0px 0 21px #b5b5b5;
    transition: all 0.2s ease-out;
  }
  &:nth-child(even) {
    background-color: rgba(0, 0, 0, 0.05);
  }
`;

export const TableRow = ({ children, backgroundColor }) => (
  <StyledRow
    flexDirection={['column', 'column', 'row']}
    width="100%"
    marginBottom={['xs', 'xs', '0']}
    border={['1px solid tinGray', '1px solid tinGray', 'none']}
    borderRadius={['8px', '8px', '0']}
    display={['inline-block', 'inline-block', 'flex']}
    bg={backgroundColor}
    boxShadow={['0px 0 12px #33333326', '0px 0 12px #33333326', 'none']}
    my={['lg', 'lg', '0px']}
  >
    {children}
  </StyledRow>
);

export const TableCell = ({
  title,
  content,
  color,
  mobileWidth,
  desktopWidth,
  mobileVisibility,
  minWidth,
}) => (
  <Box
    width={[mobileWidth, mobileWidth, desktopWidth]}
    border={['none', 'none', '1px solid lightgray']}
    marginLeft="-1px"
    marginBottom="-1px"
    padding="xs"
    textAlign={['left', 'left', 'center']}
    display={[
      mobileVisibility ? 'inline-block' : 'none',
      mobileVisibility ? 'inline-block' : 'none',
      'block',
    ]}
    minWidth={minWidth}
  >
    {title && (
      <Box
        fontSize="xs"
        fontFamily="Sans"
        display={['block', 'block', 'none']}
        textAlign="center"
      >
        <b>{title}</b>
      </Box>
    )}
    <Box fontSize={['md', 'md', 'default']} color={color} textAlign="center" fontFamily="Sans">
      {content}
    </Box>
  </Box>
);

TableCell.defaultProps = {
  minWidth: '0px',
  mobileWidth: '50%',
  desktopWidth: '100%',
  color: 'black',
  mobileVisibility: true,
  title: '',
  content: '',
};

TableCell.propTypes = {
  minWidth: PropTypes.string,
  mobileWidth: PropTypes.string,
  desktopWidth: PropTypes.string,
  color: PropTypes.oneOfType([PropTypes.array, PropTypes.string]),
  mobileVisibility: PropTypes.bool,
  title: PropTypes.string,
  content: PropTypes.oneOfType([PropTypes.node, PropTypes.string, PropTypes.number]),
};

TableRow.defaultProps = {
  backgroundColor: 'white',
};

TableRow.propTypes = {
  children: PropTypes.node.isRequired,
  backgroundColor: PropTypes.string,
};

TableHeader.propTypes = {
  children: PropTypes.node.isRequired,
};
