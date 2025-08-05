import pandas as pd
import sys
import os
import click


@click.command()
@click.option("--sel", help="0:borghees, 1:available, \
    2:missing, 3:standort, 4:index", default=4)
def main(sel: int):
    root = "./"

    df = pd.read_csv(os.path.join(root,'Gisla_WV.csv'), sep=',')
    df.head(1)
    df.columns
    #df.Standort.unique()

    title = 'Werkverzeichnis Gisla Burkhardt'

    original_stdout = sys.stdout

    def add_euro(x):
        return f"{str(x)} &#8364;"

    print(df.shape[0])
    print(f"selected {sel}")
    if sel == 0:
        df = df[df['Standort'].isin(['Borghees'])]
        name = os.path.join(root,'werkverzeichnis_borghees.html')
    elif sel == 1:
        df = df[df['Standort'].isin(['Luzie', 'Gisla','Felix'])]
        name = os.path.join(root,'werkverzeichnis_available.html')
    elif sel == 2:
        df = df[df.Standort == 'missing']
        name = os.path.join(root,'werkverzeichnis_missing.html')
    elif sel == 3:
        name = os.path.join(root,'werkverzeichnis_standort.html')
    else:
        available = ['Luzie', 'Gisla','Felix', 'Atelier', 'Borghees']
        df_got_it = df[df['Standort'].isin(available)]
        df_got_it['Preis'] = df_got_it['Preis'].map(lambda x: add_euro(x)).values
        df_not_got_it = df[~df['Standort'].isin(available)]
        df_not_got_it['Preis'] = '<span style="color:red;">verkauft</span>'
        df = pd.concat([df_got_it, df_not_got_it])
        df = df.sort_values('Nummer')
        df.loc[df["Thema"]=="WDV", "Preis"]= "-"
        name = os.path.join(root,'werkverzeichnis.html')
        df = df.assign(Standort='')


    print(df.shape[0])

    with open(name, 'w', encoding='utf-8') as f:
        sys.stdout = f
        print('<!DOCTYPE html>')
        print('<html lang="de">')
        print('<head>')
        print('<meta charset="UTF-8">')
        print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        print(f'<title>{title}</title>')
        print('<link href="../css/design.css" rel="stylesheet" type="text/css">')
        print('<link href="lightbox/css/lightbox.min.css" rel="stylesheet">')
        print('<script src="lightbox/js/lightbox.min.js"></script>')
        print('</head>')
        print('<body>')

        # Include your header.txt content here, if you want
        with open(os.path.join(root, 'header.txt'), 'r', encoding='utf-8') as header_file:
            print(header_file.read())

        categories = ['AAA', 'LFG', 'MET', 'ORJ', 'UNY', 'WBW', 'WNN', 'WDV', 'WWW', 'ZUB']

        theme_display_names = {
            'AAA': 'Augenblicke–Annäherungen',
            'LFG': 'In Linien und Farben versteckte Geschichten',
            'MET': 'Metamorphosen',
            'ORJ': 'Orte-Reise-Jahreszeiten',
            'UNY': 'Underfoot in New York',
            'WBW': 'Wachsen-Blühen-Welken',
            'WNN': 'Warum gibt es etwas und nicht nichts?',
            'WDV': 'Wider das Vergessen',
            'WWW': 'Wasser-Wellen-Wind',
            'ZUB': 'Zauber und Bann',
        }
        
        cols = ['Nummer', 'Format', 'Technik', 'Jahr', 'Preis']
        picsperrow = 4

        for theme in categories:
            group_df = df[df['Thema'] == theme]
            if group_df.empty:
                continue

            display_name = theme_display_names.get(theme, theme)
            print(f'<div class="theme_section" id="{theme}">')
            print(f'<h2>{display_name}</h2>')  
            print('<div class="grid_wv">')

            for ind in group_df.index:
                print('<div class="grid_item">')
                print('<div class="image_wrapper">')
                print(f"<a href='images/{group_df['Nummer'][ind]}.jpg' data-lightbox='gallery' data-title='{group_df['Titel'][ind]}'>")
                print(f"<img src='img_small/{group_df['Nummer'][ind]}.jpg' alt='{group_df['Titel'][ind]}'/>")
                print("</a>")
                print('</div>')  # close image_wrapper

                print('<div class="text_wrapper">')  # NEW wrapper for text
                print(f'<p><i>{group_df["Titel"][ind]}</i></p>')
                print('<ul>')
                for field in cols:
                    print(f'<li><strong>{field}:</strong> {group_df[field][ind]}</li>')
                print('</ul>')
                print('</div>')  # close text_wrapper

                print('</div>')  # close grid_item

            print('</div>')  # close grid_wv
            print('</div>')  # close theme_section
        print('</div></body>')
        with open(os.path.join(root, 'footer.txt'), 'r') as f:
            print(f.read())
        print('</html>')
        sys.stdout = original_stdout

if __name__ == "__main__":
    main()
