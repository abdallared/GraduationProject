import urllib.request, re, sys

def get_info(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'facebookexternalhit/1.1'})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        final_url = resp.geturl()
        html = resp.read().decode('utf-8', errors='ignore')
        return final_url, html
    except Exception as e:
        return url, str(e)

u1, h1 = get_info('https://lnkd.in/p/eqgBp3t9')
sys.stdout.buffer.write(f'--- LINK 1 ---\n{u1}\n'.encode('utf-8'))
for tag in ['title', 'og:title', 'og:description', 'description']:
    m = re.search(r'property="' + tag + r'"\s+content="([^"]*)"', h1) or re.search(r'name="' + tag + r'"\s+content="([^"]*)"', h1)
    if m:
        sys.stdout.buffer.write(f'{tag}: {m.group(1)}\n'.encode('utf-8'))

# also extract any google form links or URLs inside the text of post 1
forms1 = re.findall(r'https?://[^\s"<>]+', h1)
for f in set(forms1):
    if 'form' in f.lower() or 'apply' in f.lower() or 'bit.ly' in f.lower() or 't.co' in f.lower():
        sys.stdout.buffer.write(f'Link in post 1: {f}\n'.encode('utf-8'))

u2, h2 = get_info('https://www.linkedin.com/posts/%D9%84%D9%88-%D8%B9%D9%86%D8%AF%D9%83-%D9%81%D9%83%D8%B1%D8%A9-%D8%AA%D8%BA%D9%8A%D8%B1-%D9%85%D8%B3%D8%AA%D9%82%D8%A8%D9%84-%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85-%D8%A3%D9%88-%D8%A7%D9%84%D8%B1%D8%B9%D8%A7%D9%8A%D8%A9-share-7518250278224121857-bfH1/?highlightedUpdateUrn=urn:li:activity:7518280083271462912')
sys.stdout.buffer.write(f'\n--- LINK 2 ---\n{u2}\n'.encode('utf-8'))
for tag in ['title', 'og:title', 'og:description', 'description']:
    m = re.search(r'property="' + tag + r'"\s+content="([^"]*)"', h2) or re.search(r'name="' + tag + r'"\s+content="([^"]*)"', h2)
    if m:
        sys.stdout.buffer.write(f'{tag}: {m.group(1)}\n'.encode('utf-8'))

forms2 = re.findall(r'https?://[^\s"<>]+', h2)
for f in set(forms2):
    if 'form' in f.lower() or 'apply' in f.lower() or 'bit.ly' in f.lower() or 't.co' in f.lower():
        sys.stdout.buffer.write(f'Link in post 2: {f}\n'.encode('utf-8'))
