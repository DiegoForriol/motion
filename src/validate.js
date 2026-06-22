import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const REQUIRED_COMPONENT_TYPES = ['HEADER', 'BODY', 'BUTTONS'];
const VALID_CATEGORIES = ['MARKETING', 'UTILITY', 'AUTHENTICATION'];
const VALID_HEADER_FORMATS = ['IMAGE', 'VIDEO', 'DOCUMENT', 'TEXT'];

function validateTemplate(templateName) {
  const templatePath = join(__dirname, '..', 'templates', `${templateName}.json`);
  const template = JSON.parse(readFileSync(templatePath, 'utf-8'));
  const errors = [];

  if (!template.name) errors.push('Missing required field: name');
  if (!template.language) errors.push('Missing required field: language');
  if (!VALID_CATEGORIES.includes(template.category)) {
    errors.push(`Invalid category "${template.category}". Must be one of: ${VALID_CATEGORIES.join(', ')}`);
  }

  const componentTypes = template.components?.map((c) => c.type) ?? [];
  for (const required of REQUIRED_COMPONENT_TYPES) {
    if (!componentTypes.includes(required)) {
      errors.push(`Missing required component: ${required}`);
    }
  }

  const header = template.components?.find((c) => c.type === 'HEADER');
  if (header && !VALID_HEADER_FORMATS.includes(header.format)) {
    errors.push(`Invalid header format "${header.format}". Must be one of: ${VALID_HEADER_FORMATS.join(', ')}`);
  }

  const body = template.components?.find((c) => c.type === 'BODY');
  if (body) {
    const variableMatches = body.text?.match(/\{\{\d+\}\}/g) ?? [];
    const exampleValues = body.example?.body_text?.[0] ?? [];
    if (variableMatches.length !== exampleValues.length) {
      errors.push(
        `Body has ${variableMatches.length} variable(s) but example provides ${exampleValues.length} value(s)`
      );
    }
  }

  if (errors.length > 0) {
    console.error(`❌ Template "${templateName}" validation failed:`);
    errors.forEach((e) => console.error(`   • ${e}`));
    process.exit(1);
  }

  console.log(`✅ Template "${templateName}" is valid.`);
  console.log(`   Category : ${template.category}`);
  console.log(`   Language : ${template.language}`);
  console.log(`   Components: ${componentTypes.join(', ')}`);
}

validateTemplate('rebajas_vosso');
