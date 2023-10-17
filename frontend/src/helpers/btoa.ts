export const btoa = (str: string) => {
  return Buffer.from(str, 'binary').toString('base64');
};
