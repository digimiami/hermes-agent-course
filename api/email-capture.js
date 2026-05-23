// Vercel Serverless Function — Email Capture via AgentMail
// Handles form submissions from the landing page email capture form.
// Sends the free skills guide via AgentMail API.

const AGENTMAIL_API_KEY = process.env.AGENTMAIL_API_KEY;
const INBOX_ID = "hermes-course@agentmail.to";
const SITE_URL = "https://www.hermesagents.pro";

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader("Access-Control-Allow-Origin", SITE_URL);
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  // Handle preflight
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  // Only accept POST
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { email } = req.body || {};

  // Validate email
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: "Invalid email address" });
  }

  try {
    // Send the welcome + free skills email via AgentMail
    const response = await fetch(`https://api.agentmail.to/v0/inboxes/${INBOX_ID}/messages/send`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${AGENTMAIL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        to: email,
        subject: "🎯 Your Free Hermes Agent Skills Are Here!",
        html: buildWelcomeEmail(email),
        text: buildWelcomeText(email),
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      console.error("AgentMail error:", response.status, err);
      return res.status(500).json({ error: "Failed to send email. Please try again." });
    }

    const result = await response.json();

    return res.status(200).json({
      success: true,
      message: "Check your inbox for the free skills guide!",
      message_id: result.message_id,
    });
  } catch (err) {
    console.error("Email capture error:", err);
    return res.status(500).json({ error: "Server error. Please try again." });
  }
};

function buildWelcomeEmail(email) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #0a0a14; color: #e0e0e0; }
    .container { max-width: 600px; margin: 0 auto; padding: 40px 24px; }
    .header { text-align: center; margin-bottom: 36px; }
    .header h1 { color: #fff; font-size: 28px; margin: 0 0 8px; }
    .header p { color: #8a8aa0; font-size: 16px; margin: 0; }
    .divider { height: 1px; background: linear-gradient(90deg, transparent, #6c5ce7, transparent); margin: 28px 0; }
    .card { background: #14142a; border: 1px solid #2a2a50; border-radius: 12px; padding: 24px; margin-bottom: 20px; }
    .card h3 { color: #a78bfa; margin: 0 0 12px; font-size: 18px; }
    .card p { color: #b0b0c0; margin: 0 0 8px; line-height: 1.6; }
    .skill { display: flex; gap: 12px; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #1e1e3a; }
    .skill:last-child { border-bottom: none; }
    .skill-icon { font-size: 20px; flex-shrink: 0; }
    .skill-name { color: #c0c0e0; font-weight: 600; margin-bottom: 2px; }
    .skill-desc { color: #8080a0; font-size: 14px; }
    .btn { display: inline-block; background: linear-gradient(135deg, #6c5ce7, #a855f7); color: #fff; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 16px; margin-top: 20px; }
    .btn:hover { background: linear-gradient(135deg, #7c6cf7, #b865ff); }
    .footer-text { text-align: center; color: #505068; font-size: 13px; margin-top: 32px; }
    .highlight { color: #a78bfa; font-weight: 600; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎯 Your Free Hermes Agent Skills Are Here!</h1>
      <p>5 powerful skills to automate your workflow — ready to use immediately.</p>
    </div>

    <div class="divider"></div>

    <div class="card">
      <h3>⚡ Quick Start: Install Hermes Agent</h3>
      <p>If you haven't already, install Hermes Agent with one command:</p>
      <p style="background:#1a1a2e;padding:12px 16px;border-radius:8px;font-family:monospace;font-size:14px;margin-top:12px;color:#a0e0a0;">pip install hermes-agent</p>
      <p style="margin-top:12px;">Or visit the <a href="https://hermes-agent.nousresearch.com" style="color:#a78bfa;">official docs</a> for other install methods.</p>
    </div>

    <div class="card">
      <h3>📦 Your 5 Free Skills</h3>

      <div class="skill">
        <div class="skill-icon">🚀</div>
        <div>
          <div class="skill-name">Deploy Skill</div>
          <div class="skill-desc">One-command deploy to any VPS. Automates server setup, Docker install, nginx config, SSL certs, and daemon management. Saves 2+ hours per deployment.</div>
        </div>
      </div>

      <div class="skill">
        <div class="skill-icon">🔍</div>
        <div>
          <div class="skill-name">Audit Skill</div>
          <div class="skill-desc">Runs comprehensive security and configuration audits on any server or codebase. Checks permissions, open ports, dependency vulnerabilities, and compliance settings.</div>
        </div>
      </div>

      <div class="skill">
        <div class="skill-icon">🕸️</div>
        <div>
          <div class="skill-name">Scrape Skill</div>
          <div class="skill-desc">Intelligent web scraper that extracts structured data from any website. Handles pagination, authentication, rate limiting, and outputs clean JSON/CSV.</div>
        </div>
      </div>

      <div class="skill">
        <div class="skill-icon">📊</div>
        <div>
          <div class="skill-name">Monitor Skill</div>
          <div class="skill-desc">Real-time server and application monitoring. Tracks CPU, memory, disk, network, and application health. Sends alerts to Telegram when thresholds are breached.</div>
        </div>
      </div>

      <div class="skill">
        <div class="skill-icon">💾</div>
        <div>
          <div class="skill-name">Backup Skill</div>
          <div class="skill-desc">Automated backup pipeline with encryption, compression, and remote storage (S3, B2, SFTP). Supports databases, config files, and directories with rotation policies.</div>
        </div>
      </div>
    </div>

    <div class="card" style="text-align:center;">
      <h3>🎓 Want the Full Course?</h3>
      <p>These 5 skills are just the beginning. The complete <span class="highlight">AI Agents: Master Hermes Agent</span> course has 10 modules covering everything — from installation to advanced multi-agent workflows and monetization.</p>
      <a href="${SITE_URL}" class="btn">View the Full Course →</a>
    </div>

    <div class="divider"></div>

    <div class="footer-text">
      <p>Sent by AI Agents Course · ${SITE_URL}</p>
      <p>You received this because you signed up for free Hermes Agent skills.</p>
      <p>No spam — unsubscribe anytime by replying to this email.</p>
    </div>
  </div>
</body>
</html>`;
}

function buildWelcomeText(email) {
  return `🎯 YOUR FREE HERMES AGENT SKILLS ARE HERE!

5 powerful skills to automate your workflow — ready to use immediately.

---

⚡ QUICK START: INSTALL HERMES AGENT

If you haven't already, install Hermes Agent with one command:

  pip install hermes-agent

Or visit https://hermes-agent.nousresearch.com for other install methods.

---

📦 YOUR 5 FREE SKILLS

🚀 Deploy Skill
One-command deploy to any VPS. Automates server setup, Docker install, nginx config, SSL certs, and daemon management. Saves 2+ hours per deployment.

🔍 Audit Skill
Runs comprehensive security and configuration audits on any server or codebase. Checks permissions, open ports, dependency vulnerabilities, and compliance settings.

🕸️ Scrape Skill
Intelligent web scraper that extracts structured data from any website. Handles pagination, authentication, rate limiting, and outputs clean JSON/CSV.

📊 Monitor Skill
Real-time server and application monitoring. Tracks CPU, memory, disk, network, and application health. Sends alerts to Telegram when thresholds are breached.

💾 Backup Skill
Automated backup pipeline with encryption, compression, and remote storage (S3, B2, SFTP). Supports databases, config files, and directories with rotation policies.

---

🎓 WANT THE FULL COURSE?

These 5 skills are just the beginning. The complete "AI Agents: Master Hermes Agent" course has 10 modules covering everything — from installation to advanced multi-agent workflows and monetization.

View the full course: ${SITE_URL}

---
Sent by AI Agents Course · ${SITE_URL}
No spam — unsubscribe anytime by replying to this email.`;
}
