from pathlib import Path
import zipfile

out = Path("/mnt/data/maison_impeccable_site")
out.mkdir(exist_ok=True)

html = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Maison Impeccable - Nettoyage à Colmar et alentours. Particuliers, bureaux, commerces, Airbnb et locations saisonnières.">
<title>Maison Impeccable | Nettoyage à Colmar</title>
<style>
:root{--navy:#0b2345;--blue:#1687d8;--green:#49a82e;--light:#f4f8fc;--text:#243247;--muted:#657184;--white:#fff}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Arial,Helvetica,sans-serif;color:var(--text);background:#fff;line-height:1.6}
a{text-decoration:none;color:inherit}
.container{width:min(1120px,92%);margin:auto}
header{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid #e7edf4}
.nav{height:76px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--navy);font-size:19px}
.logo-mark{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--blue),var(--green));display:grid;place-items:center;color:white;font-weight:900}
nav{display:flex;gap:25px;font-size:14px;font-weight:700;color:#425168}
nav a:hover{color:var(--blue)}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:13px 21px;border-radius:10px;background:var(--blue);color:white;font-weight:800;border:none;cursor:pointer;box-shadow:0 8px 20px rgba(22,135,216,.2)}
.btn:hover{transform:translateY(-1px)}
.btn.secondary{background:white;color:var(--navy);border:1px solid #dce5ee;box-shadow:none}
.hero{background:linear-gradient(135deg,#f5faff 0%,#fff 60%,#f5fbf2 100%);padding:90px 0 80px}
.hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:55px;align-items:center}
.badge{display:inline-block;background:#eaf5ff;color:#0874c1;padding:7px 12px;border-radius:30px;font-size:13px;font-weight:800;margin-bottom:18px}
h1{font-size:clamp(38px,5vw,65px);line-height:1.05;color:var(--navy);letter-spacing:-2px;margin-bottom:20px}
h1 span{color:var(--blue)}
.hero p{font-size:19px;color:var(--muted);max-width:620px;margin-bottom:28px}
.actions{display:flex;gap:12px;flex-wrap:wrap}
.hero-card{background:white;border:1px solid #e4ebf2;border-radius:24px;padding:30px;box-shadow:0 25px 60px rgba(11,35,69,.10)}
.clean-icon{height:260px;border-radius:18px;background:linear-gradient(145deg,var(--navy),#173f72);display:grid;place-items:center;color:white;font-size:90px;position:relative;overflow:hidden}
.clean-icon:after{content:"";position:absolute;width:210px;height:210px;border:35px solid rgba(255,255,255,.08);border-radius:50%;right:-70px;bottom:-80px}
.hero-card h3{color:var(--navy);margin-top:20px;font-size:22px}
.hero-card p{font-size:14px;margin:7px 0 0}
section{padding:80px 0}
.section-head{text-align:center;max-width:700px;margin:0 auto 45px}
.section-head h2{font-size:36px;color:var(--navy);margin-bottom:10px}
.section-head p{color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{padding:28px;border:1px solid #e3eaf1;border-radius:18px;background:white;box-shadow:0 10px 30px rgba(11,35,69,.05)}
.card .icon{font-size:34px;margin-bottom:13px}
.card h3{color:var(--navy);font-size:20px;margin-bottom:8px}
.card p{color:var(--muted);font-size:15px}
.soft{background:var(--light)}
.about{display:grid;grid-template-columns:1fr 1fr;gap:50px;align-items:center}
.about h2{font-size:38px;color:var(--navy);line-height:1.1;margin-bottom:16px}
.about p{color:var(--muted);margin-bottom:15px}
.checks{display:grid;gap:10px;margin-top:20px}
.check{font-weight:700;color:var(--navy)}
.check::before{content:"✓";display:inline-grid;place-items:center;width:24px;height:24px;background:#eaf7e5;color:var(--green);border-radius:50%;margin-right:9px}
.contact{display:grid;grid-template-columns:.9fr 1.1fr;gap:35px}
.contact-box{background:var(--navy);color:white;border-radius:22px;padding:35px}
.contact-box h2{font-size:32px;margin-bottom:12px}
.contact-box p{color:#d6e1ef;margin-bottom:20px}
.contact-line{padding:13px 0;border-top:1px solid rgba(255,255,255,.14)}
form{border:1px solid #e3eaf1;border-radius:22px;padding:30px}
label{font-weight:700;font-size:14px;color:var(--navy);display:block;margin-bottom:6px}
input,textarea,select{width:100%;padding:13px 14px;border:1px solid #d7e0e9;border-radius:9px;font:inherit;margin-bottom:16px}
textarea{min-height:120px;resize:vertical}
footer{background:#071a33;color:#cbd6e4;padding:30px 0;text-align:center;font-size:13px}
@media(max-width:800px){nav{display:none}.hero-grid,.about,.contact{grid-template-columns:1fr}.cards{grid-template-columns:1fr}.hero{padding:65px 0}.hero-card{order:-1}section{padding:60px 0}}
</style>
</head>
<body>
<header>
  <div class="container nav">
    <a class="logo" href="#accueil"><span class="logo-mark">MI</span> Maison Impeccable</a>
    <nav>
      <a href="#prestations">Prestations</a>
      <a href="#apropos">À propos</a>
      <a href="#contact">Contact</a>
    </nav>
    <a class="btn" href="tel:+33780548663">Appeler</a>
  </div>
</header>

<main>
<section class="hero" id="accueil">
  <div class="container hero-grid">
    <div>
      <span class="badge">NETTOYAGE À COLMAR & ALENTOURS</span>
      <h1>Votre intérieur,<br><span>notre exigence.</span></h1>
      <p>Maison Impeccable vous accompagne pour le nettoyage des particuliers, bureaux, commerces, Airbnb et locations saisonnières.</p>
      <div class="actions">
        <a class="btn" href="#contact">Demander un devis</a>
        <a class="btn secondary" href="tel:+33780548663">07 80 54 86 63</a>
      </div>
    </div>
    <div class="hero-card">
      <div class="clean-icon">✨</div>
      <h3>Un service propre, simple et fiable</h3>
      <p>Nettoyage régulier ou ponctuel, grand nettoyage et remise en état selon vos besoins.</p>
    </div>
  </div>
</section>

<section id="prestations">
  <div class="container">
    <div class="section-head">
      <h2>Nos prestations</h2>
      <p>Des solutions de nettoyage adaptées aux particuliers comme aux professionnels.</p>
    </div>
    <div class="cards">
      <article class="card"><div class="icon">🏠</div><h3>Particuliers</h3><p>Entretien de votre maison ou appartement, régulièrement ou ponctuellement.</p></article>
      <article class="card"><div class="icon">🏢</div><h3>Bureaux & commerces</h3><p>Nettoyage et entretien des espaces professionnels pour un environnement agréable.</p></article>
      <article class="card"><div class="icon">🏡</div><h3>Airbnb & locations</h3><p>Préparation et remise en état des logements entre deux séjours.</p></article>
      <article class="card"><div class="icon">✨</div><h3>Nettoyage régulier</h3><p>Des passages planifiés selon vos besoins et votre rythme.</p></article>
      <article class="card"><div class="icon">🧹</div><h3>Grand nettoyage</h3><p>Remise en état et nettoyage approfondi lorsque votre logement en a besoin.</p></article>
      <article class="card"><div class="icon">📍</div><h3>Colmar & alentours</h3><p>Intervention sur Colmar et les secteurs alentours, selon disponibilité.</p></article>
    </div>
  </div>
</section>

<section class="soft" id="apropos">
  <div class="container about">
    <div>
      <h2>Une maison impeccable, sans contrainte.</h2>
      <p>Maison Impeccable est une entreprise de nettoyage basée autour de Colmar, dirigée par <strong>Mukhtar MAHSUMI</strong>.</p>
      <p>Notre objectif : vous faire gagner du temps avec un service sérieux et adapté à chaque espace.</p>
      <div class="checks">
        <div class="check">Nettoyage régulier ou ponctuel</div>
        <div class="check">Particuliers et professionnels</div>
        <div class="check">Airbnb et locations saisonnières</div>
        <div class="check">Devis personnalisé</div>
      </div>
    </div>
    <div class="card">
      <h3 style="font-size:25px;color:#0b2345;margin-bottom:12px">Pourquoi Maison Impeccable ?</h3>
      <p>Parce que la propreté fait la différence. Nous proposons une prestation claire, avec un contact direct et une organisation adaptée à vos besoins.</p>
      <br>
      <a class="btn" href="#contact">Parler de votre besoin</a>
    </div>
  </div>
</section>

<section id="contact">
  <div class="container">
    <div class="section-head">
      <h2>Demandez votre devis</h2>
      <p>Expliquez-nous votre besoin et nous vous recontacterons.</p>
    </div>
    <div class="contact">
      <div class="contact-box">
        <h2>Contact</h2>
        <p>Pour une demande de ménage, d'entretien ou de remise en état.</p>
        <div class="contact-line"><strong>Mukhtar MAHSUMI</strong></div>
        <div class="contact-line">📞 <a href="tel:+33780548663">07 80 54 86 63</a></div>
        <div class="contact-line">✉️ <a href="mailto:mahsumim588@gmail.com">mahsumim588@gmail.com</a></div>
        <div class="contact-line">📍 Colmar & alentours</div>
      </div>
      <form action="mailto:mahsumim588@gmail.com" method="post" enctype="text/plain">
        <label for="nom">Nom</label>
        <input id="nom" name="Nom" required>
        <label for="tel">Téléphone</label>
        <input id="tel" name="Téléphone" type="tel">
        <label for="service">Prestation souhaitée</label>
        <select id="service" name="Prestation">
          <option>Particulier</option>
          <option>Bureau / commerce</option>
          <option>Airbnb / location saisonnière</option>
          <option>Nettoyage régulier</option>
          <option>Grand nettoyage / remise en état</option>
        </select>
        <label for="message">Votre besoin</label>
        <textarea id="message" name="Message" placeholder="Décrivez votre logement ou votre besoin..."></textarea>
        <button class="btn" type="submit">Envoyer ma demande</button>
      </form>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="container">
    <strong>Maison Impeccable</strong> — Nettoyage à Colmar & alentours<br>
    Mukhtar MAHSUMI • 07 80 54 86 63 • mahsumim588@gmail.com
  </div>
</footer>
</body>
</html>'''

html_path=out/"index.html"
html_path.write_text(html, encoding="utf-8")

readme = """MAISON IMPECCABLE — SITE INTERNET

Fichier principal : index.html

Pour tester :
1. Ouvre index.html dans Chrome, Edge ou Firefox.
2. Le site fonctionne sans installation.

Pour mettre le site en ligne :
- Acheter un nom de domaine (ex. maison-impeccable.fr s'il est disponible).
- Héberger ce fichier chez un hébergeur.
- Remplacer [À compléter] par l'adresse professionnelle et le SIRET lorsqu'ils seront disponibles.

Le formulaire utilise le logiciel de messagerie du visiteur via mailto.
Pour un formulaire professionnel sans dépendre du logiciel de messagerie, il faudra ensuite le connecter à un service de formulaire ou à l'hébergement.

Coordonnées intégrées :
Mukhtar MAHSUMI
07 80 54 86 63
mahsumim588@gmail.com
Colmar & alentours
"""
(out/"README.txt").write_text(readme, encoding="utf-8")

zip_path=Path("/mnt/data/Maison_Impeccable_site_web.zip")
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    z.write(html_path,"index.html")
    z.write(out/"README.txt","README.txt")

print(f"Site créé : {html_path}")
print(f"Pack ZIP : {zip_path}")
