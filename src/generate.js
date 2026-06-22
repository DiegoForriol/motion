import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

function loadTemplate(templateName) {
  const templatePath = join(__dirname, '..', 'templates', `${templateName}.json`);
  return JSON.parse(readFileSync(templatePath, 'utf-8'));
}

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

function generateCampaign() {
  // Edit config.json to change contacts, URLs and image — no code changes needed
  const config = JSON.parse(readFileSync(join(__dirname, '..', 'config.json'), 'utf-8'));

  const results = config.contacts.map((contact) =>
    buildMessagePayload({
      to: contact.phone,
      templateName: 'rebajas_vosso',
      headerImageUrl: config.headerImageUrl,
      bodyVariables: [contact.fullName],
      ctaUrl: config.shopUrl,
    })
  );

  const outputPath = join(__dirname, '..', 'output', 'campaign_payloads.json');
  writeFileSync(outputPath, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`Generated ${results.length} message payload(s) → output/campaign_payloads.json`);
  return results;
}

generateCampaign();
