from typing import Dict

from .. import Provider as LoremProvider


class Provider(LoremProvider):
    """Implement lorem provider for ``bn_BD`` locale."""

    # source 1: https://en.wikipedia.org/wiki/Bengali_vocabulary
    # source 2: https://en.wikipedia.org/wiki/Bengali_grammar

    word_connector = " "
    sentence_punctuation = "।"
    word_list = (
        "পানি",
        "লবণ",
        "দাওয়াত",
        "মরিচ",
        "খালা",
        "ফুফু",
        "গোসল",
        "বাতাস",
        "চাহিদা",
        "স্বাগতম",
        "যোগ",
        "আসন",
        "আশ্রম",
        "আয়ুর্বেদ",
        "বন্ধন",
        "খাট",
        "ধুতি",
        "মায়া",
        "স্বামী",
        "লক্ষ্মী",
        "লক্ষ্মণ",
        "কুড়ি",
        "খুকি",
        "খোকা",
        "খোঁচা",
        "খোঁজ",
        "চাল",
        "চিংড়ি",
        "চুলা",
        "ঝিনুক",
        "ঝোল",
        "ঠ্যাং",
        "ঢোল",
        "পেট",
        "বোবা",
        "মাঠ",
        "মুড়ি",
        "আবহাওয়া",
        "চাকরি",
        "আয়না",
        "আরাম",
        "বকশিশ",
        "আস্তে",
        "কাগজ",
        "খারাপ",
        "খোদা",
        "খুব",
        "গরম",
        "চশমা",
        "চাকর",
        "চাদর",
        "জান",
        "জায়গা",
        "ডেগচি",
        "দম",
        "দেরি",
        "দোকান",
        "পর্দা",
        "বদ",
        "বাগান",
        "রাস্তা",
        "রোজ",
        "হিন্দু",
        "পছন্দ",
        "টেক্কা",
        "আলু",
        "নখ",
        "খুন",
        "আওয়াজ",
        "আসল",
        "এলাকা",
        "ওজন",
        "কলম",
        "খবর",
        "খালি",
        "খেয়াল",
        "গরিব",
        "জমা",
        "তারিখ",
        "দুনিয়া",
        "নকল",
        "ফকির",
        "বদল",
        "বাকি",
        "শয়তান",
        "সাহেব",
        "সনদ",
        "সাল",
        "সন",
        "হিসাব",
        "দাদা",
        "বাবা",
        "নানি",
        "চকমক",
        "বাবুর্চি",
        "বেগম",
        "কেচি",
        "লাশ",
        "তবলা",
        "আলমারি",
        "ইস্ত্রি",
        "ইস্তিরি",
        "ইস্পাত",
        "কামিজ",
        "গামলা",
        "চাবি",
        "জানালা",
        "তামাক",
        "পেরেক",
        "ফিতা",
        "বারান্দা",
        "বালতি",
        "বেহালা",
        "বোতাম",
        "মেজ",
        "সাবান",
        "কেদারা",
        "আতা",
        "আনারস",
        "কাজু",
        "কপি",
        "পেঁপে",
        "পেয়ারা",
        "সালাদ",
        "গির্জা",
        "যিশু",
        "পাদ্রি",
        "ইংরেজ",
        "অফিস",
        "জেল",
        "ডাক্তার",
        "পুলিশ",
        "ব্যাংক",
        "ভোট",
        "স্কুল",
        "হাসপাতাল",
        "কাপ",
        "গ্লাস",
        "চেয়ার",
        "টেবিল",
        "বাক্স",
        "লণ্ঠন",
        "প্লাস্টিক",
        "কলেজ",
        "সাইকেল",
        "রেস্তোরাঁ",
        "সুড়ঙ্গ",
        "চা",
        "চিনি",
        "সুনামি",
        "রিক্সা",
        "বোকা",
        "ছোট্ট",
        "লুঙ্গি",
        "ডেঙ্গু",
        "মানুষজন",
        "মাফিয়া",
        "স্টুডিও",
        "ম্যালেরিয়া",
        "ক্যাঙারু",
        "বুমেরাং",
        "আমি",
        "তুই",
        "তুমি",
        "আপনি",
        "এ",
        "ইনি",
        "ও",
        "উনি",
        "সে",
        "তিনি",
        "সেটি",
        "আমরা",
        "তোরা",
        "তোমরা",
        "আপনারা",
        "এরা",
        "এগুলো",
        "ওরা",
        "এঁরা",
        "ওঁরা",
        "তারা",
        "তাঁরা",
        "সেগুলো",
        "আমাকে",
        "তোকে",
        "আমাদেরকে",
        "তোদেরকে",
        "তোমাকে",
        "তোমাদেরকে",
        "আপনাকে",
        "আপনাদেরকে",
        "একে",
        "এদেরকে",
        "এঁকে",
        "এঁদেরকে",
        "এটি",
        "এটা",
        "ওকে",
        "ওদেরকে",
        "ওঁকে",
        "ওঁদেরকে",
        "ওটি",
        "ওটা",
        "ওগুলো",
        "তাকে",
        "তাদেরকে",
        "তাঁকে",
        "তাঁদেরকে",
        "সেটা",
        "কে",
        "কার",
        "কাকে",
        "কোন",
        "কি",
        "কেউ",
        "কারও",
        "কাউকে",
        "কোনও",
        "কিছু",
    )

    parts_of_speech: Dict[str, tuple] = {}
