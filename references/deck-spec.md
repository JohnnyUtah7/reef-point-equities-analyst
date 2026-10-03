# Deck spec

Master: `assets/house-template.pptx` (16:9 generated chrome — not a Marketing Futures export).  
Logo: `assets/rpc-logo.png`.  
Official path: `skills/pptx-to-google-slides`. Never Zapier. Never `gws`.

## Canvas

- 13.333 in × 7.5 in. Margins 0.55 in.
- Type: Calibri / Arial (or Open Sans if embedded).
- Fill: `#FFFFFF` field, `#0A0A0A` ink, `#6B7280` secondary, `#B91C1C` downside, `#047857` upside.

## Chrome

**Cover:** white, logo centered, optional ticker + date under the mark. No header, no slide number.  
**Interior:** takeaway line, slide number bottom-left, proprietary footer bottom-right, small mark top-right if payload allows.

## 10-slide spine

1. Cover  
2. Agenda  
3. Business / model  
4. Thesis pillars (claim + kill)  
5. Financial snapshot  
6. Football field (bars; circular dashed)  
7. Load-bearing method (usually DCF)  
8. Risks + killing conditions  
9. Catalysts  
10. Recommendation = memo rating + disclaimer  

Football field is shapes (low–high bar, mid tick, last-print line), not a table pretending to be a field.

If Drive `create_file` overflows, shrink extras — **do not strip the cover logo** as the first resort. Local PPTX still counts if Drive 401.
