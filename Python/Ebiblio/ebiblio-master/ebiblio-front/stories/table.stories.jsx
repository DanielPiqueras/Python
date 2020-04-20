/** Packages */
import { storiesOf } from '@storybook/react';
import React from 'react';

/** Modules */
import {
  Box, TableCell, TableHeader, TableRow,
} from '../src/components';

const stories = storiesOf('Table', module);


stories.add('Custom props', () => {
  const header = ['test', 'test1', 'test2', 'test3', 'test4', 'test5'];
  const content = [
    ['test', 'test1', 'test2', 'test3', 'test4', 'test5'],
    ['test', 'test1', 'test2', 'test3', 'test4', 'test5'],
    ['test', 'test1', 'test2', 'test3', 'test4', 'test5'],
    ['test', 'test1', 'test2', 'test3', 'test4', 'test5'],
  ];
  return (
    <Box textAlign="center">
      <TableHeader>
        {header.map(data => (
          <TableCell content={data} color="white" />
        ))}
      </TableHeader>
      {content.map(data => (
        <TableRow>
          {data.map(cell => (
            <TableCell title={cell} content={cell} />
          ))}
        </TableRow>
      ))}
    </Box>
  );
});
