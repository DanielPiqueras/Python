/** Packages */
import { boolean, withKnobs } from '@storybook/addon-knobs';
import { storiesOf } from '@storybook/react';
import React from 'react';

/** Modules */
import { LanguageSelector } from '../src/components';

const stories = storiesOf('Language selector', module);

stories.addDecorator(withKnobs);

stories.add('Custom props', () => (
  <LanguageSelector isLabelVisible={boolean('Is label visible', true)} />
));
