/** Packages */
import React from 'react';
import { Redirect, Switch } from 'react-router-dom';
import {
  AdminRoute, Layout, UnloggedRoute, UserRoute,
} from '../components';

/** Modules */
import { withTitlePage } from '../misc';
import { BookCreate, BookListAdmin, BookListUser } from './Books';
import { HistoryAdminList, HistoryAdminListBy, HistoryUserList } from './Histories';
import { Login } from './Login';
import Logout from './Logout';
import {
  UserCreate, UserList, UserProfile, UserUpdate,
} from './Users';

const Root = () => (
  <Layout sideBar centerTop centerMain>
    <Switch>
      <AdminRoute path="/admin/users/history/:id" component={HistoryAdminListBy} />
      <AdminRoute path="/admin/books/history/:id" component={HistoryAdminListBy} />
      <AdminRoute path="/admin/users/create" component={UserCreate} />
      <AdminRoute path="/admin/books/create" component={BookCreate} />
      <AdminRoute path="/admin/users/:id" component={UserUpdate} />
      <AdminRoute path="/admin/users" component={UserList} />
      <AdminRoute path="/admin/books" component={BookListAdmin} />
      <AdminRoute path="/admin/history" component={HistoryAdminList} />
      <UserRoute path="/profile" component={UserProfile} />
      <UserRoute path="/books" component={BookListUser} />
      <UserRoute path="/history" component={HistoryUserList} />
      <UserRoute path="/logout" component={Logout} />
      <UnloggedRoute exact path="/" component={Login} />
      <Redirect to="/" />
    </Switch>
  </Layout>
);

export default withTitlePage(Root);
