// Packages
import PropTypes from "prop-types";
import React from "react";
import { Helmet } from "react-helmet";
import { useTranslation } from "react-i18next";
import { withRouter } from "react-router-dom";
// Modules
import { APP_NAME, titlePages } from "../_constants";

// Utils

/** Get current page title */
export const getCurrentTitle = (currentPathname = "") => {
  const titleObj = titlePages.find(({ key }) => {
    const regex = new RegExp(key);
    return regex.test(currentPathname);
  });
  return titleObj && titleObj.title ? titleObj.title : APP_NAME;
};

// Context
export const TitleContext = React.createContext({
  title: APP_NAME,
  setTitle: () => {}
});

// Hook
export const useTitlePage = () => React.useContext(TitleContext);

// Hoc
export const ComposedCurrentTitlePage = ({ Component, location, ...props }) => {
  const { t } = useTranslation();
  const memoizeTitle = React.useMemo(() => getCurrentTitle(location.pathname), [
    location.pathname
  ]);
  const translatedTitle = t(memoizeTitle);

  const valueContext = {
    title: translatedTitle
  };
  return (
    <>
      <Helmet>
        <title>{`${APP_NAME} - ${translatedTitle}`}</title>
      </Helmet>
      <TitleContext.Provider value={valueContext}>
        <Component {...props} />
      </TitleContext.Provider>
    </>
  );
};

ComposedCurrentTitlePage.displayName = "ComposedCurrentTitlePage";
ComposedCurrentTitlePage.propTypes = {
  Component: PropTypes.func.isRequired,
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired
  }).isRequired
};

/** Enhance Composed component with router props */
export const EnhancedCurrentTitlePage = withRouter(ComposedCurrentTitlePage);
EnhancedCurrentTitlePage.displayName = "EnhancedCurrentTitlePage";

/** Hoc to add the title page on html document */
const withTitlePage = Component => props => (
  <EnhancedCurrentTitlePage Component={Component} {...props} />
);
withTitlePage.displayName = "withTitlePage";

// Export
export default withTitlePage;
