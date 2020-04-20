import { createStore, applyMiddleware } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import thunkMiddleware from 'redux-thunk';
import immutableStateInvariantMiddleware from 'redux-immutable-state-invariant';
// import { createLogger } from 'redux-logger';
import rootReducer from '../_reducers';

// const loggerMiddleware = createLogger();

export default createStore(
  rootReducer,
  composeWithDevTools(
    applyMiddleware(thunkMiddleware, immutableStateInvariantMiddleware()),
  ),
);
