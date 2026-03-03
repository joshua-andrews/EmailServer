#!/usr/bin/env python3
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv('/Users/gene/EmailServer/email_api/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERROR: Supabase credentials not found")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

domains = [
    "usecopyculture.com", "trycopyculture.com", "joincopyculture.com",
    "joshs-blog.com", "joshs-art.com", "joshs-computers.com",
    "joshs-music.com", "joshs-anime.com", "joshs-photography.com"
]

users = ["josh", "joshua", "josh.andrews"]

print("🔄 Syncing 27 new accounts to Supabase...")

count = 0
for domain in domains:
    for user in users:
        email = f"{user}@{domain}"
        try:
            # Check if exists
            existing = supabase.table("email_accounts").select("*").eq("email", email).execute()
            if not existing.data:
                supabase.table("email_accounts").insert({
                    "email": email,
                    "domain": domain
                }).execute()
                print(f"  ✅ Added: {email}")
                count += 1
            else:
                print(f"  ℹ️  Exists: {email}")
        except Exception as e:
            print(f"  ❌ Error {email}: {e}")

print(f"\n✅ Done! {count} accounts added to Supabase.")
