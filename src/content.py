# -*- coding: utf-8 -*-
"""
NEWSPORTVISION — content source of truth.

Every string below is transcribed verbatim from the live site
(www.newsportvision.com, crawled 2026-09-14), English from the default
locale and Italian from ?lang=it. Nothing here is invented, summarised
or rewritten. Where the live site's Italian is missing, the key is set
to None and the builder falls back to English, exactly as the live site
does today.

Known source-side defects are preserved with a note rather than silently
"fixed"; see NOTES at the bottom of this file.
"""

SITE = {
    "domain": "https://www.newsportvision.com",
    "email": "office@newsportvision.com",
    "social": [
        ("Instagram", "https://www.instagram.com/newsportvision/"),
        ("Facebook", "https://www.facebook.com/New-Sport-Vision-197163350852306/"),
        ("Twitter", "https://twitter.com/NewSportVision1"),
    ],
    "entity": "SMACT DOO",
    "entity_address": "Via Danicareva 4 — 11118 Beograd — Serbia",
    "entity_vat": "P.I.B. 108912131",
    "bam_url": "http://www.bambasketballmovementhistory.com",
}

LANGS = ("en", "it")

# ---------------------------------------------------------------------------
# UI chrome
# ---------------------------------------------------------------------------

UI = {
    "en": {
        "skip": "Skip to content",
        "menu": "Menu",
        "close": "Close",
        "index": "Index",
        "nav_home": "Home",
        "nav_services": "SERVICES",
        "nav_products": "PRODUCTS",
        "nav_about": "ABOUT US",
        "nav_more": "More",
        "lang_name": "English",
        "lang_other": "Italiano",
        "lang_switch_label": "Switch language",
        "contact_line": "For Questions / Contact us at",
        "privacy": "Privacy & Cookie policy",
        "copyright": "© 2026 Newsportvsion",
        "back": "Back",
        "next": "Next",
        "view": "View",
        "open": "Open",
        "read": "Read",
        "colophon": "Colophon",
        "figure": "Fig.",
        "to_top": "Top of page",
        "in_this_page": "On this page",
        "external": "External site",
    },
    "it": {
        "skip": "Vai al contenuto",
        "menu": "Menu",
        "close": "Chiudi",
        "index": "Indice",
        "nav_home": "Home",
        "nav_services": "SERVIZI",
        "nav_products": "PRODOTTI",
        "nav_about": "CHI SIAMO",
        "nav_more": "More",
        "lang_name": "Italiano",
        "lang_other": "English",
        "lang_switch_label": "Cambia lingua",
        "contact_line": "For Questions / Contact us at",
        "privacy": "Privacy & Cookie policy",
        "copyright": "© 2026 Newsportvision",
        "back": "Indietro",
        "next": "Avanti",
        "view": "Vedi",
        "open": "Apri",
        "read": "Leggi",
        "colophon": "Colophon",
        "figure": "Fig.",
        "to_top": "Torna su",
        "in_this_page": "In questa pagina",
        "external": "Sito esterno",
    },
}

# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------

HOME = {
    "en": {
        "title": "Nsv | Italia | NewSportVision",
        "description": "NewSportVision is an international concept that deals with the "
                       "articulation of the new interests in sport. It was born in Milan "
                       "in 2014 and operates in Europe.",
        # hero — set as four lines exactly as the live site breaks them
        "hero": ["QUICK", "STEPS", "INTO THE SPORTS", "FUTURE"],
        "hero_kicker": "NEW TRENDS IN SPORT",
        "hero_sub": "A NEWSPORTVISION CONCEPT",
        "event_eyebrow": "coming next",
        "event_about": "ABOUT THE NEXT EVENT",
        "event_name": "FUTURESPORTFUTURE 2026",
        "event_date": "3 October 2026",
        "event_place": "Belgrade (Serbia)",
        "event_body": "It's time to talk about new chances of making sport the way to "
                      "improve the future. Who are the new stakeholders? Which are the "
                      "investments that should be done in the future of sport? Is there "
                      "an evolution? Should be.",
        "event_close": ["We see the new direction.", "NEWSPORTVISION."],
        "strap_moving": "NSV•MOVING FORWARD",
        "strap_ps": "PRODUCTS•SERVICES",
        "products_head": "THOSE LITTLE THINGS THAT MAKE EVERYDAY LIFE BETTER",
        "products_body": "All the products are the result of our direct experience. Sport "
                         "has great potentials. You need the right tools to express them all.",
        "services_head": "RIGHT SOLUTIONS FOR WHO IS LOOKING AT THE RIGHT WAY TO APPROACH SPORT",
        "services_body": "Services that NSV provides are customized. Professionalism and "
                         "flexibility is what you need. That's what we have.",
        "concept": [
            "NewSportVision is an international concept born in Milan in 2014.",
            "It operates in the northern European countries, Swiss, Serbia and Italy.",
            "The mission is to create an axis: culture - sport - art.",
            "Business is not an enemy of sport, but only if it is articulated.",
        ],
        "articulation": "NSV articulates interests in sport. There are much more targets "
                        "to achieve and stakeholders to detect, all the old techniques of "
                        "dealing with sport are coming to an end. New ways and styles are "
                        "needed to use all the potential that sport, as a social movement, "
                        "has. Media, enterprises, companies and institutions are not asked "
                        "to make any revolution, but an evolution is needed. NewSportVision "
                        "brings no revolution, but free evolution.",
        "learn_more": "learn more",
        "contact_invite": ["Contact us if you have something to say!",
                           "Don't be afraid, remember:",
                           "a good communication is the best start to Success."],
        "got_idea": "Got an idea?",
    },
    "it": {
        "title": "Nsv | Italia | NewSportVision",
        "description": "NewSportVision is an international concept that deals with the "
                       "articulation of the new interests in sport. It was born in Milan "
                       "in 2014 and operates in Europe.",
        "hero": ["CELERI", "PASSI", "NELLO SPORT DEL", "FUTURO"],
        "hero_kicker": "NUOVE TENDENZE NELLO SPORT",
        "hero_sub": "UN CONCETTO DI NEWSPORTVISION",
        "event_eyebrow": "prossimamente",
        "event_about": "RIGUARDO L'ULTIMO EVENTO/",
        "event_name": "FUTURESPORTFUTURE 2026",
        "event_date": "3 Ottobre 2026",
        "event_place": "BELGRADO (Serbia)",
        "event_body": "È tempo di parlare di nuove possibilità per fare dello sport la "
                      "strada per migliorare il futuro. Chi sono i nuovi stakeholder? "
                      "Quali sono gli investimenti da fare nel futuro dello sport? "
                      "C'è un'evoluzione? Dovrebbe esserci.",
        "event_close": ["Scopriamo le nuove direzioni .", "NEWSPORTVISION ."],
        "strap_moving": "NSV•PROCEDE IN AVANTI",
        "strap_ps": "PRODOTTI E SERVIZI",
        # NOTE: these two blocks are NOT translated on the live Italian site.
        # Preserved in English exactly as the source serves them.
        "products_head": "THOSE LITTLE THINGS THAT MAKE EVERYDAY LIFE BETTER",
        "products_body": "All the products are the result of our direct experience. Sport "
                         "has great potentials. You need the right tools to express them all.",
        "services_head": "RIGHT SOLUTIONS FOR WHO IS LOOKING AT THE RIGHT WAY TO APPROACH SPORT",
        "services_body": "Services that NSV provides are customized. Professionalism and "
                         "flexibility is what you need. That's what we have.",
        "concept": [
            "NewSportVision è un concept internazionale nato a Milano nel 2014.",
            "Opera nei paesi del nord Europa, Svizzera, Serbia e Italia.",
            "La mission è creare un asse: cultura - sport - arte.",
            "Il business non è nemico dello sport, ma solo se è articolato.",
        ],
        "articulation": "NSV articola gli interessi nello sport. Ci sono molti più "
                        "obiettivi da raggiungere e parti interessate da rilevare, tutte "
                        "le vecchie tecniche per affrontare lo sport stanno per esaurirsi. "
                        "Sono necessari nuovi modi e stili per utilizzare tutto il "
                        "potenziale che lo sport, come movimento sociale, ha. Ai media, "
                        "alle imprese, alle aziende e alle istituzioni non viene chiesto "
                        "di fare nessuna rivoluzione ma serve un'evoluzione. NewSportVision "
                        "non porta rivoluzione ma libera evoluzione.",
        "learn_more": "Per saperne di più",
        "contact_invite": ["Contattaci se hai qualcosa da dire!",
                           "Non aver paura, ricorda:",
                           "una buona comunicazione è il miglior inizio per raggiungere l'obbiettivo."],
        "got_idea": "Hai un'idea?",
    },
}

# ---------------------------------------------------------------------------
# PRODUCTS  (order and wording exactly as listed on /products)
# ---------------------------------------------------------------------------

PRODUCTS_INDEX = {
    "en": {
        "title": "PRODUCTS | newsportvision",
        "statement": "Sport without culture is a fake product.",
        "items": [
            ("guidelines",       "Guidelines",           "/guidelines"),
            ("my-12-seconds",    "My 12 Seconds",        "/work-in-progress"),
            ("books",            "Books",                "/books"),
            ("futuresportfuture","FutureSportFuture",    "/work-in-progress"),
            ("3-balls",          "3 Balls 1 Champion",   "/work-in-progress"),
            ("camst",            "Master Course: CAMST", "/work-in-progress"),
            ("back-to-school",   "Back to School",       "/work-in-progress"),
        ],
    },
    "it": {
        "title": "PRODUCTS | newsportvision",
        "statement": "Lo sport senza cultura non è un prodotto",
        "items": [
            ("guidelines",       "Guide",                "/guidelines"),
            ("my-12-seconds",    "I miei 12 secondi",    "/work-in-progress"),
            ("books",            "Libri",                "/books"),
            ("futuresportfuture","FuturoSportFuturo",    "/work-in-progress"),
            ("3-balls",          "3 Palloni 1 Campione", "/work-in-progress"),
            ("camst",            "Corso Master: CAMST",  "/work-in-progress"),
            ("back-to-school",   "Back to school",       "/work-in-progress"),
        ],
    },
}

SERVICES_INDEX = {
    "en": {
        "title": "SERVICES | newsportvision",
        "statement": "Sport without culture is a disservice.",
        "items": [
            ("help-desk", "Help Desk",                                "/help-desk"),
            ("parents",   "Association of Parents of Young Athletes", "/arms/"),
            ("nsv-pass",  "NSV Pass",                                 "/work-in-progress"),
        ],
    },
    "it": {
        "title": "SERVICES | newsportvision",
        "statement": "Lo sport senza cultura è un disservizio.",
        "items": [
            ("help-desk", "Help Desk",                        "/help-desk"),
            ("parents",   "Associazione Genitori Giovani Atleti", "/arms/"),
            ("nsv-pass",  "Tessera NSV",                      "/work-in-progress"),
        ],
    },
}

# ---------------------------------------------------------------------------
# The axis. "The mission is to create an axis: culture - sport - art."
#
# Every product, service and chapter of the history is placed on one of those
# three terms, and that placement is what gives it its colour. The reading:
#   CULTURE  what is published, taught or convened
#   SPORT    what is played, trained or practised
#   ART      what is made as a designed object
# ---------------------------------------------------------------------------

AXIS = {
    "guidelines":        "art",      # three printed, designed booklets
    "my-12-seconds":     "sport",
    "books":             "culture",
    "futuresportfuture": "culture",  # an international summit
    "3-balls":           "sport",
    "camst":             "culture",  # a master course
    "back-to-school":    "sport",
    "help-desk":         "sport",
    "parents":           "arms",     # the row that opens the ARMS chapter
    "nsv-pass":          "art",
}

AXIS_LABEL = {
    "en": {"culture": "Culture", "sport": "Sport", "art": "Art"},
    "it": {"culture": "Cultura", "sport": "Sport", "art": "Arte"},
}

# The history moves along the same axis: it begins as a school (sport), is
# recognised by a federation (culture), and becomes a concept (art).
CHAPTER_AXIS = ["sport", "sport", "culture", "art"]

# ---------------------------------------------------------------------------
# PRODUCT / SERVICE DETAIL PAGES
# ---------------------------------------------------------------------------

GUIDELINES = {
    "en": {
        "title": "GUIDELINES | newsportvision",
        "head": "GUIDELINES",
        "body": [
            "An attempt to give some short inputs to make everyday sport a better experience.",
            "3 chapters, What you should: Know, Do, Don't do. In each chapter you'll find 10 "
            "hints. It means that every Guideline has 30 advices for better sport enjoyment.",
            "There are three examples so far. Guidelines for: Parents, Young Athletes, Fans.",
            "These Guidelines can be customized with the graphics of your "
            "company-assotiation-brand and be used as a cool and useful promotive material.",
            "You can show that you care for your costumer health and lifestyle in an elegant "
            "and smart way.",
            "The format is 180X105 cm: light, pocket-size and it doesn't take too much "
            "attention to be read.",
            "Contact us to have more information or if you are interested.",
        ],
    },
    "it": {
        "title": "GUIDELINES | newsportvision",
        "head": "GUIDE",
        "body": [
            "Un tentativo di dare alcuni brevi input per rendere lo sport quotidiano "
            "un'esperienza migliore.",
            "3 capitoli, cosa dovresti: sapere, fare, non fare. In ogni capitolo troverai "
            "10 suggerimenti. Significa che ogni Guida contiene 30 consigli per una migliore "
            "fruizione dello sport.",
            "Ad oggi esiste una Guida per: Genitori, Giovani Atleti e Tifosi.",
            "Queste Guide possono essere personalizzate con la grafica della tua "
            "azienda-associazione-brand ed essere utilizzate come materiale promozionale "
            "fresco e utile.",
            "Puoi dimostrare che tieni alla salute e allo stile di vita dei tuoi clienti in "
            "modo elegante e intelligente.",
            "Il formato è 180X105 cm: leggero, tascabile e non richiede troppa attenzione "
            "per essere letto.",
            "Contattaci per avere maggiori informazioni o se sei interessato.",
        ],
    },
}

BOOKS = {
    "en": {
        "title": "BOOKS | newsportvision",
        "head": "BOOKS",
        "eyebrow": "abcdefg...",
        "body": [
            '"Verba volant. Scripta manent.". It sounds good but is not the reason why we '
            'are writing books.',
            "Sometimes it takes a lot of time to get somewhere, almost a life time. There is "
            "no chance to tell most people what you have achieved and conquered in your "
            "experience, so best way to tell to most people what you want is to write, then "
            "people will decide if your story is worth their time.",
            "The themes are many and also the authors. Our goal is to have a literature that "
            "permits our readers to be inspired and motivated to invest in sport. Money is "
            "not the only thing that can be object of an investment.",
            'NSV has specific manuals for investing "money&not" in sport. Those books are '
            "based on multi-sector and long studies.",
            "The year 2018 will be the one in which we'll make a big exit in terms of books.",
            'First edition will be "Articulation on New Interests in Sport & Management".',
            "If you want to be part of the story or if you want to be a partner of the "
            "project contact us.",
            "To learn more contact us too.",
        ],
    },
    "it": {
        "title": "BOOKS | newsportvision",
        "head": "LIBRI",
        "eyebrow": "abcdefg...",
        "body": [
            '"Verba volant. Scripta manent.". Suona bene, ma non è il motivo per cui abbiamo '
            "scritto e stiamo scrivendo libri.",
            "A volte ci vuole molto tempo per arrivare da qualche parte, quasi una vita. Non "
            "c'è possibilità di dire alla maggior parte delle persone ciò che hai raggiunto e "
            "conquistato nella tua esperienza, quindi il modo migliore per comunicare ciò che "
            "vuoi è scrivere. I lettori decideranno se la tua storia vale il loro tempo.",
            "I temi sono tanti e anche gli autori. Il nostro obiettivo è proporre una "
            "letteratura che permetta ai nostri lettori di essere ispirati e motivati ​​ad "
            "investire nello sport. Il denaro non è l'unica cosa che può essere oggetto di "
            "investimento.",
            'NSV ha manuali specifici per investire "money&not" nello sport.',
            'La prima edizione è stata "L\'articolazione dei nuovi interessi nello sport e '
            'nel management".',
            "Se vuoi essere parte di questa storia o se vuoi essere partner del progetto "
            "contattaci.",
        ],
    },
}

WORKSHOPS = {
    "en": {
        "title": "WORKSHOP | newsportvision",
        "head": "WORKSHOPS",
        "body": [
            "Connection is one of the words we like the most. Making new connections is as "
            "important as staying connected.",
            "One of the ways to make new connections, while keeping the previous, is "
            "organizing meetings and workshops.",
            "NSV organizes international summits all over Europe with the purpose of giving "
            "voice to new waves and products in sport's world.",
            "During the years the NSV network has grown a lot, that's the explanation for the "
            "caliber of the speakers and the audience.",
            "The first step is to find the right themes which are actual and have the "
            "potential to make changes in the near future. The second step is to find the "
            "right speakers, who have great skills and knowledge. The third step is to find "
            "the right audience, that can comprehend the messages and use them from the very "
            "next day after the event.",
            "The workshops have always an eclectic content, because NSV wants to preserve an "
            "axis in which strongly believes: culture-sport-art.",
            "This is the reason why during all the workshops an artistic exhibition is "
            "installed. Sport is the art of motion, at any level it's played, and without "
            "motion there is no art.",
            "If you are interested in making an event with us or to host an NSV event, "
            "contact us.",
            "To learn more don't hesitate to contact us too.",
        ],
    },
    "it": {
        "title": "WORKSHOP | newsportvision",
        "head": "LABORATORI",
        "body": [
            "Connessione è una delle parole che ci piace di più.",
            "Fare nuove connessioni è importante quanto rimanere in contatto.",
            "Uno dei modi per fare nuove connessioni, mantenendo le precedenti, è organizzare "
            "incontri e workshops.",
            "NSV organizza summit internazionali in tutta Europa con lo scopo di dare voce a "
            "nuove tendenze e prodotti nel mondo dello sport.",
            "Negli anni la rete NSV è cresciuta molto, ecco la spiegazione della caratura dei "
            "relatori e del pubblico.",
            "Il primo passo è trovare i temi giusti che siano reali e che abbiano il "
            "potenziale per apportare cambiamenti nel prossimo futuro. Il secondo passo è "
            "trovare i relatori giusti, dotati di grandi capacità e conoscenze. Il terzo "
            "passo è trovare il pubblico giusto, in grado di comprendere i messaggi e "
            "utilizzarli fin dal giorno successivo all'evento.",
            "I laboratori hanno sempre un contenuto eclettico, perché NSV vuole preservare un "
            "asse in cui crede fortemente: cultura-sport-arte.",
            "Questo è il motivo per cui durante tutti i workshops viene allestita una mostra "
            "artistica. Lo sport è l'arte del movimento, a qualsiasi livello venga praticato, "
            "e senza movimento non c'è arte.",
            "Se sei interessato a realizzare un evento con noi o ad ospitare un evento NSV, "
            "contattaci.",
        ],
    },
}

HELPDESK_NEWS = {
    "en": {
        "title": "NEW PRODUCT | newsportvision",
        "head": "HELP DESK",
        "body": [
            "New product was presented at the international summit FutureSportFuture, on "
            "Tuesday 21 November in Monza - Italy.",
            "Big news came.",
        ],
    },
    "it": {
        "title": "NEW PRODUCT | newsportvision",
        "head": "HEL DESK",   # NOTE: typo is on the live Italian page; preserved.
        "body": [
            "Il nuovo prodotto è stato presentato al summit internazionale FutureSportFuture, "
            "martedì 21 novembre a Monza - Italia.",
            "Sono arrivate grandi novità.",
        ],
    },
}

WORK_IN_PROGRESS = {
    "en": {
        "title": "WORK IN PROGRESS | newsportvision",
        "date": "8.02.2022",
        "lines": ["JUST A MOMENT. news are coming.", "COME BACK IN FEW DAYS."],
    },
    "it": {
        "title": "WORK IN PROGRESS | newsportvision",
        "date": "22.06.2022",
        "lines": ["SOLO UN MOMENTO. riordino estivo.", "TORNAte TRA qualche GIORNo."],
    },
}

# ---------------------------------------------------------------------------
# ABOUT — the history. Chapters are a presentational grouping of the
# existing paragraphs; not one word of the source text is altered.
# ---------------------------------------------------------------------------

ABOUT = {
    "en": {
        "title": "ABOUT US | newsportvision",
        "intro": [
            "NewSportVision is a new approach regarding the sport practice throughout the new "
            "products and services (see NSV Activities).",
            "NewSportVision promotes sports practice as an act of personal expression and "
            "personal culture.",
            "NewSportVision products and services aim to satisfy every specific need of any "
            "athlete (professional or not) , any sports organization or institution, school or "
            "university, any company or businessman, always regarding their sports activities "
            "or activities in some connection with sport (see NSV Help Desk).",
        ],
        "chapters": [
            {
                "year": "1989",
                "label": "BasketBam",
                "body": [
                    "NewSportVision Concept has a deep and long roots. In the first and the "
                    "deepest part of the NewSportVision background and history you'll find the "
                    "first private basketball school in Europe: BasketBam (6 April 1989, "
                    "Belgrade - Yugoslavia).",
                ],
            },
            {
                "year": "BAM",
                "label": "BAM Movement",
                "body": [
                    "After the great success in Yugoslavia the concept of small basketball "
                    "school became pan-European basketball movement (BAM Movement) devoted to "
                    "the development of a youth basketball (especially for the most numerous "
                    "category of players aged 12-15 years).",
                ],
            },
            {
                "year": "1999",
                "label": "Basket BAM",
                "body": [
                    "33 European countries took part in the BAM Movement Program. "
                    "International Basketball Federation (FIBA) officially recognized the BAM "
                    "Movement (1999, Malta). Actual system of the youth official competition "
                    "(European Championships) is based on the BAM Movement Concept established "
                    "on the end of the previous century (for more informationvisit "
                    "www.bambasketballmovementhistory.com or consult the book "
                    '"Sport del Futuro?").',
                ],
            },
            {
                "year": "2014",
                "label": "NewSportVision",
                "body": [
                    "Advanced stage and actual fase of the development of the BAM Movement "
                    "Concept brings a new title/name: NewSportVision. New period starts with "
                    'the organization of the International Summit titled "Il Ruolo del '
                    'Genitore nello Sport" ( 5 April 2014, Milano).',
                    "The reasons for choosing that date are clear, simple and significant: "
                    "25th anniversary of the BAM Movement and the International Day of Sport "
                    "for Development and Peace (6 April of every Year) proclaimed by the "
                    "General Assembly of the United Nations in August 2013.",
                ],
            },
        ],
    },
    "it": {
        "title": "ABOUT US | newsportvision",
        "intro": [
            "NewSportVision è un nuovo modo di approcciarsi allo sport, attraverso innovativi "
            "prodotti e servizi (vedi NSV Activities).",
            "NewSportVision promuove la pratica sportiva come atto di espressione e cultura "
            "personali.",
            "I prodotti e i servizi di NewSportVision mirano a soddisfare le nuove esigenza di "
            "qualsiasi atleta (professionista e non), organizzazione o istituzione sportiva, "
            "scuola, università, azienda e imprenditore che vuole evolvere il proprio modo di "
            "relazionarsi con il mondo dello sport.",
        ],
        "chapters": [
            {
                "year": "1989",
                "label": "BasketBam",
                "body": [
                    "NewSportVision Concept ha radici profonde e lunghe. Nella prima e più "
                    "profonda parte del background e della storia di NewSportVision si trova "
                    "la prima scuola privata di basket in Europa: BasketBam (6 aprile 1989, "
                    "Belgrado - Jugoslavia).",
                ],
            },
            {
                "year": "BAM",
                "label": "BAM Movement",
                "body": [
                    "Dopo il grande successo in Jugoslavia il concetto della piccola scuola di "
                    "pallacanestro è diventato un movimento paneuropeo di basket (BAM Movement) "
                    "dedicato allo sviluppo della pallacanestro giovanile (soprattutto per la "
                    "categoria più numerosa di giocatori, cioè quella di età compresa tra i "
                    "12-15 anni).",
                ],
            },
            {
                "year": "1999",
                "label": "Basket BAM",
                "body": [
                    "33 paesi europei hanno preso parte al BAM Movement Program. La "
                    "Federazione Internazionale di Basket (FIBA) ha riconosciuto ufficialmente "
                    "il Movimento BAM (1999, Malta). Il sistema attuale della competizione "
                    "ufficiale giovanile (Campionato Europeo) si basa sul BAM Movement Concept "
                    "stabilito alla fine del secolo scorso (per maggiori informazioni visita "
                    'www.bambasketballmovementishtory.com o consulta il libro "Sport del '
                    'Futuro?").',
                ],
            },
            {
                "year": "2014",
                "label": "NewSportVision",
                "body": [
                    "L'evoluzione di BAM Movement Concept porta un nuovo nome: NewSportVision, "
                    "che esordisce con l'organizzazione del Summit Internazionale "
                    '"Il Ruolo del Genitore nello Sport" (5 aprile 2014, Milano).',
                    "Le ragioni per scegliere quella data sono chiare, semplici e "
                    "significative: 25° anniversario del Movimento BAM e Giornata "
                    "Internazionale dello Sport per lo Sviluppo e la Pace (6 aprile di ogni "
                    "anno) proclamata dall'Assemblea Generale delle Nazioni Unite nell'agosto "
                    "2013.",
                ],
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# HELP DESK — the whole decision tree from /1, /home-hd and the 43
# duplicated "copia-di-*" pages, reassembled as one instrument.
# ---------------------------------------------------------------------------

HELPDESK = {
    "en": {
        "title": "HELP DESK | newsportvision",
        "eyebrow": "need help?",
        "head": "Help desk",
        "intro_a": "SPORT HELP DESK",
        "intro_b": "is meant to be used by:",
        "step1": "is meant to be used by",
        "step2": "which sport",
        "step3": "what do you need",
        "audiences": [
            ("person",     "every single person, adult or child"),
            ("clubs",      "sports clubs"),
            ("federation", "national or international sports federation"),
            ("institution","other sports organization or institution"),
            ("schools",    "schools"),
            ("universities","universities"),
            ("companies",  "companies"),
        ],
        "sport_q": ["Which is the appropriate sport for me?",
                    "Which is the appropriate sport for my child?"],
        "sports": [
            ("basketball", "basketball"),
            ("football",   "football"),
            ("volleyball", "volleyball"),
            ("tennis",     "tennis"),
            ("other",      "other"),
        ],
        "topics": [
            ("equipment",  "equipment"),
            ("supply",     "diet & supplementation"),
            ("injuries",   "injuries"),
            ("recovery",   "recovery"),
            ("training",   "training"),
            ("scouting",   "scouting"),
            ("legal",      "legal matters"),
        ],
        "topic_other_extra": ("any-other", "any other argument"),
        "org_topics": [("plans", "plans"), ("seminar", "seminar"), ("camps", "camps")],
        "form_head": "HELP DESK",
        "f_name": "Nome",
        "f_surname": "Cognome",
        "f_email": "Email",
        "f_phone": "Numero di Telefono",
        "f_insurance": "Sei assicurato con una di queste polizze?",
        "f_choose": "Scegli un'opzione.",
        "f_message": "Messaggio",
        "f_terms": "Accetto termini e condizioni",
        "f_send": "send",
        "f_sent": "The message has been delivered. You will be contacted soon.",
    },
    "it": {
        "title": "HELP DESK | newsportvision",
        "eyebrow": "hai bisogno di aiuto?",
        "head": "Help desk",
        "intro_a": "SPORT HELP DESK",
        "intro_b": "pensato per:",
        "step1": "pensato per",
        "step2": "quale sport",
        "step3": "di cosa hai bisogno",
        "audiences": [
            ("person",     "ogni singola persona, adulto o bambino"),
            ("clubs",      "società sportive"),
            ("federation", "federazione sportiva nazionale o internazionale"),
            ("institution","altra organizzazione o istituzione sportiva"),
            ("schools",    "scuole"),
            ("universities","università"),
            ("companies",  "aziende"),
        ],
        "sport_q": ["Qual'è lo sport adatto a me?",
                    "Qual'è lo sport adatto a mio figlio?"],
        "sports": [
            ("basketball", "pallacanestro"),
            ("football",   "calcio"),
            ("volleyball", "pallavolo"),
            ("tennis",     "tennis"),
            ("other",      "altro"),
        ],
        "topics": [
            ("equipment",  "equipment"),
            ("supply",     "diet & supplementation"),
            ("injuries",   "injuries"),
            ("recovery",   "recovery"),
            ("training",   "training"),
            ("scouting",   "scouting"),
            ("legal",      "legal matters"),
        ],
        "topic_other_extra": ("any-other", "any other argument"),
        "org_topics": [("plans", "plans"), ("seminar", "seminar"), ("camps", "camps")],
        "form_head": "HELP DESK",
        "f_name": "Nome",
        "f_surname": "Cognome",
        "f_email": "Email",
        "f_phone": "Numero di Telefono",
        "f_insurance": "Sei assicurato con una di queste polizze?",
        "f_choose": "Scegli un'opzione.",
        "f_message": "Messaggio",
        "f_terms": "Accetto termini e condizioni",
        "f_send": "send",
        "f_sent": "The message has been delivered. You will be contacted soon.",
    },
}

# ---------------------------------------------------------------------------
# PRIVACY — Italian legal text, served identically on both locales by the
# live site. Verbatim, split into its existing headings.
# ---------------------------------------------------------------------------

PRIVACY_TITLE = "Privacy | newsportvision"
PRIVACY_HEAD = "Informativa in materia di trattamento dei dati personali"

PRIVACY_LEAD = [
    "Informativa resa, ai sensi dell'art. 13 e segg. del Regolamento UE 679/2016, e degli "
    "artt. 13 e 122 del Codice in materia di protezione dei dati personali (D.Lgs. 196/03) "
    "resa a coloro che interagiscono con i servizi web di Newsportvision accessibili per via "
    "telematica a partire dal sito www.newsportvision.com e non anche per altri siti web "
    "eventualmente consultabili dall’Utente tramite link.",
    "Avviso agli Utenti europei: la presente informativa privacy è redatta in adempimento "
    "degli obblighi previsti dall’Art. 10 della Direttiva n. 95/46/CE, nonché a quanto "
    "previsto dalla Direttiva 2002/58/CE, come aggiornata dalla Direttiva 2009/136/CE, in "
    "materia di Cookie.",
]

PRIVACY_SECTIONS = [
    ("definizioni", "Definizioni", [
        "Dati Personali (o Dati): Costituisce dato personale qualunque informazione relativa a "
        "persona fisica, identificata o identificabile, anche indirettamente, mediante "
        "riferimento a qualsiasi altra informazione, ivi compreso un numero di identificazione "
        "personale.",
        "Dati di Utilizzo : Sono i dati personali raccolti in maniera automatica dal sito (o "
        "dalle applicazioni di parti terze che la stessa utilizza), tra i quali: gli indirizzi "
        "IP o i nomi a dominio dei computer utilizzati dall’Utente che si connette al sito, gli "
        "indirizzi in notazione URI (Uniform Resource Identifier), l’orario della richiesta, il "
        "metodo utilizzato nel sottoporre la richiesta al server, la dimensione del file "
        "ottenuto in risposta, il codice numerico indicante lo stato della risposta dal server "
        "(buon fine, errore, ecc.) il Paese di provenienza, le caratteristiche del browser e "
        "del sistema operativo utilizzati dal visitatore, le varie connotazioni temporali della "
        "visita (ad esempio il tempo di permanenza su ciascuna pagina) e i dettagli relativi "
        "all’itinerario seguito all’interno dell’Applicazione, con particolare riferimento alla "
        "sequenza delle pagine consultate, ai parametri relativi al sistema operativo e "
        "all’ambiente informatico dell’Utente.",
        "Utente: L’individuo che utilizza questo sito, che deve coincidere con l’Interessato o "
        "essere da questo autorizzato ed i cui Dati Personali sono oggetto del trattamento.",
        "Interessato: La persona fisica o giuridica cui si riferiscono i Dati Personali.",
        "Trattamento: Per Trattamento si intende qualsiasi operazione di dati (raccolta, "
        "registrazione, organizzazione, conservazione, consultazione, elaborazione, "
        "modificazione, selezione, estrazione, raffronto, utilizzo, interconnessione, blocco, "
        "comunicazione, diffusione, cancellazione e distruzione) effettuata con o senza "
        "l’ausilio di processi automatizzati.",
        "Titolare del Trattamento (o Titolare): La persona fisica, giuridica, la pubblica "
        "amministrazione e qualsiasi altro ente, associazione od organismo cui competono, anche "
        "unitamente ad altro titolare, le decisioni in ordine alle finalità, alle modalità del "
        "trattamento di dati personali ed agli strumenti utilizzati, ivi compreso il profilo "
        "della sicurezza, in relazione al funzionamento e alla fruizione di questo sito. Il "
        "Titolare del Trattamento, salvo quanto diversamente specificato, è il proprietario di "
        "questa Applicazione.",
        "Sito: Lo strumento hardware o software mediante il quale sono raccolti i Dati "
        "Personali degli Utenti.",
        "Cookie: Piccola porzione di dati conservata all’interno del dispositivo dell’Utente.",
    ]),
    ("tipologie", "Tipologie di Dati raccolti", [
        "Vi informiamo che a seguito della consultazione di questo sito possono essere trattati "
        "dati relativi a persone fisiche o giuridiche, enti od associazioni, identificate o "
        "identificabili.",
        "Fra i Dati Personali raccolti da questo sito, in modo autonomo o tramite terze parti, "
        "ci possono essere: Cookie, Dati di utilizzo, Numero di Telefono, Nome, Cognome ed "
        "Email. Altri Dati Personali raccolti potrebbero essere indicati mediante testi "
        "informativi visualizzati contestualmente alla raccolta dei Dati stessi. I Dati "
        "Personali possono essere inseriti volontariamente dall’Utente, oppure raccolti in modo "
        "automatico durante l’uso del sito. L’eventuale utilizzo di Cookie – o di altri "
        "strumenti di tracciamento – da parte di questo sito o dei titolari dei servizi terzi "
        "utilizzati, ove non diversamente precisato, ha la finalità di identificare l’Utente e "
        "registrare le relative preferenze per finalità strettamente legate all’erogazione del "
        "servizio richiesto dall’Utente. Il mancato conferimento da parte dell’Utente di alcuni "
        "Dati Personali potrebbe impedire l’erogazione dei servizi. L’Utente assume la "
        "responsabilità dei Dati Personali di terzi pubblicati o condivisi mediante questo sito "
        "e garantisce di avere il diritto di comunicarli o diffonderli, liberando il Titolare "
        "da qualsiasi responsabilità verso terzi.",
        "I dati così raccolti e i dati volontariamente forniti dagli Utenti formano oggetto di "
        "trattamento, in forma manuale e/o informatica, secondo i criteri di liceità, "
        "correttezza e nella piena tutela dei diritti e della riservatezza degli Utenti.",
    ]),
    ("titolare", "Titolare del Trattamento dei Dati", [
        "Il Titolare del Trattamento dei Dati personali è la Società SMACT DOO con sede legale "
        "in Via Danicareva 4 - 11118 Beograd - Serbia – P.I.B. 108912131 in persona del legale "
        "rappresentante pro tempore.",
    ]),
    ("modalita", "Modalità e luogo del trattamento dei Dati raccolti", [
        "<em>Modalità di trattamento</em>",
        "Il Titolare tratta i Dati Personali degli Utenti adottando le opportune misure di "
        "sicurezza volte ad impedire l’accesso, la divulgazione, la modifica o la distruzione "
        "non autorizzate dei Dati Personali.",
        "Il trattamento viene effettuato mediante operazioni di raccolta, registrazione, "
        "organizzazione, elaborazione, utilizzo, consultazione, conservazione sia attraverso "
        "supporti cartacei sia con l’ausilio di strumenti elettronici o telematici, con logiche "
        "e modalità strettamente connesse con le proprie finalità. Oltre al Titolare, in alcuni "
        "casi, potrebbero avere accesso ai Dati categorie di incaricati coinvolti "
        "nell’organizzazione del sito (personale amministrativo, commerciale, marketing, "
        "legali, amministratori di sistema) ovvero soggetti esterni (come fornitori di servizi "
        "tecnici terzi, corrieri postali, hosting provider, società informatiche, agenzie di "
        "comunicazione) nominati anche, se necessario, Responsabili del Trattamento da parte "
        "del Titolare. L’elenco aggiornato dei Responsabili potrà sempre essere richiesto al "
        "Titolare del Trattamento.",
        "I Dati Personali saranno trattati con mezzi manuali e/o elettronici ad accesso "
        "riservato al personale addetto, incaricati del trattamento da parte del Titolare. il "
        "Titolare ha predisposto le misure di sicurezza informatica necessarie per ridurre al "
        "minimo il rischio di violazione della privacy da parte di terzi e di quanti altri "
        "accedono al sito (persone fisiche o giuridiche) ed è in ogni momento pronto ad "
        "adottare ogni altra misura di sicurezza si dimostri necessaria.",
        "<em>Luogo</em>",
        "I Dati sono trattati presso le sedi operative del Titolare ed in ogni altro luogo in "
        "cui le parti coinvolte nel trattamento siano localizzate. Per ulteriori informazioni, "
        "contatta il Titolare.",
        "<em>Tempi</em>",
        "I Dati sono trattati per il tempo necessario allo svolgimento del servizio richiesto "
        "dall’Utente, o richiesto dalle finalità descritte in questo documento, e l’Utente può "
        "sempre chiedere l’interruzione del Trattamento o la cancellazione dei Dati.",
    ]),
    ("finalita", "Finalità del Trattamento dei Dati raccolti", [
        "I Dati dell’Utente sono raccolti per consentire al Titolare di fornire i propri "
        "servizi, così come per le seguenti finalità: Statistica, Affiliazione commerciale, "
        "Contattare l’Utente, erogazione di servizi.",
        "I dati personali potranno essere comunicati e/o messi a disposizione dei soggetti "
        "deputati all’espletamento delle relative mansioni all’interno dell’organizzazione del "
        "Titolare e/o all’esterno presso i soggetti dallo stesso incaricati. In particolare, i "
        "dati dell’Utente saranno trattati dai dipendenti e dai collaboratori del Titolare "
        "incaricati del trattamento che operano sotto la diretta autorità dello stesso ed hanno "
        "ricevuto, al riguardo, adeguate istruzioni operative. Oltre che dai soggetti appena "
        "citati, alcuni trattamenti dei dati personali dell’Utente, sempre per le finalità di "
        "cui alla presente informativa, potranno essere effettuati anche da soggetti terzi ai "
        "quali lo stesso Titolare affida incarichi funzionali allo svolgimento della sua "
        "attività. In tal caso gli stessi soggetti saranno designati come responsabili o "
        "incaricati del trattamento e riceveranno adeguate istruzioni operative, con "
        "particolare riferimento all’adozione delle misure minime di sicurezza, al fine di "
        "poter garantire la riservatezza e la sicurezza dei Dati. Alcuni dati potranno essere "
        "comunicati per esigenze finanziarie e di monitoraggio, resi disponibili per visite in "
        "loco da parte di eventuali Organi Giudiziari, di Polizia ed Amministrativi.",
    ]),
    ("dettagli", "Dettagli sul trattamento dei Dati Personali", [
        "I Dati Personali sono raccolti per le seguenti finalità ed utilizzando i seguenti "
        "servizi:",
        "<em>Contattare l’Utente</em>",
        "L’Utente, compilando con i propri Dati il modulo di contatto, acconsente al loro "
        "utilizzo per rispondere alle richieste di informazioni, di preventivo, o di qualunque "
        "altra natura indicata dall’intestazione del modulo. Dati personali raccolti: CAP, "
        "Cognome, Email, Nome e Numero di Telefono.",
        "<em>Statistica</em>",
        "I servizi contenuti nella presente sezione permettono al Titolare del Trattamento di "
        "monitorare e analizzare i dati di traffico e servono a tener traccia del comportamento "
        "dell’Utente. A tale scopo verranno raccolti Dati Personali per tracciare ed esaminare "
        "l’utilizzo di questo sito, compilare report e condividerli con altri servizi.",
        "<em>Interazione tramite form di contatto</em>",
        "Si applica alle richieste di consulenza online (tramite il servizio “Help Desk”), di "
        "suggerimenti ecc. Oltre ai dati espressamente inseriti dall'utente nella maschera "
        "(nome, cognome, numero di telefono ed Email), registriamo nei nostri database le "
        "seguenti informazioni:",
        "<ul><li>il consenso al trattamento dei dati in base alla presente informativa;</li>"
        "<li>l'indirizzo IP da cui provengono le richieste (questa informazione è classificata "
        "dal GDPR come \"dato personale\");</li>"
        "<li>il tipo di browser utilizzato e se si tratta di un dispositivo mobile;</li>"
        "<li>l'identificativo anonimo dell'utente creato da un algoritmo interno proprietario. "
        "L'identificativo è costruito in modo che non si possa risalire all'indirizzo IP "
        "dell'utente.</li>"
        "<li>in taluni casi anche la pagina del sito visitata immediatamente prima di inoltrare "
        "la richiesta.</li>"
        "<li>la data e l'ora dell'operazione.</li></ul>",
        "Relativamente alle richieste di consulenza inoltrate tramite il sito possono essere "
        "richiesti ulteriori documenti da inviare tramite Email per i quali si applica la "
        "disciplina del GDPR.",
        "<em>Visualizzazione di contenuti da piattaforme esterne</em>",
        "Questi servizi permettono di visualizzare contenuti ospitati su piattaforme esterne "
        "direttamente dalle pagine di questo sito e di interagire con essi. È possibile che "
        "anche se gli utenti non utilizzino questi servizi, essi raccolgano ugualmente dati di "
        "traffico relativi alle pagine in cui sono installati.",
        "<ul><li>Google Analytics</li><li>YouTube (Google)</li><li>Twitter</li>"
        "<li>Facebook.</li></ul>",
    ]),
    ("cookie", "Informazioni sui Cookie", [
        "I cookie sono brevi file di testo che vengono scaricati sul dispositivo dell’utente "
        "quando si visita un sito web. Ad ogni visita successiva i cookie sono reinviati al "
        "sito web che li ha originati (cookie di prime parti) o a un altro sito che li "
        "riconosce (cookie di terze parti). I cookie sono utili perché consentono a un sito web "
        "di riconoscere il dispositivo dell’utente. Essi hanno diverse finalità come, per "
        "esempio, consentire di navigare efficientemente tra le pagine, ricordare i siti "
        "preferiti e, in generale, migliorare l’esperienza di navigazione. Contribuiscono anche "
        "a garantire che i contenuti pubblicitari visualizzati online siano più mirati ad un "
        "utente e ai suoi interessi. In base alla funzione e alla finalità di utilizzo. In "
        "generale i cookie possono essere disattivati completamente nel proprio browser in "
        "qualsiasi istante.",
        "Dal momento che l’installazione dei Cookie e di altri sistemi di tracciamento operata "
        "da terze parti tramite i servizi utilizzati all’interno di questo sito non può essere "
        "tecnicamente controllata dal Titolare, ogni riferimento specifico a Cookie e sistemi "
        "di tracciamento installati da terze parti è da considerarsi indicativo. Per ottenere "
        "informazioni complete, consulta la privacy policy degli eventuali servizi terzi "
        "elencati in questo documento.",
    ]),
    ("ulteriori", "Ulteriori informazioni sul trattamento", [
        "<em>Difesa in giudizio</em>",
        "I Dati Personali dell’Utente possono essere utilizzati per la difesa da parte del "
        "Titolare in giudizio o nelle fasi propedeutiche alla sua eventuale instaurazione, da "
        "abusi nell’utilizzo della stessa o dei servizi connessi da parte dell’Utente. "
        "L’Utente dichiara di essere consapevole che il Titolare potrebbe essere richiesto di "
        "rivelare i Dati su richiesta delle pubbliche autorità.",
        "<em>Informative specifiche</em>",
        "Su richiesta dell’Utente, in aggiunta alle informazioni contenute in questa privacy "
        "policy, questo sito potrebbe fornire all’Utente delle informative aggiuntive e "
        "contestuali riguardanti servizi specifici, o la raccolta ed il trattamento di Dati "
        "Personali.",
        "<em>Log di sistema e manutenzione</em>",
        "Per necessità legate al funzionamento ed alla manutenzione, questo sito e gli "
        "eventuali servizi terzi da essa utilizzati potrebbero raccogliere Log di sistema, "
        "ossia file che registrano le interazioni e che possono contenere anche Dati Personali, "
        "quali l’indirizzo IP Utente.",
        "<em>Informazioni non contenute in questa policy</em>",
        "Maggiori informazioni in relazione al trattamento dei Dati Personali potranno essere "
        "richieste in qualsiasi momento al Titolare del Trattamento utilizzando le informazioni "
        "di contatto.",
    ]),
    ("diritti", "Esercizio dei diritti da parte degli Utenti", [
        "I soggetti cui si riferiscono i Dati Personali hanno il diritto in qualunque momento "
        "di ottenere la conferma dell’esistenza o meno degli stessi presso il Titolare del "
        "Trattamento, di conoscerne il contenuto e l’origine, di verificarne l’esattezza o "
        "chiederne l’integrazione, la cancellazione, l’aggiornamento, la rettifica, la "
        "trasformazione in forma anonima o il blocco dei Dati Personali trattati in violazione "
        "di legge, nonché di opporsi in ogni caso, per motivi legittimi, al loro trattamento. "
        "Le richieste vanno rivolte al Titolare del Trattamento. Questo sito non supporta le "
        "richieste “Do Not Track”.",
    ]),
    ("reclamo", "Diritto di reclamo", [
        "Gli Interessati hanno il diritto di ottenere dal Titolare del Trattamento, nei casi "
        "previsti, l’accesso ai propri dati personali e la rettifica o la cancellazione degli "
        "stessi o la limitazione del trattamento che li riguarda o di opporsi al trattamento "
        "(artt. 15 e segg. del Regolamento UE 679/2016) attraverso specifica richiesta rivolta "
        "a: <a href=\"mailto:office@newsportvision.com\">office@newsportvision.com</a>",
    ]),
    ("modifiche", "Modifiche a questa privacy policy", [
        "Il Titolare del Trattamento si riserva il diritto di apportare modifiche alla presente "
        "privacy policy in qualunque momento dandone pubblicità agli Utenti su questa pagina. "
        "Si prega dunque di consultare spesso questa pagina, prendendo come riferimento la data "
        "di ultima modifica indicata in fondo. Nel caso di mancata accettazione delle modifiche "
        "apportate alla presente privacy policy, l’Utente è tenuto a cessare l’utilizzo di "
        "questo sito e può richiedere al Titolare del Trattamento di rimuovere i propri Dati "
        "Personali. Salvo quanto diversamente specificato, la precedente privacy policy "
        "continuerà ad applicarsi ai Dati Personali sino a quel momento raccolti.",
    ]),
    ("about-policy", "Informazioni su questa privacy policy", [
        "Il Titolare del Trattamento dei Dati è responsabile per questa privacy policy "
        "conservata sui server dallo stesso scelti.",
    ]),
    ("profilazione", "Profilazione", [
        "Non sono svolti processi decisionali automatizzati sui dati aggregati se non "
        "finalizzati alla migliore gestione del sito.",
    ]),
    ("avvertenza", "Avvertenza", [
        "Non è possibile garantire che i servizi esterni al sito internet blocchino "
        "effettivamente l’installazione dei propri cookie o che questi utilizzino solo cookie "
        "proprio e non anche quelli di parti a loro terze. Per questo, qualora si voglia "
        "bloccarne l’installazione, è opportuno fornire o negare il proprio consenso "
        "direttamente sui siti internet delle parti terze, già elencati nella presente "
        "informativa.",
        "Vi preghiamo di prendere visione della seguente Privacy Policy e di controllarla "
        "periodicamente con attenzione al fine di verificare eventuali aggiornamenti o "
        "revisioni che si dovessero rendere necessari.",
    ]),
]

# ---------------------------------------------------------------------------
# MEDIA — every image is a real asset lifted from the live site.
# ---------------------------------------------------------------------------

MEDIA = {
    "skate": {
        "focus": "58% 36%",
        "src": "skate-architecture.jpg", "w": 1980, "h": 1200,
        "alt": {"en": "A skateboarder riding the curved steel wall of a concert hall.",
                "it": "Uno skateboarder sulla parete curva in acciaio di un auditorium."}},
    "leap": {
        "focus": "57% 38%",
        "src": "leap-street.jpg", "w": 2200, "h": 1466,
        "alt": {"en": "A runner mid-leap in an empty street, backlit by low sun.",
                "it": "Un corridore in salto in una strada vuota, controluce."}},
    "guides": {
        "focus": "50% 62%",
        "src": "guides-three.jpg", "w": 2200, "h": 1466,
        "alt": {"en": "Three printed NewSportVision guides laid on a wooden slab.",
                "it": "Tre guide NewSportVision stampate, appoggiate su un tagliere di legno."}},
    # The NSV Pass mark, as it is drawn on the live site. A designed object,
    # not a photograph — so it is shown whole, never cropped.
    "nsvpass": {
        "mark": True,
        "focus": "50% 50%",
        "src": "nsv-pass.png", "w": 512, "h": 512,
        "alt": {"en": "The NSV Pass mark.", "it": "Il marchio NSV Pass."}},
    # --- basketball, which is where this company actually begins -----------
    "basket_youth": {
        "focus": "50% 46%",
        "src": "basket-youth.jpg", "w": 2200, "h": 1466,
        "alt": {"en": "Children playing basketball in a gym, numbered shirts.",
                "it": "Bambini che giocano a basket in palestra, maglie numerate."}},
    "basket_hoop": {
        "focus": "44% 44%",
        "src": "basket-hoop.jpg", "w": 2200, "h": 1457,
        "alt": {"en": "A basketball dropping through the net, hands on the rim.",
                "it": "Un pallone da basket che entra nella retina, mani sul ferro."}},
    "coach_youth": {
        "focus": "46% 44%",
        "src": "coach-youth.jpg", "w": 2200, "h": 1466,
        "alt": {"en": "A coach going through a plan with young players in training bibs.",
                "it": "Un allenatore spiega uno schema a giovani giocatori in casacca."}},
    "school_bus": {
        "focus": "50% 62%",
        "src": "school-bus.jpg", "w": 2200, "h": 1463,
        "alt": {"en": "Schoolchildren standing together in front of a school bus.",
                "it": "Bambini davanti a uno scuolabus."}},
    "summit_room": {
        "focus": "50% 58%",
        "src": "summit-room.jpg", "w": 2200, "h": 1467,
        "alt": {"en": "A long table and chairs set for a meeting.",
                "it": "Un tavolo lungo apparecchiato per una riunione."}},
    "finish_line": {
        "focus": "42% 40%",
        "src": "finish-line.jpg", "w": 1024, "h": 682,
        "alt": {"en": "Runners crossing a finish line, race numbers, arms raised.",
                "it": "Corridori al traguardo, pettorali, braccia alzate."}},
    "course_room": {
        "focus": "50% 50%",
        "src": "course-room.jpg", "w": 1920, "h": 1280,
        "alt": {"en": "A workroom with desks laid out for a course.",
                "it": "Una sala di lavoro con banchi disposti per un corso."}},
    "gathering": {
        "focus": "50% 50%",
        "src": "gathering.jpg", "w": 2200, "h": 1579,
        "alt": {"en": "A crowd of people seen from above.",
                "it": "Una folla vista dall'alto."}},
    "guide_open": {
        "focus": "46% 42%",
        "src": "guide-open.jpg", "w": 2200, "h": 1466,
        "alt": {"en": "A hand holding an open NewSportVision guide.",
                "it": "Una mano che tiene aperta una guida NewSportVision."}},
    "court": {
        "focus": "50% 50%",
        "src": "court-lines.jpg", "w": 2200, "h": 1472,
        "alt": {"en": "White court lines dividing green and terracotta playing surfaces.",
                "it": "Linee bianche che dividono superfici di gioco verde e terracotta."}},
    "desk": {
        "focus": "50% 52%",
        "src": "desk-editorial.jpg", "w": 2200, "h": 2200,
        "alt": {"en": "An overhead desk scene with magazines, a laptop and hand lettering.",
                "it": "Una scrivania vista dall'alto con riviste, un portatile e un lettering."}},
}

# ---------------------------------------------------------------------------
# REDIRECTS — every legacy Wix URL keeps working.
# ---------------------------------------------------------------------------

# Destinations carry their trailing slash so a host never has to add one:
# without it every legacy link costs two hops instead of one.
REDIRECTS = {
    "/1": "/help-desk/",
    "/home-hd": "/help-desk/",
    "/helpdesk": "/help-desk/news/",
    "/workshop": "/workshops/",
    "/about-us": "/about/",
    "/shop": "/products/",
    "/product-page/sono-un-prodotto-1": "/products/",
    "/product-page/sono-un-prodotto-2": "/products/",
    "/product-page/sono-un-prodotto-5": "/products/",
}

# Every "copia-di-*" / "hd-*" Help Desk duplicate, mapped onto the step of the
# instrument it represented. Slug -> live page title -> new deep link.
_HD = {
    "hd-basketball":                  "sport=basketball",
    "hd-basketball-equipment":        "sport=basketball&topic=equipment",
    "hd-basketball-supply":           "sport=basketball&topic=supply",
    "copia-di-basket-supply":         "sport=basketball&topic=injuries",
    "copia-di-basketball-injuries":   "sport=basketball&topic=training",
    "copia-di-basketball-training":   "sport=basketball&topic=scouting",
    "copia-di-basketball-scouting":   "sport=basketball&topic=legal",
    "copia-di-3":                     "sport=football",
    "copia-di-football-1":            "sport=football&topic=equipment",
    "copia-di-football-equipment":    "sport=football&topic=supply",
    "copia-di-football-supply":       "sport=football&topic=injuries",
    "copia-di-football-injuries":     "sport=football&topic=training",
    "copia-di-football-training":     "sport=football&topic=scouting",
    "copia-di-football-scouting":     "sport=football&topic=legal",
    "copia-di-football":              "sport=volleyball",
    "copia-di-volleyball-1":          "sport=volleyball&topic=equipment",
    "copia-di-volley-equipment":      "sport=volleyball&topic=supply",
    "copia-di-volley-supply":         "sport=volleyball&topic=injuries",
    "copia-di-volley-injuries":       "sport=volleyball&topic=training",
    "copia-di-volley-training":       "sport=volleyball&topic=scouting",
    "copia-di-volley-scouting":       "sport=volleyball&topic=legal",
    "copia-di-volleyball":            "sport=tennis",
    "copia-di-tennis-1":              "sport=tennis&topic=equipment",
    "copia-di-tennis-equipment":      "sport=tennis&topic=supply",
    "copia-di-tennis-supply":         "sport=tennis&topic=injuries",
    "copia-di-tennis-injuries":       "sport=tennis&topic=training",
    "copia-di-tennis":                "sport=other",
    "copia-di-email-basketball":      "sport=basketball&step=contact",
    "copia-di-email-football":        "sport=volleyball&step=contact",
    "copia-di-email-volley":          "sport=tennis&step=contact",
    "copia-di-email-tennis":          "sport=other&step=contact",
    "copia-di-email-which-sport":     "who=person&step=contact",
    "copia-di-email-which-sport-1":   "who=person&step=contact",
    "copia-di-volley-legal":          "who=clubs",
    "copia-di-football-training-1":   "who=federation",
    "copia-di-basketball-injuries-1": "who=institution",
    "copia-di-tennis-training":       "who=schools",
    "copia-di-volley-supply-1":       "who=clubs&topic=camps",
    "copia-di-email-clubs":           "who=federation&step=contact",
    "copia-di-email-federation":      "who=institution&step=contact",
    "copia-di-email-institution":     "who=schools&step=contact",
    "copia-di-email-volley-1":        "who=clubs&step=contact",
    "copia-di-volley-training-1":     "who=clubs&topic=plans",
}
for _slug, _q in _HD.items():
    REDIRECTS["/" + _slug] = "/help-desk/?" + _q

# The "sport advisor" partner portals were empty shells on the live site
# (a header and nothing else). They keep their URLs and land on the Help Desk.
for _slug in ("active-benessere-sport-advisor", "formula-salute-sport-advisor",
              "salute-piu-benessere-sport-advisor", "tua-benessere-sport-advisor",
              "portale-benessere-sport-advisor-home"):
    REDIRECTS["/" + _slug] = "/help-desk/"

# ---------------------------------------------------------------------------
# NOTES on source-side defects, deliberately preserved rather than corrected:
#
#  1. Footer copyright reads "Newsportvsion" in English and "Newsportvision"
#     in Italian. Both are kept as served.
#  2. The Italian Help Desk news page heading reads "HEL DESK".
#  3. The Italian homepage leaves the Products and Services blurbs in English.
#  4. The English About text reads "for more informationvisit" with no space.
#  5. The Italian About page prints www.bambasketballmovementishtory.com
#     (transposed letters, dead). The printed text is left exactly as served;
#     only the href is pointed at the working spelling so the link resolves.
#  6. The Italian and English "work in progress" pages carry different dates
#     and different messages. Both are preserved.
# ---------------------------------------------------------------------------
