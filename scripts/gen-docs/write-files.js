#!node
const fs = require('fs');
const path = require('path');

// Read from stdin
let inputData = '';

process.stdin.setEncoding('utf-8');

process.stdin.on('data', chunk => {
  inputData += chunk;
});

process.stdin.on('end', () => {
  try {
    const data = JSON.parse(inputData);
    const currentDir = process.cwd();

    if (!data.files || !Array.isArray(data.files)) {
      throw new Error("Invalid input format: 'files' should be an array.");
    }

    data.files.forEach(file => {
      const filePath = path.resolve(currentDir, file.filename);

      // Check if the file path is within the current directory or its children
      if (!filePath.startsWith(currentDir)) {
        throw new Error(`File path "${file.filename}" is outside the allowed directory.`);
      }

      if (file.new_content === '') {
        // Delete the file if it exists and content is empty
        if (fs.existsSync(filePath)) {
          fs.unlinkSync(filePath);
          console.log(`Deleted empty file: ${file.filename}`);
        }
      } else {
        // Ensure the directory exists before writing the file
        const dir = path.dirname(filePath);
        fs.mkdirSync(dir, { recursive: true });

        // Write the content to the file
        fs.writeFileSync(filePath, file.new_content, 'utf-8');
        console.log(`Wrote file: ${file.filename}`);
      }
    });
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
});
