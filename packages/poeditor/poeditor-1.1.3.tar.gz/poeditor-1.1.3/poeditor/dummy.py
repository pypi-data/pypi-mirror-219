from poeditor import POEditorAPI

API_TOKEN = ""
client = POEditorAPI(api_token=API_TOKEN)


project_id = client.create_project(
    name='dummy project',
    description='Created by python-poeditor for test purposes'
)

client.set_reference_language(project_id, '')


client.list_projects()
client.view_project_details(project_id)
client.list_project_languages(project_id)

client.add_language_to_project(
    project_id=project_id,
    language_code='fr'
)

client.list_project_languages(project_id)

client.view_project_terms(
    project_id=project_id,
    language_code='fr'
)

client.add_terms(
    project_id=project_id,
    data=[
        {
            "term": "The awesome cat",
            "context": "image alt",
            "reference": "",
            "plural": "The awesome cats"
        }
    ]
)

client.export(
    project_id=project_id,
    language_code='fr',
    file_type='po',
    local_file='dummy_export.po',
    filters=['untranslated', 'not_fuzzy']
)
