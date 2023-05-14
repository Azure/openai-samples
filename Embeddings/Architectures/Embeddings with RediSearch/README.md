# RediSearch
<img align="right" src="../images/redis.svg" style="width: 10%; margin-right: 10%; margin-left: 5%">

For scenarios with a larger number of embeddings, or running in a production environment, the best option is to index the embeddings and metadata in a low-latency vector database. This works well at all scales because the data is stored and managed by an external data store (i.e. it can scale/grow separately from your application).

In this example, we use the [RediSearch](https://redis.io/docs/stack/search/reference/vectors/) module in [Azure Cache for Redis](https://azure.microsoft.com/en-us/products/cache/) to store the vector embeddings and associated metadata.

## When to use this approach

We recommend this approach for production-ready scenarios where you have 10,000 or more embeddings, data needs to be updated, and current (or future) scale is a concern.

Pros:
* Externalized data storage for easier vector index updates
* Scalable and performant
* Enterprise-readiness and guaranteed SLAs
* Easy-to-use with client libraries available in most languages

Cons:
* Can be more costly depending on the situation

## Architecture Overview
This folder shows a basic end to end example of how to use RediSearch to store and query vector embeddings. To see an example of a more full embeddings architecture, see [https://github.com/ruoccofabrizio/azure-open-ai-embeddings-qna](https://github.com/ruoccofabrizio/azure-open-ai-embeddings-qna).

![RediSearch Architecture](../images/redisearch_architecture.png)

The App receives the text as an input:
1. Convert input text to an embedding with OpenAI
2. Find the top `k` most similar paragraphs to the input embedding in RediSearch
3. Build a full prompt using the relevant document sections as context
4. Answer the question with OpenAI and the provided context

In this [notebook](./Question_Answering_with_Embeddings_in_Redis.ipynb), we walk you through the process of:
1. Connecting to your Redis cluster, either in Azure Cache for Redis or through docker
2. Creating a RediSearch index
3. Loading documents into the index
4. Querying the index

The notebook shows the end-to-end flow for a question answering scenario and you can easily pull the relevant code to work well for your use case.

## Running the example

To run this sample, you either need to have a Redis cluster running locally or in Azure Cache for Redis. Follow the instuctions here to use [RediSearch with Azure Cache for Redis](https://learn.microsoft.com/azure/azure-cache-for-redis/cache-redis-modules#adding-modules-to-your-cache).

Alternatively, to run this tutorial with a docker container, see the instructions in the [docker folder](../docker/README.md).

## Other Resources

- [Vector Similarity Search: From Basics to Production](https://mlops.community/vector-similarity-search-from-basics-to-production/)
- [AI-Powered Document Search in Redis](https://datasciencedojo.com/blog/ai-powered-document-search/)
- Another [Azure OpenAI Question Answering Example](https://github.com/ruoccofabrizio/azure-open-ai-embeddings-qna)
- [Rediscover Redis for Vector Similarity Search](https://redis.com/blog/rediscover-redis-for-vector-similarity-search/)
- [arXiv Paper Search with Redis](https://github.com/RedisVentures/redis-arXiv-search)
