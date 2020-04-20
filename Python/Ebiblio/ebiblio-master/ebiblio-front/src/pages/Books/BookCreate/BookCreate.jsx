/* eslint-disable jsx-a11y/label-has-for */
/** Packages */
import TextField from '@material-ui/core/TextField';
import { SearchOutlined } from '@material-ui/icons';
import { path, prop } from 'ramda';
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';

/** Modules */
import {
  Box, Button, Flex, Loading, MyForm,
} from '../../../components';
import { bookActions } from '../../../_actions';
import { BookCreateSchema } from './validationSchema';

export const BookCreateComponent = () => {
  const { t } = useTranslation();
  const bookInfo = useSelector(prop('bookInfo'));
  const isCreating = useSelector(path(['books', 'creating']));

  const [isbn, setIsbnState] = useState('');
  const updateIsbnState = e => setIsbnState(e.target.value);

  const [searched, setSearchedState] = useState(false);
  const searchedState = () => setSearchedState(state => !state);

  const dispatch = useDispatch();
  const handleGetInfo = () => {
    searchedState();
    if (isbn) dispatch(bookActions.getInfoByISBN(isbn));
  };
  const handleSubmit = (book) => {
    dispatch(
      bookActions.create({
        ...book,
        isbn,
      }),
    );
  };

  if (!isbn) dispatch(bookActions.clearInfo());

  const fields = [
    {
      name: 'title',
      type: 'text',
      label: 'books:title',
      required: true,
    },
    {
      name: 'author',
      type: 'text',
      label: 'books:author',
      required: true,
    },
    {
      name: 'editorial',
      type: 'text',
      label: 'books:editorial',
      required: true,
    },
    {
      name: 'language',
      type: 'text',
      label: 'books:language',
      required: true,
    },
    {
      name: 'description',
      type: 'text',
      label: 'books:description',
      multiline: true,
    },
  ];

  let initialValues = {
    title: '',
    author: '',
    editorial: '',
    language: '',
    description: '',
  };

  if (bookInfo.items && !bookInfo.error) {
    const info = bookInfo.items;

    initialValues = {
      title: info.Title,
      author: info.Authors ? info.Authors[0] : '',
      editorial: info.Publisher,
      language: info.Language,
      description: info.Desc || '',
    };
  }

  return (
    <Flex flexDirection="column" alignItems="center" p="md" width="100%">
      <TextField
        label={t('books:isbn')}
        value={isbn}
        onChange={updateIsbnState}
        InputProps={{
          endAdornment: <SearchOutlined onClick={handleGetInfo} />,
        }}
        error={searched && !isbn}
        helperText={searched && !isbn && t('books:isbnMessage')}
        fullWidth
      />
      {bookInfo.loading && <Loading width="50%" height="50%" />}
      {bookInfo.items && (
        <Box mt="md">
          <MyForm
            initialValues={initialValues}
            fields={fields}
            handleSubmit={handleSubmit}
            validationSchema={BookCreateSchema}
            formKey="bookForm"
          >
            <Flex justifyContent="center" my="md" width="100%">
              <Button type="submit" variant="primary">
                {isCreating ? (
                  <Loading color="white" width="40px" height="40px" />
                ) : (
                  t('common:save')
                )}
              </Button>
            </Flex>
          </MyForm>
        </Box>
      )}
    </Flex>
  );
};

BookCreateComponent.displayName = 'BookCreateComponent';

export default BookCreateComponent;
