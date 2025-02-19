user_template = """
{src_lng} source:\n{source_segment}\n{tgt_lng} translation:\n{target_segment}
"""



accuracy_user_shot = [
    user_template.format(src_lng="English", tgt_lng="German", source_segment="Good Afternoon, thank you for getting in contact with us today, you're through to #NAME#.", target_segment="Guten Tag, vielen Dank, dass Sie sich heute mit uns in Verbindung gesetzt haben, Sie sind durch zu #NAME#."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I'm unable to make any changes once the order has been placed however, when the rider leaves the restaurant you will be able to contact them through the app.", target_segment="Ich kann keine Änderungen vornehmen, sobald die Bestellung aufgegeben wurde, aber wenn der Fahrer das Restaurant verlässt, können Sie ihn über die App kontaktieren."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="It is a rear occasion that it happens.", target_segment="Es ist eine hintere Gelegenheit, dass es passiert."),
]
accuracy_mem_shot = ['''
{"annotations":[{"error_span": "Sie sind durch zu", "category": "accuracy/mistranslation", "severity": "major", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "hintere", "category": "accuracy/mistranslation", "severity": "minor", "is_source_error": "no"}, {"error_span": "es", "category": "accuracy/mistranslation", "severity": "minor", "is_source_error": "no"}]}
''',
]
# 3

fluency_user_shot = [
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I'll share with a couple of steps to perform into your device, okay?", target_segment="Ich werde mit ein paar Schritten teilen, um in Ihr Gerät zu spielen, okay?"),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="Thank you for contacting #PRS_ORG#, it was my pleasure to assist you today.", target_segment="Vielen Dank für die Kontaktaufnahme mit #PRS_ORG#, es war mir eine Freude, Ihnen heute behilflich zu sein."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I was scared that Covid was going to be worse.", target_segment="Ich hatte Angst, dass Covid schlimmer wird."),
]
fluency_mem_shot = [
'''
{"annotations": [{"error_span": "mit", "category": "fluency/grammar", "severity": "minor", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "wird", "category": "fluency/grammar", "severity": "minor", "is_source_error": "no"}]}
''',
]

# 3

term_user_shot = [
    user_template.format(src_lng="English", tgt_lng="German", source_segment="Deluxe Manual/ Battery Powered Vacuum Erection Penis Pump, manufactured by VVI Ltd England, allows you to get a handle on your erectile dysfunction, commonly known as ED.", target_segment="Mit der von VVI Ltd England hergestellten Deluxe Manual / Battery Powered Vacuum Erection Penis Pump können Sie Ihre erektile Dysfunktion, allgemein bekannt als ED, in den Griff bekommen."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="So far, 58,595,066 people have received the first dose of the COVID vaccine, 49,157,835 have received the second dosage and 2,237,841 have gotten the booster shots.", target_segment="Bisher haben 58.595.066 Menschen die erste Dosis des COVID-Impfstoffs erhalten, 49.157.835 haben die zweite Dosis erhalten und 2.237.841 haben die Auffrischimpfungen erhalten."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I hope you have an excellent day.", target_segment="Ich wünsche Ihnen einen schönen Tag."),
]
term_mem_shot = [
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "Auffrischimpfungen", "category": "terminology/inappropriate", "severity": "minor", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
'''
]

# 2
style_user_shot = [
    user_template.format(src_lng="English", tgt_lng="German", source_segment="Iran reports lowest number of daily COVID-19 cases in more than one year", target_segment="Der Iran meldet die niedrigste Anzahl täglicher COVID-19-Fälle seit mehr als einem Jahr"),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="Over the past 24 hours, 19 provinces reported almost no death case or only one dead.", target_segment="In den letzten 24 Stunden meldeten 19 Provinzen fast keinen Todesfall oder nur einen Toten."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="Shiba Inu is the latest meme-crypto to go viral and despite being down almost 60% from it's all-time high, the market cap still stands at an eye-watering $20 billion, making it the 12th biggest crypto in the world by valuation.", target_segment="Shiba Inu ist die neueste Meme-Krypto, die viral wird, und obwohl sie fast 60% von ihrem Allzeithoch entfernt ist, liegt die Marktkapitalisierung immer noch bei atemberaubenden 20 Milliarden US-Dollar und ist damit die 12. größte Krypto der Welt nach Bewertung.")
]
style_mem_shot = [
'''
{"annotations": [{"error_span": "Anzahl", "category": "style/awkward", "severity": "minor", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "wird", "category": "style/awkward", "severity": "minor", "is_source_error": "no"}]}
'''
]

nontran_user_shot = [
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I love playing football with my friends.", target_segment="Der Hund läuft im Park."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I love playing football with my friends.", target_segment="Der Hund läuft im Park."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I love playing football with my friends.", target_segment="Der Hund läuft im Park."),
    user_template.format(src_lng="English", tgt_lng="German", source_segment="I love playing football with my friends.", target_segment="Der Hund läuft im Park."),
]
nontran_mem_shot = [
'''
{"annotations": [{"error_span": "all", "category": "non-translation", "severity": "major", "is_source_error": "no"}]}
''',
'''
{"annotations": [{"error_span": "all", "category": "non-translation", "severity": "major", "is_source_error": "no"}]}
''',
'''
{"annotations": [{"error_span": "all", "category": "non-translation", "severity": "major", "is_source_error": "no"}]}
''',
'''
{"annotations": [{"error_span": "all", "category": "non-translation", "severity": "major", "is_source_error": "no"}]}
''',
]