import deepl
import argparse
import csv

def main():
    parser = argparse.ArgumentParser(
                    prog = 'Glossary Editor',
                    description = 'Upload Glossary CSV to your API Key')
    parser.add_argument('-f', '--filename')
    parser.add_argument('-a', '--api-key')
    parser.add_argument('-s', '--source-lang')
    parser.add_argument('-t', '--target-lang')
    parser.add_argument('-n', '--name')
    parser.add_argument('-g', '--glossary-id')
    parser.add_argument('-d', '--delete', action='store_true')
    parser.add_argument('-l', '--list', action='store_true')
    

    args = parser.parse_args()
    if not args.api_key:
        print('no api key')
        return

    if(args.delete and args.api_key):
        deleteGlossary(args.glossary_id, args.api_key)
        return

    if(args.list):
         listGlossary(args.api_key)
         return

    createGlossary(createEntriesJson(args.filename),args.api_key, args.source_lang, args.target_lang, args.name)



def createEntriesJson(filename):
    json = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            json[row[0]] = row[1]
    return json


def listGlossary(api_key):
    translator = deepl.Translator(api_key)
    glossaries = translator.list_glossaries()
    for glossary in glossaries:
        print(glossary)
        print(glossary.source_lang,glossary.target_lang)
        print(translator.get_glossary_entries(glossary))


def deleteGlossary(glossary_id, api_key):
    print(glossary_id, api_key)
    translator = deepl.Translator(api_key)
    translator.delete_glossary(glossary_id)


def createGlossary(entries, api_key, source_lang, target_lang, name):
    translator = deepl.Translator(api_key)
    my_glossary = translator.create_glossary(
        name,
        source_lang=source_lang,
        target_lang=target_lang,
        entries=entries,
    )
    print(
        f"Created '{my_glossary.name}' ({my_glossary.glossary_id}) "
        f"{my_glossary.source_lang}->{my_glossary.target_lang} "
        f"containing {my_glossary.entry_count} entries"
    )

main()