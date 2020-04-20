/** Packages */
import PropTypes from 'prop-types';
import { groupBy, prop } from 'ramda';
import React from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import Icon from '@material-ui/core/Icon';

/** Modules */
import CustomNavLink from './CustomNavLink';
import { sections } from '../../_constants';

const StyledHeader = styled.p`
  text-decoration: none;
  display: flex;
  justify-content: center;
  padding: 4px 8px;
  color: gray;
  cursor: default;
  transition: all 0.25s ease-out;
`;

const MenuSection = ({ isOpen, subsections }) => {
  const { t } = useTranslation();
  const filteredSubsections = groupBy(prop('section'), subsections);
  const Sections = Object.keys(filteredSubsections).reduce((acc = [], key) => {
    const section = sections[key];
    const translatedTitle = t(section.text);
    const currentSection = filteredSubsections[key];
    const links = Object.values(currentSection)
      .map(current => <CustomNavLink key={current.to} isOpen={isOpen} {...current} />);
    acc.push(
      <div key={key}>
        <StyledHeader fontSize="default">
          {isOpen
            ? translatedTitle
            : section.icon && (
            <Icon title={translatedTitle} alt={translatedTitle} fontWeight="bold">
              {section.icon}
            </Icon>
            )}
        </StyledHeader>
        {links}
      </div>,
    );
    return acc;
  }, []);
  return Sections;
};

MenuSection.displayName = 'MenuSection';
MenuSection.propTypes = {
  subsections: PropTypes.arrayOf(
    PropTypes.shape({
      section: PropTypes.string.isRequired,
      to: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      icon: PropTypes.object.isRequired,
    }),
  ),
};

/** Export */
export default React.memo(MenuSection);
