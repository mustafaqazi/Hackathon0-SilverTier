#!/usr/bin/env node

/**
 * Example Usage of Email MCP Server
 *
 * This file demonstrates how to use the email MCP server
 * to send emails, verify configuration, and list templates.
 *
 * For production use with Claude, use the MCP protocol directly.
 * This file is for testing and demonstration purposes.
 */

import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const EMAIL_CONFIG = {
  service: 'gmail',
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

/**
 * Example 1: Verify Email Configuration
 */
async function example1_verifyConfig() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 1: Verify Email Configuration');
  console.log('='.repeat(60));

  try {
    const transporter = nodemailer.createTransport({
      service: EMAIL_CONFIG.service,
      host: EMAIL_CONFIG.host,
      port: EMAIL_CONFIG.port,
      secure: EMAIL_CONFIG.secure,
      auth: EMAIL_CONFIG.auth,
    });

    const verified = await transporter.verify();

    if (verified) {
      console.log('✓ Email configuration is VALID');
      console.log(`  From: ${EMAIL_CONFIG.from_name} <${EMAIL_CONFIG.from_email}>`);
      console.log(`  Service: ${EMAIL_CONFIG.service}`);
      console.log(`  Host: ${EMAIL_CONFIG.host}:${EMAIL_CONFIG.port}`);
    } else {
      console.log('✗ Email configuration is INVALID');
      console.log('  Check your EMAIL_USER and EMAIL_PASS in .env file');
    }
  } catch (error) {
    console.error('✗ Error verifying configuration:', error.message);
  }
}

/**
 * Example 2: Send Simple Email
 */
async function example2_sendSimpleEmail() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 2: Send Simple Email');
  console.log('='.repeat(60));

  try {
    const transporter = nodemailer.createTransport({
      service: EMAIL_CONFIG.service,
      host: EMAIL_CONFIG.host,
      port: EMAIL_CONFIG.port,
      secure: EMAIL_CONFIG.secure,
      auth: EMAIL_CONFIG.auth,
    });

    const mailOptions = {
      from: `${EMAIL_CONFIG.from_name} <${EMAIL_CONFIG.from_email}>`,
      to: EMAIL_CONFIG.from_email, // Send to self for testing
      subject: 'Test Email from MCP Server',
      html: `
        <h1>Hello! 👋</h1>
        <p>This is a test email from the Email MCP Server.</p>
        <p>Sent at: ${new Date().toLocaleString()}</p>
        <p>If you received this, everything is working!</p>
      `,
      text: 'Hello! This is a test email from the Email MCP Server.',
    };

    console.log('Sending email to:', mailOptions.to);
    const info = await transporter.sendMail(mailOptions);

    console.log('✓ Email sent successfully!');
    console.log('  Message ID:', info.messageId);
    console.log('  Response:', info.response);
  } catch (error) {
    console.error('✗ Failed to send email:', error.message);
  }
}

/**
 * Example 3: Send Email with CC/BCC
 */
async function example3_sendWithCCBCC() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 3: Send Email with CC/BCC');
  console.log('='.repeat(60));

  try {
    const transporter = nodemailer.createTransport({
      service: EMAIL_CONFIG.service,
      host: EMAIL_CONFIG.host,
      port: EMAIL_CONFIG.port,
      secure: EMAIL_CONFIG.secure,
      auth: EMAIL_CONFIG.auth,
    });

    const mailOptions = {
      from: `${EMAIL_CONFIG.from_name} <${EMAIL_CONFIG.from_email}>`,
      to: EMAIL_CONFIG.from_email,
      cc: EMAIL_CONFIG.from_email, // Include yourself in CC for demo
      subject: 'Email with CC/BCC Support',
      html: `
        <h2>Team Update</h2>
        <p>This email demonstrates CC/BCC functionality.</p>
        <ul>
          <li>To: Primary recipient</li>
          <li>CC: Carbon Copy (recipients can see each other)</li>
          <li>BCC: Blind Carbon Copy (hidden from others)</li>
        </ul>
      `,
    };

    console.log('Sending email with CC/BCC support');
    const info = await transporter.sendMail(mailOptions);

    console.log('✓ Email sent with CC/BCC!');
    console.log('  Message ID:', info.messageId);
  } catch (error) {
    console.error('✗ Failed to send email:', error.message);
  }
}

/**
 * Example 4: Send Bulk Emails
 */
async function example4_sendBulkEmails() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 4: Send Bulk Emails');
  console.log('='.repeat(60));

  try {
    const transporter = nodemailer.createTransport({
      service: EMAIL_CONFIG.service,
      host: EMAIL_CONFIG.host,
      port: EMAIL_CONFIG.port,
      secure: EMAIL_CONFIG.secure,
      auth: EMAIL_CONFIG.auth,
    });

    const recipients = [
      {
        email: EMAIL_CONFIG.from_email,
        name: 'Recipient 1',
      },
      {
        email: EMAIL_CONFIG.from_email,
        name: 'Recipient 2',
      },
    ];

    let successful = 0;
    let failed = 0;

    console.log(`Sending emails to ${recipients.length} recipients...`);

    for (const recipient of recipients) {
      try {
        const mailOptions = {
          from: `${EMAIL_CONFIG.from_name} <${EMAIL_CONFIG.from_email}>`,
          to: recipient.email,
          subject: `Bulk Email Test - ${recipient.name}`,
          html: `
            <p>Hi ${recipient.name},</p>
            <p>This is a bulk email test.</p>
            <p>Sent to: ${recipient.email}</p>
            <p>Time: ${new Date().toLocaleString()}</p>
          `,
        };

        await transporter.sendMail(mailOptions);
        successful++;
        console.log(`  ✓ Sent to: ${recipient.email}`);
      } catch (error) {
        failed++;
        console.log(`  ✗ Failed for ${recipient.email}: ${error.message}`);
      }
    }

    console.log(`\n✓ Bulk send completed!`);
    console.log(`  Successful: ${successful}`);
    console.log(`  Failed: ${failed}`);
    console.log(`  Total: ${recipients.length}`);
  } catch (error) {
    console.error('✗ Bulk email error:', error.message);
  }
}

/**
 * Example 5: Send Email from HTML Template
 */
async function example5_sendFromTemplate() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 5: Send Email from Template');
  console.log('='.repeat(60));

  try {
    const transporter = nodemailer.createTransport({
      service: EMAIL_CONFIG.service,
      host: EMAIL_CONFIG.host,
      port: EMAIL_CONFIG.port,
      secure: EMAIL_CONFIG.secure,
      auth: EMAIL_CONFIG.auth,
    });

    // Simple template with variables
    const templateHTML = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body { font-family: Arial, sans-serif; }
          .container { max-width: 600px; margin: 20px auto; }
          .header { background: #4CAF50; color: white; padding: 20px; }
          .content { padding: 20px; }
          .button { background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Welcome, {{name}}!</h1>
          </div>
          <div class="content">
            <p>Hi {{name}},</p>
            <p>Welcome to {{company}}! We're excited to have you on board.</p>
            <p>Click below to get started:</p>
            <p><a href="{{cta_url}}" class="button">{{cta_text}}</a></p>
            <p>Best regards,<br>The {{company}} Team</p>
          </div>
        </div>
      </body>
      </html>
    `;

    // Replace template variables
    const templateData = {
      name: 'John Doe',
      company: 'Acme Corp',
      cta_url: 'https://example.com/onboarding',
      cta_text: 'Get Started',
    };

    let html = templateHTML;
    Object.keys(templateData).forEach((key) => {
      const regex = new RegExp(`{{${key}}}`, 'g');
      html = html.replace(regex, templateData[key]);
    });

    const mailOptions = {
      from: `${EMAIL_CONFIG.from_name} <${EMAIL_CONFIG.from_email}>`,
      to: EMAIL_CONFIG.from_email,
      subject: `Welcome to ${templateData.company}!`,
      html: html,
      text: `Welcome ${templateData.name} to ${templateData.company}!`,
    };

    console.log('Sending templated email...');
    const info = await transporter.sendMail(mailOptions);

    console.log('✓ Template email sent!');
    console.log('  Message ID:', info.messageId);
    console.log('  Subject:', mailOptions.subject);
  } catch (error) {
    console.error('✗ Failed to send template email:', error.message);
  }
}

/**
 * Main: Run all examples
 */
async function main() {
  console.log('\n╔═══════════════════════════════════════════════════════╗');
  console.log('║   Email MCP Server - Usage Examples                   ║');
  console.log('╚═══════════════════════════════════════════════════════╝');

  // Check if credentials are configured
  if (!EMAIL_CONFIG.auth.user || !EMAIL_CONFIG.auth.pass) {
    console.error('\n✗ ERROR: Email credentials not configured!');
    console.error('  Please configure .env file with:');
    console.error('    EMAIL_USER=your-email@gmail.com');
    console.error('    EMAIL_PASS=your-app-password');
    process.exit(1);
  }

  // Run examples
  await example1_verifyConfig();
  await example2_sendSimpleEmail();
  await example3_sendWithCCBCC();
  await example4_sendBulkEmails();
  await example5_sendFromTemplate();

  console.log('\n' + '='.repeat(60));
  console.log('All examples completed!');
  console.log('='.repeat(60));
  console.log('\nFor production use, run the MCP server:');
  console.log('  npm start');
  console.log('\nThen use Claude to invoke email tools.');
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export {
  example1_verifyConfig,
  example2_sendSimpleEmail,
  example3_sendWithCCBCC,
  example4_sendBulkEmails,
  example5_sendFromTemplate,
};
