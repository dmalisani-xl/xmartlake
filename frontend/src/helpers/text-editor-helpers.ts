const jsFunctionDeclarationLength = 28;
const pythonFunctionDeclarationLength = 19;

export const javascriptStartFunction = 
`const botFunction = () => {
  // Write your code here
}`;

export const pythonStartFunction =
`def botFunction():
  # Write your code here
`;

export const convertToBase64 = (file: File) => {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);
    fileReader.onload = () => {
      resolve(fileReader.result);
    };
    fileReader.onerror = (error) => {
      reject(error);
    };
  });
};

export const getRange = (language: string) => {
  if (language === 'javascript') {
    return jsFunctionDeclarationLength;
  }
  if (language === 'python') {
    return pythonFunctionDeclarationLength;
  }
  return 0;
};