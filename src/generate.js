import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * Loads a template definition from the templates directory.
 */
function loadTemplate(templateName) {
  const templatePath = join(__dirname, '..', 'templates', `${templateName}.json`);
  return JSON.parse(readFileSync(templatePath, 'utf-8'));
}

/**
 * Replaces {{n}} variable placeholders in the body text.
 */
function fillBodyVariables(text, variables) {
  return variables.reduce(
    (result, value, index) => result.replaceAll(`{{${index + 1}}}`, value),
    text
  );
}

/**
 * Builds a WhatsApp API-ready message payload for a single recipient.
 */
function buildMessagePayload({ to, templateName, headerImageUrl, bodyVariables, ctaUrl }) {
  const template = loadTemplate(templateName);

  return {
    messaging_product: 'whatsapp',
    to,
    type: 'template',
    template: {
      name: template.name,
      language: { code: template.language },
      components: [
        {
          type: 'header',
          parameters: [
            {
              type: 'image',
              image: { link: headerImageUrl },
            },
          ],
        },
        {
          type: 'body',
          parameters: bodyVariables.map((value) => ({ type: 'text', text: value })),
        },
        {
          type: 'button',
          sub_type: 'url',
          index: '0',
          parameters: [{ type: 'text', text: ctaUrl }],
        },
      ],
    },
  };
}

/**
 * Generates message payloads for a list of contacts and saves them to output/.
 */
function generateCampaign(contacts) {
  const results = contacts.map((contact) =>
    buildMessagePayload({
      to: contact.phone,
      templateName: 'rebajas_vosso',
      headerImageUrl: contact.headerImageUrl,
      bodyVariables: [contact.fullName],
      ctaUrl: contact.shopUrl,
    })
  );

  const outputPath = join(__dirname, '..', 'output', 'campaign_payloads.json');
  writeFileSync(outputPath, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`Generated ${results.length} message payload(s) → output/campaign_payloads.json`);
  return results;
}

// --- Example usage ---
const contacts = [
  {
    phone: '+34626930927',
    fullName: 'Juana ROMERO RODENAS',
    headerImageUrl: 'https://example.com/images/rebajas-vosso-30.jpg',
    shopUrl: 'https://vosso.es/rebajas',
  },
];

generateCampaign(contacts);
