// Vercel Serverless Function — Stripe Webhook + Course Access Email
// Triggered when a checkout.session.completed event fires from Stripe.
// Sends the course access password and links to the buyer's email via AgentMail.

const AGENTMAIL_API_KEY = process.env.AGENTMAIL_API_KEY;
const INBOX_ID = "hermes-course@agentmail.to";
const COURSE_URL = "https://www.hermesagents.pro";
const PASSWORD = "HERMES-XK7M-PQ92";

module.exports = async (req, res) => {
  // Only accept POST
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  // Verify it's a Stripe event
  const event = req.body;
  if (!event || !event.type) {
    return res.status(400).json({ error: "Not a valid Stripe event" });
  }

  // We only care about completed checkouts
  if (event.type !== "checkout.session.completed") {
    return res.status(200).json({ received: true, ignored: true });
  }

  const session = event.data.object;
  const customerEmail = session.customer_details?.email || session.customer_email;

  if (!customerEmail) {
    console.error("No customer email in Stripe session");
    return res.status(200).json({ error: "No email found" });
  }

  try {
    const response = await fetch(`https://api.agentmail.to/v0/inboxes/${INBOX_ID}/messages/send`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${AGENTMAIL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        to: customerEmail,
        subject: "🎉 Welcome to AI Agents: Master Hermes Agent — Your Course Access",
        html: buildAccessEmail(customerEmail),
        text: buildAccessText(),
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      console.error("AgentMail error:", response.status, err);
      return res.status(500).json({ error: "Failed to send email" });
    }

    console.log(`Course access email sent to ${customerEmail}`);
    return res.status(200).json({ success: true, email: customerEmail });
  } catch (err) {
    console.error("Webhook error:", err);
    return res.status(500).json({ error: "Server error" });
  }
};

function buildAccessEmail(email) {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 0; background: #0a0a14; color: #e0e0e0; }
    .container { max-width: 600px; margin: 0 auto; padding: 40px 24px; }
    .header { text-align: center; margin-bottom: 32px; }
    .header h1 { color: #fff; font-size: 26px; margin: 0 0 8px; }
    .header p { color: #8a8aa0; font-size: 16px; margin: 0; }
    .divider { height: 1px; background: linear-gradient(90deg, transparent, #6c5ce7, transparent); margin: 28px 0; }
    .card { background: #14142a; border: 1px solid #2a2a50; border-radius: 12px; padding: 24px; margin-bottom: 20px; }
    .card h3 { color: #a78bfa; margin: 0 0 12px; font-size: 18px; }
    .card p { color: #b0b0c0; margin: 0 0 8px; line-height: 1.6; }
    .password-box { background: #1a1a2e; border: 1px solid #6c5ce7; border-radius: 10px; padding: 16px; text-align: center; margin: 16px 0; }
    .password-box .label { color: #808098; font-size: 13px; margin-bottom: 6px; }
    .password-box .code { font-family: monospace; font-size: 28px; font-weight: 700; color: #00cec9; letter-spacing: 4px; }
    .step { display: flex; gap: 12px; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #1e1e3a; }
    .step:last-child { border-bottom: none; }
    .step-num { background: linear-gradient(135deg, #6c5ce7, #00cec9); color: #fff; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; flex-shrink: 0; }
    .step-content { color: #b0b0c0; font-size: 14px; line-height: 1.5; }
    .step-content strong { color: #e0e0e8; }
    .btn { display: inline-block; background: linear-gradient(135deg, #6c5ce7, #00cec9); color: #fff; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 16px; margin-top: 20px; }
    .footer-text { text-align: center; color: #505068; font-size: 13px; margin-top: 32px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎉 Welcome to AI Agents: Master Hermes Agent!</h1>
      <p>Your purchase is confirmed. You now have lifetime access to the full course.</p>
    </div>

    <div class="divider"></div>

    <div class="card">
      <h3>🔐 Your Course Access Password</h3>
      <p>Use this password to unlock the course dashboard and all 10 modules.</p>
      <div class="password-box">
        <div class="label">Course Password</div>
        <div class="code">HERMES-XK7M-PQ92</div>
      </div>
      <p style="text-align:center;">
        <a href="${COURSE_URL}/course/" class="btn">Start Learning Now</a>
      </p>
    </div>

    <div class="card">
      <h3>📚 Your Learning Path</h3>

      <div class="step">
        <div class="step-num">1</div>
        <div class="step-content"><strong>Start with Module 1</strong> — "What is Hermes Agent" (15 min)</div>
      </div>
      <div class="step">
        <div class="step-num">2</div>
        <div class="step-content"><strong>Install Hermes</strong> — One command, running on your machine</div>
      </div>
      <div class="step">
        <div class="step-num">3</div>
        <div class="step-content"><strong>Build Your First Skill</strong> — By Module 5, you'll create custom skills</div>
      </div>
      <div class="step">
        <div class="step-num">4</div>
        <div class="step-content"><strong>Deploy &amp; Monetize</strong> — Modules 8-10 cover VPS, automation, and revenue</div>
      </div>
    </div>

    <div class="card" style="text-align:center;">
      <h3>💬 Need Help?</h3>
      <p>Email us anytime at <strong style="color:#a78bfa;">hermes-course@agentmail.to</strong></p>
      <p style="font-size:13px;color:#707090;">We typically reply within 12 hours.</p>
    </div>

    <div class="divider"></div>
    <div class="footer-text">
      <p>AI Agents: Master Hermes Agent · ${COURSE_URL}</p>
      <p>You received this because you purchased the course.</p>
    </div>
  </div>
</body>
</html>`;
}

function buildAccessText() {
  return `🎉 WELCOME TO AI AGENTS: MASTER HERMES AGENT!

Your purchase is confirmed. You now have lifetime access.

🔐 YOUR COURSE PASSWORD: HERMES-XK7M-PQ92

Use this password at ${COURSE_URL}/course/ to unlock the course.

📚 YOUR LEARNING PATH:
1. Start with Module 1 - "What is Hermes Agent" (15 min)
2. Install Hermes - one command on your machine
3. Build Your First Skill - by Module 5
4. Deploy & Monetize - Modules 8-10

💬 Need help? Email hermes-course@agentmail.to

Start learning: ${COURSE_URL}/course/`;
}
