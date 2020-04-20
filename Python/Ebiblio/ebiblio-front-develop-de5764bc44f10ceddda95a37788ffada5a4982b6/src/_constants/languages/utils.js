import {
  map, prop, find, propEq,
} from 'ramda';
import languages from './languages';

export const DEFAULT_LANGUAGE = 'en-GB';

export const getAllCodes = map(prop('code'), languages);

export const getAllLocales = map(prop('locale'), languages);

const findBy = filter => value => find(propEq(filter, value))(languages);

export const languageFindByCode = findBy('code');
export const languageFindByLocale = findBy('locale');
export const languageFindByName = findBy('name');
