# vim ze je ten kod hroznej pls nekoukejte se na nej
import os
import re

# webgame structure:
# {{{
# UROVEN: skola
# MISTO: trida
# zacatek;Jsi ve třídě. Máš hlad.;trida.jpg;jidelna@Jít do jídelny;kantyna@Jít do kantýny
structure = """
UROVEN: skola
MISTO: trida
zacatek;Ráno jsi přišel do školy. Z rozhlasu se ozvalo, že tvůj spolužák Michal zmizel. Co budeš dělat?;idc@Je mi to jedno;kantyna@Podívám se po něm v kantýně;zachody@Půjdu ho hledat na záchody
idc;Michala nikdo nikdy nenašel a svět zachvátila apokalypsa;zacatek@Zkusím hrát znovu
MISTO: zachody
zachody;Na záchodech nikoho nevidíš, ale 3 kabinky jsou zamčené. Třeba je Michal v jedné z nich...;kantyna@Radši se podívám do kantýny;kabinka1@Vlámu se do první kabinky;kabinka2@Vlámu se do druhé kabinky;kabinka3@Vlámu se do třetí kabinky
kabinka1;Nikdo tu není, jen Michalův mobil leží na zemi vedle mísy. Odemkneš ho a vidíš, že michal včera napsal mámě SMS s následujícím obsahem: "Cs mami, neboj se o mě, odcházím do sigma dimenze.";zachody@Vyjdu z kabinky
kabinka2;V kabince byl skibidi toilet který tě zabil!;zacatek@Zkusím to znovu
kabinka3;V kabince seděl rozzuřený Jakub, který tě seřval a zabouchl dveře.;zachody@Musím se rozhodnout co dělat dál
MISTO: kantyna
kantyna;Zeptáš se prodavačky v kantýně, jestli neviděla Michala. "Ale ano, včera jsem ho zahlédla jít do sklepa školy.";otazka@Zeptám se proč tam asi šel;sklep@Jdu za ním do sklepa, tady může jít o vteřiny!
otazka;"Asi tuším proč mohl tvůj kamarád jít do sklepa. Jsou tam totiž portály do všemožných dimenzí...";sklep@Jdu tam!
MISTO: sklep
sklep;Vběhl jsi do sklepa a před sebou vidíš čtyři zářící kamenné dveře s vytesanými nápisy. Do dveří s jakým nápisem chceš vejít?;skibidi@SKIBIDI;masivni@MASIVNI;sigma@SIGMA;mango@MANGO MANGO MANGO
UROVEN: dimenze
MISTO: skibidi
skibidi;Dveře tě přenesly do skibidi dimenze, kde se na tebe okamžitě vrhly skibidi toilety. Při hledání michala jsi tak přišel o život.;zacatek@Zkusím to znovu
MISTO: mango
mango;Prošel jsi dveřmi a ocitl ses v mangové dimenzi. Než se stačíš vzpamatovat, obstoupí tě místní obyvatelé a sborově křičí: "POLOŽ TO MANGO!!!" Co odpovíš?;mango_ne@Žádné mango nemám!;mango_ne@Nepoložím!;zimni@To je pro moji zimní kapitolu!
mango_ne;Jak to domorodí mangodimenzané uslyšeli, začali po tobě házet manga, až tě umangovali k smrti.;zacatek@Zkusím to znovu
zimni;"Dobrá", odpoví mangodimenzané, "necháme tě tedy poklidně odejít. Vrať se odkud jsi přišel";sklep@Projdu dveřmi zpátky
MISTO: masivni
masivni;Dveřmi ze sklepa jsi prošel přímo do barber shopu. Barber k tobě ihned přispěchal a ptá se tě, jaký masivní učes chceš.;uces@Mohawk;uces@Buzzcut;low@Low Taper Fade
uces;Barber v masivní dimenzi bohužel neumí jiný účes než Low Taper Fade, a proto tě při stříhání omylem přestřihl.;zacatek@Zkusím to znovu
low;S novým účesem je z tebe rázem sigma, a tak ses znenadání teleportoval do sigma dimenze;sigma@Tak jo!
MISTO: sigma
sigma;Ocitl ses v sigma dimenzi. Otočíš se a za sebou vidíš starou cihlovou zeď, na které je vyrytý symbol řeckého písmena Sigma. Opodál stojí tajemný sigma muž. Michala ale nikde nevidíš.;muz@Zeptám se tajemného sigma muže, jestli Michala neviděl;zed@Zeptám se Sigmy na zdi, jestli o Michalovi něco neví
muz;Tajemný sigma muž tě místo odpovědi moggnul, otočil se, a beze slova odešel;cizicesta@Půjdu za ním, snad ho doženu;zed@Kašlu na něj, zeptám se raději té Sigmy na zdi
cizicesta;Buhví odkud se přihnali sigma strážníci. Nasadili ti pouta a oznámili ti, že sigma kráčí vlatní cestou, což jsi právě porušil. Uvrhli tě do sigma vězení, kde budeš hnít zbytek života;zacatek@Zkusím to znovu
zed;Přistoupíš ke zdi a proneseš: "Sigma sigma on the wall, who's the skibidiest of them all?" Sigma na zdi odpoví: "To Michal je, v zemi zdejší, ze všech sigem nejsigmnější! Najdeš ho v jeho paláci na Sigmím Vrchu.";vrch@Půjdu na sigmí vrch přímo - lesem;cizicesta@Půjdu po pohodlnější, ale trochu delší vyšlapané cestě
vrch;Dorazil jsi na Sigmí Vrch, kde tě král sigmí dimenze Michal ihned přijal na audienci;cringe@"Michale, všichni tě v naší dimenzi hledají!";ministr@"Tvá dimenze je úžasná, mohl bych být ministrem stojaté vody na tvém dvoře?"
cringe;Král sigma Michal ti dal zobrazeno. Musíš odejít ze sigmí dimenze, neboť už nejsi sigma.;zpet@Půjdu zpátky
zpet;Ve škole ti nikdo nevěří žes byl v jiné dimenzi, a Zdráhala ti navíc za odchod ze školy dal 69 hodin u školníka. Konec;zacatek@Zkusím to znovu
ministr;Michal souhlasí, jelikož ministra stojaté vody zrovna sháněl.;jsi_ministr@Super!
jsi_ministr;Zbytek života jsi dožil v blahobytu jako ministr stojaté vody v sigma dimenzi. Konec.;zacatek@Zpátky na začátek
"""  # }}}

# html template
# {{{
html = """<!DOCTYPE html>
<html lang="cs">
  <head>
    <title>%pageId%</title>
    <meta charset="UTF-8">
  </head>
  <body>
    <p>%content%</p>
    %image%
%links%  </body>
</html>"""
# }}}
with open("template.html", "r") as file:
    html = file.read()


def parseStructure():  # {{{
    os.makedirs("game")
    parsedStructure = dict()
    structureList = structure.split("\n")
    level = ""
    place = ""
    for line in structureList:
        location = dict()
        if line != "":
            if line.startswith("UROVEN: "):
                level = line.replace("UROVEN: ", "")
                place = ""
                os.makedirs(os.path.join("game", level))

            elif line.startswith("MISTO: "):
                place = line.replace("MISTO: ", "")
                if level != "":
                    os.makedirs(os.path.join("game", level, place))
                else:
                    print("SPECIFIKOVANO MISTO ALE NE UROVEN 😤")
            else:
                if not re.match(r"^([^;@]+;){1}[^;@]*(;[^;@]+@[^;@]+)*$", line):
                    print("NECO JE SPATNE!!! na radku:\n" + line)
                location["level"] = level
                location["place"] = place
                parsedLine = line.split(";")
                i = 0
                location["links"] = list()
                for item in parsedLine:
                    if i == 0:
                        pageId = item
                        location["image"] = item + ".jpg"
                    elif i == 1:
                        location["content"] = item
                    # elif i == 2:
                    #     location["image"] = item
                    else:
                        location["links"].append(item.split("@"))
                    i += 1
                if pageId not in parsedStructure:
                    parsedStructure[pageId] = location
                else:
                    print(
                        "Mas tam minimalne dvakrat radek s ID "
                        + pageId
                        + "!\nPRIJDE TO TO JAKO NORMALNI????"
                    )
    return parsedStructure


# }}}
parsedStructure = parseStructure()


def writeFiles():  # {{{
    for pageId, location in parsedStructure.items():
        linksString = ""
        for link in location["links"]:
            if link[0] not in parsedStructure:
                print(
                    "TYVOLE NEFUNGUJE TO MAS TAM ODKAZ NA ID KTERY NEEXISTUJE PROBER SE MORE!!!"
                )
                print(
                    "lokace s ID "
                    + pageId
                    + " odkazuje na lokaci s ID "
                    + link[0]
                    + ", KTERA ALE NEEXISTUJE!"
                )
            target = parsedStructure[link[0]]
            linksString = (
                linksString
                + '    <li>\n       <a href="../../'
                + target["level"]
                + "/"
                + target["place"]
                + "/"
                + link[0]
                + '.html">'
                + link[1]
                + "</a></li>\n"
            )
        tmpHtml = html.replace("%pageId%", pageId, -1)
        tmpHtml = tmpHtml.replace("%content%", location["content"], -1)
        if location["image"] == "":
            imageHtml = ""
        else:
            imageHtml = '<img src="../../../images/' + location["image"] + '"  />'
            if not os.path.exists(os.path.join("images", location["image"])):
                print(f"Obrazek {location['image']} neexistuje!!1!!1!!11!!!!!!")
        tmpHtml = tmpHtml.replace("%image%", imageHtml, -1)
        tmpHtml = tmpHtml.replace("%links%", linksString, -1)
        with open(
            os.path.join(
                "game", location["level"], location["place"], pageId + ".html"
            ),
            "w",
        ) as file:
            file.write(tmpHtml)  # }}}


writeFiles()
