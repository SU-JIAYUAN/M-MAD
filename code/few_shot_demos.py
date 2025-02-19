user_template = """
{src_lng} source:\n{source_segment}\n{tgt_lng} translation:\n{target_segment}
"""


accuracy_user_shot = [
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="工厂直销生产，欢迎代理批发！", target_segment="Factory direct production, welcome agent wholesale!"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="性能稳定，四个出风口散热没问题，值得推荐", target_segment="The performance is stable, and the heat dissipation of the four air outlets is no problem, which is worth recommending"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="小编为大家带来洁面乳霜哪款好？", target_segment="Xiaobian brings cleansing cream to everyone. Which one is good?"),
]
accuracy_mem_shot = ['''
{"annotations":[{"error_span": "Factory direct production", "category": "accuracy/mistranslation", "severity": "major"}, {"error_span": "agent wholesale", "category": "accuracy/mistranslation", "severity": "major"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "Xiaobian", "category": "accuracy/mistranslation", "severity": "minor"}]}
''',
]
# 3

fluency_user_shot = [
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="这是我除了驾驶证之外一本觉得重要的技能证书之一！", target_segment="This is one of the skills certificates that I think are important besides my driver's license!"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="餐厅表示已经煮好食物半个多小时了", target_segment="The restaurant said it had cooked the food for more than half an hour"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="感观不错，色彩还原好，质量可以！", target_segment="Good sense, good color restoration and good quality!"),
]
fluency_mem_shot = [
'''
{"annotations": [{"error_span": "are", "category": "fluency/grammar", "severity": "minor"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": " and", "category": "fluency/punctuation", "severity": "minor"}]}
''',
]

# 3

term_user_shot = [
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="散热效果：散热非常好，基本无热度 轻薄程度：方便携带 外观材质：Thinkpad传统设计，满意", target_segment="Heat dissipation effect: very good heat dissipation, basically no heat, light and thin degree: easy to carry appearance material: Thinkpad traditional design, satisfactory"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="有习近平总书记作为党中央的核心、全党的核心领航掌舵，有习近平新时代中国特色社会主义思想科学指引，有全党全国各族人民团结一心、顽强奋斗，我们就一定能够战胜各种艰难险阻，在全面建设社会主义现代化国家新征程上创造新的时代辉煌、铸就新的历史伟业。", target_segment="With General Secretary 　 as the core of the CPC Central Committee and the core of the whole party at the helm, With the scientific guidance of 　 's thought of socialism with Chinese characteristics in the new era, and the unity and tenacious struggle of the whole Party and the people of all ethnic groups, we will be able to overcome all kinds of difficulties and obstacles, create new era glory and create new historical great achievements in the new journey of building a socialist modernized country in an all-round way."),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="A字短裙会很显瘦，比较适合胖女孩，上衣要选择紧身一些的，形成层次感会更显瘦。", target_segment="A-line skirt will be very thin, which is more suitable for fat girls. The jacket should be tight, forming a sense of hierarchy will be thinner."),
]
term_mem_shot = [
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "thought of socialism with Chinese characteristics in the new era", "category": "terminology/inappropriate for context", "severity": "minor"}]}
''',
'''
{"annotations": []}
'''
]

# 2
style_user_shot = [
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="商家服务态度好！", target_segment="Good service attitude of merchants!"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="打拐执法，首要目标是寻回被拐的孩子，保护其人身安全、自由。", target_segment="The primary goal of law enforcement against abduction is to find abducted children and protect their personal safety and freedom."),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="从党的百年奋斗史中汲取奋进力量", target_segment="Draw the strength of forging ahead from the party's hundred-year struggle history")
]
style_mem_shot = [
'''
{"annotations": [{"error_span": "merchants", "category": "style/awkward", "severity": "minor"}]}
''',
'''
{"annotations": []}
''',
'''
{"annotations": [{"error_span": "hundred-year struggle history", "category": "style/awkward", "severity": "minor"}]}
'''
]

nontran_user_shot = [
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="赴宴来支雲，留下好心情！", target_segment="I'm Xiao Yun, looking forward to meeting you again!"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="赴宴来支雲，留下好心情！", target_segment="I'm Xiao Yun, looking forward to meeting you again!"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="赴宴来支雲，留下好心情！", target_segment="I'm Xiao Yun, looking forward to meeting you again!"),
    user_template.format(src_lng="Chinese", tgt_lng="English", source_segment="赴宴来支雲，留下好心情！", target_segment="I'm Xiao Yun, looking forward to meeting you again!"),
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