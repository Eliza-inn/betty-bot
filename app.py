import nltk
from flask import Flask,request,Response
from chatterbot import ChatBot
import re
from nltk.tokenize import word_tokenize
from chatterbot.trainers import ListTrainer
app = Flask(__name__)

all_questions = {
    "helo":"mambo vipi",
    "inakuwaje":"safi",
    "Mambo":"Poa",
    "mambo":"poa",
    "unaendeleaje?":"vizuri vipi wewe",
    "salama":"vizuri",
    "sijui":"sawa",
    "upo":"nipo",
    "ukimwi ni nini":"inamaanisha upungufu wa kinga mwilini, na hutokana na virusi wanaitwa AIDs au VVU kitaalamu",
    "vvu ni nini":"ni kifupi cha maneno yafuatayo Virusi vya Ukimwi",
    "Nambie":"Nipo hapa kukujulisha kuhusu HIV",
    "HIV ni nini?":"human immunodeficiency virus",
    "hiv":"je unaujua ugonjwa huu?",
    "ndio":"vizuri",
    "hapana":"ngoja nikujuze, huu ni ugonjwa unaotokana na virusi ambavyo kwa Kiswahili vinaitwa kifupi VVU(Virusi vya Ukimwi)",
    "vvu ni nini":"inamaanisha virusi vya ukimwi",
    "ukimwi ni nini":"inamaanisha upungufu wa kinga mwilini",
    "Hiv huenezwa na nini?":"Husababishwa na AIDS, ambao ni virusi wanaopunguza kinga mwilini.",
    "history ya HIV":"Mwaka wa 1981, daktari mmoja wa California Marekani aliona vijana wa kiume watano, walioshiriki katika mapenzi ya jinsia moja, wakiwa na ugonjwa usiokuwa wa kawaida.",
    "nini maana ya AIDS":"Ni  Acquired Immuno Deficiency Syndrome",
    "AIDS":" Acquired Immuno Deficiency Syndrome",
    "ukimwi husababishwa na nini":"1.Kufanya Ngono Zembe\n2.kutoka kwa mama mwenye maambukizi kwenda kwa mtoto wakati wa kumnyonyesha au kujifungua.\n3.kuchangia vitu venye ncha kali.\n4.Kuwa na wapenzi wengi",
    "njia za kupata ukimwi":"1.Kufanya Ngono Zembe\n2.Kutotumia Kondomu wakati wa kujamiana\n3.kuchangia vitu venye ncha kali.\n5.Kuwa na wapenzi wengi",
    "dalili za ukimwi":"1.kutokwa na jasho jingi wakati wa usiku\n2.Kupata homa za mara kwa mara na kuhisi baridi\n3.Kikohozi\n4.Kushindwa kupumua vyema\n5.Madoa madoa kwenye ulimi na mdomoni\n6.Maumivu ya kichwa\n7.Uchovu usiokuwa na sababu na usioisha\n8.Kutokuona vyema\n9.Kupungua uzito\n10.Mapele na ukurutu kwenye ngozi",
    "njinsi ya kujikinga":"1.Kuacha ngono zembe\n2.Kuwa na mpenzi mmoja\n3.kutochangia vitu na watu haswa miswaki na sindano\n4.kupima damu kabla ya kumpatia mtu mwingine.",
    "ntajuaje kama nina ukimwi":"nenda kapime kituo chochote cha afya kilicho karibu yako.",
    "ntakufa nikipata ukimwi":"ndiyo utakufa, kama hauto zingatia kanuni kutoka kwa daktari.",
    "kuna tiba ya ukimwi?":"Tiba kwa sasa haipo, ila kuna dawa za kupunguza makali kama ARV ambazo zinapatikana vituo vya afya.",
    "unanitisha":"sikutishi ila gonjwa lenye ndo tishio. Ukimwi unaepukika...",
    "dalili zake ni zipi":"hizi ni dalili za awali\n 1.kufimba kwa tezi za kwenye makwapa, mapaja na shingo\n 2.Homa\n3.Uchovu\n4.Kuharisha\n5.Kupungua uzito\n6.Kikohozi\n7.Pumzi kutoka kidogodogo\n8.Mafua",
    "dalili za awali ni":"hizi ni dalili za awali\n 1.kufimba kwa tezi za kwenye makwapa, mapaja na shingo\n 2.Homa\n3.Uchovu\n4.Kuharisha\n5.Kupungua uzito\n6.Kikohozi\n7.Pumzi kutoka kidogodogo\n8.Mafua",
    "dalili":"1.kutokwa na jasho jingi wakati wa usiku\n2.Kupata homa za mara kwa mara na kuhisi baridi\n3.Kikohozi\n4.Kushindwa kupumua vyema\n5.Madoa madoa kwenye ulimi na mdomoni\n6.Maumivu ya kichwa\n7.Uchovu usiokuwa na sababu na usioisha\n8.Kutokuona vyema\n9.Kupungua uzito\n10.Mapele na ukurutu kwenye ngozi"
}

stop_words = [
    "akasema","alikuwa","alisema",
    "baada","basi","bila","cha",
    "chini","hadi","hapo","hata",
    "hivyo","hiyo","huku","huo","ili",
    "ilikuwa","juu","kama","karibu","katika",
    "kila","kima","kisha","kubwa","kutoka","kuwa",
    "kwa","kwamba","kwenda","kwenye","la","lakini",
    "mara","mdogo","mimi","mkubwa","mmoja","moja",
    "muda","mwenye","na","naye","ndani","ng","ni",
    "nini","nonkungu","pamoja","pia","sana","sasa",
    "sauti","tafadhali","tena","tu","vile","wa",
    "wakati","wake","walikuwa","wao","watu",
    "what",
    "wengine","wote","ya","yake","yangu","yao",
    "yeye","yule","za","zaidi","zake"]



chatBotHiv = ChatBot("hiv", logic_adapters=[
        'chatterbot.logic.BestMatch'
    ])
trainer = ListTrainer(chatBotHiv)

trainer.train(all_questions)


@app.route("/", methods=["POST"])
def ask():
    responseNoResult = Response(status= 500)
    question = request.get_json()["question"].lower().replace("?", "").strip()

    #Angalia kama kuna matokeo yoyote
    if question in all_questions.keys():
        return all_questions[question]
    else:
        #kama hakuna basi inabidi to chukue swali letu alafu tuligawanyee
        #katika maneno binafsi kwa process ya tokenization

        splitQuestion = question.split()
        for word in splitQuestion:
            if word in stop_words:
                splitQuestion.remove(word)


        searchWord = " ".join(splitQuestion)
        size = len(splitQuestion)

        if searchWord in all_questions:
            return all_questions[searchWord]
        else:
            return "Hakuna matokeo"



if __name__ == '__main__':
    app.run()

