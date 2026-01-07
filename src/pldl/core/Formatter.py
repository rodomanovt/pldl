import re
from typing import Tuple


def remove_special_chars(filename: str) -> str:
    for char in '<>:"/\\|?*': 
        filename = filename.replace(char, '')
    filename = filename.strip(' .')
    return filename
    
    
KEEP_WORDS = {
    'remix', 'remastered', 'remaster', 'feat', 'featuring', 'ft',
    'slowed', 'reverb', 'speed', 'sped', 'sped up', 'lofi', 'live',
    'acoustic', 'instrumental', 'cover', 'edit', 'extended', 'radio'
}


NOISE_WORDS = {
    'official', 'music', 'video', 'audio', 'lyric', 'lyrics',
    'premiere', 'original', 'single', 'version', 'hd', 'hq',
    " - Topic", "TikTok", 'visualizer'
}


def get_smart_song_name(channel: str, name: str) -> Tuple[str, str]:
    # Пытаемся извлечь из name в любом случае
    artist, title = _parse_name(name)
    
    # Если не удалось — fallback на channel
    if not artist.strip() or artist.lower().strip() == "unknown":
        artist = _clean_part(channel or "Unknown Artist", is_artist=True)
    
    if not title.strip() or title.lower().strip() == "unknown":
        title = _clean_part(name or "Unknown Title", is_artist=False)

    artist = remove_special_chars(artist)
    title = remove_special_chars(title)

    if artist and channel:
        title = title.replace(artist, "").replace(channel, "")
        title = title.replace('-', " ")
        # index = title.rfind("  ")
        # if index != -1:
        #     title = title[:index]

        
    return artist, title


def _parse_name(name: str) -> Tuple[str, str]:
    name = name.strip()
    
    # 🔹 Сначала пробуем кавычки (приоритет: они явно выделяют название)
    # Поддерживаем: «», “”, ""
    quote_match = re.search(r'[«“"](.+?)[»”"]', name)
    if quote_match:
        title_part = quote_match.group(1).strip()
        # Всё, что до кавычек — предположительно artist
        before = name[:quote_match.start()].strip()
        after = name[quote_match.end():].strip()
        
        # Собираем возможного артиста (до + после, но без мусора)
        artist_candidate = (before + " " + after).strip()
        # Если до кавычек есть слово — скорее всего, это артист
        if before and _looks_like_artist(before):
            artist_candidate = before
        
        return _clean_part(artist_candidate, is_artist=True), _clean_part(title_part, is_artist=False)
    
    # 🔹 Затем пробуем " - " (только если кавычек нет)
    if "-" in name:
        parts = name.split("-", 1)
        if _looks_like_artist(parts[0]):
            return _clean_part(parts[0], is_artist=True), _clean_part(parts[1], is_artist=False)
    
    # 🔹 Не удалось распарсить
    return "", name


def _clean_part(text: str, is_artist: bool = False) -> str:
    if not text:
        return text

    def clean_brackets(match):
        content = match.group(1)
        content_lower = content.lower().strip()
        words = re.findall(r'\b\w+\b', content_lower)
        if any(word in KEEP_WORDS for word in words):
            return f" ({content.strip()})"
        return ""

    text = re.sub(r'[\(\[\{](.*?)[\)\]\}]', clean_brackets, text)
    noise_pattern = r'\b(?:' + '|'.join(re.escape(w) for w in NOISE_WORDS) + r')\b'
    text = re.sub(noise_pattern, ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*#(?:\w+)', ' ', text)
    text = re.sub(r'^[\s\-_\.]+|[\s\-_\.]+$', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text or "Unknown"


def _looks_like_artist(text: str) -> bool:
    if not text.strip():
        return False
    text_lower = text.lower()
    bad_for_artist = {
        'official', 'video', 'audio', 'lyric', 'phonk', 'music', 'remix',
        'slowed', 'reverb', 'edit', 'version', 'single', 'premiere',
        'title', 'song', 'track', 'hq', 'hd'
    }
    return not any(word in text_lower for word in bad_for_artist)


# def get_smart_song_name(channel: str, name: str) -> Tuple[str, str]:
#     artist = _clean_part(channel or "Unknown Artist", is_artist=True)
#     title = _clean_part(name or "Unknown Title", is_artist=False)

#     # Попытка извлечь artist из title
#     if " - " in title:
#         parts = title.split(" - ", 1)
#         if _looks_like_artist(parts[0]):
#             artist = _clean_part(parts[0], is_artist=True)
#             title = _clean_part(parts[1], is_artist=False)

#     if artist in title:
#         title = title.replace(artist, "")

#     return remove_special_chars(artist.strip()), remove_special_chars(title.strip())


# def _clean_part(text: str, is_artist: bool = False) -> str:
#     if not text:
#         return text

#     # handle brackets
#     def clean_brackets(match):
#         content = match.group(1)  # brackets content
#         content_lower = content.lower().strip()
        
#         # split into words
#         words = re.findall(r'\b\w+\b', content_lower)
        
#         # If any important words, keep all content
#         if any(word in KEEP_WORDS for word in words):
#             return f" ({content.strip()})"  # keep with whitespace and brackets
        
#         # else delete brackets with content
#         return ""

#     # keep/delete brackets: (), [], {}
#     text = re.sub(r'[\(\[\{](.*?)[\)\]\}]', clean_brackets, text)

#     # remove noise words
#     noise_pattern = r'\b(?:' + '|'.join(re.escape(w) for w in NOISE_WORDS) + r')\b'
#     text = re.sub(noise_pattern, ' ', text, flags=re.IGNORECASE)

#     # remove hashtags
#     text = re.sub(r'\s*#(?:\w+)', ' ', text)

#     # remove whitespaces and punctuation marks
#     text = re.sub(r'^[\s\-_\.]+|[\s\-_\.]+$', '', text)
#     text = re.sub(r'\s+', ' ', text)

#     return text


# def _looks_like_artist(text: str) -> bool:
#     """checks if name looks like artist name"""
#     text_lower = text.lower()
#     bad_for_artist = {'official', 'video', 'audio', 'lyric', 'music'}
#     return not any(word in text_lower for word in bad_for_artist)