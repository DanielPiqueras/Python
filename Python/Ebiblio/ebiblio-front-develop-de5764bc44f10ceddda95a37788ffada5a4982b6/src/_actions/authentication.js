import { generateAction } from './utils';
import { userService } from '../_services';

/** Actions types */
export const AUTH_LOGOUT = 'AUTH/LOGOUT';

/** Actions to dispatch */
export const authLogout = generateAction([AUTH_LOGOUT, userService.logout]);
