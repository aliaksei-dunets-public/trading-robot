from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from app.graphql.queries import Query
from app.graphql.mutations import Mutation

app = FastAPI()

schema = Schema(query=Query, mutation=Mutation)

app.add_route("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Trading Robot API"}
