import colors from './colors';
import fontSizes from './fontSizes';

const normal = Object.freeze({
  margin: 2,
  fontWeight: '400',
  textAlign: 'center',
  whiteSpace: 'nowrap',
  verticalAlign: 'middle',
  userSelect: 'none',
  border: '1px solid transparent',
  padding: '.375rem .75rem',
  fontSizes: fontSizes.default,
  lineHeight: '1.5',
  borderRadius: '.25rem',
  color: colors.black,
  backgroundColor: colors.white,
  borderColor: colors.white,
  transition:
    'color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out',
  '&:focus': {
    outline: '0px',
  },
  '&:after, &:before': {
    boxSizing: 'border-box',
  },
});

const primary = Object.freeze({
  ...normal,
  color: colors.white,
  backgroundColor: colors.primary,
  borderColor: colors.primary,
  '&:hover': {
    backgroundColor: '#0069d9',
    borderColor: '#0062cc',
  },
});

const secondary = Object.freeze({
  ...normal,
  color: colors.white,
  backgroundColor: colors.secondary,
  borderColor: colors.secondary,
  '&:hover': {
    backgroundColor: '#5a6268',
    borderColor: '#545b62',
  },
});

const success = Object.freeze({
  ...normal,
  color: colors.white,
  backgroundColor: colors.success,
  borderColor: colors.success,
  '&:hover': {
    backgroundColor: '#218838',
    borderColor: '#1e7e34',
  },
});

const danger = Object.freeze({
  ...normal,
  color: colors.white,
  backgroundColor: colors.danger,
  borderColor: colors.danger,
  '&:hover': {
    backgroundColor: '#c82333',
    borderColor: '#bd2130',
  },
});

const warning = Object.freeze({
  ...normal,
  color: colors.black,
  backgroundColor: colors.warning,
  borderColor: colors.warning,
  '&:hover': {
    backgroundColor: '#e0a800',
    borderColor: '#d39e00',
  },
});

const info = Object.freeze({
  ...normal,
  color: colors.white,
  backgroundColor: colors.info,
  borderColor: colors.info,
  '&:hover': {
    backgroundColor: '#138496',
    borderColor: '#117a8b',
  },
});

const light = Object.freeze({
  ...normal,
  color: colors.black,
  backgroundColor: colors.light,
  borderColor: colors.light,
  '&:hover': {
    backgroundColor: '#e2e6ea',
    borderColor: '#dae0e5',
  },
});

const dark = Object.freeze({
  ...normal,
  color: colors.white,
  backgroundColor: colors.dark,
  borderColor: colors.dark,
  '&:hover': {
    backgroundColor: '#23272b',
    borderColor: '#1d2124',
  },
});

const link = Object.freeze({
  ...normal,
  fontWeight: 'bold',
  backgroundColor: 'transparent',
  border: 'transparent',
  '&:hover': {
    textDecoration: 'underline',
  },
});

const allButtons = {
  normal,
  primary,
  secondary,
  success,
  danger,
  warning,
  info,
  light,
  dark,
  link,
};

export default allButtons;
