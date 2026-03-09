const fs = require('fs');

function checkBraceBalance(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  
  let braces = 0;
  let brackets = 0;
  let parens = 0;
  
  for (let i = 0; i < content.length; i++) {
    const char = content[i];
    switch (char) {
      case '{': braces++; break;
      case '}': braces--; break;
      case '[': brackets++; break;
      case ']': brackets--; break;
      case '(': parens++; break;
      case ')': parens--; break;
    }
  }
  
  console.log(`Brace balance check for ${filePath}:`);
  console.log(`Braces: ${braces === 0 ? 'BALANCED' : 'UNBALANCED (' + braces + ')'}`);
  console.log(`Brackets: ${brackets === 0 ? 'BALANCED' : 'UNBALANCED (' + brackets + ')'}`);
  console.log(`Parentheses: ${parens === 0 ? 'BALANCED' : 'UNBALANCED (' + parens + ')'}`);
  
  const isBalanced = braces === 0 && brackets === 0 && parens === 0;
  console.log(`Overall: ${isBalanced ? 'PASS' : 'FAIL'}`);
  
  return isBalanced;
}

if (process.argv.length < 3) {
  console.log('Usage: node balance-check.js <file>');
  process.exit(1);
}

const filePath = process.argv[2];
const result = checkBraceBalance(filePath);
process.exit(result ? 0 : 1);