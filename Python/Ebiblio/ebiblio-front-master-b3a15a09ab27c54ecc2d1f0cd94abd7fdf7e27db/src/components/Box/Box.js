import styled from 'styled-components';
import {
  background,
  backgroundImage,
  backgroundPosition,
  backgroundRepeat,
  backgroundSize,
  borderColor,
  borderRadius,
  borders,
  bottom,
  boxShadow,
  color,
  typography,
  display,
  flex,
  fontSize,
  height,
  left,
  maxHeight,
  maxWidth,
  minHeight,
  minWidth,
  overflow,
  position,
  right,
  size,
  space,
  top,
  verticalAlign,
  width,
  zIndex,
} from 'styled-system';

const Box = styled.div`
  ${background};
  ${backgroundImage};
  ${backgroundPosition};
  ${backgroundRepeat};
  ${backgroundSize};
  ${borders};
  ${borderColor};
  ${borderRadius};
  ${bottom};
  ${boxShadow};
  ${color};
  ${display};
  ${flex};
  ${height};
  ${left};
  ${maxHeight};
  ${maxWidth};
  ${minHeight};
  ${minWidth};
  ${position};
  ${space},
  ${size},
  ${right};
  ${top};
  ${fontSize};
  ${width};
  ${zIndex};
  ${verticalAlign};
  ${overflow};
  ${typography};
`;

Box.displayName = 'Box';

export default Box;
