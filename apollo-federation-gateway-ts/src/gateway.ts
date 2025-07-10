// import { ApolloServer } from '@apollo/server';
// import { startStandaloneServer } from '@apollo/server/standalone';
// import { ApolloGateway, IntrospectAndCompose } from '@apollo/gateway';

// const gateway = new ApolloGateway({
//   supergraphSdl: new IntrospectAndCompose({
//    subgraphs: [
//   { name: 'user_services', url: "http://user_services:8000/graphql" },
//   { name: 'asset_service', url: "http://asset_service:8000/graphql" },
//     ],
//   }),
// });

// async function startServer() {
//   const server = new ApolloServer({
//     gateway,
//   });

//   const { url } = await startStandaloneServer(server, {
//     listen: { port: 4000 },
//   });

//   console.log(`🚀 Gateway ready at ${url}`);
// }

// startServer().catch(console.error);




import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import {
  ApolloGateway,
  IntrospectAndCompose,
  RemoteGraphQLDataSource,
} from '@apollo/gateway';

// Define the Apollo Gateway with header forwarding logic
const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
  { name: 'user_services', url: "http://user_services:8000/graphql" },
  { name: 'asset_service', url: "http://asset_service:8000/graphql" },
    ],
  }),

  // Forward the `Authorization` header to subgraphs
  buildService({ url }) {
    return new RemoteGraphQLDataSource({
      url,
      willSendRequest({ request, context }) {
        const token = context.authorization;
        if (token && request.http?.headers) {
          request.http.headers.set('authorization', token);
        }
      },
    });
  },
});

// Start the server with context forwarding
async function startServer() {
  const server = new ApolloServer({
    gateway,
    // Disable subscriptions (not supported in gateway mode)
    // if not needed, this line is optional:
    // subscriptions: false,
  });

  const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
    context: async ({ req }) => {
      console.log("HEADERS", req.headers);
      return {
        // Forward `authorization` header from client (e.g., Apollo Sandbox)
        authorization: req.headers.authorization || '',
      };
    },
  });

  console.log(`🚀 Apollo Gateway running at ${url}`);
}

startServer().catch((err) => {
  console.error('🚨 Failed to start Apollo Gateway:', err);
});
