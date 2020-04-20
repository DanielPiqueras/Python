/** Packages */
import PropTypes from 'prop-types';
import React from 'react';
import ReactFlagsSelect from 'react-flags-select';
import 'react-flags-select/css/react-flags-select.css';
import { useTranslation } from 'react-i18next';

/** Modules */
import {
  getAllCodes, languageFindByCode, languageFindByLocale, languages,
} from '../../_constants';

const LanguageSelector = ({ isLabelVisible }) => {
  const { i18n } = useTranslation();

  const currentLanguage = languageFindByLocale(localStorage.getItem('i18nextLng'));

  const changeLanguage = (countryCode) => {
    const selectedLanguage = languageFindByCode(countryCode);
    i18n.changeLanguage(selectedLanguage.locale);
  };
  return (
    <ReactFlagsSelect
      defaultCountry={currentLanguage.code}
      countries={getAllCodes}
      customLabels={languages.reduce(
        (acc, language) => ({ ...acc, [language.code]: language.name }),
        {},
      )}
      selectedSize={15}
      optionsSize={15}
      onSelect={changeLanguage}
      showSelectedLabel={isLabelVisible}
      showOptionLabel={isLabelVisible}
    />
  );
};

LanguageSelector.defaultProps = {
  isLabelVisible: true,
};

LanguageSelector.propTypes = {
  isLabelVisible: PropTypes.bool,
};

export default LanguageSelector;
