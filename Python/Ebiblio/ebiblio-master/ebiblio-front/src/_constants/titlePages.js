export default [
  {
    key: '/admin/users/create',
    title: 'pages:adminUserNew',
  },
  {
    key: '/admin/books/create',
    title: 'pages:adminBookNew',
  },
  {
    key: '/admin/(users|books)/history/.+',
    title: 'pages:adminHistoryOf',
  },
  {
    key: '/admin/books',
    title: 'pages:adminBookList',
  },
  {
    key: '/admin/users/.+',
    title: 'pages:adminUserUpdate',
  },
  {
    key: '/admin/users',
    title: 'pages:adminUserList',
  },
  {
    key: '/admin/history',
    title: 'pages:adminBookHistory',
  },
  {
    key: '/profile',
    title: 'pages:profile',
  },
  {
    key: '/history',
    title: 'pages:personalHistory',
  },
  {
    key: '/books',
    title: 'pages:bookList',
  },
  {
    key: '/logout',
    title: 'pages:logout',
  },
  {
    key: '/',
    title: 'pages:login',
  },
];
