/** Packages */
import {
  always, cond, equals, pipe, prop, T,
} from 'ramda';
import styled from 'styled-components';

/** Modules */
import { notificationsTypes } from '../../_constants';

/** Utils */
// FIXME: Replace by theme color when it's available
const getColorNotificationByType = pipe(
  prop('type'),
  cond([
    [equals(notificationsTypes.SUCCESS), always('#4CAF50')],
    [equals(notificationsTypes.ERROR), always('#F44336')],
    [equals(notificationsTypes.INFO), always('#007bff')],
    [T, always('#3F51B5')],
  ]),
);

/** Styles */
export const StyledNotifications = styled.div`
  position: absolute;
  top: 60px;
  width: 100%;
  padding: 0 20px;

  @media (min-width: ${({ theme }) => theme.breakpointsFormated.md}) {
    right: 24px;
    width: 100%;
    max-width: 400px;
  }

`;

export const StyledNotification = styled.div`
  transition: all 0.2s;
  background: #fff;
  padding: 15px 20px;
  border-radius: 3px;
  margin-bottom: 9px;
  border-top: 8px solid;
  border-color: ${getColorNotificationByType};
  box-shadow: 0 2px 2px #33333366;
  :hover {
    opacity: 0.7;
  }
`;
