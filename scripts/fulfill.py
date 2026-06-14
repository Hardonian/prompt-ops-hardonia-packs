#!/usr/bin/env python3
"""
Prompt Ops Packs - Fulfillment Script

Usage:
  python3 fulfill.py --email customer@example.com --pack starter-outreach
  python3 fulfill.py --email customer@example.com --pack all

Requires: pip install stripe sendgrid (or use smtplib)
"""

import json
import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

PACKS_DIR = Path(__file__).resolve().parent.parent / 'packs'
PACK_PRICES = {
    'starter-outreach': 79,
    'operator-workbook': 129,
    'gtm-starter': 199,
}

def load_pack(name):
    path = PACKS_DIR / f'{name}.json'
    if not path.exists():
        raise FileNotFoundError(f'Pack not found: {path}')
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

def list_packs():
    return sorted([p.stem for p in PACKS_DIR.glob('*.json')])

def format_pack_for_email(pack_data):
    """Format pack content as clean markdown for email delivery."""
    lines = [
        f"# {pack_data['name']}",
        f"**Price:** ${pack_data['price']}",
        f"**Description:** {pack_data['description']}",
        "",
        "---",
        ""
    ]
    for i, prompt in enumerate(pack_data['prompts'], 1):
        lines.append(f"## Prompt {i}: {prompt['title']}")
        lines.append("")
        lines.append("```")
        lines.append(prompt['prompt'])
        lines.append("```")
        if 'notes' in prompt:
            lines.append(f"**Notes:** {prompt['notes']}")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)

def create_delivery_email(customer_email, pack_names):
    """Create email message with pack content."""
    subject = "Your Prompt Ops Pack(s) — Hardonia"
    
    body_parts = [
        "Thanks for your purchase! Your Prompt Ops pack(s) are attached.",
        "",
        "Each pack contains ready-to-use prompts. Copy the prompt blocks into your AI tool of choice (ChatGPT, Claude, etc.), fill in the {{VARIABLES}}, and execute.",
        "",
        "---",
        ""
    ]
    
    attachments = []
    for pack_name in pack_names:
        pack = load_pack(pack_name)
        content = format_pack_for_email(pack)
        
        # Attach as .md file
        filename = f"{pack_name}.md"
        attachments.append((filename, content))
        
        body_parts.append(f"### {pack['name']} (${pack['price']})")
        body_parts.append(f"{pack['description']}")
        body_parts.append("")
    
    body_parts.extend([
        "---",
        "",
        "Questions? Reply to this email.",
        "",
        "— Scott, Hardonia",
        "scott@hardonia.com"
    ])
    
    return subject, "\n".join(body_parts), attachments

def send_email(to_email, subject, body, attachments, smtp_config):
    """Send email via SMTP."""
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = smtp_config['from_email']
    msg['To'] = to_email
    
    msg.attach(MIMEText(body, 'plain'))
    
    for filename, content in attachments:
        attachment = MIMEApplication(content.encode('utf-8'), _subtype='md')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
    
    with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
        server.starttls()
        server.login(smtp_config['user'], smtp_config['password'])
        server.send_message(msg)
    
    print(f"✓ Delivered to {to_email}")

def main():
    parser = argparse.ArgumentParser(description='Deliver Prompt Ops Packs')
    parser.add_argument('--email', required=True, help='Customer email')
    parser.add_argument('--pack', required=True, choices=list_packs() + ['all'], help='Pack to deliver')
    parser.add_argument('--smtp-host', default=os.getenv('SMTP_HOST'), help='SMTP host')
    parser.add_argument('--smtp-port', type=int, default=int(os.getenv('SMTP_PORT', 587)), help='SMTP port')
    parser.add_argument('--smtp-user', default=os.getenv('SMTP_USER'), help='SMTP username')
    parser.add_argument('--smtp-pass', default=os.getenv('SMTP_PASS'), help='SMTP password')
    parser.add_argument('--from-email', default=os.getenv('FROM_EMAIL', 'scott@hardonia.com'), help='From email')
    parser.add_argument('--dry-run', action='store_true', help='Print email content instead of sending')
    
    args = parser.parse_args()
    
    if args.pack == 'all':
        packs_to_deliver = list_packs()
    else:
        packs_to_deliver = [args.pack]
    
    # Validate packs exist
    for p in packs_to_deliver:
        load_pack(p)  # will raise if not found
    
    subject, body, attachments = create_delivery_email(args.email, packs_to_deliver)
    
    if args.dry_run:
        print(f"TO: {args.email}")
        print(f"SUBJECT: {subject}")
        print("---")
        print(body)
        print("---")
        print(f"Attachments: {[a[0] for a in attachments]}")
        return
    
    smtp_config = {
        'host': args.smtp_host,
        'port': args.smtp_port,
        'user': args.smtp_user,
        'password': args.smtp_pass,
        'from_email': args.from_email,
    }
    
    if not all([smtp_config['host'], smtp_config['user'], smtp_config['password']]):
        print("ERROR: SMTP config missing. Set SMTP_HOST, SMTP_USER, SMTP_PASS env vars or use --dry-run")
        sys.exit(1)
    
    send_email(args.email, subject, body, attachments, smtp_config)
    print(f"✓ Delivered {len(packs_to_deliver)} pack(s) to {args.email}")

if __name__ == '__main__':
    main()