/** Packages */
import { LensTwoTone } from '@material-ui/icons';
import { prop } from 'ramda';
import React, { useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

/** Modules */
import {
  Box,
  ConditionalButton,
  Loading,
  StyledLink,
  TableCell,
  TableHeader,
  TableRow,
} from '../../components';
import { bookActions } from '../../_actions';

export const BookListAdminComponent = () => {
  const { t } = useTranslation();

  const books = useSelector(prop('books'));

  const dispatch = useDispatch();
  const handleGetAllBooks = useCallback(() => dispatch(bookActions.getAll()), [dispatch]);
  const handleDeleteBook = useCallback(uuidBook => dispatch(bookActions.delete(uuidBook)), [
    dispatch,
  ]);

  if (!books.loaded && !books.requesting) handleGetAllBooks();

  const processedBooks = books && books.items
    ? books.items.map((book, key) => {
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
      const deleteColor = ['black', 'black', book.deletedBook ? 'danger' : 'black'];
      return (
        <TableRow key={book.uuidBook}>
          <TableCell
            minWidth="40px"
            desktopWidth="1%"
            title="#"
            content={key + 1}
            mobileVisibility={false}
            color={deleteColor}
          />
          <TableCell
            mobileWidth="100%"
            title={t('books:title')}
            content={book.title}
            color={deleteColor}
          />
          <TableCell
            mobileWidth="100%"
            title={t('books:author')}
            content={book.author}
            color={deleteColor}
          />
          <TableCell
            mobileWidth="100%"
            title={t('books:editorial')}
            content={book.editorial}
            color={deleteColor}
          />
          <TableCell
            minWidth="145px"
            title={t('books:isbn')}
            content={book.isbn}
            color={deleteColor}
          />
          <TableCell
            minWidth="100px"
            desktopWidth="1%"
            title={t('books:language')}
            content={book.language}
            color={deleteColor}
          />
          <TableCell
            minWidth="100px"
            desktopWidth="1%"
            title={t('books:user')}
            content={book.lastUser ? book.lastUser : '-'}
            color={deleteColor}
          />
          <TableCell
            minWidth="75px"
            desktopWidth="1%"
            title={t('common:status')}
            content={
                  book.deletedBook === false && (
                    <LensTwoTone htmlColor={colorAvailableBook} title={textAvailableBook} />
                  )
                }
          />
          <TableCell
            mobileWidth="100%"
            content={(
              <>
                <StyledLink
                  variant="link"
                  color="success"
                  to={`/admin/books/history/${book.uuidBook}`}
                >
                  {t('common:history')}
                </StyledLink>
                {' '}
                <ConditionalButton
                  condition={!book.deletedBook && book.availableBook}
                  variant="link"
                  color="danger"
                  onClick={() => handleDeleteBook(book.uuidBook)}
                >
                  {t('common:delete')}
                </ConditionalButton>
              </>
)}
          />
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
            <TableCell minWidth="40px" desktopWidth="1%" content="#" color="white" />
            <TableCell content={t('books:title')} color="white" />
            <TableCell content={t('books:author')} color="white" />
            <TableCell content={t('books:editorial')} color="white" />
            <TableCell minWidth="145px" content={t('books:isbn')} color="white" />
            <TableCell
              minWidth="100px"
              desktopWidth="1%"
              content={t('books:language')}
              color="white"
            />
            <TableCell minWidth="100px" desktopWidth="1%" content={t('books:user')} color="white" />
            <TableCell
              minWidth="75px"
              desktopWidth="1%"
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

BookListAdminComponent.displayName = 'BookListAdminComponent';

export default BookListAdminComponent;
