user_template = """
{src_lng} source:\n{source_segment}\n{tgt_lng} translation:\n{target_segment}
"""

accuracy_user_shot = [
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="ברוך הבא! תודה על יצירת הקשר היום.", target_segment="Welcome! Thank you for getting in touch today."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="לא ניתן לבצע שינויים ברגע שההזמנה הוזמנה, אך לאחר שהשליח יצא מהמסעדה, תוכל ליצור איתו קשר דרך האפליקציה.", target_segment="I can't make changes once the order has been placed, but after the rider leaves the restaurant, you can contact them through the app."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="זו הזדמנות נדירה שזה קורה.", target_segment="It is a rare occasion that it happens."),
]

accuracy_mem_shot = [
'''
{"annotations":[{"error_span": "שזה קורה", "category": "accuracy/mistranslation", "severity": "minor", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "זה קורה", "category": "accuracy/mistranslation", "severity": "minor", "is_source_error": "no"}]}
''',
]

fluency_user_shot = [
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="אני אשתף אתכם בכמה שלבים להפעיל במכשיר שלכם, בסדר?", target_segment="I'll share with you a few steps to perform on your device, okay?"),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="תודה על יצירת קשר, היה לי תענוג לעזור לך היום.", target_segment="Thank you for getting in touch, it was my pleasure to assist you today."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="הייתי מפחד שזה יהיה יותר גרוע.", target_segment="I was scared it would get worse."),
]

fluency_mem_shot = [
'''
{"annotations": [{"error_span": "להפעיל במכשיר", "category": "fluency/grammar", "severity": "minor", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "יותר גרוע", "category": "fluency/grammar", "severity": "minor", "is_source_error": "no"}]}
''',
]

term_user_shot = [
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="מנקה ריאות ידני/ מיני עם מנוע, המיוצר על ידי VVI Ltd מבריטניה, מאפשר לך לשלוט על בעיות זיקפה.", target_segment="Deluxe Manual/Battery Powered Vacuum Erection Penis Pump, manufactured by VVI Ltd UK, allows you to control erectile dysfunction."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="עד כה, 58,595,066 אנשים קיבלו את המנה הראשונה של חיסון הקורונה, 49,157,835 קיבלו את המנה השנייה ו-2,237,841 קיבלו את החיסון המחדש.", target_segment="So far, 58,595,066 people have received the first dose of the COVID vaccine, 49,157,835 have received the second dose and 2,237,841 have received the booster shot."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="אני מקווה שיהיה לך יום מצוין.", target_segment="I hope you have an excellent day."),
]

term_mem_shot = [
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "החיסון המחדש", "category": "terminology/inappropriate", "severity": "minor", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
'''
]

style_user_shot = [
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="איראן מדווחת על מספר הנדבקים היומי הנמוך ביותר מזה יותר משנה", target_segment="Iran reports the lowest number of daily COVID-19 cases in more than a year"),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="ב-24 השעות האחרונות, 19 מחוזות דיווחו על כמעט אפס מקרים של מוות או רק מקרה אחד.", target_segment="In the past 24 hours, 19 provinces reported almost no death cases or only one death."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="שיבא אינו הוא הקריפטו החדש ביותר שמגיע לוויראלי ובזמן שהיא ירדה כמעט ב-60% מהשיא שלה, ההון השוקי שלה עדיין עומד על 20 מיליארד דולר.", target_segment="Shiba Inu is the latest meme-crypto to go viral, and despite being down almost 60% from its all-time high, its market cap still stands at $20 billion."),
]

style_mem_shot = [
'''
{"annotations": [{"error_span": "הנדבקים", "category": "style/awkward", "severity": "minor", "is_source_error": "no"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "מגיע לוויראלי", "category": "style/awkward", "severity": "minor", "is_source_error": "no"}]}
'''
]

nontran_user_shot = [
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="אני אוהב לשחק כדורגל עם חברים.", target_segment="The dog is running in the park."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="אני אוהב לשחק כדורגל עם חברים.", target_segment="The dog is running in the park."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="אני אוהב לשחק כדורגל עם חברים.", target_segment="The dog is running in the park."),
    user_template.format(src_lng="Hebrew", tgt_lng="English", source_segment="אני אוהב לשחק כדורגל עם חברים.", target_segment="The dog is running in the park."),
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
