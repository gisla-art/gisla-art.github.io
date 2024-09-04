import pandas as pd
import sys
import os

root = "werksverzeichnis/"

df = pd.read_csv(os.path.join(root,'Gisla_WV.csv'), sep=',')
df.head(1)
df.columns
#df.Standort.unique()

title = 'Werksverzeichnis Gisla Burkhardt'

original_stdout = sys.stdout

def add_euro(x):
    return f"{str(x)} &#8364;"

print(df.shape[0])
sel = 3
if sel == 1:
    df = df[df['Standort'].isin(['Luzie', 'Gisla','Felix'])]
    name = os.path.join(root,'werksverzeichnis.html')
elif sel == 2:
    df = df[df.Standort == 'Atelier']
    name = os.path.join(root,'werksverzeichnis_missing.html')
elif sel == 3:
    df_got_it = df[df['Standort'].isin(['Luzie', 'Gisla','Felix'])]
    df_got_it['Standort'] = ""
    df_got_it['Preis'] = df_got_it['Preis'].map(lambda x: add_euro(x)).values
    df_not_got_it = df[~df['Standort'].isin(['Luzie', 'Gisla','Felix'])]
    df_not_got_it['Standort'] = ""
    df_not_got_it['Preis'] = "verkauft"
    df = pd.concat([df_got_it, df_not_got_it])
    df = df.sort_values('Nummer')
    name = os.path.join(root,'werksverzeichnis.html')
else:
    name = os.path.join(root,'werksverzeichnis_alle.html')

print(df.shape[0])

with open(name, 'w') as f:
    sys.stdout = f
    print(f'<html>')
    print(f'<meta http-equiv="content-type" content="text/html; charset=utf-8">')
    print(f'<head><title>{title}</title>')
    print("<style>body {font-family: Arial, sans-serif;}</style>")
    print(f'</head>')
    #print(f'<body><h1>{title}</h1>')
    with open(os.path.join(root, 'header.txt'), 'r') as f:
        print(f.read())

    print('<table id="tableausstellungen" align="center" width="860px" border="0" bgcolor="#FFFFFF" cellpadding="5" cellspacing="2" p class="text2">')

    cols = ['Thema', 'Nummer', 'Format', 'Technik', 'Jahr', 'Standort', 'Preis']
    picsperrow = 2
    act_theme = df['Thema'][0]
    for i, ind in enumerate(df.index):
        theme = df['Thema'][ind]
        if i%picsperrow == 0:
            if theme!=act_theme:
                act_theme = theme
                print(f'<tr name="{act_theme}" id="{act_theme}">')
            else:
                print("<tr>")

        print("<td>")
        print('<table border="0">')
        print('<tr colspan="2">')
        print(f'<td>"<i>{df["Titel"][ind]}</i>"</td>')
        print('</tr><tr>')
        print(f'<td rowspan="{len(cols)+1}"><a href="images/{df["Nummer"][ind]}.jpg"><img src="img_small/{df["Nummer"][ind]}.jpg"/></a></td>')
        for i, field in enumerate(cols):
            # if i == len(cols_1)-1:
            #     print(f'<tr><td>{df[field][ind]} &#8364;</td></tr>')
            # else:
            print(f'<tr><td>{df[field][ind]}</td></tr>')
        print('</tr>')
        print('</table>')

        print("</td>")

        if i%picsperrow == picsperrow-1:
            print("</tr>")
    print('</table></body>')
    with open(os.path.join(root, 'footer.txt'), 'r') as f:
        print(f.read())
    print('</html>')
    sys.stdout = original_stdout
