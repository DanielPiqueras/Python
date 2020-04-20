import {
  both, either, isEmpty, isNil, not, pipe, is,
} from 'ramda';

export const isNotEmpty = pipe(
  isEmpty,
  not,
);

export const isNotNil = pipe(
  isNil,
  not,
);

export const isTruthy = both(isNotEmpty, isNotNil);

export const isNotTruthy = either(isEmpty, isNil);

export const isString = is(String);

export const isNotString = pipe(
  is(String),
  not,
);
