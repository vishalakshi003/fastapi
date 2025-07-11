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

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'user_services', url: "http://user_services:8000/graphql" },
      { name: 'asset_service', url: "http://asset_service:8000/graphql" },
    ],
  }),
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

async function startServer() {
  const server = new ApolloServer({
    gateway,
    plugins: [
      {
        async requestDidStart() {
          return {
            async willSendResponse({ response }) {
              const body = response.body as any;
              const errors = body?.singleResult?.errors;

              if (errors?.length) {
                const statusCode =
                  errors[0]?.extensions?.status_code ||
                  errors[0]?.extensions?.status ||
                  errors[0]?.extensions?.response?.status ||
                  400;

                if (response.http) {
                  response.http.status = statusCode;
                  response.http.headers.set('X-Original-Status', String(statusCode));
                }
              }
            },
          };
        },
      },
    ],
  });

  const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
    context: async ({ req }) => {
      console.log("HEADERS", req.headers);
      return {
        authorization: req.headers.authorization || '',
      };
    },
  });

  console.log(`🚀 Apollo Gateway running at ${url}`);
}

startServer().catch(console.error);
