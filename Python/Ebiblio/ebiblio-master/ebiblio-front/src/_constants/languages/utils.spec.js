import { languageFindByCode, languageFindByLocale, languageFindByName } from './utils';

describe('Utils', () => {
  describe('Find by code', () => {
    test('Success', () => {
      const mockResult = {
        name: 'Español',
        code: 'ES',
        locale: 'es-ES',
      };
      expect(languageFindByCode('ES')).toStrictEqual(mockResult);
    });

    test('With invalid value', () => {
      expect(languageFindByName('Test')).toStrictEqual(undefined);
      expect(languageFindByName(123)).toStrictEqual(undefined);
      expect(languageFindByCode([])).toStrictEqual(undefined);
      expect(languageFindByCode({})).toStrictEqual(undefined);
    });
  });

  describe('Find by locale', () => {
    test('Success', () => {
      const mockResult = {
        name: 'Español',
        code: 'ES',
        locale: 'es-ES',
      };
      expect(languageFindByLocale('es-ES')).toStrictEqual(mockResult);
    });

    test('With invalid value', () => {
      expect(languageFindByName('Test')).toStrictEqual(undefined);
      expect(languageFindByName(123)).toStrictEqual(undefined);
      expect(languageFindByLocale([])).toStrictEqual(undefined);
      expect(languageFindByLocale({})).toStrictEqual(undefined);
    });
  });

  describe('Find by name', () => {
    test('Success', () => {
      const mockResult = {
        name: 'Español',
        code: 'ES',
        locale: 'es-ES',
      };
      expect(languageFindByName('Español')).toStrictEqual(mockResult);
    });

    test('With invalid value', () => {
      expect(languageFindByName('Test')).toStrictEqual(undefined);
      expect(languageFindByName(123)).toStrictEqual(undefined);
      expect(languageFindByName([])).toStrictEqual(undefined);
      expect(languageFindByName({})).toStrictEqual(undefined);
    });
  });
});
