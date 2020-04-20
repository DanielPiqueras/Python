import {
  is,
  mergeDeepLeft,
  pipe,
  prop,
  replace,
  toUpper,
  toLower,
  always,
  when,
  identity,
} from 'ramda';

import { isNotString } from '../misc';

export const keyToCamelCase = pipe(
  when(isNotString, always('')),
  replace(
    /((_|-)\w)/g,
    pipe(
      toUpper,
      prop(1),
    ),
  ),
);

export const keyToSnakeCase = pipe(
  when(isNotString, always('')),
  replace(
    /([A-Z|0-9])/g,
    pipe(
      toLower,
      x => `_${x}`,
    ),
  ),
);

const processMapObjectTo = (input, mapper, transformer) => Object.keys(input).reduce((acc, key) => {
  const currentValue = input[key];
  const isCurrentValueObject = is(Object, currentValue);
  const isCurrentValueArray = is(Array, currentValue);
  const newValue = isCurrentValueObject ? mapper(currentValue, transformer) : currentValue;
  const transformeddKey = transformer(key);
  const newKey = new RegExp(/^_[0-9]/).test(transformeddKey)
    ? prop(1, transformeddKey)
    : transformeddKey;
  const output = mergeDeepLeft(
    {
      [newKey]: isCurrentValueArray ? Object.values(newValue) : newValue,
    },
    acc,
  );
  return output;
}, {});

export const mapObjectTo = (input, transformer = identity) => {
  if (!is(Object, input)) return {};
  const isInputArray = is(Array, input);
  const dataToProcess = isInputArray ? { ...input } : input;
  const processedData = processMapObjectTo(dataToProcess, mapObjectTo, transformer);
  return isInputArray ? Object.values(processedData) : processedData;
};

export const mapObjectToCamelCase = data => mapObjectTo(data, keyToCamelCase);
export const mapObjectToSnakeCase = data => mapObjectTo(data, keyToSnakeCase);
