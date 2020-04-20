import { mapObjectToCamelCase } from '../utils';
import { bookConstants } from '../_constants';
import { bookService } from '../_services';
import {
  notificationsNewSuccess as notificationsNewSuccessAction,
  notificationsNewError as notificationsNewErrorAction,
} from './notifications';

const getAll = () => {
  const request = () => ({ type: bookConstants.GETALL_REQUEST });
  const success = bookResponse => ({
    type: bookConstants.GETALL_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });

  return (dispatch) => {
    dispatch(request());

    bookService
      .getAll()
      .then((books) => {
        dispatch(success(books.data));
      })
      .catch((error) => {
        dispatch(notificationsNewErrorAction(error.response.data));
      });
  };
};

const getInfoByISBN = (isbn) => {
  const request = () => ({ type: bookConstants.GETINFO_REQUEST });
  const success = bookInfoResponse => ({
    type: bookConstants.GETINFO_SUCCESS,
    payload: mapObjectToCamelCase(bookInfoResponse),
  });
  const failure = () => ({ type: bookConstants.GETINFO_FAILURE });

  return (dispatch) => {
    dispatch(request());

    bookService
      .getInfoByISBN(isbn)
      .then((bookInfo) => {
        dispatch(success(bookInfo.data));
      })
      .catch((error) => {
        dispatch(failure());
        dispatch(notificationsNewErrorAction(error.response.data));
      });
  };
};

const clearInfo = () => (dispatch) => {
  dispatch({ type: bookConstants.CLEAR_INFO });
};

const create = (book) => {
  const request = () => ({ type: bookConstants.CREATE_REQUEST });
  const success = bookResponse => ({
    type: bookConstants.CREATE_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });

  return (dispatch) => {
    dispatch(request(book));

    bookService.create(book).then(
      (bookResult) => {
        dispatch(success(bookResult.data));
        dispatch(notificationsNewSuccessAction('El libro ha sido creado correctamente'));
      },
      (error) => {
        dispatch(notificationsNewErrorAction(error.response.data));
      },
    );
  };
};

const update = (book) => {
  const request = bookResponse => ({ type: bookConstants.UPDATE_REQUEST, payload: bookResponse });
  const success = bookResponse => ({
    type: bookConstants.UPDATE_SUCCESS,
    payload: mapObjectToCamelCase(bookResponse),
  });

  return (dispatch) => {
    dispatch(request(book));

    bookService
      .update(book)
      .then((result) => {
        dispatch(success(result.data));
        dispatch(notificationsNewSuccessAction('El libro ha sido actualizado correctamente'));
      })
      .catch((error) => {
        dispatch(notificationsNewErrorAction(error.response.data));
      });
  };
};

const deleteBook = (id) => {
  const request = () => ({ type: bookConstants.DELETE_REQUEST });
  const success = deletedId => ({
    type: bookConstants.DELETE_SUCCESS,
    payload: { uuidBook: deletedId },
  });

  return (dispatch) => {
    dispatch(request());

    bookService.delete(id).then(
      () => {
        dispatch(success(id));
        dispatch(notificationsNewSuccessAction('El libro ha sido eliminado correctamente'));
      },
      (error) => {
        dispatch(notificationsNewErrorAction(error.response.data));
      },
    );
  };
};

export default {
  getAll,
  getInfoByISBN,
  create,
  update,
  delete: deleteBook,
  clearInfo,
};
