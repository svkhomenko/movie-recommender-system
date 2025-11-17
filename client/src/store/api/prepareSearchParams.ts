export const prepareSearchParams = (params: { [key: string]: any }) => {
  let query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined) {
      if (Array.isArray(value)) {
        value.forEach((v) => query.append(key, v));
      } else query.append(key, value);
    }
  });

  return query;
};
