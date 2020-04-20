export const mockObjectSnakeToCamel = {
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
};

export const mockArraySnakeToCamel = [
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

export const mockObjectCamelToSnake = {
  parentFirstLevel: {
    childrenSecondLevel: {
      primitiveThirdLevel: false,
    },
  },
  arrayFirstLevel: [
    {
      testArray: false,
    },
    {
      testArray: true,
      testArray2: false,
    },
    {
      testArray: false,
      testArray2: false,
      testArray3: false,
    },
  ],
  primitiveFirstLevel: true,
};

export const mockArrayCamelToSnake = [
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
