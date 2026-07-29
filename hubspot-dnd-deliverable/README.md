# être PROF — HubSpot DnD Email Package

Portable **Design Manager** source package for 5 editable HubSpot marketing emails.

## Important (read before import)

This is **not** a Marketplace website theme, and it is **not** imported via Theme Settings.

HubSpot email drag-and-drop templates + custom EMAIL modules must be uploaded into the **Design Manager / developer file system**.

Official constraints used:
- Exactly **one** `dnd_area` per email template
- Custom modules with `content_types: ["EMAIL"]`
- No `module.css` / `module.js` for email modules
- Required CAN-SPAM tokens in footer
- Preview text field in each template

## Requirements

- Marketing Hub **Professional** or **Enterprise**
- Design Manager / Design tools permission
- HubSpot CLI recommended (`npm i -g @hubspot/cli`)

## Package contents

```text
etreprof-email-dnd/
  templates/                 # 5 coded email templates
  modules/*.module/          # editable EMAIL modules
  images/ icons/             # default assets
```

## Install (recommended)

1. Extract `etreprof-email-dnd.zip` if needed.
2. Authenticate CLI: `hs account auth`
3. Upload:

```bash
hs cms upload etreprof-email-dnd etreprof-email-dnd
```

4. In HubSpot: **Marketing → Email → Create email → Regular**
5. Select one of the uploaded templates (label starts with `être PROF —`)
6. Edit modules in the visual editor sidebar
7. Send a test email and verify Outlook / Gmail / Apple Mail

## ZIP / API alternative

A ZIP alone is **not** a one-click Theme Settings import.

If using HubSpot Source Code API:
1. Upload the ZIP into the developer file system
2. Call the extract endpoint for that ZIP path
3. Publish templates/modules in Design Manager

## Editable modules

- `email_header` — logo / paddings
- `email_hero` — hero image, badges, heading, body, CTA
- `email_content_block` — reassurance / incentive / partner
- `email_resource_card` — newsletter resource rows
- `email_workshop_card` — workshop/event cards
- `email_quote` — quote CTA
- `email_lesson_card` — lesson split card
- `email_steps` — numbered steps
- `email_feature_card` — welcome feature rows
- `email_cta` — solid CTA band
- `email_password` — password reset content
- `email_footer` — socials + required unsubscribe/address tokens

## Personalization

Where relevant, greeting uses:

`{{ contact.firstname|default('Prénom') }}`

Replace password CTA URL with your live reset token/link before sending.

## Validation after upload

- Modules appear under email editor / More
- Sections can be reordered, removed, duplicated
- Images resolve
- Footer shows company address + unsubscribe links from account settings
