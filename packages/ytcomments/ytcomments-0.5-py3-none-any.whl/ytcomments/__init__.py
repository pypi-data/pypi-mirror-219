def ytcmttranslate(L,lang):
    from translatepy import Translator
    translator = Translator()
    translated=[]
    from tqdm import tqdm
    for i in tqdm(range(len(L))):
        x=str(L[i])
        translated.append(str(translator.translate(x, lang)))
    return translated

global iso_639
iso_639="""

Dutch                  : nl |   Greek                  : el |   Malayalam              : ml |   Telugu                 : te
Frisian                : fy |   Gujarati               : gu |   Maltese                : mt |   Thai                   : th
English                : en |   Haitian Creole         : ht |   Maori                  : mi |   Turkish                : tr
Afrikaans              : af |   Hausa                  : ha |   Marathi                : mr |   Ukrainian              : uk
Albanian               : sq |   Hawaiian               : aw |   Myanmar (Burmese)      : my |   Urdu                   : ur
Amharic                : am |   Hebrew                 : iw |   Nepali                 : ne |   Uzbek                  : uz
Arabic                 : ar |   Hindi                  : hi |   Norwegian              : no |   Vietnamese             : vi
Armenian               : hy |   Mongolian              : mn |   Pashto                 : ps |   Welsh                  : cy
Azerbaijani            : az |   Hungarian              : hu |   Persian                : fa |   Xhosa                  : xh
Basque                 : eu |   Icelandic              : is |   Polish                 : pl |   Yiddish                : yi
Belarusian             : be |   Igbo                   : ig |   Portuguese             : pt |   Yoruba                 : yo
Bengali                : bn |   Indonesian             : id |   Punjabi                : pa |   Zulu                   : zu
Bosnian                : bs |   Irish                  : ga |   Romanian               : ro |   Chinese (Traditional)  : TW


    """

    
def main():
    global iso_639
    import getch
    import youtube_comment_downloader as downloader
    from itertools import islice
    import pyperclip as pc
    d=downloader.YoutubeCommentDownloader()
    print("""
                        _________
                    ________________
                  _____________________
               __________________________           
               
    ---------> Youtube Comments downloader <---------
               ___________________________
                  _____________________
                     _______________
                        _________
    
    ")
    url=str(input("\nEnter youtube video url : "))
    print("""
    Sort by :
             1 : Popular
             2 : Recent
             
    """)
    sortby=int(getch.getch())
    d=d.get_comments_from_url(url,sortby-1)
    
    cmts=[]
    print("""
    1. Load all comments
    2. Load specific number of comments
    
    """)
    ch=int(getch.getch())
    num_cmts=10**6
    if ch==2:
        num_cmts=str(input("\n Number of comment to be loaded : "))

    from tqdm import tqdm
    for comment in tqdm(islice(d, num_cmts)):
        cmts.append(comment["text"])
    print("\nFetched "+str(len(cmts))+" comments !")


    print("""
    1. Print and copy to clipboard
    2. Only copy to clipboard
    3. Translate
    
    """)
    m=int(getch.getch())
    
    
    if m==1:
        print(cmts)
        pc.copy("\n\n".join(cmts))
        return 1
    if m==2:
        print("\n Results copied to clipboard\n")
        pc.copy("\n\n".join(cmts))
        return 1
    if m==3:
        print("""
    You can specify language in  ISO 639-1-Codes or ISO 639-2 or Endonym
    ex: ml mal  മലയാളം

    Want to show the ISO 639-codes chart (y/n) ?

        """)

        iso_chart=getch.getch()
        if iso_chart =="y":
            print(iso_639)

        lang=input(str("\n Enter the language to translate to : "))

        print("\n")

        tr=ytcmttranslate(cmts,lang)

        pc.copy("\n\n".join(tr))
        print("\n Do you want to print results ? (y/n) ")
        pr=getch.getch()
        if pr=="y":
            for r in tr:
                print(r)
            print("\n Results copied to clipboard\n")
        else:
            print("\n Results copied to clipboard\n")
