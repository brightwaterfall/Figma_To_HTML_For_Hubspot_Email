être PROF — HubSpot HTML Email Templates
========================================

Project overview
----------------
Production-ready, HubSpot-compatible HTML emails converted from the Figma
Emailify file (être PROF / Buffer Emailify Template community base).

Each email is a self-contained 600px table-based HTML file with inline CSS,
Outlook VML button fallbacks, and mobile media queries.

Templates
---------
  index.html     Local preview hub (not for HubSpot import)
  email-01.html  Feedback survey — "On construit la suite avec toi."
  email-02.html  Newsletter — "L'essentiel pour ta classe"
  email-03.html  Activation — "Ta prochaine séance, prête en un instant."
  email-04.html  Password reset — "Nouveau mot de passe"
  email-05.html  Welcome — "Bienvenue dans ta nouvelle salle des profs"

Design width: 600px (Figma source of truth)


How to preview locally
----------------------
  python -m http.server 8765
  Open http://127.0.0.1:8765/


How to import into HubSpot
--------------------------
1. Upload all files from /images and /icons to HubSpot File Manager
   (or your CDN).
2. Open the desired email-0X.html file.
3. Replace relative image paths (images/... and icons/...) with the
   absolute HubSpot File Manager URLs.
4. In HubSpot Marketing > Email > Create email > "Coded file" / custom HTML,
   paste the email body HTML.
5. Map HubSpot personalization tokens:
     [Prénom]  →  {{ contact.firstname }}
6. Replace CTA href values with real campaign URLs.
7. Send test emails to Gmail, Outlook, Apple Mail before publishing.


Folder structure
----------------
  /index.html
  /email-01.html … /email-05.html
  /css/styles.css          (optional media-query helpers; emails are inline-first)
  /images/                 heroes, cards, logos, decorations
  /icons/                  social PNG icons (email-safe)
  /fonts/                  reserved (web fonts loaded via Google Fonts CDN)
  /assets/                 Figma export helpers / QA frame renders
  /README.txt


Technical approach
------------------
  - Table-based layout (no Flexbox/Grid as primary structure)
  - Inline CSS for critical styles
  - <style> block for resets + @media mobile only
  - Bulletproof buttons with VML for Outlook
  - PNG icons preferred over SVG for Outlook/HubSpot reliability
  - No JavaScript
  - No Bootstrap / Tailwind / frameworks
  - Google Fonts: Merriweather + Assistant (with Georgia/Arial fallbacks)


Design tokens (from Figma)
--------------------------
  Purple           #5F2EC8
  Soft purple CTA  #9A69E9
  Lavender         #F8F3FF
  Cream outer bg   #F3F3E9
  Off-white        #FFFFF9
  Ink              #313233 / #231F20
  Navy headings    #0E1E38
  Button radius    ~22px (Figma rectangleCornerRadii)


Email client support
--------------------
  HubSpot Email, Gmail, Outlook (Windows + Web), Apple Mail,
  Yahoo Mail, iPhone Mail, Android Mail


Notes
-----
  - Do not minify before HubSpot import if you need to edit merge tags.
  - Host images on HTTPS absolute URLs for production sends.
  - QA against Figma frame renders in /images/email-0X-figma.png
  - If a Figma API token was shared during build, revoke it after delivery.
