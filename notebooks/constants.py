from datetime import timedelta
import codecs


LIST_OF_ALLOWED_LINKS = [
    'discord.gg',
    'scratch.mit.edu',
    'www.figma.com',
    'replit.com',
    'colab.research.google.com',
    't.me',
    'github.com',
    'www.canva.com'
    ]

INTERVAL = timedelta(minutes=15)

f = codecs.open('obscene_corpus.txt', mode='r', encoding='utf-8')
OBSCENE_WORDS = f.read().replace('\n', ' ').lower()
f.close()
