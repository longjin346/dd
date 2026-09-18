# Slack thread export — Pricing config (`foodSaverOptionDiscount`)

| Field | Value |
|---|---|
| Permalink | https://grab.slack.com/archives/C04KSAY0K/p1787642328064969 |
| Channel ID | `C04KSAY0K` |
| Parent TS | `1787642328.064969` |
| Messages | 1 parent + 25 replies |
| Exported | 2026-09-17 |

Mentions kept as `@username`. Full URLs preserved. Reactions listed under the message.

---

## Parent

**jomil.villareal** · jomil.villareal@grabtaxi.com · **2026-08-25 15:18:48 +08** · ts `1787642328.064969`

Hi @randy.tedjakusuma / @pricing-team, may we proceed with this approval request from @rahadiyan.wisesa

Justification Reason :applying saver discount for selected MEX (Kalbe & Wardah) for tactical purpose  
Approval links :  
https://experiments.grab.com/t/variables/foodSaverOptionDiscount/rollout/approve-request/455492?env=prd

JIRA: [Approval_Request - ID for Mart](https://grabtaxi.atlassian.net/browse/TECHOPS-117402)

---

## Replies

### 1. **cui.ju** · cui.ju@grabtaxi.com · **2026-08-25 15:20:10 +08** · ts `1787642410.610609`

please inform the respective eng PIC and get approval from them first

### 2. **jomil.villareal** · jomil.villareal@grabtaxi.com · **2026-08-25 15:21:15 +08** · ts `1787642475.273729`

@cui.ju if @randy.tedjakusuma is on leave, who can we contact in their place?

### 3. **jomil.villareal** · jomil.villareal@grabtaxi.com · **2026-08-25 15:21:52 +08** · ts `1787642512.924959`

Product is from under Fulfillment

### 4. **cui.ju** · cui.ju@grabtaxi.com · **2026-08-25 15:22:33 +08** · ts `1787642553.193629`

@arpit.goel could you help to check?

### 5. **arpit.goel** · arpit.goel@grabtaxi.com · **2026-08-25 15:23:19 +08** · ts `1787642599.500519`

Can u share more on the tactical reasons?

### 6. **rahadiyan.wisesa** · rahadiyan.wisesa@grabtaxi.com · **2026-08-25 15:26:40 +08** · ts `1787642800.623149`

- **Strong brand visibility, but demand is constrained by pickup-point accessibility.**
- Many PAX are located far from Kalbe & Wardah pickup points, creating delivery friction as it’s too expensive
- **Free delivery helps remove this barrier and unlock incremental demand beyond the existing pickup-point catchment.**

### 7. **cui.ju** · cui.ju@grabtaxi.com · **2026-08-25 16:01:04 +08** · ts `1787644864.581729`

@arpit.goel is the above clarification ok to approve?

### 8. **rahadiyan.wisesa** · rahadiyan.wisesa@grabtaxi.com · **2026-08-25 16:27:23 +08** · ts `1787646443.116449`

fyi @moch.zulfa @rangga.pratama

### 9. **arpit.goel** · arpit.goel@grabtaxi.com · **2026-08-25 17:06:51 +08** · ts `1787648811.720149`

Can you share more about this merchant group?  
How will this be maintained going forward? It's really hard to know how the mex are selected and 6 months later if this saver fare is still relevant to this group.

### 10. **moch.zulfa** · moch.zulfa@grabtaxi.com · **2026-08-25 17:11:45 +08** · ts `1787649105.342929`

The merchant group is prioritized by the ID business team based on our strategic priorities. In this case, these merchants are important for enabling and maintaining our e-commerce partnerships with FMCG principals.

For this group, having a more competitive Saver fare is one of the key requirements to drive sufficient sales volume and make the partnership sustainable.

Going forward, the merchant list will continue to be reviewed and maintained by the business team based on partnership needs and merchant performance. So if the relevance changes over time, we can adjust the group accordingly rather than treating this as a fixed merchant setup.

### 11. **arpit.goel** · arpit.goel@grabtaxi.com · **2026-08-25 17:29:37 +08** · ts `1787650177.927519`

Understand. I am worried about losing the context with time.  
Putting into merchant group with no documentation will have that problem.

### 12. **moch.zulfa** · moch.zulfa@grabtaxi.com · **2026-08-25 17:43:06 +08** · ts `1787650986.529469`

What do you mean with no documentation?

### 13. **arpit.goel** · arpit.goel@grabtaxi.com · **2026-08-25 18:18:09 +08** · ts `1787653089.376769`

Since there is no governance on the grabx group - no approvals/documentation/freshness check there are chances of mistakes.  
If 6 months down the line, we trace that some merchants are wrongly in the group, we have no documentation on knowing what the right set of merchants are, how they are derived.  
CC: @yoel.frans @albert.lim @renrong.weng

**Reactions:** `+1` (2)

### 14. **albert.lim** · albert.lim@grabtaxi.com · **2026-08-26 08:50:06 +08** · ts `1787705406.762369`

@long.jin is it possible to use your decision capture tool to record this context?

### 15. **albert.lim** · albert.lim@grabtaxi.com · **2026-08-26 08:51:50 +08** · ts `1787705510.607799`

Also @sengkeong.ho what is our principle here in terms of balancing FR during crunch?

### 16. **Slackbot** · **2026-08-26 08:51:51 +08** · ts `1787705511.434269`

Heart, Hunger, Honour, Humility

### 17. **sengkeong.ho** · sengkeong.ho@grabtaxi.com · **2026-08-26 08:54:37 +08** · ts `1787705677.072149`

For mart/ecomm - we are trying to grow by pushing more fare certainty on longer SLA service types, in line with competition. When there is a supply crunch, we can use the longer SLA to batch more aggressively

### 18. **long.jin** · long.jin@grabtaxi.com · **2026-08-26 08:55:04 +08** · ts `1787705704.807739`

Yes @albert.lim , is all the information source in this thread ? Or do we have additional zoom transcripts, decks etc

### 19. **sengkeong.ho** · sengkeong.ho@grabtaxi.com · **2026-08-26 08:55:14 +08** · ts `1787705714.920629`

Can I understand the concern about documentation further? Handling mex specific pricing configs on ExP is not a new practice. If it helps, can we set up an wiki page to document this for all markets?

### 20. **albert.lim** · albert.lim@grabtaxi.com · **2026-08-26 08:57:51 +08** · ts `1787705871.916779`

@sengkeong.ho ya that helps

Maybe to provide some context; the team is trying to cleanup pricing configs, many of them legacy that were set up by ops long time ago

And now today we're stuck in a situation where we see the configs, but have no idea what it is for and why, which makes them hard to remove or find the owner/requestor.

So part of solving that problem is to properly document the incoming new ones, so that we can fix this.

### 21. **sengkeong.ho** · sengkeong.ho@grabtaxi.com · **2026-08-26 08:59:07 +08** · ts `1787705947.022279`

Ok got it. @rahadiyan.wisesa lets set up a wiki page for this variable and document all the configs here? and then find a way to link this variable to this wiki so this becomes the central source of truth

### 22. **albert.lim** · albert.lim@grabtaxi.com · **2026-08-26 08:59:27 +08** · ts `1787705967.131299`

@long.jin ya should be, trying to extract more context atm

### 23. **albert.lim** · albert.lim@grabtaxi.com · **2026-08-26 09:02:14 +08** · ts `1787706134.277719`

Pointing out another thing, in crunch even if you try to batch, if it's an LO it won't be batchable, and Mart orders can be quite large

So the only real FR lever you have is pricing and visibility, messing with this permanently can and will likely result in poorer FR, we're also combining both levers under DMS-Go+

Fyi @zhikang.wong on this eComm decision

**Reactions:** `ack` (1)

### 24. **sengkeong.ho** · sengkeong.ho@grabtaxi.com · **2026-08-26 09:06:13 +08** · ts `1787706373.647389`

Yes fair - we need larger capacity vehicles but also have to prove demand thesis, so its kinda chicken and egg. Also, cos of the longer SLA, the bet here is the crunch will clear closer to allocation time. Not ideal but our interim stopgap is to use mex ZFF and correct for dax EAR by overpaying for these jobs. Anyways these are ecomm with small vol & higher AOV, so I guess we can take some risks on both FF & margins haha.

**Reactions:** `+1` (2)

### 25. **arpit.goel** · arpit.goel@grabtaxi.com · **2026-08-26 23:23:54 +08** · ts `1787757834.535809`

Hey All  
Thanks for sharing these inputs.  
I have documented the thread here - [foodSaverOptionDiscount](https://grabtaxi.atlassian.net/wiki/spaces/FSTF/pages/2341437752/foodSaverOptionDiscount)  
@sengkeong.ho @moch.zulfa @rangga.pratama - Would need your help to add in the logic to recreate the merchant list - Is it based on a SQL? Or based on some partnerships?

Also linked Confluence page card: [foodSaverOptionDiscount](https://grabtaxi.atlassian.net/wiki/spaces/FSTF/pages/2341437752/foodSaverOptionDiscount) · Owned by: Arpit Goel
