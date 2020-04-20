/** Packages */
import PropTypes from 'prop-types';
import { withProps } from 'recompose';

/** Modules */
import { notificationsTypes } from '../../_constants';
import { StyledNotification } from './styles';

/** Notification component */
const Notification = withProps(({ message }) => ({
  children: message,
}))(StyledNotification);

Notification.propTypes = {
  type: PropTypes.oneOf(Object.values(notificationsTypes)),
  message: PropTypes.string.isRequired,
};

/** Export */
export default Notification;
