import zipfile, re, sys, io

path = sys.argv[1]
z = zipfile.ZipFile(path)
xml = z.read('word/document.xml').decode('utf-8', errors='ignore')

# paragraph split
xml = xml.replace('</w:p>', '\n[[P]]\n')
# tabs / breaks
xml = xml.replace('<w:tab/>', '\t')
xml = xml.replace('<w:br/>', '\n')
# remove all tags
text = re.sub(r'<[^>]+>', '', xml)
# unescape
import html
text = html.unescape(text)

out = []
for para in text.split('[[P]]'):
    p = para.replace('\n', '')
    out.append(p)

result = '\n'.join(out)
result = re.sub(r'\n{3,}', '\n\n', result)
sys.stdout.buffer.write(result.encode('utf-8'))
