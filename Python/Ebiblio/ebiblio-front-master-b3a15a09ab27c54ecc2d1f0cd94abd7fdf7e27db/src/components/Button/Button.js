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
  buttonStyle,
  color,
  display,
  flex,
  fontSize,
  height,
  left,
  maxHeight,
  maxWidth,
  minHeight,
  minWidth,
  position,
  right,
  size,
  space,
  top,
  width,
  zIndex,
} from 'styled-system';

const Button = styled.button`
  ${buttonStyle};
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
`;

Button.displayName = 'Button';

export default Button;
