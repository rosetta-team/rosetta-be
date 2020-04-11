import json
import pytest
from .conftest import client
# from graphene.test import Client
from flaskr.app import schema

def test_translations(client):
    # print('hello world')
    query = """
    {
        translations(targetLanguageId: 2,methodId: 58) {
            name
            snippet
            syntax
            description
            docsUrl
            methodResults {
                edges {
                    node {
                        relevanceRating
                    }
                }
            }
        }
    }
    """
    # client = Client(schema)
    # response = client.execute(query)
    # import code; code.interact(local=locals())
    response = client.post('/graphql', query)
    print(response)
    # print('I am here!')
    # assert response == {
