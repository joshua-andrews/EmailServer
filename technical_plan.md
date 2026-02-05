# Custom Email Infrastructure Implementation Plan

## Goal

Build a self-hosted email system that allows you to:
- Create unlimited email accounts across multiple custom domains
- Receive emails from eCommerce brands and contact form replies
- Send transactional replies with high deliverability
- Access all emails programmatically via API
- Store emails in Supabase for analysis

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Your Domains                          │
│  (company1.com, company2.com, company3.com, etc.)       │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │         DNS Configuration             │
        │  MX, SPF, DKIM, DMARC, rDNS          │
        └──────────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                      │
        ▼                                      ▼
┌───────────────┐                    ┌────────────────┐
│   RECEIVING   │                    │    SENDING     │
│               │                    │                │
│  Maddy Server │                    │    AWS SES     │
│   (VPS)       │                    │                │
└───────┬───────┘                    └────────┬───────┘
        │                                      │
        └──────────────────┬───────────────────┘
                           ▼
                  ┌─────────────────┐
                  │   FastAPI       │
                  │   (Railway)     │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │   Supabase      │
                  │   (Database)    │
                  └─────────────────┘
```

## Phase 1: Infrastructure Setup

### Step 1.1: Purchase Domains
**Where**: Namecheap, Porkbun, or Squarespace
**How many**: Start with 3-5 domains for testing
**Cost**: ~$10-15/year per domain

**Recommended naming:**
- Use business-sounding names
- Avoid spammy keywords
- Consider: `[brandname]-labs.com`, `[brandname]-co.com`, etc.

### Step 1.2: Rent VPS
**Provider**: Hetzner (cheapest) or DigitalOcean (easier)
**Specs needed**:
- 2 GB RAM minimum
- 40 GB storage
- Ubuntu 22.04 LTS
- Dedicated IPv4 address

**Recommended:**
- **Hetzner CPX11**: €4.51/month (~$5 USD)
- **DigitalOcean Basic Droplet**: $12/month

> [!IMPORTANT]
> **Critical**: Request a clean IP address. Check the IP against blacklists BEFORE setting up:
> - https://mxtoolbox.com/blacklists.aspx
> - https://multirbl.valli.org/
> 
> If blacklisted, request a different IP from your provider.

### Step 1.3: AWS SES Setup
**Purpose**: Sending emails with high deliverability

**Steps**:
1. Create AWS account
2. Go to AWS SES (Simple Email Service)
3. Request production access (takes 24-48 hours)
4. Verify your domains
5. Generate SMTP credentials

**Cost**: $0.10 per 1,000 emails (very cheap)

---

## Phase 2: VPS & Maddy Installation

### Step 2.1: Initial VPS Setup
```bash
# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y curl wget git ufw fail2ban

# Configure firewall
ufw allow 22/tcp    # SSH
ufw allow 25/tcp    # SMTP
ufw allow 143/tcp   # IMAP
ufw allow 587/tcp   # SMTP submission
ufw allow 993/tcp   # IMAPS
ufw enable

# Set hostname
hostnamectl set-hostname mail.yourdomain.com
```

### Step 2.2: Install Maddy Mail Server
```bash
# Download Maddy
wget https://github.com/foxcpp/maddy/releases/download/v0.7.1/maddy-0.7.1-x86_64-linux-musl.tar.zst

# Extract
tar -xf maddy-0.7.1-x86_64-linux-musl.tar.zst

# Move to system
mv maddy /usr/local/bin/
chmod +x /usr/local/bin/maddy

# Create maddy user
useradd -r -s /bin/false -d /var/lib/maddy maddy

# Create directories
mkdir -p /etc/maddy /var/lib/maddy
chown -R maddy:maddy /var/lib/maddy

# Create systemd service
cat > /etc/systemd/system/maddy.service << 'EOF'
[Unit]
Description=Maddy Mail Server
After=network.target

[Service]
Type=notify
User=maddy
Group=maddy
ExecStart=/usr/local/bin/maddy -config /etc/maddy/maddy.conf
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Enable service
systemctl enable maddy
```

### Step 2.3: Configure Maddy
Create `/etc/maddy/maddy.conf`:

```conf
# Maddy Mail Server Configuration

# Hostname - change to your domain
hostname mail.yourdomain.com

# TLS certificates (Let's Encrypt)
tls file /etc/maddy/certs/fullchain.pem /etc/maddy/certs/privkey.pem

# Storage backend
storage.imapsql local_mailboxes {
    driver sqlite3
    dsn /var/lib/maddy/imapsql.db
}

# Authentication
auth.pass_table local_authdb {
    table sql_table {
        driver sqlite3
        dsn /var/lib/maddy/credentials.db
        table_name passwords
    }
}

# SMTP receiving (port 25)
smtp tcp://0.0.0.0:25 {
    limits {
        all rate 20 1s
        all concurrency 10
    }

    dmarc yes
    check {
        require_mx_record
        dkim
        spf
    }

    source $(local_domains) {
        deliver_to &local_mailboxes
    }

    default_source {
        reject 550 5.7.1 "Relay access denied"
    }
}

# SMTP submission (port 587) - for sending
submission tcp://0.0.0.0:587 {
    auth &local_authdb

    source $(local_domains) {
        deliver_to &remote_queue
    }
}

# IMAP (port 143 and 993)
imap tcp://0.0.0.0:993 {
    auth &local_authdb
    storage &local_mailboxes
}

# Outbound delivery
target.remote outbound_delivery {
    targets &remote_queue
}

target.queue remote_queue {
    target &outbound_delivery

    max_tries 8
    bounce {
        destination postmaster $(primary_domain)
        deliver_to &local_mailboxes
    }
}

# Local domains - add all your domains here
$(local_domains) = company1.com company2.com company3.com
$(primary_domain) = company1.com
```

---

## Phase 3: DNS Configuration

For **each domain**, configure these DNS records:

### MX Record (Mail Exchange)
```
Type: MX
Name: @
Value: mail.yourdomain.com
Priority: 10
TTL: 3600
```

### A Record (For mail server)
```
Type: A
Name: mail
Value: [YOUR_VPS_IP]
TTL: 3600
```

### SPF Record (Sender Policy Framework)
```
Type: TXT
Name: @
Value: v=spf1 ip4:[YOUR_VPS_IP] include:amazonses.com ~all
TTL: 3600
```

### DKIM Record (DomainKeys Identified Mail)
Maddy will generate this. Run:
```bash
maddyctl dkim generate yourdomain.com
```

Then add the output as a TXT record:
```
Type: TXT
Name: default._domainkey
Value: [DKIM_PUBLIC_KEY from maddy]
TTL: 3600
```

### DMARC Record
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
TTL: 3600
```

### PTR Record (Reverse DNS)
Contact your VPS provider to set:
```
[YOUR_VPS_IP] → mail.yourdomain.com
```

---

## Phase 4: FastAPI Email Management System

### Step 4.1: Create Email Management API

**Features**:
- Create email accounts programmatically
- Fetch emails via IMAP
- Send emails via AWS SES
- Store emails in Supabase

**Endpoints**:
- `POST /accounts/create` - Create new email account
- `GET /emails/{account}` - Fetch emails for an account
- `POST /emails/send` - Send email via AWS SES
- `GET /emails/html/{email_id}` - Get HTML content of email

### Step 4.2: Supabase Schema

```sql
-- Email accounts table
create table email_accounts (
  id uuid default gen_random_uuid() primary key,
  email text unique not null,
  domain text not null,
  password_hash text not null,
  created_at timestamptz default now()
);

-- Emails table
create table emails (
  id uuid default gen_random_uuid() primary key,
  account_id uuid references email_accounts(id),
  from_address text not null,
  to_address text not null,
  subject text,
  html_body text,
  text_body text,
  received_at timestamptz not null,
  message_id text unique,
  headers jsonb,
  created_at timestamptz default now()
);

-- Create indexes
create index idx_emails_account on emails(account_id);
create index idx_emails_received on emails(received_at desc);
```

---

## Phase 5: Testing & Verification

### Step 5.1: Test Receiving
1. Send test email to `test@yourdomain.com`
2. Check Maddy logs: `journalctl -u maddy -f`
3. Verify email appears in mailbox

### Step 5.2: Test Sending via AWS SES
1. Use FastAPI endpoint to send test email
2. Check delivery to Gmail/Outlook
3. Verify SPF, DKIM, DMARC pass using mail-tester.com

### Step 5.3: Deliverability Testing
**Tools**:
- https://www.mail-tester.com/ (spam score)
- https://mxtoolbox.com/emailhealth/ (DNS health)
- https://dmarcian.com/dmarc-inspector/ (DMARC validation)

**Target scores**:
- Mail-tester: 9/10 or higher
- All DNS records: Green checkmarks
- DMARC: Pass

---

## Phase 6: Scaling & Automation

### Step 6.1: Automated Account Creation
Script to create accounts programmatically:
```python
import requests

def create_email_account(email, password):
    response = requests.post(
        "https://your-api.railway.app/accounts/create",
        json={"email": email, "password": password}
    )
    return response.json()

# Create 18 accounts
for i in range(1, 19):
    email = f"account{i}@company1.com"
    password = generate_secure_password()
    create_email_account(email, password)
```

### Step 6.2: Email Scraping Service
Background job to continuously fetch new emails:
```python
# Runs every 5 minutes
# Connects to Maddy via IMAP
# Fetches new emails
# Stores in Supabase
```

---

## Cost Breakdown

| Item | Provider | Cost |
|------|----------|------|
| VPS | Hetzner | $5/month |
| Domains (5) | Namecheap | ~$6/month |
| AWS SES | AWS | ~$0.10/1000 emails |
| Railway | Railway | Free tier |
| Supabase | Supabase | Free tier |
| **Total** | | **~$11-15/month** |

---

## Timeline

- **Day 1**: Purchase domains, rent VPS, set up AWS SES
- **Day 2**: Install Maddy, configure DNS
- **Day 3**: Build FastAPI management system
- **Day 4**: Testing and verification
- **Day 5**: Deploy and create accounts

**Total: ~5 days to full deployment**

---

## Next Steps

1. Choose VPS provider (Hetzner or DigitalOcean)
2. Purchase 3-5 domains for testing
3. Set up AWS account and request SES production access
4. Begin VPS setup and Maddy installation

Ready to start?
