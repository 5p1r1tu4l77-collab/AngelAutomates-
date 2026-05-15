# Make.com automation blueprints

Make.com's free tier doesn't expose an API to create scenarios remotely (that's gated to Core plan, $9/mo). So we ship **step-by-step recipes** instead of importable JSON.

**See `docs/MAKE-COM-PLAYBOOK.md`** for the full recipes. Two scenarios chosen to fit the free-tier ceiling (2 active, 1k ops/month):

1. **Gmail → GitHub** — when a cold-email reply lands, fire `gmail-reply-received` event into the repo so `reply-triage` runs only when there's actual work.
2. **Cal.com booking → GitHub** — when a discovery call books, fire `calendar-booking-created` event so `sales-ops` pre-stages the contract before the call.

Each recipe is ~10 minutes to build in the Make UI. The GitHub side (workflows that catch the events) is shipped in this commit.

## If you outgrow Make's free tier

| Volume | Recommended path |
|--------|------------------|
| ≤ 1k ops/mo (current) | Make.com free |
| 1k–10k ops/mo | Make.com Core ($9/mo) — easiest upgrade |
| 10k+ ops/mo | n8n self-hosted on a $5/mo VPS — unlimited |
| Webhook-receivers only | Cloudflare Workers free (100k req/day forever) |

`docs/AUTOMATION-LAYER.md` (next commit) compares the four paths in detail.
