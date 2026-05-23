#!/usr/bin/env python3
"""
Stripe Checkout Setup Script
Run this to create a Stripe product and price for your course.

Usage:
  python3 setup_stripe.py
  
Prerequisites:
  - Stripe account
  - STRIPE_SECRET_KEY in environment or .env
"""

import os, json, sys
from pathlib import Path

def run_setup():
    print("=" * 60)
    print("STRIPE CHECKOUT SETUP FOR YOUR COURSE")
    print("=" * 60)
    print()
    
    stripe_key = os.environ.get("STRIPE_SECRET_KEY", "")
    
    if not stripe_key:
        print("❌ STRIPE_SECRET_KEY not set.")
        print()
        print("To set up Stripe:")
        print("  1. Go to https://dashboard.stripe.com/apikeys")
        print("  2. Copy your secret key (sk_live_... or sk_test_...)")
        print("  3. Run: export STRIPE_SECRET_KEY='sk_live_...'")
        print("  4. Run this script again")
        print()
        print("Or manually create: Product → \"AI Agents: Master Hermes Agent\"")
        print("  Price: $97.00 one-time")
        print("  Then update landing.html with your Price ID")
        sys.exit(1)
    
    print("✅ Stripe key found!")
    print()
    print("--- MANUAL SETUP INSTRUCTIONS ---")
    print()
    print("1. Go to https://dashboard.stripe.com/products")
    print("2. Click 'Add Product'")
    print("3. Name: 'AI Agents: Master Hermes Agent'")
    print("4. Description: '10-module course teaching you to install, configure, train, and monetize an open-source AI agent. Includes installation guides, skills system, gateway setup, VPS deployment, and 7 monetization strategies.'")
    print("5. Price: One-time → $97.00 USD")
    print("6. Save → Get the Price ID (looks like: price_abc123...)")
    print()
    print("7. Update /root/hermes-course/sales/landing.html:")
    print("   - Replace 'pk_live_YOUR_KEY_HERE' with your publishable key")
    print("   - Replace 'price_YOUR_PRICE_ID_HERE' with the Price ID")
    print("   - Update SUCCESS_URL and CANCEL_URL")
    print()
    print("8. Deploy the landing page to your domain (Netlify, Vercel, or your own server)")
    print()
    
    print("--- NETLIFY FREE DEPLOYMENT ---")
    print("  netlify deploy --prod --dir=/root/hermes-course/sales/")
    print()
    print("--- OR DROP ON VERCEL ---")
    print("  npm i -g vercel && vercel --prod /root/hermes-course/sales/")
    print()
    
    print("--- COURSE FILE DELIVERY ---")
    print("After purchase, you can:")
    print("  a) Email the PDF/manual download link (manual delivery)")
    print("  b) Use Stripe webhooks + a simple server to auto-grant access")
    print("  c) Upload to Gumroad as hosted product (easiest)")
    print()
    print("For option (a), just set up Stripe's email receipt + attach the course files as a download link in the confirmation page.")

if __name__ == "__main__":
    run_setup()
