import { createGlobalStyle } from 'styled-components';
import { normalize } from 'polished';

const GlobalStyle = createGlobalStyle`
    ${normalize()}

    * {
        line-height: 1.45;
        font-family: 'Roboto', sans-serif;
    }

    *,
    *::before,
    *::after {
        box-sizing: inherit;
    }

    html {
        box-sizing: border-box;
    }

    body {
        scroll-behavior: smooth;
        overflow: 'none';
    }
`;

export default GlobalStyle;
