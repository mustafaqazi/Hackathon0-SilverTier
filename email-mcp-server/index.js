#!/usr/bin/env node

/**
 * Email MCP Server
 * A Model Context Protocol server for sending emails via Gmail using nodemailer
 *
 * Usage:
 *   node index.js
 *
 * This server implements MCP tools that Claude can invoke to send emails.
 * Configuration is handled via environment variables or .env file.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ToolSchema,
} from '@modelcontextprotocol/sdk/types.js';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Email configuration from environment variables
const EMAIL_CONFIG = {
  service: process.env.EMAIL_SERVICE || 'gmail',
  host: process.env.EMAIL_HOST || 'smtp.gmail.com',
  port: parseInt(process.env.EMAIL_PORT || '587'),
  secure: process.env.EMAIL_SECURE === 'true' || false,
  auth: {
    user: process.env.EMAIL_USER || '',
    pass: process.env.EMAIL_PASS || '',
  },
  from_name: process.env.EMAIL_FROM_NAME || 'AI Employee',
  from_email: process.env.EMAIL_FROM_EMAIL || process.env.EMAIL_USER || '',
};

// Create transporter for sending emails
let transporter = null;

/**
 * Initialize email transporter
 */
function initializeTransporter() {
  if (!EMAIL_CONFIG.auth.user || !EMAIL_CONFIG.auth.pass) {
    console.error('ERROR: Email credentials not configured!');
    console.error('Please set EMAIL_USER and EMAIL_PASS environment variables');
    console.error('Or configure them in .env file');
    return null;
  }

  try {
    transporter = nodemailer.createTransport({
      service: EMAIL_CONFIG.service,
      host: EMAIL_CONFIG.host,
      port: EMAIL_CONFIG.port,
      secure: EMAIL_CONFIG.secure,
      auth: {
        user: EMAIL_CONFIG.auth.user,
        pass: EMAIL_CONFIG.auth.pass,
      },
    });

    console.error('[✓] Email transporter initialized successfully');
    return transporter;
  } catch (error) {
    console.error('[✗] Failed to initialize email transporter:', error.message);
    return null;
  }
}

/**
 * Send a single email
 *
 * @param {string} to - Recipient email address
 * @param {string} subject - Email subject
 * @param {string} html - HTML content of email
 * @param {string} text - Plain text fallback
 * @param {Array} cc - CC recipients (optional)
 * @param {Array} bcc - BCC recipients (optional)
 * @returns {Promise<Object>} - Result with status and details
 */
async function sendEmail(to, subject, html, text = null, cc = [], bcc = []) {
  if (!transporter) {
    throw new Error('Email transporter not initialized. Check your configuration.');
  }

  if (!to) {
    throw new Error('Recipient email address is required');
  }

  if (!subject) {
    throw new Error('Email subject is required');
  }

  if (!html && !text) {
    throw new Error('Email content (HTML or text) is required');
  }

  const mailOptions = {
    from: `${EMAIL_CONFIG.from_name} <${EMAIL_CONFIG.from_email}>`,
    to: to,
    subject: subject,
    html: html || null,
    text: text || null,
    cc: cc && cc.length > 0 ? cc : undefined,
    bcc: bcc && bcc.length > 0 ? bcc : undefined,
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    return {
      success: true,
      messageId: info.messageId,
      response: info.response,
      timestamp: new Date().toISOString(),
      to: to,
      subject: subject,
    };
  } catch (error) {
    throw new Error(`Failed to send email: ${error.message}`);
  }
}

/**
 * Send bulk emails to multiple recipients
 *
 * @param {Array} recipients - Array of {to, subject, html, text}
 * @returns {Promise<Object>} - Result with success/failed counts
 */
async function sendBulkEmails(recipients) {
  if (!Array.isArray(recipients) || recipients.length === 0) {
    throw new Error('Recipients array is required and must not be empty');
  }

  const results = {
    total: recipients.length,
    successful: 0,
    failed: 0,
    errors: [],
    timestamp: new Date().toISOString(),
  };

  for (const recipient of recipients) {
    try {
      await sendEmail(
        recipient.to,
        recipient.subject,
        recipient.html,
        recipient.text,
        recipient.cc,
        recipient.bcc
      );
      results.successful++;
    } catch (error) {
      results.failed++;
      results.errors.push({
        to: recipient.to,
        error: error.message,
      });
    }
  }

  return results;
}

/**
 * Send email from template
 *
 * @param {string} to - Recipient email
 * @param {string} subject - Email subject
 * @param {string} templateName - Name of template to use
 * @param {Object} data - Data to replace in template
 * @returns {Promise<Object>} - Result
 */
async function sendEmailFromTemplate(to, subject, templateName, data = {}) {
  const templatePath = path.join(__dirname, 'templates', `${templateName}.html`);

  if (!fs.existsSync(templatePath)) {
    throw new Error(`Template '${templateName}' not found`);
  }

  let html = fs.readFileSync(templatePath, 'utf8');

  // Replace template variables
  Object.keys(data).forEach((key) => {
    const regex = new RegExp(`{{${key}}}`, 'g');
    html = html.replace(regex, data[key]);
  });

  return sendEmail(to, subject, html);
}

/**
 * Verify email configuration
 *
 * @returns {Promise<Object>} - Verification result
 */
async function verifyConfiguration() {
  if (!transporter) {
    return {
      verified: false,
      error: 'Email transporter not initialized',
      config: {
        service: EMAIL_CONFIG.service,
        user: EMAIL_CONFIG.auth.user ? '***configured***' : '***NOT SET***',
      },
    };
  }

  try {
    await transporter.verify();
    return {
      verified: true,
      message: 'Email configuration is valid',
      config: {
        service: EMAIL_CONFIG.service,
        from_email: EMAIL_CONFIG.from_email,
        from_name: EMAIL_CONFIG.from_name,
        user: EMAIL_CONFIG.auth.user,
      },
    };
  } catch (error) {
    return {
      verified: false,
      error: error.message,
      config: {
        service: EMAIL_CONFIG.service,
        user: EMAIL_CONFIG.auth.user,
      },
    };
  }
}

/**
 * List available email templates
 *
 * @returns {Object} - List of available templates
 */
function listTemplates() {
  const templatesDir = path.join(__dirname, 'templates');

  if (!fs.existsSync(templatesDir)) {
    return {
      available: false,
      message: 'Templates directory not found',
      templates: [],
    };
  }

  const templates = fs
    .readdirSync(templatesDir)
    .filter((file) => file.endsWith('.html'))
    .map((file) => file.replace('.html', ''));

  return {
    available: templates.length > 0,
    count: templates.length,
    templates: templates,
    templatesDir: templatesDir,
  };
}

/**
 * Define MCP tools
 */
const TOOLS = [
  {
    name: 'send_email',
    description: 'Send an email to a recipient with HTML and/or text content',
    inputSchema: {
      type: 'object',
      properties: {
        to: {
          type: 'string',
          description: 'Recipient email address (required)',
        },
        subject: {
          type: 'string',
          description: 'Email subject line (required)',
        },
        html: {
          type: 'string',
          description: 'HTML content of the email',
        },
        text: {
          type: 'string',
          description: 'Plain text version of the email (fallback)',
        },
        cc: {
          type: 'array',
          items: { type: 'string' },
          description: 'CC recipients (array of email addresses)',
        },
        bcc: {
          type: 'array',
          items: { type: 'string' },
          description: 'BCC recipients (array of email addresses)',
        },
      },
      required: ['to', 'subject'],
    },
  },
  {
    name: 'send_bulk_emails',
    description: 'Send emails to multiple recipients at once',
    inputSchema: {
      type: 'object',
      properties: {
        recipients: {
          type: 'array',
          description: 'Array of recipients with to, subject, html, text',
          items: {
            type: 'object',
            properties: {
              to: { type: 'string' },
              subject: { type: 'string' },
              html: { type: 'string' },
              text: { type: 'string' },
              cc: { type: 'array', items: { type: 'string' } },
              bcc: { type: 'array', items: { type: 'string' } },
            },
            required: ['to', 'subject'],
          },
        },
      },
      required: ['recipients'],
    },
  },
  {
    name: 'send_email_from_template',
    description:
      'Send an email using a template file with variable substitution',
    inputSchema: {
      type: 'object',
      properties: {
        to: {
          type: 'string',
          description: 'Recipient email address',
        },
        subject: {
          type: 'string',
          description: 'Email subject',
        },
        template: {
          type: 'string',
          description: 'Name of template file (without .html extension)',
        },
        data: {
          type: 'object',
          description: 'Data object for template variable replacement',
        },
      },
      required: ['to', 'subject', 'template'],
    },
  },
  {
    name: 'verify_email_config',
    description: 'Verify that email configuration is correct and working',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
  {
    name: 'list_templates',
    description: 'List all available email templates',
    inputSchema: {
      type: 'object',
      properties: {},
    },
  },
];

/**
 * Create and start MCP server
 */
const server = new Server(
  {
    name: 'email-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

/**
 * Handle list tools request
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: TOOLS,
  };
});

/**
 * Handle tool calls
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request;

  try {
    let result;

    switch (name) {
      case 'send_email':
        result = await sendEmail(
          args.to,
          args.subject,
          args.html,
          args.text,
          args.cc,
          args.bcc
        );
        break;

      case 'send_bulk_emails':
        result = await sendBulkEmails(args.recipients);
        break;

      case 'send_email_from_template':
        result = await sendEmailFromTemplate(
          args.to,
          args.subject,
          args.template,
          args.data
        );
        break;

      case 'verify_email_config':
        result = await verifyConfiguration();
        break;

      case 'list_templates':
        result = listTemplates();
        break;

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(
            {
              error: error.message,
              tool: name,
              timestamp: new Date().toISOString(),
            },
            null,
            2
          ),
        },
      ],
      isError: true,
    };
  }
});

/**
 * Start server
 */
async function main() {
  // Initialize email transporter
  initializeTransporter();

  // Start MCP server
  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error('[✓] Email MCP Server started successfully');
  console.error('[✓] Server is listening for Claude requests');
  console.error('[ℹ] Available tools: send_email, send_bulk_emails, send_email_from_template, verify_email_config, list_templates');
}

main().catch((error) => {
  console.error('[✗] Server error:', error);
  process.exit(1);
});
