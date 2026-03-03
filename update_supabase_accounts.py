#!/usr/bin/env python3
"""
Script to update Supabase email_accounts table
- Removes old accounts: support@getcopyculture.com, contact@getcopyculture.com
- Adds new accounts: josh@getcopyculture.com, joshua@getcopyculture.com, josh.andrews@getcopyculture.com
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/gene/EmailServer/email_api/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Supabase credentials not found in .env file")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔄 Connecting to Supabase...")

# Accounts to remove
old_accounts = [
    "support@getcopyculture.com",
    "contact@getcopyculture.com"
]

# Accounts to add
new_accounts = [
    {"email": "josh@getcopyculture.com", "domain": "getcopyculture.com"},
    {"email": "joshua@getcopyculture.com", "domain": "getcopyculture.com"},
    {"email": "josh.andrews@getcopyculture.com", "domain": "getcopyculture.com"}
]

print("\n📋 Step 1: Removing old accounts...")
for email in old_accounts:
    try:
        result = supabase.table("email_accounts").delete().eq("email", email).execute()
        print(f"  ✅ Deleted: {email}")
    except Exception as e:
        print(f"  ⚠️  Could not delete {email}: {e}")

print("\n📋 Step 2: Adding new accounts...")
for account in new_accounts:
    try:
        # Check if account already exists
        existing = supabase.table("email_accounts").select("*").eq("email", account["email"]).execute()
        
        if existing.data:
            print(f"  ℹ️  Account already exists: {account['email']}")
        else:
            # Insert new account
            result = supabase.table("email_accounts").insert({
                "email": account["email"],
                "domain": account["domain"]
            }).execute()
            print(f"  ✅ Added: {account['email']}")
    except Exception as e:
        print(f"  ❌ Error adding {account['email']}: {e}")

print("\n📋 Step 3: Verifying final state...")
try:
    all_accounts = supabase.table("email_accounts").select("email").eq("domain", "getcopyculture.com").execute()
    print("\n✅ Current accounts in Supabase:")
    for account in all_accounts.data:
        print(f"  - {account['email']}")
except Exception as e:
    print(f"  ❌ Error fetching accounts: {e}")

print("\n✅ Done! Supabase database has been updated.")
