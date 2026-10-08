# Free domain + business email for OrgMind

Target: domain `orgmind.is-a.dev`, mailbox `hello@orgmind.is-a.dev`. Cost: $0.

## 1. Get the free domain (is-a.dev)
1. Push this repo to GitHub as `orgmind` (public).
2. Fork https://github.com/is-a-dev/register.
3. Add `domains/orgmind.json`:
   ```json
   {
     "owner": { "username": "<your-github-username>", "email": "davision.hq@gmail.com" },
     "records": {
       "CNAME": "<your-github-username>.github.io",
       "MX": ["mx.zoho.eu", "mx2.zoho.eu", "mx3.zoho.eu"],
       "TXT": ["zoho-verification=<code from step 2>", "v=spf1 include:zoho.eu ~all"]
     }
   }
   ```
   (Use `zoho.com` hosts instead of `zoho.eu` if Zoho puts your account in the US data centre.)
4. Open a pull request. Read the repo's rules first; it requires a real project page.

Fallback: `orgmind.eu.org` (free at https://nic.eu.org, slower approval), or a ~$10/yr `.com` via Cloudflare Registrar, which looks more credible to investors.

## 2. Free business mailbox (Zoho Mail Forever Free: up to 5 users)
1. Sign up at https://www.zoho.com/mail/ → "Forever Free" plan → "Add an existing domain" → `orgmind.is-a.dev`.
2. Copy the TXT verification code into the PR above (or a follow-up PR).
3. Create `hello@`, then add the DKIM TXT record Zoho gives you (`zmail._domainkey`).
4. Add DMARC: TXT on `_dmarc` → `v=DMARC1; p=none; rua=mailto:hello@orgmind.is-a.dev`.

Alternative without a mailbox: Cloudflare Email Routing (forward to Gmail) + Gmail "Send mail as" via Zoho/Brevo SMTP.

## 3. Project page
Enable GitHub Pages on the repo (root `README.md` is enough) so the domain shows the project.
