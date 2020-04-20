import PropTypes from 'prop-types';
import { compose, setDisplayName, withProps } from 'recompose';
import styled from 'styled-components';
import {
  alignContent,
  alignItems,
  alignSelf,
  display as displayFunc,
  flex,
  flexBasis,
  flexDirection,
  flexWrap,
  justifyContent,
  justifySelf,
  order,
} from 'styled-system';
import Box from '../Box';

const StyledFlex = styled(Box)`
  ${alignContent};
  ${alignItems};
  ${alignSelf};
  ${displayFunc};
  ${flex};
  ${flexBasis};
  ${flexDirection};
  ${flexWrap};
  ${justifyContent};
  ${justifySelf};
  ${order};
`;

StyledFlex.displayName = 'StyledFlex';

StyledFlex.defaultProps = {
  children: undefined,
  as: 'div',
};

StyledFlex.propTypes = {
  children: PropTypes.node,
};

export default compose(
  setDisplayName('Flex'),
  withProps(({ isFlexChild, display }) => ({
    display: !isFlexChild && !display ? 'flex' : display,
  })),
  // omitProps(['isFlexChild']),
)(StyledFlex);
