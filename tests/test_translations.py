import pytest
from graphene.test import Client
from flaskr.app import schema

def test_translations(client):
    query = """
    { translations(targetLanguageId: 2, methodId: 58)
        {
          	relevanceRating
          	method {
          	  id
              name
              description
              syntax
              snippet
              docsUrl
          	}
    	}
    }
    """
    client = Client(schema)
    response = client.execute(query)
    assert response['data']
