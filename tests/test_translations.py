import json
import pytest
# from .conftest import client
from graphene.test import Client
from flaskr.app import schema

def test_translations():
    print('hello world')
    # import code; code.interact(local=dict(globals(), **locals()))
    query = """
    {
        translations(sourceLanguageId: 1,targetLanguageId: 2,sourceMethodId: 58) {
            sourceMethod {
                name
                snippet
                syntax
                description
                docs_url
            }
            methodResults(first: 5) {
                edges {
                    node {
                        name
                        snippet
                        syntax
                        description
                        docs_url
                    }
                }
            }
        }
    }
    """
    client = Client(schema)
    response = client.execute(query)
    print(response)
    print('I am here!')
    # assert response == {
