import PyPDF2

alfabet='abcdefghijklmnopqrstuvwxyzáéíóúüñ¿¡'.upper()
book = ''

pages = 0

reader = PyPDF2.PdfReader('Patria.pdf')
for i in range(len(reader.pages)):
    page = reader.pages[i]
    book += page.extract_text()

pages += len(reader.pages)

reader = PyPDF2.PdfReader('Sombra.pdf')
for i in range(len(reader.pages)):
    page = reader.pages[i]
    book += page.extract_text()

pages += len(reader.pages)

reader = PyPDF2.PdfReader('costuras.pdf')
for i in range(len(reader.pages)):
    page = reader.pages[i]
    book += page.extract_text()

pages += len(reader.pages)

reader = PyPDF2.PdfReader('Allende.pdf')
for i in range(len(reader.pages)):
    page = reader.pages[i]
    book += page.extract_text()

pages += len(reader.pages)

reader = PyPDF2.PdfReader('Todo.pdf')
for i in range(len(reader.pages)):
    page = reader.pages[i]
    book += page.extract_text()

pages += len(reader.pages)

print(len(book))
print(pages)
book = book.upper()

book2 = ''.join( [x for x in book if x.isalpha() and x in alfabet ] )
dct, srt = {}, []
for bigram in [ a+b+c+d for a in alfabet for b in alfabet for c in alfabet for d in alfabet]:
    dct[ bigram ] = 0
for i in range( len( book2)-4 ):
    dct[ book2[i] + book2[i+1] + book2[i+2] + book2[i+3] ] += 1
for k in dct.keys():
    srt.append( (dct[k],k) )
srt.sort(reverse=True)
with open('my_spanish_quadgrams.txt', 'w', encoding='utf-8') as f:
    for elem in srt: f.write( elem[1] + ' ' + str( elem[0] ) + '\n' )
