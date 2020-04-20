import { buildHeaders } from '../_helpers';

const axios = require('axios');

const getAll = () => axios.get('library/history/', buildHeaders());

const getAllByUser = id => axios.get(`library/history/user/${id}/`, buildHeaders());

const create = (uuidBook, pk, reservedBook) => {
  const bookFormated = {
    uuid_book: uuidBook,
    reserved_book: reservedBook,
    pk,
  };

  return axios.post('library/history/', bookFormated, buildHeaders());
};

const update = (uuidLoan, uuidBook, pk, renew) => {
  const bookFormated = {
    uuid_loan: uuidLoan,
    uuid_book: uuidBook,
    pk,
    renew_loan: renew,
  };

  return axios.put(`library/history/${bookFormated.uuid_loan}/`, bookFormated, buildHeaders());
};

export const historyBookService = {
  getAll,
  getAllByUser,
  create,
  update,
};
