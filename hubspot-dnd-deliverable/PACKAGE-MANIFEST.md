# Package manifest

## Templates

| File | Label |
|---|---|
| templates/email-01-survey.html | etre PROF - Barometre |
| templates/email-02-newsletter.html | etre PROF - Infolettre |
| templates/email-03-lesson.html | etre PROF - Activation |
| templates/email-04-password.html | etre PROF - Transactionnel |
| templates/email-05-welcome.html | etre PROF - Bienvenue |

## Modules

| Module | Purpose |
|---|---|
| modules/email_header.module | Logo header |
| modules/email_hero.module | Hero / scoop / intro CTA |
| modules/email_content_block.module | Text sections |
| modules/email_resource_card.module | Resource cards |
| modules/email_divider_spacer.module | Divider / adjustable spacing |
| modules/email_workshop_card.module | Workshop cards |
| modules/email_quote.module | Quote section |
| modules/email_lesson_card.module | Lesson card |
| modules/email_steps.module | Numbered steps |
| modules/email_feature_card.module | Feature cards |
| modules/email_cta.module | CTA band |
| modules/email_password.module | Password reset |
| modules/email_footer.module | Footer + CAN-SPAM |

## Notes

- Default visual content matches the approved flat HTML emails.
- Hero scoop overlap + badge seam restored to match Figma flats.
- DnD email grid minimum width is 624px; original 600px content is centered inside.
- Resource/workshop/feature card CTAs are available but off by default (match approved design).
- Final portal preview/test is still required by the client after `hs cms upload`.
- Password reset CTA URL must be replaced with the live HubSpot reset link before send.
