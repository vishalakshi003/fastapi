from src.api.graphql.schemas import schema
with open("schema.graphql", "w") as f:
    f.write(schema.as_str())