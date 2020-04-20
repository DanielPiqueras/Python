import React from 'react';
import { storiesOf } from '@storybook/react';
import { withKnobs, text, boolean } from '@storybook/addon-knobs';
import { Logo } from '../src/components';

const stories = storiesOf('Logo', module);

stories.addDecorator(withKnobs);
stories.add('default', () => <Logo />);
stories.add('with custom props', () => (
  <Logo
    width={text('Width', '50px')}
    color={text('Color', 'black')}
    withTitle={boolean('With title', true)}
  />
));
