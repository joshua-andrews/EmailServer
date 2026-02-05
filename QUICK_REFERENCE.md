# Email System Quick Reference

## 🔑 Credentials Template

**Save this information as you go through the setup!**

### Domains
```
1. ____________________
2. ____________________
3. ____________________
4. ____________________
5. ____________________
6. ____________________
7. ____________________
8. ____________________
9. ____________________
10. ____________________
```

### VPS Server
```
Provider: Hetzner
IP Address: ____________________
Root Password: ____________________
```

### AWS SES
```
SMTP Username: ____________________
SMTP Password: ____________________
```

### Supabase
```
Project URL: ____________________
Anon Key: ____________________
Service Role Key: ____________________
```

### Railway
```
API URL: ____________________
```

---

## 📋 Daily Checklist

### Day 1
- [ ] Purchase 10 domains from Namecheap
- [ ] Rent VPS from Hetzner
- [ ] Create AWS account
- [ ] Request AWS SES production access
- [ ] Create Supabase account

### Day 2
- [ ] Connect to VPS via SSH
- [ ] Install Maddy mail server
- [ ] Configure DNS for all 10 domains
- [ ] Get SSL certificates

### Day 3
- [ ] Configure Maddy
- [ ] Create 30 email accounts
- [ ] Test receiving emails
- [ ] Verify all domains

### Day 4
- [ ] Configure AWS SES
- [ ] Add DKIM records
- [ ] Set up Supabase database
- [ ] Deploy API to Railway
- [ ] Test complete system

---

## 🆘 Emergency Contacts

**If stuck, contact Josh with:**
1. Screenshot of error
2. Which step you're on
3. What you tried already

---

## 📊 Cost Tracking

| Item | Monthly Cost |
|------|--------------|
| VPS (Hetzner) | $5 |
| Domains (10) | $10 |
| AWS SES | $1-5 |
| Railway | $0 (free tier) |
| Supabase | $0 (free tier) |
| **Total** | **~$16-20** |

---

## 🔗 Important Commands

### Check Maddy Status
```bash
systemctl status maddy
```

### View Maddy Logs
```bash
journalctl -u maddy -f
```

### Create Email Account
```bash
maddyctl creds create email@domain.com
```

### Restart Maddy
```bash
systemctl restart maddy
```

---

**Keep this file handy during setup!**
