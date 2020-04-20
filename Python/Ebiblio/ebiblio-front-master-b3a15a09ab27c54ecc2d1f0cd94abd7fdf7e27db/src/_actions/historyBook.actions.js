import {
  juxt, mergeAll, path, pickAll, pipe, prop,
} from 'ramda';

import { mapObjectToCamelCase } from '../utils';
import { bookConstants, historyBookConstants } from '../_constants';
import { historyBookService } from '../_services';
import {
  notificationsNewSuccess as notificationsNewSuccessAction,
  notificationsNewError as notificationsNewErrorAction,
} from './notifications';

const getAll = () => {
  const request = () => ({ type: historyBookConstants.GETALL_REQUEST });
  const success = bookResponse => ({
    type: historyBookConstants.GETALL_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });
  const failure = error => ({ type: historyBookConstants.GETALL_FAILURE, payload: error });

  return (dispatch) => {
    dispatch(request());

    historyBookService
      .getAll()
      .then((books) => {
        dispatch(success(books.data));
      })
      .catch((error) => {
        const message = path(['response', 'data'], error);
        dispatch(failure(message));
        dispatch(notificationsNewErrorAction(message));
      });
  };
};

const getAllByUser = (pk) => {
  const request = () => ({ type: historyBookConstants.GETALL_USER_REQUEST });
  const success = bookResponse => ({
    type: historyBookConstants.GETALL_USER_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });
  const failure = error => ({ type: historyBookConstants.GETALL_USER_FAILURE, payload: error });

  return (dispatch) => {
    dispatch(request());
    historyBookService
      .getAllByUser(pk)
      .then((books) => {
        dispatch(success(books.data));
      })
      .catch((error) => {
        const message = path(['response', 'data'], error);
        dispatch(failure(message));
        dispatch(notificationsNewErrorAction(message));
      });
  };
};

// TODO: Move to book.action maybe
const create = (uuidBook, pk, reservedBook) => {
  const request = () => ({ type: historyBookConstants.CREATE_REQUEST });
  const success = bookResponse => ({
    type: historyBookConstants.CREATE_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });
  const failure = error => ({ type: historyBookConstants.CREATE_FAILURE, payload: error });

  const updateBook = bookResponse => ({
    type: bookConstants.UPDATE_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });

  return (dispatch) => {
    dispatch(request());

    historyBookService.create(uuidBook, pk, reservedBook).then(
      (bookResult) => {
        dispatch(success(bookResult.data));
        const newBookData = pipe(
          juxt([
            path(['data', 'book']),
            pipe(
              prop('data'),
              pickAll(['uuid_loan']),
            ),
          ]),
          mergeAll,
        )(bookResult);

        dispatch(updateBook(newBookData));
        dispatch(notificationsNewSuccessAction('El historial ha sido creado correctamente'));
      },
      (error) => {
        dispatch(failure(error.response.data));
        dispatch(notificationsNewErrorAction(error.response.data));
      },
    );
  };
};

// TODO: Move to book.action maybe
const update = (uuidLoan, uuidBook, pk, renew) => {
  const request = () => ({
    type: bookConstants.UPDATE_REQUEST,
  });

  const failure = error => ({ type: bookConstants.UPDATE_FAILURE, payload: error });

  const updateBook = bookResponse => ({
    type: bookConstants.UPDATE_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });

  return (dispatch) => {
    dispatch(request());

    historyBookService
      .update(uuidLoan, uuidBook, pk, renew)
      .then((bookResult) => {
        const newBookData = {
          ...bookResult.data.book,
          uuid_loan: renew ? bookResult.data.uuid_loan : null,
        };

        dispatch(updateBook(newBookData));
        dispatch(notificationsNewSuccessAction('El historial ha actualizado correctamente'));
      })
      .catch((error) => {
        const message = path(['response', 'data'], error);
        dispatch(failure(message));
        dispatch(notificationsNewErrorAction(message));
      });
  };
};

export default {
  getAllByUser,
  getAll,
  create,
  update,
};
