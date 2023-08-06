# Wacom Private Knowledge Library

The required tenant API key is only available for selected partner companies.
Please contact your Wacom representative for more information.

## Introduction

In knowledge management there is a distinction between data, information and knowledge.
In the domain of digital ink this means:

- **Data** - The equivalent would be the ink strokes
- **Information** - After using handwriting-, shape-, math-, or other recognition processes ink strokes are converted into machine readable content, such as text, shapes, math representations, other other digital content
- **Knowledge / Semantics** -  Beyond recognition content needs to be semantically analysed to become semantically understood based on a shared common knowledge.

The following illustration shows the different layers of knowledge:
![Levels of ink knowledge layers](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/knowledge-levels.png)

For handling semantics, Wacom introduced the Wacom Private Knowledge (WPK) cloud service to manage personal ontologies and its associated personal knowledge graph.

This library provide simplified access to Wacom's personal knowledge cloud service.
It contains:

- Basic datastructures for Ontology object and entities from the knowledge graph
- Clients for the REST APIs
- Connector for Wikidata public knowledge graph

**Ontology service:**

- List all Ontology structures
- Modify Ontology structures
- Delete Ontology structures

**Entity service:**

- List all entities
- Add entities to knowledge graph
- Access object properties

**Search service:**

- Search for entities for labels and descriptions with a given language
- Search for literals (data properties) 
- Search for relations (object properties)

**Group service:**

- List all groups
- Add groups, modify groups, delete groups
- Add users and entities to groups

**Ontology service:**

- List all Ontology structures
- Modify Ontology structures

**Named Entity Linking service:**

- Linking words to knowledge entities from graph in a given text (Ontology-based Named Entity Linking)

**Wikidata connector:**

- Import entities from Wikidata
- Mapping Wikidata entities to WPK entities

# Technology stack

## Domain Knowledge

The tasks of the ontology within Wacom's private knowledge system is to formalised the domain the technology is used in, such as education-, smart home-, or creative domein.
The domain model will be the foundation for the entities collected within the knowledge graph, describing real world concepts in a formal language understood by artificial intelligence system:

- Foundation for structured data, knowledge representation as concepts and relations among concepts
- Being explicit definitions of shared vocabularies for interoperability
- Being actionable fragments of explicit knowledge that engines can use for inferencing (Reasoning)
- Can be used for problem solving

An ontology defines (specifies) the concepts, relationships, and other distinctions that are relevant for modelling a domain.

## Knowledge Graph

- Knowledge graph is generated from unstructured and structured knowledge sources
- Contains all structured knowledge gathered from all sources
- Foundation for all semantic algorithms

## Semantic Technology

- Extract knowledge from various sources (Connectors)
- Linking words to knowledge entities from graph in a given text (Ontology-based Named Entity Linking)
- Enables a smart search functionality which understands the context and finds related documents (Semantic Search)


# Functionality

## Import Format

For importing entities into the knowledge graph, the tools/import_entities.py script can be used.

The ThingObject support a NDJSON based import format, where the individual JSON files can contain the following structure.

| Field name             | Subfield name | Data Structure | Description                                                                                    |
|------------------------|---------------|----------------|------------------------------------------------------------------------------------------------|
| source_reference_id    |               | str            | A unique identifier for the entity used in the source system                                  |
| source_system          |               | str            | The source system describes the original source of the entity, such as wikidata, youtube, ... |
| image                  |               | str            | A string representing the URL of the entity's icon.                                           |
| labels                 |               | array          | An array of label objects, where each object has the following fields:                       |
|                        | value         | str            | A string representing the label text in the specified locale.                                |
|                        | locale        | str            | A string combining the ISO-3166 country code and the ISO-639 language code (e.g., "en-US").  |
|                        | isMain        | bool           | A boolean flag indicating if this label is the main label for the entity (true) or an alias (false). |
| descriptions           |               | array          | An array of description objects, where each object has the following fields:                 |
|                        | description   | str            | A string representing the description text in the specified locale.                          |
|                        | locale        | str            | A string combining the ISO-3166 country code and the ISO-639 language code (e.g., "en-US").  |
| type                   |               | str            | A string representing the IRI of the ontology class for this entity.                         |
| literals               |               | array[map]     | An array of data property objects, where each object has the following fields:               |


## Access API

The personal knowledge graph backend is implement as a multi-tenancy system.
Thus, several tenants can be logically separated from each other and different organisations can build their one knowledge graph.

![Tenant concept](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/tenant-concept.png)

In general, a tenant with their users, groups, and entities are logically separated.
Physically the entities are store in the same instance of the Wacom Private Knowledge (WPK) backend database system.

The user management is rather limited, each organisation must provide their own authentication service and user management.
The backend only has a reference of the user (*“shadow user”*) by an **external user id**.

The management of tenants is limited to the system owner - Wacom -, as it requires a **tenant management API** key.
While users for each tenant can be created by the owner of the **Tenant API Key**.
You will receive this token from the system owner after the creation of the tenant.


> :warning: Store the **Tenant API Key** in a secure key store, as attackers can use the key to harm your system.


The **Tenant API Key** should be only used by your authentication service to create shadow users and to login your user into the WPK backend.
After a successful user login, you will receive a token which can be used by the user to create, update, or delete entities and relations.

The following illustration summarizes the flows for creation of tenant and users:

![Tenant and user creation](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/tenant-user-creation.png)

The organisation itself needs to implement their own authentication service which:

- handles the users and their passwords,
- controls the personal data of the users,
- connects the users with the WPK backend and share with them the user token.

The WPK backend only manages the access levels of the entities and the group management for users.
The illustration shows how the access token is received from the WPK endpoint:

![Access token request.](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/access-token.png)

# Entity API

The entities used within the knowledge graph and the relationship among them is defined within an ontology that is manage with Wacom Ontology Management System (WOMS).

An entity within the personal knowledge graphs consist of these major parts:

- **Icon** - a visual representation of the entity, for instance a portrait of a person.
- **URI** - a unique resource identifier of an entity in the graph.
- **Type** - the type links to the defined concept class in the ontology.
- **Labels** - labels are the word(s) use in a language for the concept.
- **Description** - a short abstract that describes the entity.
- **Literals** - literals are properties of an entity, such as first name of a person. The ontology defines all literals of the concept class as well as its data type.
- **Relations** - the relationship among different entities is described using relations.

The following illustration provides an example for an entity:

![Entity description](https://github.com/Wacom-Developer/personal-knowledge-library/blob/main/assets/entity-description.png)

## Entity content

Entities in general are language-independent as across nationalities or cultures we only use different scripts and words for a shared instance of a concept.

Let's take Leonardo da Vinci as an example.
The ontology defines the concept of a Person, a human being.
Now, in English its label would be _Leonardo da Vinci_, while in Japanese _レオナルド・ダ・ヴィンチ_.
Moreover, he is also known as _Leonardo di ser Piero da Vinci_ or _ダ・ビンチ_.

### Labels

Now, in the given example all words that a assigned to the concept are labels.
The label _Leonardo da Vinci_ is stored in the backend with an additional language code, e.g. _en_.

There is always a main label, which refers to the most common or official name of entity.
Another example would be Wacom, where _Wacom Co., Ltd._ is the official name while _Wacom_ is commonly used and be considered as an alias.

>  :pushpin: For the language code the **ISO 639-1:2002**, codes for the representation of names of languages—Part 1: Alpha-2 code. Read more, [here](https://www.iso.org/standard/22109.html)

## Samples

### Entity handling

This samples shows how to work with graph service.

```python
import argparse
from typing import Optional

from knowledge.base.entity import LanguageCode, Description, Label
from knowledge.base.ontology import OntologyClassReference, OntologyPropertyReference, ThingObject, ObjectProperty
from knowledge.services.graph import WacomKnowledgeService

# ------------------------------- Knowledge entities -------------------------------------------------------------------
LEONARDO_DA_VINCI: str = 'Leonardo da Vinci'
SELF_PORTRAIT_STYLE: str = 'self-portrait'
ICON: str = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Mona_Lisa_%28copy%2C_Thalwil%2C_Switzerland%29."\
            "JPG/1024px-Mona_Lisa_%28copy%2C_Thalwil%2C_Switzerland%29.JPG"
# ------------------------------- Ontology class names -----------------------------------------------------------------
THING_OBJECT: OntologyClassReference = OntologyClassReference('wacom', 'core', 'Thing')
"""
The Ontology will contain a Thing class where is the root class in the hierarchy. 
"""
ARTWORK_CLASS: OntologyClassReference = OntologyClassReference('wacom', 'creative', 'VisualArtwork')
PERSON_CLASS: OntologyClassReference = OntologyClassReference('wacom', 'core', 'Person')
ART_STYLE_CLASS: OntologyClassReference = OntologyClassReference.parse('wacom:creative#ArtStyle')
IS_CREATOR: OntologyPropertyReference = OntologyPropertyReference('wacom', 'core', 'created')
HAS_TOPIC: OntologyPropertyReference = OntologyPropertyReference.parse('wacom:core#hasTopic')
CREATED: OntologyPropertyReference = OntologyPropertyReference.parse('wacom:core#created')
HAS_ART_STYLE: OntologyPropertyReference = OntologyPropertyReference.parse('wacom:creative#hasArtstyle')


def print_entity(display_entity: ThingObject, list_idx: int, auth_key: str, client: WacomKnowledgeService,
                 short: bool = False):
    """
    Printing entity details.

    Parameters
    ----------
    display_entity: ThingObject
        Entity with properties
    list_idx: int
        Index with a list
    auth_key: str
        Authorization key
    client: WacomKnowledgeService
        Knowledge graph client
    short: bool
        Short summary
    """
    print(f'[{list_idx}] : {display_entity.uri} <{display_entity.concept_type.iri}>')
    if len(display_entity.label) > 0:
        print('    | [Labels]')
        for la in display_entity.label:
            print(f'    |     |- "{la.content}"@{la.language_code}')
        print('    |')
    if not short:
        if len(display_entity.alias) > 0:
            print('    | [Alias]')
            for la in display_entity.alias:
                print(f'    |     |- "{la.content}"@{la.language_code}')
            print('    |')
        if len(display_entity.data_properties) > 0:
            print('    | [Attributes]')
            for data_property, labels in entity.data_properties.items():
                print(f'    |    |- {data_property.iri}:')
                for li in labels:
                    print(f'    |    |-- "{li.value}"@{li.language_code}')
            print('    |')

        relations_obj: Dict[OntologyPropertyReference, ObjectProperty] = client.relations(auth_key=auth_key,
                                                                                          uri=entity.uri)
        if len(relations_obj) > 0:
            print('    | [Relations]')
            for re in relations_obj.values():
                print(f'    |--- {re.relation.iri}: ')
                print(f'           |- [Incoming]: {re.incoming_relations} ')
                print(f'           |- [Outgoing]: {re.outgoing_relations}')
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default='https://private-knowledge.wacom.com',
                        help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom personal knowledge REST API Client
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(application_name="Wacom Knowledge Listing",
                                                                    service_url=args.instance)
    # Use special tenant for testing:  Unit-test tenant
    user_token, refresh_token, expiration_time = knowledge_client.request_user_token(TENANT_KEY, EXTERNAL_USER_ID)
    page_id: Optional[str] = None
    page_number: int = 1
    entity_count: int = 0
    print('-----------------------------------------------------------------------------------------------------------')
    print(' First step: Find Leonardo da Vinci in the knowledge graph.')
    print('-----------------------------------------------------------------------------------------------------------')
    res_entities, next_search_page = knowledge_client.search_labels(auth_key=user_token, search_term=LEONARDO_DA_VINCI,
                                                                    language_code=LanguageCode('en_US'), limit=1000)
    leo: Optional[ThingObject] = None
    s_idx: int = 1
    for res_entity in res_entities:
        #  Entity must be a person and the label match with full string
        if res_entity.concept_type == PERSON_CLASS and LEONARDO_DA_VINCI in [la.content for la in res_entity.label]:
            leo = res_entity
            break

    print('-----------------------------------------------------------------------------------------------------------')
    print(' What artwork exists in the knowledge graph.')
    print('-----------------------------------------------------------------------------------------------------------')
    relations_dict: Dict[OntologyPropertyReference, ObjectProperty] = knowledge_client.relations(auth_key=user_token,
                                                                                                 uri=leo.uri)
    print(f' Artwork of {leo.label}')
    print('-----------------------------------------------------------------------------------------------------------')
    idx: int = 1
    if CREATED in relations_dict:
        for e in relations_Dict[CREATED].outgoing_relations:
            print(f' [{idx}] {e.uri}: {e.label}')
            idx += 1
    print('-----------------------------------------------------------------------------------------------------------')
    print(' Let us create a new piece of artwork.')
    print('-----------------------------------------------------------------------------------------------------------')

    # Main labels for entity
    artwork_labels: List[Label] = [
        Label('Ginevra Gherardini', LanguageCode('en_US')),
        Label('Ginevra Gherardini', LanguageCode('de_DE'))
    ]
    # Alias labels for entity
    artwork_alias: List[Label] = [
        Label("Ginevra", LanguageCode('en_US')),
        Label("Ginevra", LanguageCode('de_DE'))
    ]
    # Topic description
    artwork_description: List[Description] = [
        Description('Oil painting of Mona Lisa\' sister', LanguageCode('en_US')),
        Description('Ölgemälde von Mona Lisa\' Schwester', LanguageCode('de_DE'))
    ]
    # Topic
    artwork_object: ThingObject = ThingObject(label=artwork_labels, concept_type=ARTWORK_CLASS,
                                              description=artwork_description,
                                              icon=ICON)
    artwork_object.alias = artwork_alias
    print(f' Create: {artwork_object}')
    # Create artwork
    artwork_entity_uri: str = knowledge_client.create_entity(user_token, artwork_object)
    print(f' Entity URI: {artwork_entity_uri}')
    # Create relation between Leonardo da Vinci and artwork
    knowledge_client.create_relation(auth_key=user_token, source=leo.uri, relation=IS_CREATOR,
                                     target=artwork_entity_uri)

    relations_dict = knowledge_client.relations(auth_key=user_token, uri=artwork_entity_uri)
    for ontology_property, object_property in relations_dict.items():
        print(f'  {object_property}')
    # You will see that wacom:core#isCreatedBy is automatically inferred as relation as it is the inverse property of
    # wacom:core#created.

    # Now, more search options
    res_entities, next_search_page = knowledge_client.search_description(user_token, 'Michelangelo\'s Sistine Chapel',
                                                                         LanguageCode('en_US'), limit=1000)
    print('-----------------------------------------------------------------------------------------------------------')
    print(' Search results.  Description: "Michelangelo\'s Sistine Chapel"')
    print('-----------------------------------------------------------------------------------------------------------')
    s_idx: int = 1
    for e in res_entities:
        print_entity(e, s_idx, user_token, knowledge_client)

    # Now, let's search all artwork that has the art style self-portrait
    res_entities, next_search_page = knowledge_client.search_labels(auth_key=user_token,
                                                                    search_term=SELF_PORTRAIT_STYLE,
                                                                    language_code=LanguageCode('en_US'), limit=1000)
    art_style: Optional[ThingObject] = None
    s_idx: int = 1
    for entity in res_entities:
        #  Entity must be a person and the label match with full string
        if entity.concept_type == ART_STYLE_CLASS and SELF_PORTRAIT_STYLE in [l.content for l in entity.label]:
            art_style = entity
            break
    res_entities, next_search_page = knowledge_client.search_relation(auth_key=user_token,
                                                                      subject_uri=None,
                                                                      relation=HAS_ART_STYLE,
                                                                      object_uri=art_style.uri,
                                                                      language_code=LanguageCode('en_US'))
    print('-----------------------------------------------------------------------------------------------------------')
    print(' Search results.  Relation: relation:=has_topic  object_uri:= unknown')
    print('-----------------------------------------------------------------------------------------------------------')
    s_idx: int = 1
    for e in res_entities:
        print_entity(e, s_idx, user_token, knowledge_client, short=True)
        s_idx += 1

    # Finally, the activation function retrieving the related identities to a pre-defined depth.
    entities, relations = knowledge_client.activations(auth_key=user_token,
                                                       uris=[leo.uri],
                                                       depth=1)
    print('-----------------------------------------------------------------------------------------------------------')
    print(f'Activation.  URI: {leo.uri}')
    print('-----------------------------------------------------------------------------------------------------------')
    s_idx: int = 1
    for e in res_entities:
        print_entity(e, s_idx, user_token, knowledge_client)
        s_idx += 1
    # All relations
    print('-----------------------------------------------------------------------------------------------------------')
    for r in relations:
        print(f'Subject: {r[0]} Predicate: {r[1]} Object: {r[2]}')
    print('-----------------------------------------------------------------------------------------------------------')
    page_id = None

    # Listing all entities which have the type
    idx: int = 1
    while True:
        # pull
        entities, total_number, next_page_id = knowledge_client.listing(user_token, ART_STYLE_CLASS, page_id=page_id,
                                                                        limit=100)
        pulled_entities: int = len(entities)
        entity_count += pulled_entities
        print('-------------------------------------------------------------------------------------------------------')
        print(f' Page: {page_number} Number of entities: {len(entities)}  ({entity_count}/{total_number}) '
              f'Next page id: {next_page_id}')
        print('-------------------------------------------------------------------------------------------------------')
        for e in entities:
            print_entity(e, idx, user_token, knowledge_client)
            idx += 1
        if pulled_entities == 0:
            break
        page_number += 1
        page_id = next_page_id
    print()
    # Delete all personal entities for this user
    while True:
        # pull
        entities, total_number, next_page_id = knowledge_client.listing(user_token, THING_OBJECT, page_id=page_id,
                                                                        limit=100)
        pulled_entities: int = len(entities)
        if pulled_entities == 0:
            break
        delete_uris: List[str] = [e.uri for e in entities]
        print(f'Cleanup. Delete entities: {delete_uris}')
        knowledge_client.delete_entities(auth_key=user_token, uris=delete_uris, force=True)
        page_number += 1
        page_id = next_page_id
    print('-----------------------------------------------------------------------------------------------------------')
```

### Named Entity Linking 

Performing Named Entity Linking (NEL) on text and Universal Ink Model.

```python
import argparse

import urllib3

from knowledge.base.entity import LanguageCode
from knowledge.base.ontology import OntologyPropertyReference, ThingObject, ObjectProperty
from knowledge.nel.base import KnowledgeGraphEntity
from knowledge.nel.engine import WacomEntityLinkingEngine
from knowledge.services.graph import WacomKnowledgeService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


LANGUAGE_CODE: LanguageCode = LanguageCode("en_US")
TEXT: str = "Leonardo da Vinci painted the Mona Lisa."


def print_entity(entity: KnowledgeGraphEntity, list_idx: int, auth_key: str, client: WacomKnowledgeService):
    """
    Printing entity details.

    Parameters
    ----------
    entity: KnowledgeGraphEntity
        Named entity
    list_idx: int
        Index with a list
    auth_key: str
        Authorization key
    client: WacomKnowledgeService
        Knowledge graph client
    """
    thing: ThingObject = knowledge_client.entity(auth_key=user_token, uri=entity.entity_source.uri)
    print(f'[{list_idx}] - {e.ref_text} [{e.start_idx}-{e.end_idx}] : {thing.uri} <{thing.concept_type.iri}>')
    if len(thing.label) > 0:
        print('    | [Labels]')
        for la in thing.label:
            print(f'    |     |- "{la.content}"@{la.language_code}')
        print('    |')
    if len(thing.label) > 0:
        print('    | [Alias]')
        for la in thing.alias:
            print(f'    |     |- "{la.content}"@{la.language_code}')
        print('    |')
    relations: Dict[OntologyPropertyReference, ObjectProperty] = client.relations(auth_key=auth_key, uri=thing.uri)
    if len(thing.data_properties) > 0:
        print('    | [Attributes]')
        for data_property, labels in thing.data_properties.items():
            print(f'    |    |- {data_property.iri}:')
            for li in labels:
                print(f'    |    |-- "{li.value}"@{li.language_code}')
        print('    |')
    if len(relations) > 0:
        print('    | [Relations]')
        for re in relations.values():
            print(f'    |--- {re.relation.iri}: ')
            print(f'           |- [Incoming]: {re.incoming_relations} ')
            print(f'           |- [Outgoing]: {re.outgoing_relations}')
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default="https://private-knowledge.wacom.com", help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom personal knowledge REST API Client
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(
        application_name="Named Entity Linking Knowledge access",
        service_url=args.instance)
    #  Wacom Named Entity Linking
    nel_client: WacomEntityLinkingEngine = WacomEntityLinkingEngine(
        service_url=args.instance,
        service_endpoint=WacomEntityLinkingEngine.SERVICE_ENDPOINT
    )
    # Use special tenant for testing:  Unit-test tenant
    user_token, refresh_token, expiration_time = nel_client.request_user_token(TENANT_KEY, EXTERNAL_USER_ID)
    entities: List[KnowledgeGraphEntity] = nel_client.\
        link_personal_entities(auth_key=user_token, text=TEXT,
                               language_code=LANGUAGE_CODE)
    idx: int = 1
    print('-----------------------------------------------------------------------------------------------------------')
    print(f'Text: "{TEXT}"@{LANGUAGE_CODE}')
    print('-----------------------------------------------------------------------------------------------------------')
    for e in entities:
        print_entity(e, idx, user_token, knowledge_client)
        idx += 1

```

### Access Management

The sample shows, how access to entities can be shared with a group of users or the tenant.

```python
import argparse

from knowledge.base.entity import LanguageCode, Label, Description
from knowledge.base.ontology import OntologyClassReference, ThingObject
from knowledge.services.base import WacomServiceException
from knowledge.services.graph import WacomKnowledgeService
from knowledge.services.group import GroupManagementServiceAPI, Group
from knowledge.services.users import UserManagementServiceAPI

# ------------------------------- User credential ----------------------------------------------------------------------
TOPIC_CLASS: OntologyClassReference = OntologyClassReference('wacom', 'core', 'Topic')


def create_entity() -> ThingObject:
    """Create a new entity.

    Returns
    -------
    entity: ThingObject
        Entity object
    """
    # Main labels for entity
    topic_labels: List[Label] = [
        Label('Hidden', LanguageCode('en_US')),
        Label('Versteckt', LanguageCode('de_DE')),
        Label('隠れた', LanguageCode('ja_JP'))
    ]

    # Topic description
    topic_description: List[Description] = [
        Description('Hidden entity to explain access management.', LanguageCode('en_US')),
        Description('Verstecke Entität, um die Zugriffsteuerung zu erlären.', LanguageCode('de_DE'))
    ]
    # Topic
    topic_object: ThingObject = ThingObject(label=topic_labels, concept_type=TOPIC_CLASS, description=topic_description)
    return topic_object


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default='https://private-knowledge.wacom.com',
                        help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom personal knowledge REST API Client
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(application_name="Wacom Knowledge Listing",
                                                                    service_url=args.instance)
    # User Management
    user_management: UserManagementServiceAPI = UserManagementServiceAPI(service_url=args.instance)
    # Group Management
    group_management: GroupManagementServiceAPI = GroupManagementServiceAPI(service_url=args.instance)
    admin_token, refresh_token, expiration_time = user_management.request_user_token(TENANT_KEY, EXTERNAL_USER_ID)
    # Now, we create a users
    u1, u1_token, _, _ = user_management.create_user(TENANT_KEY, "u1")
    u2, u2_token, _, _ = user_management.create_user(TENANT_KEY, "u2")
    u3, u3_token, _, _ = user_management.create_user(TENANT_KEY, "u3")

    # Now, let's create an entity
    thing: ThingObject = create_entity()
    entity_uri: str = knowledge_client.create_entity(u1_token, thing)
    # Only user 1 can access the entity from cloud storage
    my_thing: ThingObject = knowledge_client.entity(u1_token, entity_uri)
    print(f'User is the owner of {my_thing.owner}')
    # Now only user 1 has access to the personal entity
    knowledge_client.entity(u1_token, entity_uri)
    # Try to access the entity
    try:
        knowledge_client.entity(u2_token, entity_uri)
    except WacomServiceException as we:
        print(f"Expected exception as user 2 has no access to the personal entity of user 1. Exception: {we}")
    # Try to access the entity
    try:
        knowledge_client.entity(u3_token, entity_uri)
    except WacomServiceException as we:
        print(f"Expected exception as user 3 has no access to the personal entity of user 1. Exception: {we}")
    # Now, user 1 creates a group
    g: Group = group_management.create_group(u1_token, "test-group")
    # Shares the join key with user 2 and user 2 joins
    group_management.join_group(u2_token, g.id, g.join_key)
    # Share entity with group
    group_management.add_entity_to_group(u1_token, g.id, entity_uri)
    # Now, user 2 should have access
    other_thing: ThingObject = knowledge_client.entity(u2_token, entity_uri)
    print(f'User 2 is the owner of the thing: {other_thing.owner}')
    # Try to access the entity
    try:
        knowledge_client.entity(u3_token, entity_uri)
    except WacomServiceException as we:
        print(f"Expected exception as user 3 still has no access to the personal entity of user 1. Exception: {we}")
    # Un-share the entity
    group_management.remove_entity_to_group(u1_token, g.id, entity_uri)
    # Now, again no access
    try:
        knowledge_client.entity(u2_token, entity_uri)
    except WacomServiceException as we:
        print(f"Expected exception as user 2 has no access to the personal entity of user 1. Exception: {we}")
    group_management.leave_group(u2_token, group_id=g.id)
    # Now, share the entity with the whole tenant
    my_thing.tenant_access_right.read = True
    knowledge_client.update_entity(u1_token, my_thing)
    # Now, all users can access the entity
    knowledge_client.entity(u2_token, entity_uri)
    knowledge_client.entity(u3_token, entity_uri)
    # Finally, clean up
    knowledge_client.delete_entity(u1_token, entity_uri, force=True)
    # Remove users
    user_management.delete_user(TENANT_KEY, u1.external_user_id, u1.id)
    user_management.delete_user(TENANT_KEY, u2.external_user_id, u2.id)
    user_management.delete_user(TENANT_KEY, u3.external_user_id, u3.id)

```

### Ontology Creation

The samples show how the ontology can be extended and new entities can be added using the added classes.

```python
# -*- coding: utf-8 -*-
# Copyright © 2021-2022 Wacom Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language_code governing permissions and
#  limitations under the License.
import argparse
from typing import Optional

from knowledge.base.entity import Label, LanguageCode, Description
from knowledge.base.ontology import DataPropertyType, OntologyClassReference, OntologyPropertyReference, ThingObject, \
    DataProperty, OntologyContext
from knowledge.services.graph import WacomKnowledgeService
from knowledge.services.ontology import OntologyService

# ------------------------------- Constants ----------------------------------------------------------------------------
LEONARDO_DA_VINCI: str = 'Leonardo da Vinci'
CONTEXT_NAME: str = 'core'
# Wacom Base Ontology Types
PERSON_TYPE: OntologyClassReference = OntologyClassReference.parse("wacom:core#Person")
# Demo Class
ARTIST_TYPE: OntologyClassReference = OntologyClassReference.parse("demo:creative#Artist")
# Demo Object property
IS_INSPIRED_BY: OntologyPropertyReference = OntologyPropertyReference.parse("demo:creative#isInspiredBy")
# Demo Data property
STAGE_NAME: OntologyPropertyReference = OntologyPropertyReference.parse("demo:creative#stageName")


def create_artist() -> ThingObject:
    """
    Create a new artist entity.
    Returns
    -------
    instance: ThingObject
        Artist entity
    """
    # Main labels for entity
    topic_labels: List[Label] = [
        Label('Gian Giacomo Caprotti', LanguageCode('en_US'))
    ]

    # Topic description
    topic_description: List[Description] = [
        Description('Hidden entity to explain access management.', LanguageCode('en_US')),
        Description('Verstecke Entität, um die Zugriffsteuerung zu erlären.', LanguageCode('de_DE'))
    ]

    data_property: DataProperty = DataProperty(content='Salaj',
                                               property_ref=STAGE_NAME,
                                               language_code=LanguageCode('en_US'))
    # Topic
    artist: ThingObject = ThingObject(label=topic_labels, concept_type=ARTIST_TYPE, description=topic_description)
    artist.add_data_property(data_property)
    return artist


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="External Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-t", "--tenant", help="Tenant Id of the shadow user within the Wacom Private Knowledge.",
                        required=True)
    parser.add_argument("-i", "--instance", default="https://private-knowledge.wacom.com", help="URL of instance")
    args = parser.parse_args()
    TENANT_KEY: str = args.tenant
    EXTERNAL_USER_ID: str = args.user
    # Wacom Ontology REST API Client
    ontology_client: OntologyService = OntologyService(service_url=args.instance)
    admin_token, refresh_token, expiration_time = ontology_client.request_user_token(TENANT_KEY, EXTERNAL_USER_ID)
    knowledge_client: WacomKnowledgeService = WacomKnowledgeService(
        application_name="Ontology Creation Demo",
        service_url=args.instance)
    context: Optional[OntologyContext] = ontology_client.context(admin_token)
    if context is None:
        # First, create a context for the ontology
        ontology_client.create_context(admin_token, name=CONTEXT_NAME, base_uri=f'demo:{CONTEXT_NAME}')
        context_name: str = CONTEXT_NAME
    else:
        context_name: str = context.context
    # Creating a class which is a subclass of a person
    ontology_client.create_concept(admin_token, context_name, reference=ARTIST_TYPE, subclass_of=PERSON_TYPE)

    # Object properties
    ontology_client.create_object_property(auth_key=admin_token, context=context_name,
                                           reference=IS_INSPIRED_BY, domains_cls=[ARTIST_TYPE],
                                           ranges_cls=[PERSON_TYPE], inverse_of=None, subproperty_of=None)
    # Data properties
    ontology_client.create_data_property(auth_key=admin_token, context=context_name,
                                         reference=STAGE_NAME,
                                         domains_cls=[ARTIST_TYPE],
                                         ranges_cls=[DataPropertyType.STRING],
                                         subproperty_of=None)
    # Commit the changes of the ontology. This is very important to confirm changes.
    ontology_client.commit(admin_token, context_name)
    # Trigger graph service. After the update the ontology is available and the new entities can be created
    knowledge_client.ontology_update(admin_token)

    res_entities, next_search_page = knowledge_client.search_labels(auth_key=admin_token, search_term=LEONARDO_DA_VINCI,
                                                                    language_code=LanguageCode('en_US'), limit=1000)
    leo: Optional[ThingObject] = None
    for entity in res_entities:
        #  Entity must be a person and the label match with full string
        if entity.concept_type == PERSON_TYPE and LEONARDO_DA_VINCI in [la.content for la in entity.label]:
            leo = entity
            break

    artist_student: ThingObject = create_artist()
    artist_student_uri: str = knowledge_client.create_entity(admin_token, artist_student)
    knowledge_client.create_relation(admin_token, artist_student_uri, IS_INSPIRED_BY, leo.uri)

```

## Tools

The following samples show how to utilize the library to work with Wacom's Personal Knowledge.

### Listing script

Listing the entities for tenant. 

```bash
>> python listing.py [-h] -u USER -t TENANT [-r] [-i INSTANCE]
```

**Parameters:**

- _-i INSTANCE, --instance INSTANCE_ - URL of instance
- _-u USER, --user USER_ - External ID to identify user of the Wacom Private Knowledge 
- _-t TENANT, --tenant TENANT_ - Tenant key to identify tenant
- _-r, --relations (optional)_ -  Requesting the relations for each entity

### Export entities script

Dump all entities of a user to a ndjson file. 

```bash
>> python export_entities.py [-h] -u USER -t TENANT [-r] [-a] [-p] [-d DUMP]
                              [-c CONCEPT_TYPE] [-i INSTANCE]
```

**Parameters:**

- _-i INSTANCE, --instance INSTANCE_ - URL of instance. (default:=https://private-
                        knowledge.wacom.com)
- _-u USER, --user USER_ - External ID to identify user of the Wacom Private Knowledge 
- _-t TENANT, --tenant TENANT_ - Tenant key to identify tenant
- _-r, --relations (optional)_ -  Requesting the relations for each entity
- _-a, --all (optional)_ - All entities the user as access to, otherwise only his own entities are dumped.
- _-p, --images (optional)_ - Include the images in the dump.
- _-d DUMP, --dump DUMP_ -  Defines the location of the dump path.
 
### Import entities script

Pushing entities to knowledge graph.

```bash
>> python import_entities.py [-h] [-u USER] [-t TENANT] [-g GROUP_NAME] [-r] [-i INSTANCE]
```

**Parameters:**

- _-i INSTANCE, --instance INSTANCE_ - URL of instance
- _-u USER, --user USER_ - External ID to identify user of the Wacom Private Knowledge 
- _-t TENANT, --tenant TENANT_ - Tenant key to identify tenant
- _-i CACHE, --cache CACHE_ - Path to entities that must be imported.
- _-g GROUP_NAME, --group_id GROUP_NAME_ - Group name where the entities will be assigned to. 
- _-p , --public_ - Group name where the entities will be assigned to.

### Wikidata scrapper

```bash
usage: wikidata_scrapper.py [-h] -u USER -t TENANT [-i INSTANCE] [-c CACHE]
                            [-m MAPPING] [-d DEPTH]
                            [-l LANGUAGES [LANGUAGES ...]]
wikidata_scrapper.py: error: the following arguments are required: -u/--user, -t/--tenant
```

**Parameters:**

- _-i INSTANCE, --instance INSTANCE_ - URL of instance
- _-u USER, --user USER_ - External ID to identify user of the Wacom Private Knowledge
- _-t TENANT, --tenant TENANT_ - Tenant key to identify tenant
- _-c CACHE, --cache CACHE_ - Path to entities that must are exports in import format.
- _-m MAPPING, --mapping MAPPING_ - Mapping file to configure the wikidata mapping.
- _-d DEPTH, --depth DEPTH_ - Depth of the graph to be scrapped.
- _-l LANGUAGES [LANGUAGES ...], --languages LANGUAGES [LANGUAGES ...]_ - Languages to be scrapped.
  
# Documentation

You can find more detailed technical documentation, [here](https://developer-docs.wacom.com/preview/semantic-ink/).
API documentation is available [here](./docs/).

## Contributing
Contribution guidelines are still work in progress.

## License
[Apache License 2.0](LICENSE)
