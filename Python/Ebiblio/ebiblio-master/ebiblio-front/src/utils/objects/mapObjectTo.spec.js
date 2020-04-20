import { keyToCamelCase, keyToSnakeCase, mapObjectTo, mapObjectToCamelCase, mapObjectToSnakeCase } from './mapObjectTo';
import { mockArrayCamelToSnake, mockArraySnakeToCamel, mockObjectCamelToSnake, mockObjectSnakeToCamel } from './__mocks__';


describe('Objects', () => {
  describe('ToCamelCase', () => {
    /** keyToCamelCase */
    describe('keyToCamelCase', () => {
      test('With invalid value', () => {
        expect(keyToCamelCase([])).toBe('');
        expect(keyToCamelCase({})).toBe('');
        expect(keyToCamelCase(null)).toBe('');
        expect(keyToCamelCase(undefined)).toBe('');
        expect(keyToCamelCase(1)).toBe('');
        expect(keyToCamelCase(true)).toBe('');
      });

      test('With string without underscore', () => {
        const key = 'test';
        expect(keyToCamelCase(key)).toBe(key);
      });

      test('With string with underscore', () => {
        const key = 'test_first_second';
        expect(keyToCamelCase(key)).toBe('testFirstSecond');
      });
    });

    describe('mapObjectToCamelCase', () => {
      test('With invalid values', () => {
        expect(mapObjectToCamelCase(undefined)).toEqual({});
        expect(mapObjectToCamelCase(1)).toEqual({});
        expect(mapObjectToCamelCase(true)).toEqual({});
        expect(mapObjectToCamelCase(null)).toEqual({});
      });

      test('With valid object', () => {
        const expectedOutput = {
          parentFirstLevel: {
            childrenSecondLevel: {
              primitiveThirdLevel: false,
            },
          },
          arrayFirstLevel: [
            {
              testArray: true,
              testArray2: false,
            },
            {
              testArray: false,
            },
          ],
          primitiveFirstLevel: true,
        };
        const output = mapObjectToCamelCase(mockObjectSnakeToCamel);
        expect(output).toEqual(expectedOutput);
      });

      test('With valid array', () => {
        const expectedOutput = [
          {
            parentFirstLevel: {
              childrenSecondLevel: {
                primitiveThirdLevel: false,
              },
            },
            arrayFirstLevel: [
              {
                testArray: true,
                testArray2: false,
              },
              {
                testArray: false,
              },
            ],
            primitiveFirstLevel: true,
          },
          {
            parentFirstLevel: {
              childrenSecondLevel: {
                primitiveThirdLevel: 1,
              },
            },
            arrayFirstLevel: [
              {
                testArray: 1,
                testArray2: 4,
              },
              {
                testArray: 3,
              },
            ],
            primitiveFirstLevel: 15,
          },
        ];
        const output = mapObjectToCamelCase(mockArraySnakeToCamel);
        expect(output).toEqual(expectedOutput);
      });
    });
  });

  describe('ToSnakeCase', () => {
    /** keyToSnakeCase */
    describe('keyToSnakeCase', () => {
      test('With invalid value', () => {
        expect(keyToSnakeCase([])).toBe('');
        expect(keyToSnakeCase({})).toBe('');
        expect(keyToSnakeCase(null)).toBe('');
        expect(keyToSnakeCase(undefined)).toBe('');
        expect(keyToSnakeCase(1)).toBe('');
        expect(keyToSnakeCase(true)).toBe('');
      });
      test('With string without underscore', () => {
        const key = 'test';
        expect(keyToSnakeCase(key)).toBe(key);
      });
      test('With string with underscore', () => {
        const key = 'testFirstSecond';
        expect(keyToSnakeCase(key)).toBe('test_first_second');
      });
    });

    /** mapObjectToSnakeCase */
    describe('mapObjectToSnakeCase', () => {
      test('With invalid values', () => {
        expect(mapObjectToSnakeCase(undefined)).toEqual({});
        expect(mapObjectToSnakeCase(1)).toEqual({});
        expect(mapObjectToSnakeCase(true)).toEqual({});
        expect(mapObjectToSnakeCase(null)).toEqual({});
      });
      test('With valid object', () => {
        const expectedOutput = {
          parent_first_level: {
            children_second_level: {
              primitive_third_level: false,
            },
          },
          array_first_level: [
            {
              test_array: false,
            },
            {
              test_array: true,
              test_array_2: false,
            },
            {
              test_array: false,
              test_array_2: false,
              test_array_3: false,
            },
          ],
          primitive_first_level: true,
        };
        const output = mapObjectToSnakeCase(mockObjectCamelToSnake);
        expect(output).toEqual(expectedOutput);
      });
      test('With valid array', () => {
        const expectedOutput = [
          {
            parent_first_level: {
              children_second_level: {
                primitive_third_level: false,
              },
            },
            array_first_level: [
              {
                test_array: true,
                test_array_2: false,
              },
              {
                test_array: false,
              },
            ],
            primitive_first_level: true,
          },
          {
            parent_first_level: {
              children_second_level: {
                primitive_third_level: 1,
              },
            },
            array_first_level: [
              {
                test_array: 1,
                test_array_2: 4,
              },
              {
                test_array: 3,
              },
            ],
            primitive_first_level: 15,
          },
        ];
        const output = mapObjectToSnakeCase(mockArrayCamelToSnake);
        expect(output).toEqual(expectedOutput);
      });
    });
  });

  test('mapObjectTo with invalid value', () => {
    expect(mapObjectTo([])).toStrictEqual([]);
    expect(mapObjectTo({})).toStrictEqual({});
    expect(mapObjectTo(null)).toStrictEqual({});
    expect(mapObjectTo(undefined)).toStrictEqual({});
    expect(mapObjectTo(1)).toStrictEqual({});
    expect(mapObjectTo(true)).toStrictEqual({});
  });
});
