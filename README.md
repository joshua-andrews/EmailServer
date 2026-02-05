# EmailServer

Custom email infrastructure for managing multiple domains and email accounts.

## 📚 Documentation

- **[README.md](README.md)** - Complete setup guide for Genesis (start here!)
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Cheat sheet and credentials template
- **[technical_plan.md](technical_plan.md)** - Technical architecture details

## 🎯 Project Overview

**Goal**: Set up custom email infrastructure for 10 domains with 30 email accounts (3 per domain)

**What We're Building:**
- Custom email receiving server (Maddy on VPS)
- High-deliverability sending (AWS SES)
- Email storage database (Supabase)
- Management API (Railway)

**Cost**: ~$16-20/month  
**Timeline**: 3-4 days

## 🚀 Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/joshua-andrews/EmailServer.git
   cd EmailServer
   ```

2. Open `README.md` and follow the day-by-day instructions

3. Use `QUICK_REFERENCE.md` to track your progress and save credentials

## 📊 What You'll Have

After completing the setup:
- ✅ 10 custom domains
- ✅ 30 email addresses (info@, support@, contact@ for each domain)
- ✅ Automated email receiving
- ✅ High-deliverability sending
- ✅ Dashboard to view all emails

## 🔗 Services Used

- [Hetzner Cloud](https://www.hetzner.com/cloud) - VPS hosting ($5/month)
- [Namecheap](https://www.namecheap.com) - Domain registration (~$10/month for 10 domains)
- [AWS SES](https://aws.amazon.com/ses/) - Email sending (~$1-5/month)
- [Supabase](https://supabase.com) - Database (free tier)
- [Railway](https://railway.app) - API hosting (free tier)

## 📞 Support

If you get stuck:
1. Check the troubleshooting section in README.md
2. Review QUICK_REFERENCE.md for common commands
3. Contact Josh with screenshots and error details

---

**Maintained By**: Josh & Genesis  
**Last Updated**: February 5, 2026
