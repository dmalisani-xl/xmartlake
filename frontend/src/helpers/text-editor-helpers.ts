const jsFunctionDeclarationLength = 35;
const pythonFunctionDeclarationLength = 26;

export const javascriptStartFunction = 
`const botFunction = (context) => {
  // Write your code here
}`;

export const pythonStartFunction =
`def botFunction(context):
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

export const extractBotFunctionCode = (botFunction: string, language: string): string => {
  switch (language) {
    case 'javascript':
      return extractJSBotFunctionCode(botFunction);
    case 'python':
      return extractPythonBotFunctionCode(botFunction);
    default:
      return "";
  }
}

export const extractJSBotFunctionCode = (botFunction: string): string => {
  // Define a regular expression to match the first line of the JavaScript function.
  const regex = /^const [a-zA-Z_][a-zA-Z0-9_]* = \(.+?\) => \{/m;

  // Use the replace method to remove the first line.
  const modifiedCode = botFunction.replace(regex, '');

  return modifiedCode
}

const extractPythonBotFunctionCode = (botFunction: string): string => {
  // Define a regular expression to match the first line of a Python function.
  const regex = /^def [a-zA-Z_][a-zA-Z0-9_]*\(.*\):/m;

  // Use the replace method to remove the first line.
  const modifiedCode = botFunction.replace(regex, '');

  return modifiedCode;
}

