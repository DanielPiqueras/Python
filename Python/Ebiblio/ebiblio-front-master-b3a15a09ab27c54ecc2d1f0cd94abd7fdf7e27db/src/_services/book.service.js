import { buildHeaders } from '../_helpers';
import { mapObjectToSnakeCase } from '../utils';

const axios = require('axios');

const getAll = () => axios.get('library/books/', buildHeaders());

const getInfoByISBN = isbn => axios.post('library/find/', { isbn }, buildHeaders());

const create = book => axios.post('library/books/', mapObjectToSnakeCase(book), buildHeaders());

const deleteBook = id => axios.delete(`library/books/${id}/`, buildHeaders());

export const bookService = {
  getAll,
  getInfoByISBN,
  create,
  delete: deleteBook,
};
