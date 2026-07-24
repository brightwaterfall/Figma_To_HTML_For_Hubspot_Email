"""
HubSpot-compatible HTML email builder from Figma Emailify specs.
No JS, no frameworks â€” table layout + inline CSS only.
"""
from pathlib import Path

ROOT = Path(r"E:\Freelancer project\figma_to_html")

# Design tokens (Figma)
PURPLE = "#5F2EC8"
PURPLE_SOFT = "#9A69E9"
QUOTE = "#A47AFF"
LAVENDER = "#F8F3FF"
CREAM = "#F3F3E9"
OFFWHITE = "#FFFFF9"
WHITE = "#FFFFFF"
INK = "#313233"
INK2 = "#231F20"
NAVY = "#0E1E38"
BODY = "#192633"
GRAY = "#777777"
MUTED = "#A6A6A6"
FOOTER = "#4B4B4B"
DIVIDER = "#CCCCCC"
# Figma button radii: TL TR BR rounded, BL = 0 (Emailify signature)
RADIUS_BTN = "22px 22px 22px 0"
RADIUS_OUTLINE = "14px 14px 14px 0"
RADIUS_TAG = "14px 14px 14px 0"

FONTS_LINK = (
    "https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700"
    "&family=Candal"
    "&family=Inter:wght@400;700"
    "&family=Merriweather:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,500&display=swap"
)


def exists(rel):
    return (ROOT / rel).exists()


def img(src, w, h=None, alt="", style=""):
    h_attr = f' height="{h}"' if h else ""
    base = f"display:block;border:0;outline:none;text-decoration:none;{style}"
    return (
        f'<img src="{src}" width="{w}"{h_attr} alt="{alt}" '
        f'style="{base}" />'
    )


def bulletproof_btn(label, href="https://www.etreprof.fr/", bg=PURPLE, width=None, height=47, radius=None):
    """Outlook-safe solid CTA — Figma pad 12/22, Merriweather 18/400, BL corner square."""
    w = width or 220
    # Longhand radii on <a> (td border-radius is unreliable in email clients)
    return f"""
                      <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                        <tr>
                          <td align="center" style="padding:0;">
                            <!--[if mso]>
                            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{href}" style="height:{height}px;v-text-anchor:middle;width:{w}px;" arcsize="50%" strokecolor="{bg}" fillcolor="{bg}">
                              <w:anchorlock/>
                              <center style="color:#FFFFFF;font-family:Georgia,serif;font-size:18px;font-weight:400;">{label}</center>
                            </v:roundrect>
                            <![endif]-->
                            <!--[if !mso]><!-->
                            <a href="{href}" target="_blank" style="display:inline-block;padding:12px 22px;font-family:'Merriweather',Georgia,'Times New Roman',serif;font-size:18px;line-height:23px;font-weight:400;color:#FFFFFF;text-decoration:none;background-color:{bg};border-top-left-radius:22px;border-top-right-radius:22px;border-bottom-right-radius:22px;border-bottom-left-radius:0;mso-hide:all;">{label}</a>
                            <!--<![endif]-->
                          </td>
                        </tr>
                      </table>"""


def outline_btn(label, href="https://www.etreprof.fr/", color=PURPLE, bg="transparent"):
    """Outline CTA — no fill so section background shows through; radii 14/14/14/0, pad 7/12."""
    # Outlook VML: unfilled stroke when bg is transparent; otherwise solid fillcolor
    if bg == "transparent":
        mso_fill = 'filled="f"'
    else:
        mso_fill = f'fillcolor="{bg}"'
    return f"""
                      <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                        <tr>
                          <td align="center" style="padding:0;">
                            <!--[if mso]>
                            <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{href}" style="height:35px;v-text-anchor:middle;width:122px;" arcsize="40%" strokecolor="{color}" {mso_fill}>
                              <w:anchorlock/>
                              <center style="color:{color};font-family:Arial,sans-serif;font-size:16px;font-weight:700;">{label}</center>
                            </v:roundrect>
                            <![endif]-->
                            <!--[if !mso]><!-->
                            <a href="{href}" target="_blank" style="display:inline-block;padding:7px 12px;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:700;color:{color};text-decoration:none;background-color:{bg};border:1px solid {color};border-top-left-radius:14px;border-top-right-radius:14px;border-bottom-right-radius:14px;border-bottom-left-radius:0;mso-hide:all;">{label}</a>
                            <!--<![endif]-->
                          </td>
                        </tr>
                      </table>"""


def pill(label, bg=PURPLE, color="#FFFFFF", font="Merriweather", size=14, weight=800):
    return f"""
                      <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="display:inline-table;">
                        <tr>
                          <td bgcolor="{bg}" style="background-color:{bg};border-radius:{RADIUS_BTN};padding:12px 22px;">
                            <span style="font-family:'{font}',Georgia,serif;font-size:{size}px;line-height:18px;font-weight:{weight};color:{color};">{label}</span>
                          </td>
                        </tr>
                      </table>"""


def logo_block(pt=13, pb=42):
    # Image overlaps logo row in Figma (starts ~y=105). Stacked HTML uses
    # pt + logo(51) + pb ≈ 105 so the hero crop (y=105.5, h=380) aligns.
    logo = "images/logo-etreprof.png"
    return f"""
            <!-- Logo -->
            <tr>
              <td align="center" bgcolor="{WHITE}" style="background-color:{WHITE};padding:{pt}px 16px {pb}px 16px;">
                <a href="https://www.etreprof.fr/" target="_blank" style="text-decoration:none;">
                  {img(logo, 48, 51, "Ãªtre PROF", "margin:0 auto;")}
                </a>
              </td>
            </tr>"""


def footer_block():
    # Prefer PNG for HubSpot/Outlook; fall back to SVG only if PNG missing
    ig = "icons/icon-instagram.png" if exists("icons/icon-instagram.png") else "icons/icon-instagram.svg"
    fb = "icons/icon-facebook.png" if exists("icons/icon-facebook.png") else "icons/icon-facebook.svg"
    x = "icons/icon-x.png" if exists("icons/icon-x.png") else "icons/icon-x.svg"
    yt = "icons/icon-youtube.png" if exists("icons/icon-youtube.png") else "icons/icon-youtube.svg"
    return f"""
            <!-- Footer -->
            <tr>
              <td align="center" bgcolor="{WHITE}" style="background-color:{WHITE};padding:32px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto 16px auto;">
                  <tr>
                    <td style="padding:0 8px;"><a href="https://www.instagram.com/" target="_blank">{img(ig, 24, 24, "Instagram")}</a></td>
                    <td style="padding:0 8px;"><a href="https://www.facebook.com/" target="_blank">{img(fb, 24, 24, "Facebook")}</a></td>
                    <td style="padding:0 8px;"><a href="https://x.com/" target="_blank">{img(x, 20, 20, "X")}</a></td>
                    <td style="padding:0 8px;"><a href="https://www.youtube.com/" target="_blank">{img(yt, 24, 24, "YouTube")}</a></td>
                  </tr>
                </table>
                <p style="margin:0 0 16px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:13px;line-height:17px;font-weight:600;color:{FOOTER};text-align:center;">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.&nbsp;
                </p>
                <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:13px;line-height:17px;font-weight:600;color:{FOOTER};text-align:center;">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.
                </p>
              </td>
            </tr>"""


def shell(title, preheader, body_rows):
    return f"""<!DOCTYPE html>
<html lang="fr" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="format-detection" content="telephone=no,address=no,email=no,date=no,url=no">
  <title>{title}</title>
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:AllowPNG/>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS_LINK}" rel="stylesheet">
  <style type="text/css">
    /* Client resets */
    body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
    table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse !important; }}
    img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
    body {{ margin: 0 !important; padding: 0 !important; width: 100% !important; height: 100% !important; background-color: {CREAM}; }}
    a[x-apple-data-detectors] {{ color: inherit !important; text-decoration: none !important; }}
    /* Mobile */
    @media only screen and (max-width: 620px) {{
      .email-container {{ width: 100% !important; max-width: 100% !important; }}
      .fluid {{ width: 100% !important; max-width: 100% !important; height: auto !important; }}
      .stack-column {{ display: block !important; width: 100% !important; max-width: 100% !important; }}
      .stack-column-pad {{ padding-left: 0 !important; padding-right: 0 !important; padding-bottom: 16px !important; }}
      .mobile-pad {{ padding-left: 24px !important; padding-right: 24px !important; }}
    }}
  </style>
</head>
<body width="100%" style="margin:0;padding:0;background-color:{CREAM};">
  <!-- Preheader -->
  <div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">
    {preheader}&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
  </div>

  <center role="article" aria-roledescription="email" lang="fr" style="width:100%;background-color:{CREAM};">
    <!--[if mso]>
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center"><tr><td>
    <![endif]-->
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width:600px;margin:0 auto;" class="email-container">
{body_rows}
    </table>
    <!--[if mso]>
    </td></tr></table>
    <![endif]-->
  </center>
</body>
</html>
"""


def email_01():
    hero = "images/email-01-hero.png"
    rows = logo_block(13, 42)
    rows += f"""
            <!-- Hero: scoop + badge + top radii baked into PNG -->
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" style="background-color:{OFFWHITE};padding:0;line-height:0;font-size:0;">
                {img(hero, 600, None, "Ton avis â€” deux enseignantes souriantes", "width:100%;max-width:600px;height:auto;")}
              </td>
            </tr>
            <!-- Title / CTA -->
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" class="mobile-pad" style="background-color:{OFFWHITE};padding:30px 66px 40px 66px;">
                <h1 style="margin:0 0 25px 0;font-family:'Merriweather',Georgia,'Times New Roman',serif;font-size:29px;line-height:35px;font-weight:500;color:{INK};text-align:center;">
                  On construit la suite avec toi.
                </h1>
                <p style="margin:0 0 25px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:400;color:{INK2};text-align:center;">
                  Tu utilises ÃŠtrePROF au quotidien. Pour que la plateforme<br>
                  rÃ©ponde vraiment Ã  tes rÃ©alitÃ©s de terrain, nous avons besoin de<br>
                  ton retour. Tes rÃ©ponses guideront nos prochaines nouveautÃ©s.
                </p>
                {bulletproof_btn("Je donne mon avis", width=202)}
                <p style="margin:25px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:15px;line-height:22.5px;font-weight:600;color:{MUTED};text-align:center;">
                  â±ï¸ Promis, cela te prendra moins de 2 minutes.
                </p>
                <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:400;color:#000000;text-align:center;">
                  Merci pour ton aide prÃ©cieuse,<br>
                  L'Ã©quipe ÃŠtrePROF
                </p>
              </td>
            </tr>
            <!-- Reassurance -->
            <tr>
              <td align="center" bgcolor="{WHITE}" class="mobile-pad" style="background-color:{WHITE};padding:23px 42px 30px 40px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                  <tr><td style="border-top:1px solid {DIVIDER};font-size:0;line-height:0;height:1px;">&nbsp;</td></tr>
                </table>
                <h2 style="margin:18px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:29px;font-weight:600;color:{NAVY};text-align:center;">
                  Pourquoi votre participation<br>est essentielle&nbsp;?
                </h2>
                <p style="margin:0 0 18px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:400;color:{BODY};text-align:center;">
                  Vos rÃ©ponses font avancer une cause commune&nbsp;: mieux comprendre les besoins du terrain pour faire Ã©voluer les solutions utiles Ã  toute la communautÃ© Ã©ducative.
                </p>
                <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:700;text-align:center;">
                  <a href="https://www.etreprof.fr/" target="_blank" style="font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:700;color:{PURPLE};text-decoration:none;">En savoir plus sur la dÃ©marche â†’</a>
                </p>
              </td>
            </tr>
            <!-- Incentive -->
            <tr>
              <td align="center" bgcolor="{LAVENDER}" class="mobile-pad" style="background-color:{LAVENDER};padding:30px 40px 20px 40px;">
                {outline_btn("À DÉCOUVRIR")}
                <div style="font-size:0;line-height:0;height:10px;">&nbsp;</div>
                <h2 style="margin:0 0 10px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:29px;font-weight:600;color:{NAVY};text-align:center;">
                  Un petit plus pour vous remercier
                </h2>
                <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:400;color:{BODY};text-align:center;">
                  Module Ã  activer uniquement lorsqu'un avantage est proposÃ©. Vocabulaire volontairement sobre pour prÃ©server la dÃ©livrabilitÃ©.
                </p>
              </td>
            </tr>
"""
    rows += footer_block()
    return shell("On construit la suite avec toi. | Ãªtre PROF", "On construit la suite avec toi.", rows)


def resource_row(img_src, title_html, proof, desc, show_nouveau=False):
    badge = ""
    if show_nouveau:
        badge = f"""
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin-top:8px;">
                          <tr>
                            <td bgcolor="{PURPLE}" style="background-color:{PURPLE};border-radius:{RADIUS_TAG};padding:4px 8px;">
                              <span style="font-family:'Merriweather',Georgia,serif;font-size:10px;line-height:12px;font-weight:800;color:#FFFFFF;">Nouveau</span>
                            </td>
                          </tr>
                        </table>"""
    return f"""
                      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin:0 0 18px 0;">
                        <tr>
                          <td class="stack-column stack-column-pad" valign="top" width="203" style="width:203px;padding:0 18px 0 0;">
                            {img(img_src, 203, None, "", "width:100%;max-width:203px;height:auto;border-radius:8px;")}
                            {badge}
                          </td>
                          <td class="stack-column" valign="top" style="padding:8px 0;">
                            <p style="margin:0 0 7px 0;font-family:'Merriweather',Georgia,serif;font-size:14px;line-height:17px;font-weight:500;color:#000000;text-align:left;">{title_html}</p>
                            <p style="margin:0 0 7px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:10px;line-height:13px;font-weight:600;color:#000000;text-align:left;">{proof}</p>
                            <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:12px;line-height:14px;font-weight:400;color:#000000;text-align:left;">{desc}</p>
                          </td>
                        </tr>
                      </table>"""


def workshop_card(avatar="images/email-02-avatar.png"):
    badge = (
        "border-top-left-radius:14px;border-top-right-radius:14px;"
        "border-bottom-right-radius:14px;border-bottom-left-radius:0;"
    )
    return f"""
                      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:{LAVENDER};border-radius:8px;margin:0 0 16px 0;">
                        <tr>
                          <td style="padding:20px 24px;">
                            <p style="margin:0 0 12px 0;font-family:'Merriweather',Georgia,serif;font-size:14px;line-height:17px;font-weight:500;color:#000000;">
                              DÃ©velopper les compÃ©tences orales des Ã©lÃ¨ves avec l'IA : activitÃ©s et prompts Ã  utiliser
                            </p>
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:0 0 14px 0;">
                              <tr>
                                <td valign="middle" width="38" height="38" style="width:38px;height:38px;padding-right:10px;line-height:0;font-size:0;">
                                  {img(avatar, 38, 38, "MickaÃ«l Bertrand", "width:38px;height:38px;border-radius:50%;")}
                                </td>
                                <td valign="middle">
                                  <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:10px;line-height:11px;font-weight:400;color:#000000;">
                                    MickaÃ«l Bertrand<br>Professeur d'histoire-gÃ©ographie-EMC
                                  </p>
                                </td>
                              </tr>
                            </table>
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                              <tr>
                                <td style="padding:0;">
                                  <span style="display:inline-block;padding:3px 12px;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:13px;line-height:17px;font-weight:700;color:#FFFFFF;background-color:{PURPLE};{badge}">19h</span>
                                </td>
                                <td width="9" style="width:9px;font-size:0;line-height:0;">&nbsp;</td>
                                <td style="padding:0;">
                                  <span style="display:inline-block;padding:3px 18px;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:13px;line-height:17px;font-weight:700;color:#FFFFFF;background-color:{PURPLE};{badge}">20 juillet 2026</span>
                                </td>
                                <td width="9" style="width:9px;font-size:0;line-height:0;">&nbsp;</td>
                                <td style="padding:0;">
                                  <span style="display:inline-block;padding:3px 12px;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:13px;line-height:17px;font-weight:700;color:{PURPLE};background-color:{WHITE};border:1px solid {PURPLE};{badge}">En ligne</span>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>"""


def email_02():
    hero = "images/email-02-hero.png"
    res1 = "images/email-02-card-1.png" if exists("images/email-02-card-1.png") else "images/email-02-res-1.png"
    res2 = "images/email-02-card-2.png" if exists("images/email-02-card-2.png") else "images/email-02-res-2.png"
    if not exists(res1):
        res1 = "images/email-02-hero.png"
    if not exists(res2):
        res2 = res1
    smile = "images/email-02-smile.png"
    hand = "images/email-02-handshake.png"
    conf = "images/email-02-confetti.png"
    rows = logo_block(13, 42)
    rows += f"""
            <!-- Hero: scoop + badge + top radii baked into PNG -->
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" style="background-color:{OFFWHITE};padding:0;line-height:0;font-size:0;">
                {img(hero, 600, None, "SpÃ©cial Inclusion â€” Maternelle", "width:100%;max-width:600px;height:auto;")}
              </td>
            </tr>
            <!-- Intro + resources -->
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" class="mobile-pad" style="background-color:{OFFWHITE};padding:37px 61px;">
                <h1 style="margin:0 0 16px 0;font-family:'Merriweather',Georgia,serif;font-size:29px;line-height:35px;font-weight:600;color:{INK};text-align:center;">
                  L'essentiel pour ta classe
                </h1>
                <p style="margin:0 0 25px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:400;color:{INK2};text-align:center;">
                  Bonjour [PrÃ©nom], dÃ©couvre les nouvelles thÃ©matiques de la<br>
                  semaine. On met le cap sur l'inclusion et les rituels de transition<br>
                  pour apaiser tes journÃ©es.
                </p>
                {bulletproof_btn("DÃ©couvrir la sÃ©lection", width=233, radius="22px 22px 16px 0")}
                <div style="height:18px;line-height:18px;font-size:0;">&nbsp;</div>
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"><tr><td style="border-top:1px solid {DIVIDER};height:1px;font-size:0;line-height:0;">&nbsp;</td></tr></table>
                <div style="height:18px;line-height:18px;font-size:0;">&nbsp;</div>
                <h2 style="margin:0 0 18px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:28px;font-weight:600;color:{INK};text-align:left;">
                  Les ressources Ã  la une
                </h2>
                {resource_row(res1, "Fiche outil : GÃ©rer le retour<br>au calme", "â­  ApprouvÃ© par 45 profs", "Une mÃ©thode clÃ© en main pour capter l'attention de tes Ã©lÃ¨ves aprÃ¨s la rÃ©crÃ©ation, sans avoir Ã  hausser le ton.", False)}
                {resource_row(res2, "Atelier : La boÃ®te Ã  Ã©motions", "â­  ApprouvÃ© par 28 profs", "Des cartes prÃªtes Ã  imprimer pour aider les Ã©lÃ¨ves Ã  verbaliser leurs ressentis dÃ¨s le rituel du matin.")}
                <h2 style="margin:24px 0 16px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:28px;font-weight:600;color:{INK};text-align:left;">
                  Prochains ateliers
                </h2>
                {workshop_card()}
                {workshop_card()}
              </td>
            </tr>
            <!-- Quote -->
            <tr>
              <td align="center" bgcolor="{LAVENDER}" class="mobile-pad" style="background-color:{LAVENDER};padding:60px 66px;">
                <p style="margin:0 0 12px 0;font-family:'Candal',Georgia,'Times New Roman',serif;font-size:53px;line-height:64px;font-weight:400;color:{QUOTE};text-align:center;">"</p>
                <p style="margin:0 0 12px 0;font-family:'Merriweather',Georgia,serif;font-size:26px;line-height:34px;font-weight:500;font-style:italic;color:{PURPLE};text-align:center;">
                  Comment gÃ©rez-vous le retour au calme<br>
                  aprÃ¨s la rÃ©crÃ©ation avec une classe trÃ¨s agitÃ©e&nbsp;?
                </p>
                <p style="margin:0 0 24px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;font-weight:400;color:{INK2};text-align:center;">
                  â€” Question de Sarah, professeure de CE2
                </p>
                {bulletproof_btn("Partager mon astuce", width=222)}
              </td>
            </tr>
            <!-- Scholavie -->
            <tr>
              <td align="center" bgcolor="{WHITE}" class="mobile-pad" style="background-color:{WHITE};padding:32px 35px 32px 32px;">
                {img("images/logo-scholavie.png", 119, 38, "Scholavie", "margin:0 auto 14px auto;") if exists("images/logo-scholavie.png") else ""}
                <h2 style="margin:0 0 14px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:28px;font-weight:600;color:{INK};text-align:center;">
                  Aller plus loin sur le bien-Ãªtre Ã  l'Ã©cole
                </h2>
                <p style="margin:0 0 14px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:400;color:{INK2};text-align:center;">
                  Dans le prolongement de cet article, Scholavie propose des ressources complÃ©mentaires pour accompagner vos Ã©lÃ¨ves.
                </p>
                <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:700;text-align:center;">
                  <a href="https://www.etreprof.fr/" target="_blank" style="font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:700;color:{PURPLE};text-decoration:none;">DÃ©couvrir les ressources â†’</a>
                </p>
              </td>
            </tr>
"""
    rows += footer_block()
    return shell("L'essentiel pour ta classe | Ãªtre PROF", "L'essentiel pour ta classe", rows)


def email_03():
    hero = "images/email-03-hero.png"
    card = "images/email-03-card-1.png" if exists("images/email-03-card-1.png") else "images/email-03-card.png"
    rows = logo_block(13, 42)
    rows += f"""
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" style="background-color:{OFFWHITE};padding:0;line-height:0;font-size:0;">
                {img(hero, 600, None, "Top chrono : 10 min", "width:100%;max-width:600px;height:auto;")}
              </td>
            </tr>
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" class="mobile-pad" style="background-color:{OFFWHITE};padding:30px 66px 24px 66px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto 16px auto;">
                  <tr>
                    <td align="center" valign="middle" style="padding:0 4px;line-height:0;font-size:0;">
                      {img("images/email-03-smile.png", 35, 35, "", "width:35px;height:35px;") if exists("images/email-03-smile.png") else ""}
                    </td>
                    <td align="center" valign="middle" style="padding:0 4px;line-height:0;font-size:0;">
                      {img("images/email-03-launch.png", 35, 35, "", "width:35px;height:35px;") if exists("images/email-03-launch.png") else ""}
                    </td>
                    <td align="center" valign="middle" style="padding:0 4px;line-height:0;font-size:0;">
                      {img("images/email-03-laptop.png", 35, 35, "", "width:35px;height:35px;") if exists("images/email-03-laptop.png") else ""}
                    </td>
                  </tr>
                </table>
                <h1 style="margin:0 0 22px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:28px;font-weight:500;color:{INK};text-align:center;">
                  Ta prochaine sÃ©ance, prÃªte en un instant.
                </h1>
                <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:21px;font-weight:400;color:{INK2};text-align:center;">
                  Bonjour [PrÃ©nom], tu as dÃ©jÃ  passÃ© ton dimanche aprÃ¨s-midi devant une page blanche&nbsp;? Sur le nouvel ÃŠtrePROF, tu ne pars plus de zÃ©ro. Gagne un temps prÃ©cieux en t'appuyant sur les sÃ©quences crÃ©Ã©es et testÃ©es par tes collÃ¨gues.
                </p>
              </td>
            </tr>
            <tr>
              <td bgcolor="{LAVENDER}" class="mobile-pad" style="background-color:{LAVENDER};padding:29px 80px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                  <tr>
                    <td class="stack-column stack-column-pad" valign="top" width="203" style="width:203px;padding:0 18px 0 0;">
                      {img(card, 203, None, "SÃ©ance systÃ¨me solaire", "width:100%;max-width:203px;height:auto;border-radius:8px;") if exists(card) else ""}
                    </td>
                    <td class="stack-column" valign="top" style="padding:8px 0;">
                      <p style="margin:0 0 10px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:25px;font-weight:500;color:#000000;">
                        SÃ©ance : DÃ©couvrir<br>le systÃ¨me solaire
                      </p>
                      <p style="margin:0 0 10px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:12px;line-height:14px;font-weight:400;color:#000000;">
                        De la Terre Ã  Neptune : 3 sÃ©ances interactives pour modÃ©liser le systÃ¨me solaire et captiver ta classe.
                      </p>
                      <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:0 0 10px 0;">
                        <tr>
                          <td bgcolor="{PURPLE}" style="background-color:{PURPLE};border-radius:{RADIUS_TAG};padding:4px 12px;">
                            <span style="font-family:'Inter',Arial,Helvetica,sans-serif;font-size:13px;line-height:16px;font-weight:700;color:#FFFFFF;">Cycle 3</span>
                          </td>
                          <td width="9">&nbsp;</td>
                          <td bgcolor="{PURPLE}" style="background-color:{PURPLE};border-radius:{RADIUS_TAG};padding:4px 12px;">
                            <span style="font-family:'Inter',Arial,Helvetica,sans-serif;font-size:13px;line-height:16px;font-weight:700;color:#FFFFFF;">Sciences</span>
                          </td>
                        </tr>
                      </table>
                      <table role="presentation" width="174" cellspacing="0" cellpadding="0" border="0" style="margin:0 0 10px 0;"><tr><td style="border-top:1px solid {DIVIDER};height:1px;font-size:0;">&nbsp;</td></tr></table>
                      <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:10px;line-height:13px;font-weight:600;color:#000000;">â­  ApprouvÃ© par 120 profs de la communautÃ©</p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td bgcolor="{WHITE}" class="mobile-pad" style="background-color:{WHITE};padding:32px 32px 19px 79px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                  <tr>
                    <td valign="top" width="45" style="font-family:Arial,Helvetica,sans-serif;font-size:45px;line-height:52px;font-weight:700;color:{PURPLE};padding-right:16px;">1</td>
                    <td valign="middle" style="font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:18px;line-height:17px;font-weight:400;color:{GRAY};padding:9px 0;">
                      <strong style="color:{INK};font-weight:400;">Trouve l'idÃ©e :</strong> Laisse-toi inspirer par les sÃ©quences de la<br>communautÃ©.
                    </td>
                  </tr>
                  <tr><td colspan="2" height="8" style="font-size:0;line-height:0;">&nbsp;</td></tr>
                  <tr>
                    <td valign="top" width="45" style="font-family:Arial,Helvetica,sans-serif;font-size:45px;line-height:52px;font-weight:700;color:{PURPLE};padding-right:16px;">2</td>
                    <td valign="middle" style="font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:18px;line-height:17px;font-weight:400;color:{GRAY};padding:9px 0;">
                      <strong style="color:{INK};font-weight:400;">Adapte au profil :</strong> Ajuste le contenu pour tes Ã©lÃ¨ves en un<br>clic.
                    </td>
                  </tr>
                  <tr><td colspan="2" height="8" style="font-size:0;line-height:0;">&nbsp;</td></tr>
                  <tr>
                    <td valign="top" width="45" style="font-family:Arial,Helvetica,sans-serif;font-size:45px;line-height:52px;font-weight:700;color:{PURPLE};padding-right:16px;">3</td>
                    <td valign="middle" style="font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:18px;line-height:17px;font-weight:400;color:{GRAY};padding:9px 0;">
                      <strong style="color:{INK};font-weight:400;">Imprime le tout :</strong> Ta fiche et tes supports sont prÃªts pour<br>demain.
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td align="center" bgcolor="{WHITE}" style="background-color:{WHITE};padding:16px;">
                {bulletproof_btn("PrÃ©parer ma sÃ©ance", width=213)}
                <p style="margin:17px 0 16px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:15px;line-height:22.5px;font-weight:600;color:{MUTED};text-align:center;">
                  Rejoins les 15 000 profs qui ont dÃ©jÃ  prÃ©parÃ© leur semaine.
                </p>
                <table role="presentation" width="482" align="center" cellspacing="0" cellpadding="0" border="0" style="margin:0 auto;max-width:100%;">
                  <tr><td style="border-top:1px solid {DIVIDER};height:1px;font-size:0;">&nbsp;</td></tr>
                </table>
              </td>
            </tr>
"""
    rows += footer_block()
    return shell("Ta prochaine sÃ©ance, prÃªte en un instant. | Ãªtre PROF", "Ta prochaine sÃ©ance, prÃªte en un instant.", rows)


def email_04():
    rows = logo_block(16, 16)
    rows += f"""
            <tr>
              <td align="center" bgcolor="{WHITE}" class="mobile-pad" style="background-color:{WHITE};padding:32px 66px 24px 66px;">
                <h1 style="margin:0 0 12px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:28px;font-weight:500;color:{INK};text-align:center;">
                  Nouveau mot de passe
                </h1>
                <p style="margin:0 0 16px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;font-weight:400;color:{INK2};text-align:center;">
                  Bonjour [PrÃ©nom], tu as demandÃ© Ã  rÃ©initialiser ton mot de passe. Clique sur le bouton ci-dessous pour en crÃ©er un nouveau et retrouver ton espace de prÃ©paration.
                </p>
                {bulletproof_btn("RÃ©initialiser mon mot de passe", bg=PURPLE_SOFT, width=311)}
                <div style="height:16px;line-height:16px;font-size:0;">&nbsp;</div>
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                  <tr><td style="border-top:1px solid {DIVIDER};height:1px;font-size:0;">&nbsp;</td></tr>
                </table>
              </td>
            </tr>
            <tr>
              <td align="center" bgcolor="{WHITE}" class="mobile-pad" style="background-color:{WHITE};padding:14px 32px 32px 32px;">
                <p style="margin:0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:14px;line-height:21px;font-weight:300;color:{INK2};text-align:center;">
                  Si tu n'es pas Ã  l'origine de cette demande, ignore simplement cet e-mail.<br>
                  Ton compte reste sÃ©curisÃ©.
                </p>
              </td>
            </tr>
"""
    rows += footer_block()
    return shell("Nouveau mot de passe | Ãªtre PROF", "RÃ©initialiser mon mot de passe", rows)


def feature_card(text_html, icon):
    """Stacked icon stats card — Figma radii [21,21,21,0], Merriweather 17/300, 2-line copy."""
    icon_html = img(icon, 43, 43, "", "") if exists(icon) else ""
    radius = (
        "border-top-left-radius:21px;border-top-right-radius:21px;"
        "border-bottom-right-radius:21px;border-bottom-left-radius:0;"
    )
    return f"""
                      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:{LAVENDER};{radius}margin:0 0 12px 0;overflow:hidden;">
                        <tr>
                          <td valign="middle" width="300" style="width:300px;max-width:300px;padding:16px 12px 16px 20px;font-family:'Merriweather',Georgia,serif;font-size:17px;line-height:21px;font-weight:300;color:#000000;text-align:left;">
                            {text_html}
                          </td>
                          <td valign="middle" align="right" style="padding:16px 20px 16px 8px;">
                            {icon_html}
                          </td>
                        </tr>
                      </table>"""


def email_05():
    hero = "images/email-05-hero.png"
    f1 = "images/email-05-school.png" if exists("images/email-05-school.png") else "images/email-05-feat-1.png"
    f2 = "images/email-05-backpack.png" if exists("images/email-05-backpack.png") else "images/email-05-feat-2.png"
    f3 = "images/email-05-people.png" if exists("images/email-05-people.png") else "images/email-05-feat-3.png"
    rows = logo_block(13, 42)
    rows += f"""
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" style="background-color:{OFFWHITE};padding:0;line-height:0;font-size:0;">
                {img(hero, 600, None, "Salle des professeurs - Maternelle Michel Bizot", "width:100%;max-width:600px;height:auto;")}
              </td>
            </tr>
            <tr>
              <td align="center" bgcolor="{OFFWHITE}" class="mobile-pad" style="background-color:{OFFWHITE};padding:30px 66px 24px 66px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto 16px auto;">
                  <tr>
                    <td align="center" valign="middle" style="padding:0 4px;line-height:0;font-size:0;">
                      {img("images/email-05-smile.png", 35, 35, "", "width:35px;height:35px;") if exists("images/email-05-smile.png") else ""}
                    </td>
                    <td align="center" valign="middle" style="padding:0 4px;line-height:0;font-size:0;">
                      {img("images/email-05-handshake.png", 35, 35, "", "width:35px;height:35px;") if exists("images/email-05-handshake.png") else ""}
                    </td>
                    <td align="center" valign="middle" style="padding:0 4px;line-height:0;font-size:0;">
                      {img("images/email-05-confetti.png", 35, 35, "", "width:35px;height:35px;") if exists("images/email-05-confetti.png") else ""}
                    </td>
                  </tr>
                </table>
                <h1 style="margin:0 0 16px 0;font-family:'Merriweather',Georgia,serif;font-size:23px;line-height:28px;font-weight:500;color:{INK};text-align:center;">
                  Bienvenue dans ta nouvelle salle des profs
                </h1>
                <p style="margin:0 0 25px 0;font-family:'Assistant',Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;font-weight:400;color:{INK2};text-align:center;">
                  Bonjour [PrÃ©nom], bienvenue sur le nouvel ÃŠtrePROF&nbsp;!<br>
                  Nous avons repensÃ© la plateforme pour qu'elle devienne ton vÃ©ritable espace d'entraide et de co-working. Ici, on ne fait pas que tÃ©lÃ©charger des fiches : on s'inspire, on Ã©change et on construit ensemble.
                </p>
                {bulletproof_btn("DÃ©couvrir mon nouvel espace", width=300)}
              </td>
            </tr>
            <tr>
              <td bgcolor="{WHITE}" class="mobile-pad" style="background-color:{WHITE};padding:16px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin:0 0 24px 0;">
                  <tr><td style="border-top:1px solid {DIVIDER};height:1px;font-size:0;">&nbsp;</td></tr>
                </table>
                {feature_card("Inspire-toi de milliers de<br>ressources testÃ©es en classe.", f1)}
                {feature_card("Adapte tes supports aux besoins<br>spÃ©cifiques de tes Ã©lÃ¨ves.", f2)}
                {feature_card("Ã‰change avec une communautÃ© qui<br>vit ton quotidien.", f3)}
              </td>
            </tr>
"""
    rows += footer_block()
    return shell("Bienvenue dans ta nouvelle salle des profs | Ãªtre PROF", "Bienvenue dans ta nouvelle salle des profs", rows)


def write_index():
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ãªtre PROF â€” HubSpot Email Templates</title>
  <link href="{FONTS_LINK}" rel="stylesheet">
  <style>
    body {{ margin:0; font-family:Assistant,Arial,sans-serif; background:{CREAM}; color:{INK}; }}
    .wrap {{ max-width:720px; margin:0 auto; padding:48px 24px; }}
    h1 {{ font-family:Merriweather,Georgia,serif; font-size:28px; margin:0 0 8px; }}
    p {{ color:{FOOTER}; line-height:1.5; }}
    a.card {{ display:block; background:#fff; border:1px solid #e6e6e0; border-radius:10px; padding:18px 20px; margin:12px 0; text-decoration:none; color:inherit; }}
    a.card strong {{ color:{PURPLE}; font-family:Merriweather,Georgia,serif; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Ãªtre PROF â€” HubSpot Email Templates</h1>
    <p>600px table-based HTML emails from the Figma Emailify frames. Open a template, then import the HTML into HubSpot Email.</p>
    <a class="card" href="email-01.html"><strong>Email 01 â€” Feedback</strong><br>On construit la suite avec toi.</a>
    <a class="card" href="email-02.html"><strong>Email 02 â€” Newsletter</strong><br>L'essentiel pour ta classe</a>
    <a class="card" href="email-03.html"><strong>Email 03 â€” Lesson</strong><br>Ta prochaine sÃ©ance, prÃªte en un instant.</a>
    <a class="card" href="email-04.html"><strong>Email 04 â€” Password</strong><br>Nouveau mot de passe</a>
    <a class="card" href="email-05.html"><strong>Email 05 â€” Welcome</strong><br>Bienvenue dans ta nouvelle salle des profs</a>
  </div>
</body>
</html>
"""


def main():
    files = {
        "email-01.html": email_01(),
        "email-02.html": email_02(),
        "email-03.html": email_03(),
        "email-04.html": email_04(),
        "email-05.html": email_05(),
        "index.html": write_index(),
    }
    for name, html in files.items():
        (ROOT / name).write_text(html, encoding="utf-8")
        print("wrote", name, len(html))


if __name__ == "__main__":
    main()
