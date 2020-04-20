/** Packages */
import {
  FaceOutlined,
  GroupOutlined,
  GroupRounded,
  HistoryOutlined,
  LibraryAddOutlined,
  LibraryBooksRounded,
  ListOutlined,
  PersonAddOutlined,
  PublicRounded,
  ViewListOutlined,
} from '@material-ui/icons';
import React from 'react';

/** Constants */
export const KEY_SECTION = {
  default: 'default',
  adminUsers: 'adminUsers',
  adminBooks: 'adminBooks',
};

export const sections = Object.freeze({
  [KEY_SECTION.default]: {
    text: 'menu:mainMenu',
    icon: <PublicRounded fontSize="inherit" />,
  },
  [KEY_SECTION.adminUsers]: {
    text: 'menu:adminUser',
    icon: <GroupRounded fontSize="inherit" />,
  },
  [KEY_SECTION.adminBooks]: {
    text: 'menu:adminBook',
    icon: <LibraryBooksRounded fontSize="inherit" />,
  },
});

export const user = Object.freeze([
  {
    section: KEY_SECTION.default,
    to: '/profile',
    title: 'menu:profile',
    icon: <FaceOutlined fontSize="inherit" />,
  },
  {
    section: KEY_SECTION.default,
    to: '/history',
    title: 'menu:personalHistory',
    icon: <HistoryOutlined fontSize="inherit" />,
  },
  {
    section: KEY_SECTION.default,
    to: '/books',
    title: 'menu:bookList',
    icon: <ListOutlined fontSize="inherit" />,
  },
]);

export const admin = Object.freeze([
  {
    section: KEY_SECTION.adminUsers,
    to: '/admin/users',
    title: 'menu:adminUserList',
    icon: <GroupOutlined fontSize="inherit" />,
  },
  {
    section: KEY_SECTION.adminUsers,
    to: '/admin/users/create',
    title: 'menu:adminUserNew',
    icon: <PersonAddOutlined fontSize="inherit" />,
  },
  {
    section: KEY_SECTION.adminBooks,
    to: '/admin/books',
    title: 'menu:adminBookList',
    icon: <ViewListOutlined fontSize="inherit" />,
  },
  {
    section: KEY_SECTION.adminBooks,
    to: '/admin/books/create',
    title: 'menu:adminBookNew',
    icon: <LibraryAddOutlined fontSize="inherit" />,
  },
  {
    section: KEY_SECTION.adminBooks,
    to: '/admin/history',
    title: 'menu:adminBookHistory',
    icon: <HistoryOutlined fontSize="inherit" />,
  },
]);
