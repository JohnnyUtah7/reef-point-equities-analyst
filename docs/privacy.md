# Equities Valuation — Privacy Policy

Effective November 14, 2026.

## Who operates the plugin

Equities Valuation is published by Chris Miller under the Reef Point Capital name ("we" or "Reef Point"). This policy covers our plugin and hosted EDGAR lookup service at `reef-point-edgar.reef-point.workers.dev`. Contact: [realchrismiller@gmail.com](mailto:realchrismiller@gmail.com), subject "Equities Valuation privacy".

We provide public-company research tools. We do not operate user accounts, sell personal information, build advertising profiles, or use plugin requests to train our own AI models. You do not need to provide your name, email, brokerage credentials, holdings, payment information or other private financial information to use the EDGAR tools. Technical processing described below is still necessary to answer a lookup.

## Data received and purposes

### EDGAR tool requests and responses

The host application sends the selected tool name, arguments and protocol information to our server. The current tools are:

| Tool | Requested inputs | Returned information | Purpose |
| --- | --- | --- | --- |
| `company_lookup` | Stock ticker | Public company name, ticker, CIK, exchange and industry classification | Identify the requested public company |
| `recent_filings` | Stock ticker and optional result limit (1–40) | Public filing types, filing/report dates, accession numbers and SEC document URLs | Retrieve recent filings |
| `company_facts` | Stock ticker | As-reported public revenue, share, cash and debt facts, units, periods and filing citations | Retrieve financial evidence |

Protocol messages may also contain a request identifier, protocol version, client name/version and connection capabilities. We use protocol fields to process calls, return results and handle errors. A request identifier is not a Reef Point account identifier.

The EDGAR service does not request a full conversation, uploaded documents, portfolio or generated research report. However, any text the host or user includes in a tool request reaches the server while it processes that request. Do not place personal information or secrets in ticker fields. Invalid input may be included in an error returned to the requesting host. We do not use unexpected personal information for another purpose or intentionally save it in an application database.

### Hosting and technical metadata

Cloudflare hosts the service and processes incoming connections, including the source IP address, HTTP headers, request URL, timestamps, response status and performance/security information. When your host makes the request on your behalf, the source IP may belong to the host rather than your device. This processing delivers responses, operates the service, diagnoses failures and protects against abuse.

Our server code does not write request bodies, tickers or responses to an application log or maintain individual research histories. Cloudflare's platform-level metrics, diagnostic logging (if enabled) and security processing are separate from application storage. We do not use these services for advertising or behavioral profiling.

### Support correspondence

If you contact us by email or through GitHub, we receive the address or account information and content you choose to send. We use it to respond, investigate issues and handle privacy requests. GitHub issues are public; send private questions by email and do not include credentials or sensitive financial information.

## Who receives data

- **Your host application, including OpenAI when used through ChatGPT or Codex:** sends tool requests and receives results and errors. Its own policies and your account settings govern conversations, files and tool history.
- **Cloudflare:** processes requests and responses to host, secure and operate the EDGAR service.
- **U.S. Securities and Exchange Commission:** receives requests for public company/filing resources. Our server resolves a ticker to a company identifier and requests SEC resources; it does not forward the incoming chat, request body or client headers to the SEC. It identifies itself using Reef Point's operator contact, not an end user's email.
- **GitHub and our email provider:** process documentation visits, repository issues and support correspondence when you use those channels.
- **Other services you choose:** if your host saves a workbook, presentation or research site to Drive, Slides, Sites or another connected service, that destination receives the content needed for your requested action under its own permissions and policies. Those generated files are not uploaded to the EDGAR endpoint as part of its three lookup tools.
- **Authorities or professional advisers:** information we actually hold may be disclosed when required by law or necessary to address abuse, security incidents or legal claims.

We do not sell or rent personal information, share it for targeted advertising, or send research requests to data brokers. Our server does not call an advertising or AI-training service.

## Retention

| Category | Retention |
| --- | --- |
| Tool request bodies, protocol fields and individual results | Processed transiently to answer the call; our application does not intentionally persist a per-user copy or history after processing. This is not a promise that hosting infrastructure or your host retains nothing. |
| Cached public SEC responses | Cached by SEC resource URL with a one-hour freshness period (`max-age=3600`), after which the service requests a fresh response when needed. Entries may be evicted sooner. The cache contains public SEC data, not a user's prompt or identity; expiration is not a guarantee of physical erasure from provider infrastructure. |
| Rate-limit state | A shared next-request timestamp is held in runtime memory, not a per-user profile. The application does not write user data to durable-object storage. |
| Hosting diagnostics and metrics | Where enabled, Cloudflare Workers Logs currently provides three-day retention on its free plan and up to seven days on its paid plan. Standard Workers analytics provides a rolling view of up to 30 days. These are provider-managed operational records, not a Reef Point research-history database. Cloudflare's separate security processing is subject to its own privacy policy and service terms. |
| Support email and issues | Retained for the duration of the support/privacy request and any necessary follow-up, dispute or legal obligation. You may request deletion of correspondence we control. Public GitHub issue/history copies and email-provider backups can follow the provider's own retention rules. |
| Conversations, generated files and third-party exports | Retained by your host, device or selected destination according to its settings and policy; uninstalling this plugin does not automatically delete those copies. |

## Your choices and controls

- Disable or disconnect the plugin/EDGAR server in your host to stop future calls. There is no Reef Point account to close.
- Send only public ticker symbols and the optional result limit to the EDGAR tools. Use your host's tool controls to review or decline calls where available.
- Use the host's deletion and data controls for conversations and tool history. Delete local outputs yourself or use the destination service's file deletion/sharing controls.
- Email [realchrismiller@gmail.com](mailto:realchrismiller@gmail.com) to ask about, access, correct or delete personal information we hold, or to raise a privacy concern. We may ask for proportionate information to verify and locate a request. We cannot retrieve a per-user research history that our application does not keep, or delete another provider's records directly. Where relevant, we will explain these limits and direct you to that provider.
- You may also have privacy rights under the law where you live, including the right to contact your data-protection authority.

## Local execution, cookies and external services

If you use the optional local `edgartools` workflow, it runs on your machine and sends the `EDGAR_IDENTITY` you configure to the SEC as its user-agent contact. Do not put authentication secrets in that setting. Local files and their deletion remain under your control.

Our EDGAR service does not set tracking cookies. We add no advertising pixels to the public repository's documentation. GitHub, Cloudflare and the host application may use their own technologies under their policies. Information may be processed in countries where these providers operate; we do not promise that all processing is confined to one country.

Provider information: [OpenAI privacy policy](https://openai.com/policies/privacy-policy/), [Cloudflare privacy policy](https://www.cloudflare.com/privacypolicy/), [Cloudflare Workers Logs](https://developers.cloudflare.com/workers/observability/logs/workers-logs/), [Cloudflare Workers metrics](https://developers.cloudflare.com/workers/observability/metrics-and-analytics/), [GitHub privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement), and [SEC privacy policy](https://www.sec.gov/privacy).

## Changes and contact

We will update this page and its effective date when our practices change. Material changes to the data requested or its use will also be reflected in the plugin's disclosures. For private privacy/support requests, contact Chris Miller at [realchrismiller@gmail.com](mailto:realchrismiller@gmail.com).
