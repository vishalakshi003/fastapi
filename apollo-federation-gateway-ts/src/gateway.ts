import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { ApolloGateway, IntrospectAndCompose } from '@apollo/gateway';

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'user_services', url: 'http://localhost:8000/graphql' },
      { name: 'asset_service', url: 'http://localhost:8001/graphql' },
    ],
  }),
});

async function startServer() {
  const server = new ApolloServer({
    gateway,
  });

  const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
  });

  console.log(`🚀 Gateway ready at ${url}`);
}

startServer().catch(console.error);
