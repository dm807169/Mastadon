#!/usr/bin/env python3
# fediverse_bot.py
# Landroverfarm Press — Poem of the Day
# Copyleft 2025 — david merritt — lrfpress@gmail.com
# No permission required. Share, reuse, modify.

#v0.1.1.a
#fixes by gemini + HOLO

import random
import csv
import io
from mastodon import Mastodon

# — Configuration —
# Replace these with your actual instance and token.
FEDIVERSE_INSTANCE_URL = 'INSTANCE_HERE'  # e.g., mastodon.social, fosstodon.org
ACCESS_TOKEN = 'TOKEN_HERE'  # Generate in your Fediverse account settings

# — Initialize Mastodon Client —
def create_mastodon_client():
    try:
        mastodon = Mastodon(
            access_token=ACCESS_TOKEN,
            api_base_url=FEDIVERSE_INSTANCE_URL
        )
        # Test connection
        mastodon.account_verify_credentials()
        print("✅ Connected to Fediverse instance.")
        return mastodon
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return None

# — Your Full Catalog Data —
CATALOG_DATA_CSV = '''isbn,title,first published,format,notes,collections,status,type,moods,themes
9780985295208,geek prayers,2008,"32p, A6 collection","geek prayer #4, 9, 17, 22 also A3 foldouts",Geek Prayers,active,collection,"contemplative, ritualistic, ironic","technology, spirituality, code-as-prayer"
9780985295215,"sniper rifle",2008,A3 foldout,"Also in Coalface collection",Coalface,active,foldout,"tense, violent, surreal","war, masculinity, absurdity"
9780985295222,"inorganic 1, 2, 3.",2008,"12p, A5","Also A3 foldout #1, 2, 3.",Mixture of Wishes,active,foldout,"detached, clinical, observational","industry, alienation, systems"
9780985295239,first friday out,2008,A5 foldout,"Also in fiddlesticks",fiddlesticks,active,foldout,"wistful, nostalgic, fleeting","work, release, ritual"
9780985295246,grist,2008,"48p, A5","38 poem collection",,active,collection,"weary, rhythmic, grounded","labour, repetition, survival"
9780985295253,"12 steps / microsoft addict",2008,A5 foldout,"Also in fiddlesticks",fiddlesticks,active,foldout,"self-aware, ironic, anxious","addiction, tech, identity"
9780985295260,"matt is a geek, 13.",2008,A5 foldout,"Also in fiddlesticks",fiddlesticks,active,foldout,"proud, defiant, youthful","identity, nerd culture, belonging"
9780985295277,"up through the gears",2008,A5 foldout,"Also in fiddlesticks",fiddlesticks,active,foldout,"kinetic, striving, mechanical","progress, effort, motion"
9780985295284,"a mixture of wishes",2008,"44p, A3/A4/A5","36 poem collection",Mixture of Wishes,active,collection,"melancholy, hopeful, fragmented","desire, loss, longing"
9780985295291,nice things,2008,A3 foldout,"",Mixture of Wishes,active,foldout,"bittersweet, ironic, tender","small joys, irony, everyday beauty"
9780986459504,"not sleeping, eh?",2009,A3 foldout,"",Mixture of Wishes,active,foldout,"insomniac, restless, intimate","anxiety, night, connection"
9780986459511,"BOXSETS + POETRY BRICKS",2009,"A3 poems in boxes","10, 12, 15, 20, 25, 40 poems",,active,boxset,"playful, conceptual, tactile","form, materiality, distribution"
9780986459528,curious diets,2009,A3 foldout,"",Mixture of Wishes,active,foldout,"absurd, satirical, bodily","consumption, control, body"
9780986459535,hydrosliding,2009,A3 foldout,"Also in Overdraft",Overdraft,active,foldout,"fluid, unstable, precarious","debt, balance, collapse"
9780986459542,tepid pool,2009,A3 foldout,"",Mixture of Wishes,active,foldout,"apathetic, stagnant, ironic","indifference, waiting, inertia"
9780986459559,machine shop,2009,A3 foldout,"Also in Mixture of Wishes + Pastoral",Mixture of Wishes,Pastoral,active,foldout,"industrial, rhythmic, grounded","labour, machinery, rural industry"
9780986459566,speed of sound,2009,A3 foldout,"Also in Mixture of Wishes collection",Mixture of Wishes,active,foldout,"urgent, fast, transient","velocity, communication, rupture"
9780986459573,"sad dog, happy dog",2009,A3 foldout,"The best friend collection",Best Friend,active,foldout,"tender, mournful, loyal","animals, companionship, grief"
9780986459580,why i am copyleft,2009,A5 foldout,"Also in fiddlesticks",fiddlesticks,active,foldout,"defiant, political, principled","open source, resistance, ethics"
9780986459597,bigger picture,2009,A3 foldout,"Also in Mixture of Wishes collection",Mixture of Wishes,active,foldout,"reflective, distanced, philosophical","perspective, scale, meaning"
9780987654908,kibble,2010,"46p, A5 & A6","30 poem collection",,active,collection,"crumbly, fragmented, everyday","scraps, survival, minimalism"
9780987654915,datura,2010,A3 foldout,"55 5-Minute poems collection",5-Minute Poems,active,foldout,"hallucinatory, dreamlike, dangerous","toxicity, altered states, risk"
9780987654922,barcode,2010,"46p, A5","32 poem collection",,active,collection,"systematic, coded, detached","surveillance, identity, data"
9780987654939,"where you at bro? (Auto-bio note #9)",2010,A5 foldout,"Also in fiddlesticks + Coalface",fiddlesticks,Coalface,active,foldout,"casual, urgent, fraternal","friendship, location, connection"
9780987654946,"good wish list #8",2010,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"hopeful, ironic, fragile","desire, futility, kindness"
9780987654953,inconsolable,2010,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"grieving, raw, unredeemed","loss, mourning, isolation"
9780987654960,migration,2010,A3 foldout,"Also in Coalface",Coalface,active,foldout,"weary, inevitable, moving","displacement, labour, journey"
9780987654977,optimist,2010,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"ironic, fragile, hopeful","resilience, doubt, perseverance"
9780987654984,if you ask,2010,A3 foldout,"Also in Coalface",Coalface,active,foldout,"guarded, conditional, wary","trust, vulnerability, silence"
9780987654991,"motherly advice",2010,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"warm, nostalgic, instructive","family, care, memory"
9780987667601,"coffee x5",2011,"A3 foldout, A5 12p","5 poem collection",,active,"foldout+booklet","ritualistic, habitual, caffeinated","routine, repetition, small comforts"
9780987667618,"how to be a hen",2011,A3 foldout,"Also in Pastoral",Pastoral,active,foldout,"absurd, instructional, rural","animals, domesticity, survival"
9780987667625,"rural interlude",2011,A3 foldout,"Also in Pastoral",Pastoral,active,foldout,"peaceful, temporary, observational","countryside, pause, reflection"
9780987667632,"death of Mrs. Stalin",2011,A3 foldout,"Also in Pastoral",Pastoral,active,foldout,"surreal, darkly comic, absurd","history, myth, rural legend"
9780987667649,"a poetical aside",2011,A3 foldout,"Also in Coalface",Coalface,active,foldout,"wry, meta, self-aware","poetry, craft, interruption"
9780987667656,"speak, act, fantail",2011,A3 foldout,"Also in Pastoral",Pastoral,active,foldout,"urgent, fragmented, ecological","nature, communication, birds"
9780987667663,hiatus,2011,A3 foldout,"Also in Coalface",Coalface,active,foldout,"quiet, suspended, waiting","pause, rest, breath"
9780987667670,"what is the rub?",2011,A5 foldout,"Also in fiddlesticks",fiddlesticks,active,foldout,"frustrated, interrogative, sharp","conflict, friction, struggle"
9780987667687,"taumarunui railway station #1",2011,A3 foldout,"",You Sleep Uphill,active,foldout,"lonely, liminal, observational","transit, small towns, waiting"
9780987667694,"taumarunui railway station #7",2011,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"nostalgic, specific, quiet","place, memory, journey"
,,ache / burn / long,2012,A3 foldout,"Also in Pastoral",Pastoral,active,foldout,"aching, persistent, physical","pain, endurance, body"
,,"a visitor with an empty soul",2012,A3 foldout,"",,withdrawn,foldout,"haunted, hollow, spectral","loneliness, absence, identity"
,,the process,2012,A3 foldout,"Also in Coalface",Coalface,active,foldout,"methodical, relentless, procedural","work, systems, repetition"
,,determination,2012,A3 foldout,"Also in Mixture of Wishes + Coalface",Mixture of Wishes,Coalface,active,foldout,"resolute, stubborn, focused","will, effort, survival"
,,watching things fall apart,2012,A3 foldout,"Also in Coalface",Coalface,active,foldout,"helpless, observational, sad","decay, collapse, witnessing"
,,locks/cops,2012,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"paranoid, tense, surveilled","control, authority, resistance"
,,dinner, not!,2012,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"frustrated, abrupt, domestic","family, conflict, refusal"
,,retrospective,2012,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"reflective, distant, evaluative","memory, time, self"
,,time of mess,2012,A3 foldout,"",,withdrawn,foldout,"chaotic, overwhelmed, raw","confusion, breakdown, emotion"
,,two!,2012,A3 foldout,"2 poems; New editions 2016, 2021",,active,foldout,"minimal, emphatic, dual","duality, contrast, brevity"
,,geek prayer #4,2013,A3 foldout,"Also in Geek Prayers",Geek Prayers,active,foldout,"ritualistic, devotional, digital","code, faith, repetition"
,,geek prayer #9,2013,A3 foldout,"Also in Geek Prayers",Geek Prayers,active,foldout,"ritualistic, devotional, digital","code, faith, repetition"
,,minimum wage slaves,2013,A3 foldout,"Also in fiddlesticks",fiddlesticks,active,foldout,"angry, defiant, exploited","labour, class, resistance"
,,no blame,2013,A3 foldout,"",,withdrawn,foldout,"resigned, numb, detached","apathy, acceptance, silence"
,,fiddlesticks,2013,"36p, A5","14 poem/rants collection",fiddlesticks,active,collection,"frenetic, ranting, energetic","anger, absurdity, protest"
,,"a small crisis of mid-career confidence",2013,"12p, A6","1 poem; Also Compound Press 2018",,active,booklet,"anxious, self-doubting, wry","identity, creativity, doubt"
,,"today / contents of pockets",2013,"16p, A6","2 poems",,active,booklet,"intimate, observational, tactile","everyday, self, materiality"
,,"beach scene #25",2013,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"still, reflective, coastal","nature, memory, pause"
,,"broken / embrace",2013,A3 foldout,"",,active,foldout,"contradictory, tender, fractured","love, damage, intimacy"
,,"mixed intellects",2013,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"confused, collaborative, chaotic","thought, dialogue, dissonance"
,,"morning tea #3-5",2013,A3 foldout,"2 poems",,active,foldout,"domestic, routine, quiet","ritual, pause, connection"
,,"pause / refresh",2013,A3 foldout,"",,active,foldout,"digital, breathless, temporary","technology, rest, reboot"
,,"android app#1 nicotine addicts",2013,A3 foldout,"12p A6",Fiddlesticks,active,foldout,"addicted, mechanical, ironic","habit, tech, dependency"
,,"perfect fit",2013,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"tender, resolved, intimate","love, belonging, connection"
,,"the fear",2013,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"dread, anticipatory, bodily","anxiety, vulnerability, presence"
,,"trigger",2013,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"reactive, sudden, psychological","trauma, memory, response"
,,vote,2014,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"urgent, civic, fragile","democracy, hope, agency"
,,geek prayer #17,2014,A3 foldout,"Also in Geek Prayers",Geek Prayers,active,foldout,"ritualistic, devotional, digital","code, faith, repetition"
,,bodies,2014,A3 foldout,"Also in Pastoral + You Sleep Uphill",Pastoral,You Sleep Uphill,active,foldout,"physical, present, vulnerable","body, intimacy, mortality"
,,geek prayers 3rd edition,2014,36p A6,"IBM punchcard cover",,active,collection,"mechanical, sacred, nostalgic","technology, ritual, memory"
,,coalface,2014,A3 foldout,"Also in Coalface collection",Coalface,active,foldout,"harsh, enduring, industrial","labour, struggle, survival"
,,I did not invent,2014,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"defiant, humble, existential","self, origin, authenticity"
,,#13; the mongrel,2014,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"hybrid, wild, untamed","identity, mix, resistance"
,,tail lights,2014,A3 foldout,"Also in Pastoral",Pastoral,active,foldout,"fleeting, observational, moving","departure, distance, memory"
,,wander,2014,A3 foldout,"",,active,foldout,"aimless, free, searching","journey, uncertainty, exploration"
,,traction,2014,A3 foldout,"Also in Coalface",Coalface,active,foldout,"gripping, effortful, mechanical","progress, resistance, force"
,,First Friday out,2014,A6 12p,"1 poem; New edition",Fiddlesticks,active,booklet,"nostalgic, ritualistic, release","work, weekend, repetition"
,,canary,2014,A3 foldout,"Also in Coalface",Coalface,active,foldout,"warning, fragile, symbolic","danger, sensitivity, labour"
,,geek prayer #22,2014,A3 foldout,"IBM punchcard cover; Also in Geek Prayers",Geek Prayers,active,foldout,"ritualistic, devotional, digital","code, faith, repetition"
,,holiday,2014,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"bittersweet, absent, ironic","escape, longing, absence"
,,we already half dress for war,2015,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"precarious, anticipatory, collective","conflict, readiness, society"
,,"The lover's table #3",2015,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"intimate, domestic, fragile","love, relationship, care"
,,"entwined",2015,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"connected, physical, inseparable","love, unity, bodies"
,,currencies,2015,A3 foldout,"Also in Coalface + You Sleep Uphill",Coalface,You Sleep Uphill,active,foldout,"exchange, value, unstable","economy, emotion, debt"
,,nerves,2015,A3 foldout,"Also in Coalface + You Sleep Uphill",Coalface,You Sleep Uphill,active,foldout,"tense, bodily, reactive","anxiety, sensitivity, response"
,,"how death works #1",2015,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"clinical, curious, calm","mortality, process, acceptance"
,,"how death works #3",2015,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"clinical, curious, calm","mortality, process, acceptance"
,,"morning tea #7",2015,A3 foldout,"Also in Coalface + You Sleep Uphill",Coalface,You Sleep Uphill,active,foldout,"domestic, routine, quiet","ritual, pause, connection"
,,simple hunger,2015,A3 foldout,"",,withdrawn,foldout,"primal, raw, basic","need, desire, survival"
,,"lifeboat #9",2015,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"precarious, hopeful, survival","rescue, crisis, hope"
,,bless,2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"grateful, quiet, sacred","grace, presence, thanks"
,,block the sun,2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"defiant, protective, intense","love, shielding, passion"
,,early/late,2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"temporal, ambiguous, relational","time, meeting, connection"
,,"good stuff #1-7",2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"affirming, accumulative, joyful","small joys, gratitude, lists"
,,airplane mode,2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"detached, quiet, internal","disconnection, reflection, self"
,,listen,2017,A3 foldout,"Also in Pastoral + You Sleep Uphill",Pastoral,You Sleep Uphill,active,foldout,"attentive, urgent, ecological","attention, nature, relationship"
,,you sleep uphill,2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"tender, spatial, intimate","love, care, domesticity"
,,"dream #3",2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"uncanny, symbolic, subconscious","dreams, psyche, image"
,,"sad rocks",2017,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"melancholy, geological, still","grief, nature, permanence"
,,regrets,2017,A3 foldout,"",,withdrawn,foldout,"haunted, remorseful, quiet","mistakes, time, sorrow"
,,coverage,2017,A3 foldout,"Also in Coalface + You Sleep Uphill",Coalface,You Sleep Uphill,active,foldout,"exposed, vulnerable, social","visibility, media, self"
,,I am tired,2017,A3 foldout,"",,withdrawn,foldout,"exhausted, honest, raw","fatigue, burnout, surrender"
,,you fumble,2018,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"clumsy, tender, intimate","love, awkwardness, care"
,,most things interest me,2018,A3 foldout,"Also in Coalface",Coalface,active,foldout,"curious, open, attentive","attention, wonder, engagement"
,,strange habits,2018,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"quirky, habitual, intimate","routine, love, eccentricity"
,,autobio note #9,2018,"12p, A5","New version of 'where you at, bro?'",,active,booklet,"casual, reflective, fraternal","friendship, identity, connection"
,,neo-liberal handbook,2018,"12p, A5 + e-book","Also in Sleep Uphill + Bunkerland",Sleep Uphill,Bunkerland,active,booklet,"satirical, political, sharp","capitalism, critique, resistance"
,,ill-wish list #12,2018,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"vengeful, ironic, cathartic","anger, curses, release"
,,yellow cars,2018,A3 foldout,"Also in Mixture of Wishes",Mixture of Wishes,active,foldout,"observational, specific, nostalgic","memory, colour, urban life"
,,pastoral,2018,"48p, A5","24 poem collection",Pastoral,active,collection,"rural, reflective, grounded","countryside, animals, quiet"
,,coalface,2018,"48p, A5","24 poem collection",Coalface,active,collection,"harsh, enduring, industrial","labour, struggle, survival"
,,3 tents,2018,A3 foldout,"Sleep Uphill collection",You Sleep Uphill,active,foldout,"temporary, fragile, intimate","shelter, love, impermanence"
,,dereliction,2018,A3 foldout,"Also in Pastoral",Pastoral,active,foldout,"abandoned, quiet, decaying","ruin, neglect, time"
,,redacted,2021,A3 foldout,"",,active,foldout,"censored, mysterious, absent","secrecy, loss, silence"
,,tour,2021,A3 foldout,"Also in Coalface",Coalface,active,foldout,"mobile, transient, observational","journey, labour, movement"
,,chatroom #4,2021,A3 foldout,"",,active,foldout,"digital, fragmented, lonely","online, connection, isolation"
,,circles,2022,A3 foldout,"You Sleep Uphill collection",You Sleep Uphill,active,foldout,"repetitive, intimate, endless","love, routine, cycles"
,,in 1979,2022,A3 foldout,"Bunkerland collection",Bunkerland,active,foldout,"nostalgic, historical, personal","memory, time, youth"
,,end of the world,2023,A3 foldout,"Bunkerland collection",Bunkerland,active,foldout,"calm, accepting, absurd","apocalypse, resignation, humour"
,,Eyes Down,2023,A3 foldout,"",Bunkerland,active,foldout,"shameful, guilty, internal","embarrassment, introspection, silence"
,,Beard trim,2023,A3 foldout,"",Bunkerland,active,foldout,"intimate, mundane, gendered","grooming, self, ritual"
,,Property Ladder,2023,A3 foldout,"",Bunkerland,active,foldout,"satirical, anxious, economic","housing, class, aspiration"
,,Spinning Noises,2023,A3 foldout,"",Bunkerland,active,foldout,"mechanical, hypnotic, anxious","machines, sound, obsession"
,,"Lifeboat #15",2023,A3 foldout,"Bunkerland collection",Bunkerland,active,foldout,"precarious, hopeful, survival","rescue, crisis, hope"
,,"Lifeboat #4",2023,A3 foldout,"Bunkerland collection",Bunkerland,active,foldout,"precarious, hopeful, survival","rescue, crisis, hope"
,,"Lifeboat #12",2023,A3 foldout,"Bunkerland collection",Bunkerland,active,foldout,"precarious, hopeful, survival","rescue, crisis, hope"
,,Bunkerland,2023,"100p A5","50+ poem/writing collection",Bunkerland,active,collection,"archival, layered, urban","memory, place, survival"
'''

# — Select a Random Publication —
def select_random_publication():
    csv_file = io.StringIO(CATALOG_DATA_CSV)
    reader = csv.DictReader(csv_file)
    publications = list(reader)
    return random.choice(publications)

# — Format the Post —
def format_post(publication):
    # --- THIS IS THE FIX ---
    # Check if the title is empty/None, which indicates a misaligned row
    if not publication.get('title') or not publication['title'].strip():
        # Data is shifted, so we get the values from the next columns
        title = publication.get('first published', '').strip()
        year = publication.get('format', '').strip()
        collections = publication.get('notes', '').strip()
        moods = publication.get('collections', '').strip()
        themes = publication.get('status', '').strip()
        isbn = "no ISBN" # It's safer to assume no ISBN for these misaligned rows
    else:
        # Data is correctly aligned, use the normal keys
        title = publication.get('title', '').strip()
        year = publication.get('first published', '').strip()
        collections = publication.get('collections', '').strip()
        moods = publication.get('moods', '').strip()
        themes = publication.get('themes', '').strip()
        isbn = publication.get('isbn', '').strip() or "no ISBN"

    # Build the post text line by line to avoid empty lines
    post_lines = [
        "A Poem of the Day from Landroverfarm Press",
        "",
        f'"{title}"',
        f"Published: {year}"
    ]
    if collections:
        post_lines.append(collections)
    if moods:
        post_lines.append(f"\n{moods}")
    if themes:
        post_lines.append(themes)
    
    post_lines.extend([
        f"\n{isbn}",
        "",
        "#DavidMerritt #LandroverfarmPress #Poetry #Fediverse"
    ])

    post_text = "\n".join(post_lines)

    if len(post_text) > 500:
        # Truncate if too long, ensuring the hashtags remain
        post_text = post_text[:497] + "..."

    return post_text

# — Post to Fediverse —
def post_to_fediverse(status_text):
    mastodon = create_mastodon_client()
    if not mastodon:
        return False

    try:
        mastodon.status_post(status_text)
        print("✅ Successfully posted to the Fediverse!")
        return True
    except Exception as e:
        print(f"❌ Failed to post: {e}")
        return False

# — Main —
def main():
    publication = select_random_publication()
    post_text = format_post(publication)
    print("📤 Preparing post:")
    print(post_text)
    print("\n" + "-"*50)
    confirm = input("Post this? (y/n): ")
    if confirm.lower().startswith('y'):
        post_to_fediverse(post_text)
    else:
        print("❌ Post cancelled.")

if __name__ == "__main__":
    main()