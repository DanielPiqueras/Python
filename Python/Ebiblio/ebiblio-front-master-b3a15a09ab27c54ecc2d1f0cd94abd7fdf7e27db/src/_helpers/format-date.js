export const formatDate = (inputDate) => {
  const currentDatetime = new Date(inputDate);
  return `${currentDatetime.getDate()}-${currentDatetime.getMonth()
    + 1}-${currentDatetime.getFullYear()}`;
};
