# Custom Email System Setup Guide for Genesis

**Project Goal**: Set up a custom email system that allows us to create unlimited email accounts across 10 domains, receive emails from businesses, and send replies with high deliverability.

**Your Role**: You'll be leading this project! Josh will help you, but you'll be doing most of the hands-on work.

**Timeline**: 3-4 days to complete everything

**Total Cost**: ~$16-20/month

---

## 📋 What You'll Build

By the end of this guide, you'll have:
- ✅ 10 custom domains (like `company1.com`, `company2.com`, etc.)
- ✅ 30 email addresses (3 per domain, like `info@company1.com`, `support@company1.com`)
- ✅ A server that receives all your emails automatically
- ✅ A system to send replies with excellent deliverability
- ✅ A dashboard to view and manage all emails

---

## 🎯 Overview: How Everything Works

```
┌─────────────────────────────────────────────────────────┐
│  Someone sends email to info@company1.com               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  Internet finds your   │
         │  domain's mail server  │
         │  (using DNS records)   │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   Your VPS Server      │
         │   (Maddy Mail Server)  │
         │   Receives the email   │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   Email stored in      │
         │   Supabase database    │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   You view email in    │
         │   your dashboard       │
         └────────────────────────┘
```

**When you reply:**
```
You write reply → AWS SES sends it → Recipient gets it ✅
```

---

## 📚 Terms You Need to Know

Before we start, let's understand some technical terms:

| Term | What It Means | Example |
|------|---------------|---------|
| **Domain** | Your website address | `company1.com` |
| **Email Address** | Your full email | `info@company1.com` |
| **VPS** | Virtual Private Server - A computer in the cloud that runs 24/7 | Like renting a computer that never turns off |
| **DNS** | Domain Name System - Phone book of the internet | Tells the internet where to find your mail server |
| **SMTP** | Simple Mail Transfer Protocol - How emails are sent | The "post office" for sending emails |
| **IMAP** | Internet Message Access Protocol - How you read emails | The "mailbox" where emails are stored |
| **IP Address** | Your server's unique address on the internet | `123.45.67.89` |
| **SSH** | Secure Shell - How you connect to your server | Like remote desktop for servers |

---

## 🛠️ Tools You'll Need

Before starting, make sure you have:

1. ✅ **A computer** (Windows, Mac, or Linux)
2. ✅ **Credit card** (for purchasing domains and VPS)
3. ✅ **Email address** (for account signups)
4. ✅ **Notepad or text editor** (to save passwords and information)
5. ✅ **About 4-6 hours** spread over 3-4 days

---

# DAY 1: Purchase & Setup Accounts

## Step 1: Purchase Domains (30 minutes)

### What You're Doing
Buying 10 domain names that will be used for your email addresses.

### Instructions

1. **Go to Namecheap.com**
   - Open your browser
   - Visit: https://www.namecheap.com

2. **Create an account**
   - Click "Sign Up" in the top right
   - Enter your email, create a password
   - Verify your email address

3. **Search for domain names**
   - Use the search bar at the top
   - Try business-sounding names like:
     - `[brandname]-labs.com`
     - `[brandname]-co.com`
     - `[brandname]-group.com`
     - `[brandname]-solutions.com`
   
   > **💡 Tip**: Avoid spammy words like "marketing", "promo", "deals" in your domain names

4. **Check availability**
   - If the domain shows a green checkmark, it's available
   - If it shows "Taken", try a different name

5. **Add 10 domains to cart**
   - Click "Add to Cart" for each domain
   - Make sure you're buying `.com` domains (they're most trusted)

6. **Purchase domains**
   - Go to your cart
   - **IMPORTANT**: Turn OFF auto-renewal if you don't want automatic charges
   - Enter payment information
   - Complete purchase

7. **Save your domain list**
   - Open Notepad or a text file
   - Write down all 10 domain names
   - Example:
     ```
     1. company1-labs.com
     2. company2-co.com
     3. company3-group.com
     ... (and so on)
     ```

**✅ Checkpoint**: You should now own 10 domains. You'll receive a confirmation email from Namecheap.

---

## Step 2: Rent a VPS Server (20 minutes)

### What You're Doing
Renting a server (computer in the cloud) that will run your email system 24/7.

### Instructions

1. **Go to Hetzner Cloud**
   - Visit: https://www.hetzner.com/cloud
   - Click "Sign Up"

2. **Create account**
   - Enter your email
   - Create a strong password
   - Verify your email

3. **Add payment method**
   - Go to your account settings
   - Add a credit card
   - You'll be charged ~$5/month

4. **Create a new project**
   - Click "New Project"
   - Name it: "Email Server"
   - Click "Create Project"

5. **Create a server**
   - Click "Add Server"
   - Choose these settings:
     - **Location**: Choose closest to you (e.g., "Ashburn, VA" if in USA)
     - **Image**: Ubuntu 22.04
     - **Type**: Shared vCPU → **CPX11** ($5.83/month)
     - **Networking**: Leave defaults
     - **SSH Key**: Skip for now (we'll set this up later)
     - **Name**: "mail-server"
   
6. **Create the server**
   - Click "Create & Buy Now"
   - Wait 30-60 seconds for server to start

7. **Save server information**
   - Once created, you'll see your server's **IP address**
   - Copy this IP address
   - Save it in your notepad:
     ```
     VPS IP Address: 123.45.67.89
     ```

8. **Get root password**
   - Click on your server name
   - Look for "Root Password" 
   - Click "Reset Root Password"
   - Copy the password and save it:
     ```
     VPS Root Password: [paste password here]
     ```

**✅ Checkpoint**: You should have a running server with an IP address and root password saved.

---

## Step 3: Set Up AWS Account (20 minutes)

### What You're Doing
Creating an Amazon Web Services account so you can use their email sending service (SES).

### Instructions

1. **Go to AWS**
   - Visit: https://aws.amazon.com
   - Click "Create an AWS Account"

2. **Sign up**
   - Enter your email
   - Choose account name: "Email System"
   - Create a password
   - Click "Continue"

3. **Enter contact information**
   - Choose "Personal" account
   - Fill in your name, address, phone number
   - Click "Continue"

4. **Add payment information**
   - Enter credit card details
   - You won't be charged much (AWS SES is very cheap)
   - Click "Verify and Continue"

5. **Phone verification**
   - Enter your phone number
   - You'll receive a code via SMS
   - Enter the code
   - Click "Continue"

6. **Choose support plan**
   - Select "Basic Support - Free"
   - Click "Complete Sign Up"

7. **Wait for account activation**
   - This can take 5-10 minutes
   - You'll receive an email when ready

8. **Log in to AWS Console**
   - Go to: https://console.aws.amazon.com
   - Sign in with your email and password

9. **Go to SES (Simple Email Service)**
   - In the search bar at top, type "SES"
   - Click "Amazon Simple Email Service"
   - Make sure you're in the **US East (N. Virginia)** region (check top right)

10. **Request production access**
    - Click "Get started" or look for "Account dashboard"
    - You'll see a notice that you're in "Sandbox mode"
    - Click "Request production access"
    - Fill out the form:
      - **Mail Type**: Transactional
      - **Website URL**: Use one of your domains (e.g., `https://company1-labs.com`)
      - **Use case description**: 
        ```
        I am setting up a custom email system for my business to receive 
        inquiries from potential customers via contact forms and respond 
        to them. I will be sending transactional replies to legitimate 
        business inquiries only. Expected volume: 100-500 emails per month.
        ```
      - **Acknowledge**: Check the box
    - Click "Submit request"

11. **Wait for approval**
    - AWS typically approves within 24-48 hours
    - You'll receive an email notification

**✅ Checkpoint**: You should have an AWS account created and SES production access requested.

---

## Step 4: Create Supabase Account (10 minutes)

### What You're Doing
Setting up a database to store all your emails.

### Instructions

1. **Go to Supabase**
   - Visit: https://supabase.com
   - Click "Start your project"

2. **Sign up with GitHub**
   - Click "Sign in with GitHub"
   - If you don't have GitHub, create one first at https://github.com
   - Authorize Supabase

3. **Create a new project**
   - Click "New Project"
   - Choose these settings:
     - **Organization**: Create new organization → "Email System"
     - **Name**: "email-database"
     - **Database Password**: Click "Generate password" and SAVE IT
     - **Region**: Choose closest to you
     - **Pricing Plan**: Free
   - Click "Create new project"

4. **Wait for database to be ready**
   - This takes 2-3 minutes
   - You'll see a loading screen

5. **Save your credentials**
   - Once ready, go to "Settings" (gear icon on left)
   - Click "API"
   - Copy and save these:
     ```
     Supabase URL: https://xxxxx.supabase.co
     Supabase Anon Key: eyJhbGc...
     Supabase Service Role Key: eyJhbGc...
     ```

**✅ Checkpoint**: You should have a Supabase project created with credentials saved.

---

## 📝 End of Day 1 Checklist

By now, you should have:
- ✅ 10 domains purchased from Namecheap
- ✅ VPS server running on Hetzner (with IP and password saved)
- ✅ AWS account created with SES production access requested
- ✅ Supabase database created

**Save all this information in a secure document!**

---

# DAY 2: Server Setup & Email Configuration

## Step 5: Connect to Your Server (15 minutes)

### What You're Doing
Logging into your VPS server so you can install the email software.

### For Windows Users:

1. **Download PuTTY**
   - Go to: https://www.putty.org
   - Download and install PuTTY

2. **Open PuTTY**
   - Run PuTTY application
   - You'll see a configuration window

3. **Connect to your server**
   - In "Host Name" field, enter your VPS IP address (from Day 1)
   - Port: 22
   - Connection type: SSH
   - Click "Open"

4. **Accept security alert**
   - First time connecting, you'll see a security alert
   - Click "Yes" to trust the server

5. **Log in**
   - Username: `root`
   - Password: [paste your root password from Day 1]
   - **Note**: When typing password, you won't see anything - this is normal!
   - Press Enter

**✅ Success**: You should see a welcome message and a command prompt like `root@mail-server:~#`

### For Mac/Linux Users:

1. **Open Terminal**
   - Press Cmd+Space, type "Terminal", press Enter

2. **Connect to server**
   - Type this command (replace with your IP):
     ```bash
     ssh root@123.45.67.89
     ```
   - Press Enter

3. **Accept fingerprint**
   - Type `yes` and press Enter

4. **Enter password**
   - Paste your root password
   - Press Enter

**✅ Success**: You should see a welcome message and a command prompt.

---

## Step 6: Install Maddy Mail Server (30 minutes)

### What You're Doing
Installing the software that will receive and store your emails.

> **💡 Note**: You'll be copying and pasting commands. Josh can help if you get stuck!

### Instructions

1. **Update the server**
   - Copy this command:
     ```bash
     apt update && apt upgrade -y
     ```
   - Right-click in PuTTY/Terminal to paste
   - Press Enter
   - Wait 2-3 minutes for it to finish

2. **Install required tools**
   - Copy and paste:
     ```bash
     apt install -y curl wget git ufw fail2ban certbot
     ```
   - Press Enter
   - Wait for installation to complete

3. **Set up firewall**
   - Copy these commands one by one:
     ```bash
     ufw allow 22/tcp
     ufw allow 25/tcp
     ufw allow 143/tcp
     ufw allow 587/tcp
     ufw allow 993/tcp
     ufw allow 80/tcp
     ufw allow 443/tcp
     ufw --force enable
     ```
   - This opens the necessary ports for email

4. **Download Maddy**
   - Copy and paste:
     ```bash
     cd /tmp
     wget https://github.com/foxcpp/maddy/releases/download/v0.7.1/maddy-0.7.1-x86_64-linux-musl.tar.zst
     ```
   - Press Enter

5. **Extract and install Maddy**
   - Copy and paste:
     ```bash
     tar -xf maddy-0.7.1-x86_64-linux-musl.tar.zst
     mv maddy /usr/local/bin/
     chmod +x /usr/local/bin/maddy
     ```

6. **Create Maddy user**
   - Copy and paste:
     ```bash
     useradd -r -s /bin/false -d /var/lib/maddy maddy
     mkdir -p /etc/maddy /var/lib/maddy
     chown -R maddy:maddy /var/lib/maddy
     ```

7. **Test Maddy installation**
   - Type:
     ```bash
     maddy -v
     ```
   - You should see version information

**✅ Checkpoint**: Maddy is installed! You should see version `0.7.1` or similar.

---

## Step 7: Configure DNS Records (45 minutes)

### What You're Doing
Telling the internet where to send emails for your domains.

> **⚠️ IMPORTANT**: You'll do this for EACH of your 10 domains. I'll show you how to do it for the first domain, then you'll repeat for the others.

### Instructions for Domain #1:

1. **Log in to Namecheap**
   - Go to: https://www.namecheap.com
   - Sign in to your account

2. **Go to domain management**
   - Click "Domain List" on the left
   - Find your first domain (e.g., `company1-labs.com`)
   - Click "Manage"

3. **Go to Advanced DNS**
   - Click the "Advanced DNS" tab

4. **Add MX Record**
   - Click "Add New Record"
   - Choose these settings:
     - **Type**: MX Record
     - **Host**: `@`
     - **Value**: `mail.company1-labs.com` (replace with your domain)
     - **Priority**: `10`
     - **TTL**: Automatic
   - Click the green checkmark to save

5. **Add A Record for mail subdomain**
   - Click "Add New Record"
   - Settings:
     - **Type**: A Record
     - **Host**: `mail`
     - **Value**: [Your VPS IP address from Day 1]
     - **TTL**: Automatic
   - Click the green checkmark

6. **Add SPF Record**
   - Click "Add New Record"
   - Settings:
     - **Type**: TXT Record
     - **Host**: `@`
     - **Value**: `v=spf1 ip4:[YOUR_VPS_IP] include:amazonses.com ~all`
       - Replace `[YOUR_VPS_IP]` with your actual IP
       - Example: `v=spf1 ip4:123.45.67.89 include:amazonses.com ~all`
     - **TTL**: Automatic
   - Click the green checkmark

7. **Add DMARC Record**
   - Click "Add New Record"
   - Settings:
     - **Type**: TXT Record
     - **Host**: `_dmarc`
     - **Value**: `v=DMARC1; p=quarantine; rua=mailto:dmarc@company1-labs.com`
       - Replace `company1-labs.com` with your domain
     - **TTL**: Automatic
   - Click the green checkmark

8. **Save changes**
   - Your DNS records are now configured!
   - **Note**: It takes 1-24 hours for DNS changes to propagate worldwide

### Repeat for All Domains

Now repeat steps 1-8 for your other 9 domains. The only thing that changes is the domain name itself.

**✅ Checkpoint**: All 10 domains should have MX, A, SPF, and DMARC records configured.

---

## Step 8: Get SSL Certificates (20 minutes)

### What You're Doing
Getting security certificates so your email connections are encrypted.

### Instructions

1. **Still connected to your server via SSH**
   - If you disconnected, reconnect using Step 5

2. **Set your hostname**
   - Replace `company1-labs.com` with your first domain:
     ```bash
     hostnamectl set-hostname mail.company1-labs.com
     ```

3. **Get SSL certificate for first domain**
   - Copy and paste (replace with your domain and email):
     ```bash
     certbot certonly --standalone -d mail.company1-labs.com --email your-email@gmail.com --agree-tos --non-interactive
     ```
   - Wait for it to complete

4. **Copy certificates to Maddy directory**
   - Copy and paste:
     ```bash
     mkdir -p /etc/maddy/certs
     cp /etc/letsencrypt/live/mail.company1-labs.com/fullchain.pem /etc/maddy/certs/
     cp /etc/letsencrypt/live/mail.company1-labs.com/privkey.pem /etc/maddy/certs/
     chown -R maddy:maddy /etc/maddy/certs
     ```

**✅ Checkpoint**: SSL certificates are installed!

---

## 📝 End of Day 2 Checklist

By now, you should have:
- ✅ Connected to your VPS server
- ✅ Installed Maddy mail server
- ✅ Configured DNS records for all 10 domains
- ✅ Obtained SSL certificates

**Tomorrow we'll configure Maddy and create your email accounts!**

---

# DAY 3: Email Account Creation & Testing

## Step 9: Configure Maddy (30 minutes)

### What You're Doing
Setting up Maddy to handle emails for all your domains.

### Instructions

1. **Create Maddy configuration file**
   - In your SSH session, type:
     ```bash
     nano /etc/maddy/maddy.conf
     ```
   - This opens a text editor

2. **Paste this configuration**
   - Copy this entire configuration:
     ```conf
     # Maddy Mail Server Configuration
     
     hostname mail.company1-labs.com
     
     tls file /etc/maddy/certs/fullchain.pem /etc/maddy/certs/privkey.pem
     
     storage.imapsql local_mailboxes {
         driver sqlite3
         dsn /var/lib/maddy/imapsql.db
     }
     
     auth.pass_table local_authdb {
         table sql_table {
             driver sqlite3
             dsn /var/lib/maddy/credentials.db
             table_name passwords
         }
     }
     
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
     
     submission tcp://0.0.0.0:587 {
         auth &local_authdb
     
         source $(local_domains) {
             deliver_to &remote_queue
         }
     }
     
     imap tcp://0.0.0.0:993 {
         auth &local_authdb
         storage &local_mailboxes
     }
     
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
     
     $(local_domains) = company1-labs.com company2-co.com company3-group.com company4-solutions.com company5-inc.com company6-llc.com company7-ventures.com company8-partners.com company9-consulting.com company10-agency.com
     $(primary_domain) = company1-labs.com
     ```

3. **IMPORTANT: Edit the configuration**
   - Replace `company1-labs.com` with your actual first domain
   - Replace all the domain names in `$(local_domains)` with your 10 actual domains
   - Use arrow keys to navigate
   - Type to edit

4. **Save the file**
   - Press `Ctrl + X`
   - Press `Y` to confirm
   - Press `Enter` to save

5. **Create systemd service**
   - Copy and paste:
     ```bash
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
     ```

6. **Start Maddy**
   - Copy and paste:
     ```bash
     systemctl daemon-reload
     systemctl enable maddy
     systemctl start maddy
     ```

7. **Check if Maddy is running**
   - Type:
     ```bash
     systemctl status maddy
     ```
   - You should see "active (running)" in green
   - Press `Q` to exit

**✅ Checkpoint**: Maddy is running!

---

## Step 10: Create Email Accounts (30 minutes)

### What You're Doing
Creating 30 email accounts (3 per domain).

### Instructions

1. **Create first email account**
   - Copy this command (replace with your domain):
     ```bash
     maddyctl creds create info@company1-labs.com
     ```
   - Press Enter
   - You'll be prompted to enter a password
   - Type a strong password (you won't see it as you type)
   - Press Enter
   - Type the password again to confirm
   - Press Enter

2. **Create second account for domain 1**
   - Repeat step 1 with:
     ```bash
     maddyctl creds create support@company1-labs.com
     ```

3. **Create third account for domain 1**
   - Repeat with:
     ```bash
     maddyctl creds create contact@company1-labs.com
     ```

4. **Save your account information**
   - In your notepad, create a list:
     ```
     Domain 1: company1-labs.com
     - info@company1-labs.com : [password]
     - support@company1-labs.com : [password]
     - contact@company1-labs.com : [password]
     ```

5. **Repeat for all 10 domains**
   - For each domain, create 3 accounts:
     - `info@[domain]`
     - `support@[domain]`
     - `contact@[domain]`
   - Save all passwords!

**✅ Checkpoint**: You should have 30 email accounts created!

---

## Step 11: Test Receiving Emails (15 minutes)

### What You're Doing
Sending a test email to make sure everything works.

### Instructions

1. **Send a test email**
   - From your personal Gmail or Outlook account
   - Send an email to: `info@company1-labs.com` (your first domain)
   - Subject: "Test Email"
   - Body: "Testing my new email system!"

2. **Wait 1-2 minutes**
   - Give the email time to arrive

3. **Check if email was received**
   - In your SSH session, type:
     ```bash
     journalctl -u maddy -f
     ```
   - You should see log entries showing the email was received
   - Press `Ctrl + C` to stop viewing logs

4. **View the email**
   - We'll set up a proper email client later
   - For now, you can check the database:
     ```bash
     sqlite3 /var/lib/maddy/imapsql.db "SELECT * FROM messages LIMIT 1;"
     ```

**✅ Checkpoint**: If you see your test email in the logs, receiving is working!

---

## 📝 End of Day 3 Checklist

By now, you should have:
- ✅ Maddy configured and running
- ✅ 30 email accounts created (3 per domain)
- ✅ Successfully received a test email

**Tomorrow we'll set up AWS SES for sending and build the dashboard!**

---

# DAY 4: AWS SES Setup & Dashboard

## Step 12: Configure AWS SES (45 minutes)

### What You're Doing
Setting up Amazon's email service so you can send replies with high deliverability.

> **Note**: By now, your AWS SES production access should be approved. Check your email for confirmation.

### Instructions

1. **Log in to AWS Console**
   - Go to: https://console.aws.amazon.com
   - Sign in

2. **Go to SES**
   - Search for "SES" in the top search bar
   - Click "Amazon Simple Email Service"
   - Make sure you're in **US East (N. Virginia)** region (top right)

3. **Verify your first domain**
   - Click "Verified identities" on the left
   - Click "Create identity"
   - Choose:
     - **Identity type**: Domain
     - **Domain**: `company1-labs.com` (your first domain)
     - **Advanced DKIM settings**: Easy DKIM
     - **DKIM signing key length**: RSA_2048_BIT
   - Click "Create identity"

4. **Add DKIM records to Namecheap**
   - AWS will show you 3 CNAME records
   - For each record:
     - Go to Namecheap → Your domain → Advanced DNS
     - Click "Add New Record"
     - Type: CNAME Record
     - Host: [copy from AWS, remove the domain part]
     - Value: [copy from AWS]
     - Click save
   - Repeat for all 3 CNAME records

5. **Wait for verification**
   - This takes 5-30 minutes
   - Refresh the page in AWS
   - When verified, you'll see a green "Verified" status

6. **Repeat for all 10 domains**
   - Go through steps 3-5 for each of your domains
   - This is tedious but important!

7. **Create SMTP credentials**
   - In AWS SES, click "SMTP settings" on the left
   - Click "Create SMTP credentials"
   - Username: `email-system-smtp`
   - Click "Create"
   - **IMPORTANT**: Download the credentials CSV file
   - Save the username and password in your notepad:
     ```
     AWS SES SMTP Username: [from CSV]
     AWS SES SMTP Password: [from CSV]
     ```

**✅ Checkpoint**: All 10 domains verified in AWS SES with SMTP credentials saved.

---

## Step 13: Set Up Supabase Database (20 minutes)

### What You're Doing
Creating tables in your database to store emails.

### Instructions

1. **Log in to Supabase**
   - Go to: https://supabase.com
   - Sign in
   - Click on your "email-database" project

2. **Open SQL Editor**
   - Click "SQL Editor" on the left sidebar
   - Click "New query"

3. **Create email accounts table**
   - Copy and paste this SQL:
     ```sql
     create table email_accounts (
       id uuid default gen_random_uuid() primary key,
       email text unique not null,
       domain text not null,
       password_hash text not null,
       created_at timestamptz default now()
     );
     ```
   - Click "Run" (or press Ctrl+Enter)

4. **Create emails table**
   - Copy and paste:
     ```sql
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
     
     create index idx_emails_account on emails(account_id);
     create index idx_emails_received on emails(received_at desc);
     ```
   - Click "Run"

5. **Verify tables were created**
   - Click "Table Editor" on the left
   - You should see `email_accounts` and `emails` tables

**✅ Checkpoint**: Database tables created successfully!

---

## Step 14: Deploy Email Management API (30 minutes)

### What You're Doing
Deploying a web application that lets you view and manage your emails.

> **Note**: Josh will help you with this part as it involves some coding.

### Instructions

1. **Ask Josh to share the API code**
   - Josh has prepared a FastAPI application
   - He'll share it via GitHub or directly

2. **Deploy to Railway**
   - Go to: https://railway.app
   - Sign in with GitHub
   - Click "New Project"
   - Click "Deploy from GitHub repo"
   - Select the email API repository
   - Railway will automatically deploy

3. **Add environment variables**
   - In Railway, go to your project
   - Click "Variables"
   - Add these variables (get values from your notepad):
     ```
     SUPABASE_URL=[your Supabase URL]
     SUPABASE_KEY=[your Supabase service role key]
     AWS_ACCESS_KEY_ID=[AWS SMTP username]
     AWS_SECRET_ACCESS_KEY=[AWS SMTP password]
     MADDY_HOST=[your VPS IP]
     MADDY_PORT=993
     ```
   - Click "Deploy"

4. **Get your API URL**
   - In Railway, go to "Settings" → "Domains"
   - Click "Generate Domain"
   - Copy the URL (e.g., `https://email-api-production-abc123.up.railway.app`)
   - Save it in your notepad

**✅ Checkpoint**: API is deployed and running!

---

## Step 15: Test the Complete System (20 minutes)

### What You're Doing
Making sure everything works end-to-end.

### Instructions

1. **Test receiving**
   - Send an email to one of your addresses
   - Wait 1-2 minutes
   - Check your API dashboard to see if it appears

2. **Test sending**
   - Use the API to send a reply
   - Check if it arrives in your personal email
   - Check spam folder if you don't see it

3. **Check deliverability**
   - Go to: https://www.mail-tester.com
   - Send a test email to the address they provide
   - Check your spam score (should be 8/10 or higher)

**✅ Checkpoint**: You can send and receive emails successfully!

---

## 📝 Final Checklist

Congratulations! You should now have:
- ✅ 10 custom domains
- ✅ 30 email accounts (3 per domain)
- ✅ Working email receiving (Maddy)
- ✅ Working email sending (AWS SES)
- ✅ Database storing all emails (Supabase)
- ✅ API to manage everything (Railway)

**Total monthly cost: ~$16-20**

---

## 🆘 Troubleshooting

### Problem: Emails not being received

**Solution:**
1. Check DNS records are correct in Namecheap
2. Wait 24 hours for DNS to propagate
3. Check Maddy logs: `journalctl -u maddy -f`
4. Ask Josh for help!

### Problem: Sent emails going to spam

**Solution:**
1. Check SPF, DKIM, DMARC records
2. Use mail-tester.com to diagnose issues
3. Make sure AWS SES domains are verified
4. Wait a few days for domain reputation to build

### Problem: Can't connect to server

**Solution:**
1. Make sure you're using the correct IP address
2. Check that port 22 is open in Hetzner firewall
3. Try resetting the root password in Hetzner console

### Problem: Maddy won't start

**Solution:**
1. Check configuration file for typos: `nano /etc/maddy/maddy.conf`
2. Check logs: `journalctl -u maddy -n 50`
3. Ask Josh to review the configuration

---

## 📞 Getting Help

**If you get stuck:**
1. Take a screenshot of the error
2. Note which step you're on
3. Send to Josh with the error message
4. Don't worry - this is complex stuff and it's normal to need help!

---

## 🎉 Next Steps

Once everything is working:
1. Start using your email addresses for business
2. Monitor the dashboard daily
3. Keep track of which emails are performing well
4. Consider adding more domains as needed

**Great job completing this project! You now have your own email infrastructure! 🚀**
