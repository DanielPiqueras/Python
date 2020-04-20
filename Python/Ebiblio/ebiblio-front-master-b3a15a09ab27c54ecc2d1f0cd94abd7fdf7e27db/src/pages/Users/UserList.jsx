/** Packages */
import { Check, Close, LensTwoTone } from '@material-ui/icons';
import { assoc, path, prop } from 'ramda';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

/** Modules */
import {
  Box, Loading, StyledLink, TableCell, TableHeader, TableRow,
} from '../../components';
import { userActions } from '../../_actions';

export const UserListComponent = () => {
  const { t } = useTranslation();
  const dispatch = useDispatch();

  const handleGetAllUsers = () => dispatch(userActions.getAll());
  const handleUpdate = userUpdate => dispatch(userActions.update(userUpdate));

  const user = useSelector(path(['authentication', 'user']));
  const users = useSelector(prop('users'));

  if (!users.loaded && !users.requesting) handleGetAllUsers();

  const notUsers = users && users.items && users.items.length === 1 && (
    <TableRow>
      <TableCell desktopWidth="100%" mobileWidth="100%" content={t('users:notUsers')} />
    </TableRow>
  );

  const processedUsers = users && users.items && users.items
    ? users.items.map(
      userList => userList.pk !== user.pk && (
        <TableRow key={userList.pk}>
          <TableCell
            minWidth="40px"
            desktopWidth="1%"
            title="#"
            content={userList.pk ? userList.pk : '-'}
            mobileVisibility={false}
          />
          <TableCell
            minWidth="100px"
            desktopWidth="1%"
            title={t('users:username')}
            content={userList.username ? userList.username : '-'}
          />
          <TableCell
            title={t('users:firstName')}
            content={`${userList.firstName} ${userList.lastName}`}
          />
          <TableCell
            minWidth="200px"
            desktopWidth="1%"
            title={t('users:email')}
            content={userList.email ? userList.email : '-'}
          />
          <TableCell
            minWidth="135px"
            desktopWidth="1%"
            title={t('users:isStaff')}
            content={
                    userList.isStaff ? (
                      <Check
                        onClick={() => handleUpdate(assoc('isStaff', !userList.isStaff, userList))}
                        htmlColor="green"
                      />
                    ) : (
                      <Close
                        onClick={() => handleUpdate(assoc('isStaff', !userList.isStaff, userList))}
                        htmlColor="red"
                      />
                    )
                  }
          />
          <TableCell
            title={t('users:active')}
            minWidth="75px"
            desktopWidth="1%"
            content={(
              <LensTwoTone
                onClick={() => handleUpdate(assoc('isActive', !userList.isActive, userList))}
                htmlColor={userList.isActive ? 'green' : 'red'}
              />
)}
          />
          <TableCell
            content={(
              <>
                <StyledLink variant="link" color="primary" to={`/admin/users/${userList.pk}`}>
                  {t('common:edit')}
                </StyledLink>
                {' '}
                <StyledLink
                  variant="link"
                  color="success"
                  to={`/admin/users/history/${userList.pk}`}
                >
                  {t('common:history')}
                </StyledLink>
              </>
)}
          />
        </TableRow>
      ),
    )
    : [];

  return (
    <>
      {!users.loaded && users.requesting && <Loading />}
      {users.loaded && (
        <Box width="100%">
          <TableHeader>
            <TableCell minWidth="40px" desktopWidth="1%" content="#" color="white" />
            <TableCell
              minWidth="100px"
              desktopWidth="1%"
              content={t('users:username')}
              color="white"
            />
            <TableCell content={t('users:firstName')} color="white" />
            <TableCell
              minWidth="200px"
              desktopWidth="1%"
              content={t('users:email')}
              color="white"
            />
            <TableCell
              minWidth="135px"
              desktopWidth="1%"
              content={t('users:isStaff')}
              color="white"
            />
            <TableCell
              minWidth="75px"
              desktopWidth="1%"
              content={t('users:active')}
              color="white"
            />
            <TableCell />
          </TableHeader>
          {notUsers}
          {processedUsers}
        </Box>
      )}
    </>
  );
};

UserListComponent.displayName = 'UserListComponent';

export default UserListComponent;
