/** Packages */
import { action } from '@storybook/addon-actions';
import { select, text, withKnobs } from '@storybook/addon-knobs';
import { storiesOf } from '@storybook/react';
import React from 'react';

/** Modules */
import { Button } from '../src/components';
import theme from '../src/theme';

const stories = storiesOf('Button', module);

stories.addDecorator(withKnobs);

stories.add('Custom props', () => (
  <Button
    variant={select(
      'variant',
      [
        'normal',
        'primary',
        'secondary',
        'success',
        'danger',
        'warning',
        'info',
        'light',
        'dark',
        'link',
      ],
      'normal',
    )}
    color={select('color', { null: null, ...theme.colors }, null)}
    onClick={action('Example text')}
  >
    {text('Text to display', 'Example text')}
  </Button>
));
