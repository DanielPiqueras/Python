/** Packages */
import PropTypes from 'prop-types';
import { prop } from 'ramda';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';
import { Redirect } from 'react-router-dom';

/** Modules */
import { useTitlePage } from '../../misc';
import {
  Box, Loading, TableCell, TableHeader, TableRow,
} from '../../components';
import {
  historyBookActions,
  notificationsNewInfo as notificationsNewInfoAction,
} from '../../_actions';
import { formatDate } from '../../_helpers';

export const HistoryAdminListByComponent = ({ match }) => {
  const { t } = useTranslation();
  const { setTitleValues } = useTitlePage();
  const dispatch = useDispatch();

  const historyBooks = useSelector(prop('historyBooks'));

  const handleGetAllHistoryBooks = () => dispatch(historyBookActions.getAll());

  if (!historyBooks.loaded && !historyBooks.requesting) handleGetAllHistoryBooks();

  const urlSplit = match.url.split('/');
  let historyBooksBy = [];
  let headerText = '';
  let menu = '';

  if (urlSplit.length === 5) {
    menu = urlSplit[2];

    if (menu === 'users') {
      historyBooksBy = historyBooks
        && historyBooks.items
        && historyBooks.items.filter(
          historyBook => historyBook.user.pk.toString() === match.params.id,
        );
      headerText = historyBooksBy && historyBooksBy[0]
        ? `${historyBooksBy[0].user.firstName} ${historyBooksBy[0].user.lastName}`
        : '';
      if (historyBooks.loaded && !historyBooks.requesting && !headerText) dispatch(notificationsNewInfoAction(t('histories:notHistoryUser')));
    }

    if (menu === 'books') {
      historyBooksBy = historyBooks
        && historyBooks.items
        && historyBooks.items.filter(historyBook => historyBook.book.uuidBook === match.params.id);
      headerText = historyBooksBy && historyBooksBy[0] ? historyBooksBy[0].book.title : '';
      if (historyBooks.loaded && !historyBooks.requesting && !headerText) dispatch(notificationsNewInfoAction(t('histories:notHistoryBook')));
    }
  }

  React.useEffect(() => {
    if (menu && headerText) {
      setTitleValues({ historyName: headerText });
    }
  });
  const processedHistory = historyBooksBy
    ? historyBooksBy.map((historyBook, key) => {
      let textAvailableBook;
      let colorAvailableBook;
      switch (true) {
        case historyBook.reservedBook:
          textAvailableBook = t('books:reserved');
          colorAvailableBook = 'warning';
          break;
        case !historyBook.returnedBook:
          textAvailableBook = t('books:loaned');
          colorAvailableBook = 'red';
          break;
        default:
          textAvailableBook = t('histories:returned');
          colorAvailableBook = 'green';
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
          {menu === 'users' && (
          <TableCell
            mobileWidth="100%"
            title={t('books:title')}
            content={historyBook.book.title}
          />
          )}
          {menu === 'books' && (
          <TableCell
            mobileWidth="100%"
            title={t('books:user')}
            content={historyBook.user.username}
          />
          )}
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
          <TableCell
            minWidth="125px"
            desktopWidth="15%"
            title={t('common:status')}
            content={<b>{textAvailableBook}</b>}
            color={colorAvailableBook}
          />
        </TableRow>
      );
    })
    : [];

  return (
    <>
      {!historyBooks.loaded && historyBooks.requesting && <Loading />}
      {historyBooks.loaded && !historyBooks.requesting && !headerText && (
        <Redirect to="/admin/history" />
      )}
      {historyBooks.loaded && headerText && (
        <Box width="100%">
          <TableHeader>
            <TableCell minWidth="40px" desktopWidth="1%" content="#" color="white" />
            {menu === 'users' && <TableCell content={t('books:title')} color="white" />}
            {menu === 'books' && <TableCell content={t('books:user')} color="white" />}
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

HistoryAdminListByComponent.displayName = 'HistoryAdminListByComponent';

HistoryAdminListByComponent.propTypes = {
  match: PropTypes.shape({
    url: PropTypes.string.isRequired,
    params: PropTypes.shape({
      id: PropTypes.string.isRequired,
    }).isRequired,
  }).isRequired,
};

export default HistoryAdminListByComponent;
