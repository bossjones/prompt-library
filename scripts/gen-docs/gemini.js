#!node
const { GoogleGenerativeAI } = require("@google/generative-ai");
const fs = require("fs").promises;
const path = require("path");
const yaml = require("js-yaml");

// Function to read all data from stdin
function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");

    process.stdin.on("data", chunk => {
      data += chunk;
    });

    process.stdin.on("end", () => {
      resolve(data.trim());
    });

    process.stdin.on("error", err => {
      reject(err);
    });
  });
}

async function run() {
  try {
    // Ensure a filename is provided as an argument
    const args = process.argv.slice(2);
    if (args.length !== 1) {
      console.error("Usage: node script.js <config-file.yaml>");
      process.exit(1);
    }

    const configPath = path.resolve(args[0]);

    // Read and parse the YAML configuration file
    const configContent = await fs.readFile(configPath, "utf8");
    let config;
    try {
      config = yaml.load(configContent);
    } catch (yamlErr) {
      console.error("Error parsing YAML configuration:", yamlErr.message);
      process.exit(1);
    }

    // Validate required properties in the config
    if (!config.model) {
      console.error("Configuration file must include a 'model' property.");
      process.exit(1);
    }

    if (!config.generationConfig) {
      console.error("Configuration file must include a 'generationConfig' property.");
      process.exit(1);
    }

    // Initialize the GoogleGenerativeAI client
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      console.error("Environment variable GEMINI_API_KEY is not set.");
      process.exit(1);
    }

    const genAI = new GoogleGenerativeAI(apiKey);

    // Get the generative model from the config
    const model = genAI.getGenerativeModel({
      model: config.model,
      systemInstruction: config.systemInstruction,
    });

    // Extract generationConfig from the config
    const generationConfig = config.generationConfig;

    // Read input from stdin
    const userInput = await readStdin();

    if (!userInput) {
      console.error("No input received from stdin.");
      process.exit(1);
    }

    // Start a chat session with the provided generationConfig
    const chatSession = model.startChat({
      generationConfig,
    });

    // Send the user's input as a message
    const result = await chatSession.sendMessage(userInput);
    console.error(result.response);
    console.log(result.response.text());
  } catch (err) {
    console.error("An error occurred:", err.message);
    process.exit(1);
  }
}

run();
