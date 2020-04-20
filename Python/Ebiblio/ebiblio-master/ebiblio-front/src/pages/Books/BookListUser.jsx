/** Packages */
import { LensTwoTone } from '@material-ui/icons';
import { equals, path, prop } from 'ramda';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

/** Modules */
import {
  Box,
  ConditionalButton,
  Loading,
  TableCell,
  TableHeader,
  TableRow,
} from '../../components';
import { bookActions, historyBookActions } from '../../_actions';
import { isTruthy } from '../../utils';

export const BookListUserComponent = () => {
  const { t } = useTranslation();

  const user = useSelector(path(['authentication', 'user']));
  const books = useSelector(prop('books'));

  const dispatch = useDispatch();
  const handleGetAllBooks = () => dispatch(bookActions.getAll());
  const handleLoanBook = (uuidBook, reservedBook) => {
    if (uuidBook && user.pk) {
      dispatch(historyBookActions.create(uuidBook, user.pk, reservedBook));
    }
  };
  const handleUpdateLoanBook = (uuidLoan, uuidBook, renew) => {
    if (uuidBook && user.pk && uuidLoan) {
      dispatch(historyBookActions.update(uuidLoan, uuidBook, user.pk, renew));
    }
  };

  if (!books.loaded && !books.requesting) handleGetAllBooks();

  const processedBooks = books && books.items
    ? books.items.map((book, key) => {
      if (book.deletedBook || !book.uuidBook) return null;

      const isSameUsername = equals(book.lastUser, user.username);
      const isLoanable = book.availableBook || (book.reservedBook && !book.lastUser);
      const isReservable = !isSameUsername && !book.reservedBook && !book.availableBook;
      const isCancelReserve = !isSameUsername && book.reservedBook && isTruthy(book.uuidLoan);
      const isRenewableOrReturn = !book.availableBook && isSameUsername;

      const allButtons = (
        <>
          <ConditionalButton
            variant="link"
            color="success"
            condition={isLoanable}
            onClick={() => handleLoanBook(book.uuidBook, false)}
          >
            {t('books:loan')}
          </ConditionalButton>
          {' '}
          <ConditionalButton
            variant="link"
            color="success"
            condition={isReservable}
            onClick={() => handleLoanBook(book.uuidBook, true)}
          >
            {t('books:reserve')}
          </ConditionalButton>
          {' '}
          <ConditionalButton
            variant="link"
            color="danger"
            condition={isCancelReserve}
            onClick={() => handleUpdateLoanBook(book.uuidLoan, book.uuidBook, false)}
          >
            {t('common:cancel')}
          </ConditionalButton>
          {' '}
          <ConditionalButton
            variant="link"
            color="primary"
            condition={isRenewableOrReturn}
            onClick={() => handleUpdateLoanBook(book.uuidLoan, book.uuidBook, false)}
          >
            {t('books:return')}
          </ConditionalButton>
          {' '}
          <ConditionalButton
            variant="link"
            color="success"
            condition={isRenewableOrReturn}
            onClick={() => handleUpdateLoanBook(book.uuidLoan, book.uuidBook, true)}
          >
            {t('books:renew')}
          </ConditionalButton>
        </>
      );

      let textAvailableBook;
      let colorAvailableBook;
      switch (true) {
        case book.reservedBook && !book.lastUser:
          textAvailableBook = t('books:reserved');
          colorAvailableBook = 'orange';
          break;
        case !book.availableBook:
          textAvailableBook = t('books:loaned');
          colorAvailableBook = 'red';
          break;
        default:
          textAvailableBook = t('books:available');
          colorAvailableBook = 'green';
          break;
      }

      return (
        <TableRow
          key={book.uuidBook}
        >
          <TableCell
            minWidth="30px"
            desktopWidth="10%"
            title="#"
            content={key + 1}
            mobileVisibility={false}
          />
          <TableCell
            minWidth="180px"
            desktopWidth="30%"
            mobileWidth="100%"
            title={t('books:title')}
            content={book.title}
          />
          <TableCell
            minWidth="80px"
            mobileWidth="100%"
            title={t('books:author')}
            content={book.author}
          />
          <TableCell
            minWidth="150px"
            mobileWidth="100%"
            title={t('books:editorial')}
            content={book.editorial}
          />
          <TableCell minWidth="160px" title={t('books:isbn')} content={book.isbn} />
          <TableCell
            minWidth="75px"
            desktopWidth="15%"
            title={t('books:language')}
            content={book.language}
          />
          <TableCell
            minWidth="80px"
            title={t('books:user')}
            content={book.lastUser ? book.lastUser : '-'}
          />
          <TableCell
            title={t('common:status')}
            minWidth="85px"
            desktopWidth="8%"
            content={<LensTwoTone htmlColor={colorAvailableBook} title={textAvailableBook} />}
          />
          <TableCell mobileWidth="100%" content={allButtons} />
        </TableRow>
      );
    })
    : [];

  return (
    <>
      {!books.loaded && books.requesting && <Loading />}
      {books.loaded && (
        <Box width="100%">
          <TableHeader>
            <TableCell minWidth="30px" desktopWidth="10%" content="#" color="white" />
            <TableCell
              minWidth="180px"
              desktopWidth="30%"
              content={t('books:title')}
              color="white"
            />
            <TableCell minWidth="80px" content={t('books:author')} color="white" />
            <TableCell minWidth="150px" content={t('books:editorial')} color="white" />
            <TableCell minWidth="160px" content={t('books:isbn')} color="white" />
            <TableCell
              minWidth="75px"
              desktopWidth="15%"
              content={t('books:language')}
              color="white"
            />
            <TableCell minWidth="80px" content={t('books:user')} color="white" />
            <TableCell
              minWidth="85px"
              desktopWidth="8%"
              content={t('common:status')}
              color="white"
            />
            <TableCell />
          </TableHeader>
          {processedBooks}
        </Box>
      )}
    </>
  );
};

BookListUserComponent.displayName = 'BookListUserComponent';

export default BookListUserComponent;
