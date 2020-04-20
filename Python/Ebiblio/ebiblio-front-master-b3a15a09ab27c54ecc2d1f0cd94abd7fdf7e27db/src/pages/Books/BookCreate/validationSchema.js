import { object, string } from 'yup';

export const BookCreateSchema = object().shape({
  title: string().required('books:titleMessage'),
  author: string().required('books:authorMessage'),
  editorial: string().required('books:editorialMessage'),
  language: string().required('books:languageMessage'),
});
