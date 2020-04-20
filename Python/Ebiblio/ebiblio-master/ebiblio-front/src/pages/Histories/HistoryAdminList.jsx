/** Packages */
import { prop } from 'ramda';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

/** Modules */
import {
  Box, Loading, TableCell, TableHeader, TableRow,
} from '../../components';
import { historyBookActions } from '../../_actions';
import { formatDate } from '../../_helpers';

export const HistoryAdminListComponent = () => {
  const { t } = useTranslation();

  const historyBooks = useSelector(prop('historyBooks'));

  const dispatch = useDispatch();
  const handleGetAllHistoryBooks = () => dispatch(historyBookActions.getAll());

  if (!historyBooks.loaded && !historyBooks.requesting) handleGetAllHistoryBooks();

  const processedHistory = historyBooks && historyBooks.items
    ? historyBooks.items.map((historyBook, key) => {
      let statusText = '';
      let statusColor = '';
      switch (true) {
        case historyBook.returnedBook:
          statusText = t('histories:returned');
          statusColor = 'success';
          break;
        case historyBook.reservedBook:
          statusText = t('books:reserved');
          statusColor = 'warning';
          break;
        default:
          statusText = t('books:loaned');
          statusColor = 'danger';
          break;
      }
      return (
        <TableRow key={historyBook.uuidLoan}>
          <TableCell
            minWidth="40px"
            desktopWidth="1%"
            title="#"
            content={key + 1}
            mobileVisibility={false}
          />
          <TableCell
            title={t('books:title')}
            content={historyBook.book.title}
            mobileWidth="100%"
          />
          <TableCell
            minWidth="125px"
            desktopWidth="15%"
            title={t('histories:initialDate')}
            content={formatDate(historyBook.dateInitialLoan)}
          />
          <TableCell
            minWidth="185px"
            desktopWidth="15%"
            title={t('histories:returnDate')}
            content={formatDate(historyBook.dateFinishedLoan)}
          />
          <TableCell title={t('books:user')} content={historyBook.user.username} />
          <TableCell
            minWidth="125px"
            desktopWidth="15%"
            title={t('common:status')}
            content={<b>{statusText}</b>}
            color={statusColor}
          />
        </TableRow>
      );
    })
    : [];

  return (
    <>
      {!historyBooks.loaded && historyBooks.requesting && <Loading />}
      {historyBooks.loaded && (
        <Box width="100%">
          <TableHeader>
            <TableCell minWidth="40px" desktopWidth="1%" content="#" color="white" />
            <TableCell content={t('books:title')} color="white" />
            <TableCell
              minWidth="125px"
              desktopWidth="15%"
              content={t('histories:initialDate')}
              color="white"
            />
            <TableCell
              minWidth="185px"
              desktopWidth="15%"
              content={t('histories:returnDate')}
              color="white"
            />
            <TableCell content={t('books:user')} color="white" />
            <TableCell
              minWidth="125px"
              desktopWidth="15%"
              content={t('common:status')}
              color="white"
            />
          </TableHeader>
          {processedHistory}
        </Box>
      )}
    </>
  );
};

HistoryAdminListComponent.displayName = 'HistoryAdminListComponent';

export default HistoryAdminListComponent;
