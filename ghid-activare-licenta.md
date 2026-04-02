# Cum activez licența pentru o integrare Home Assistant

## De ce există un sistem de licențiere?

Fiecare integrare din acest proiect este scrisă, testată și întreținută de o singură persoană. Și nu e doar cod — în spatele fiecărei integrări e un proces continuu: reverse engineering al aplicațiilor mobile ale furnizorilor pentru a înțelege cum comunică cu serverele lor, debugging pe zeci de scenarii diferite, analiză cu ajutorul inteligenței artificiale pentru a accelera dezvoltarea și a rezolva probleme complexe, adaptare la fiecare actualizare Home Assistant care poate strica compatibilitatea, și monitorizarea constantă a API-urilor care se pot schimba fără preaviz.

La asta se adaugă infrastructura reală care costă bani în fiecare lună: servere de licențiere, domenii, certificate SSL, baze de date, și sistemul automat de emitere și validare a licențelor. Plus documentația, suportul oferit pe GitHub, și timpul investit în fiecare bug raportat.

Toate astea consumă timp, energie și bani — iar pe termen lung, nu e sustenabil fără sprijinul comunității.

Sistemul de licențiere nu e o barieră pusă din dorința de a monetiza. E un mod prin care proiectul poate continua să existe și să crească. Fiecare contribuție, oricât de mică, face diferența. Tu, ca utilizator, ești partea cea mai importantă din ecuație — fără implicarea ta, aceste integrări pur și simplu nu ar mai putea fi menținute la zi.

## Perioadă de test — 30 de zile, fără restricții

Când instalezi o integrare pentru prima dată, ai la dispoziție **30 de zile** în care totul funcționează complet, fără nicio limitare. Nu trebuie să introduci niciun cod, nu trebuie să faci nimic special — pur și simplu folosești integrarea ca și cum ar fi fost dintotdeauna acolo.

După cele 30 de zile, dacă nu ai activat o licență, integrarea va afișa un senzor cu mesajul **„Licență necesară"** în locul datelor obișnuite. Nimic nu se șterge, nimic nu se pierde — pur și simplu datele nu mai sunt afișate până la activarea licenței.

## Cum obțin o licență?

Simplu — prin susținerea proiectului pe [Buy Me a Coffee](https://buymeacoffee.com/cnecrea).

Nu e un abonament, nu e o plată lunară. E o contribuție unică, echivalentul unei cafele, prin care spui „apreciez munca asta și vreau să continue". Atât.

Foarte important: **introdu corect adresa de email** la contribuție, pentru că pe aceasta vei primi automat cheia de licență.

## Formatul cheilor de licență

Fiecare integrare are un prefix unic, ca să știi imediat pentru ce e cheia primită:

| Integrare | Exemplu cheie | Nume complet | Trial |
|-----------|--------------|--------------|:-----:|
| myelectrica | `MELC-XXXX-XXXX-XXXX-XXXX` | MyElectrica | 30 zile |
| eonmyline | `EONL-XXXX-XXXX-XXXX-XXXX` | E-ON myLine | 30 zile |
| hidroelectrica | `HDEL-XXXX-XXXX-XXXX-XXXX` | Hidroelectrica | 30 zile |
| opcom | `OPCM-XXXX-XXXX-XXXX-XXXX` | OPCOM | 30 zile |
| vehicule | `VULE-XXXX-XXXX-XXXX-XXXX` | Vehicule | 30 zile |
| erovinieta | `EROV-XXXX-XXXX-XXXX-XXXX` | CNAIR eRovinieta | 30 zile |

## Pași pentru activare

**1.** Deschide Home Assistant și mergi la **Setări** → **Dispozitive și servicii**, apoi selectează integrarea pentru care ai primit licența.

**2.** Apasă pe butonul **Configurare** (sau **Opțiuni**, în funcție de versiunea HA). Vei vedea un câmp unde poți introduce cheia de licență.

**3.** Copiază cheia primită pe email (de exemplu: `MELC-A1B2-C3D4-E5F6-G7H8`) și lipește-o în câmpul **Cheie de licență**. Apoi apasă **Salvează**.

**4.** Gata! Integrarea verifică automat licența și totul e funcțional.

## Ce se întâmplă în fiecare scenariu?

**Integrare cu licență activă** — nu trebuie să faci nimic. Totul funcționează normal, senzorii afișează datele, iar licența se validează automat în fundal. Pur și simplu folosești integrarea.

**Integrare în perioada de test (trial)** — la fel, totul funcționează complet. Singura diferență e că ai un interval de 30 de zile de la prima instalare. În acest timp nu ai nevoie de nicio cheie.

**Integrare fără licență (trial expirat)** — senzorii nu vor mai afișa date, în locul lor apare un senzor cu mesajul **„Licență necesară"**. Nimic nu se șterge, configurația rămâne intactă — odată ce introduci licența, totul revine instant la normal.

**După activarea licenței** — senzorul „Licență necesară" dispare automat, iar datele tale revin în câteva secunde. Nu trebuie să repornești Home Assistant sau să reconfigurezi ceva.

## Lucruri bune de știut

Licența este **perpetuă** — o primești o singură dată și rămâne activă. Nu expiră, nu trebuie reînnoită.

Dacă **reinstalezi Home Assistant**, licența poate fi reemisă fără nicio problemă. Scrie-ne și rezolvăm.

Dacă faci **restore din backup**, licența rămâne activă automat — nu trebuie să faci nimic.

Contribuția ta nu e legată de o singură integrare — **susții proiectul în ansamblu**. O cafea, toate integrările.

## Susținerea continuă contează

Costurile din spatele proiectului nu sunt o cheltuială unică — serverele, domeniile, certificatele și infrastructura se plătesc în fiecare lună, iar munca de întreținere nu se oprește niciodată. O contribuție nu rezolvă problema pentru totdeauna, ci ajută în momentul în care e făcută.

De aceea, orice susținere suplimentară este întotdeauna binevenită. Dacă integrările îți sunt utile în continuare și vrei să te asiguri că proiectul merge mai departe, poți reveni oricând pe [Buy Me a Coffee](https://buymeacoffee.com/cnecrea). Nu e o obligație — e doar un mod prin care poți spune „continuă, merge bine".

## Ai nevoie de ajutor?

Dacă ai întâmpinat vreo problemă cu activarea, dacă nu ai primit licența pe email, sau dacă pur și simplu ai o întrebare — deschide un [Discuții pe GitHub](https://github.com/cnecrea/cnecrea/discussions) sau scrie-ne direct. Suntem aici și răspundem cu drag.

Mulțumim că faci parte din comunitate.
