import { combineReducers } from 'redux';

import authentication from './authentication.reducer';
import { historyBooks } from './historyBook.reducer';
import { historyBookUser } from './historyBookUser.reducer';
import { users } from './user.reducer';
import { books } from './book.reducer';
import { bookInfo } from './bookInfo.reducer';
import notifications from './notifications';

const rootReducer = combineReducers({
  authentication,
  historyBooks,
  historyBookUser,
  users,
  books,
  bookInfo,
  notifications,
});

export default rootReducer;
