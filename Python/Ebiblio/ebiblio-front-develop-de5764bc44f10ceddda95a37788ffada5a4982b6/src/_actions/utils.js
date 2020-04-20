import { is } from 'ramda';

export const generateAction = input => (payload) => {
  const isInputArray = Array.isArray(input);
  const [data, serviceLogic = null] = isInputArray ? input : [input];
  const [type, modifier] = Array.isArray(data) ? data : [data];
  if (serviceLogic) serviceLogic();
  if (!payload) return { type };
  const isModifier = is(Function, modifier);
  return {
    type,
    payload: isModifier ? modifier(payload) : payload,
  };
};

export const generateActions = (...actions) => actions.map(generateAction);
