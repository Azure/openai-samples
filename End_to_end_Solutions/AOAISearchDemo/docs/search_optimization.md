# Overview

Search is a fundamental part of this solution, which helps find the results in the enterprise resources adequately.
This entails the ability to leverage both forms of data (structured and unstructured data) as well as managing the amount of content that is being presented to the models.
In the following we would consider the different approaches to help optimize the end-to-end experience and using search in multiple manners.

# Optimization of unstructured content

The unstructured content is more challenging in the sense that the data needs to be organized, indexed, and then used in the runtime experience to retrieve responses to the user queries.
In turn there are choices to be exercised at the various stages of this process. In the following we would be exploring each of these choices with pros and cons

## Creating the Index

Documents used in the enterprise come in different forms, including mostly in DocX and PDFs.
In turn these documents need to be parsed and processed in some textual manner to be injected into an index that is usable for the purpose of this solution.
There are two approaches to do this parsing that work with different resolutions namely:

1. Page based parsing: This divides the documents (mostly PDF docs) into individual pages of content. The segmentation is done using the [Read API in the Form Understanding Cognitive Service](https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/concept-read?view=form-recog-3.0.0). The Read API can identify the individual pages and encapsulate all the content within this page in the output. The search index now uses this whole page as the target. Since the entire page is injected in the index, it has the potential to have more context in each content. The downside of this is that at retrieval time, each search result is an entire page. So when all of that is passed to AOAI to formulate the final answer, it has risk of growing the token size quickly. To be under the token limit, number of search results used needs to be reduced which can be done by filtering the search results that has less-relevant content.
2. Paragraph based parsing: This considers the paragraph as the basic building block of a document. It identifies the paragraph by location within a given section heading. This could be achieved using the [Layout API from the Form Understanding Cognitive Service](https://learn.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/concept-layout?view=form-recog-3.0.0) for PDF files or [OpenXML](https://learn.microsoft.com/en-us/office/open-xml/open-xml-sdk) for DocX files. The output of these APIs enable segmenting the document based on the paragraph mark and adding section heading tags to the index element. This has the potential of providing nugget sized elements and in-turn would not risk growing the prompt quickly, but has the risk of not providing enough context to produce a valuable answer. It is worth mentioning that context could be grown by merging multiple results that represent the same context.

## AOAI Prompt Formation

To answer user’s question, along with the System Prompt relevant search results returned from Azure Cognitive Search are sent to AOAI. There are different approaches that needs to be considered when considering how many search results needs to be included with the System Prompt

1. Thresholding: The number of documents retrieved to be included with the System Prompt is dependent on the type of query that the user presents as well as the index approach selected.
For example: A question about a very specific topic that is localized in the documents would require a limited number of documents. In this we can filter out large number of low-relevance ranked documents. This means we can have a very strict threshold value on search relevance score/rank for the results. On the other hand, a query that spans a
sparse set of information that is spread across multiple documents would entail the need to retrieve multiple content elements to compose a meaningful answer. This means that threshold value needs to be relaxed.
There is also dependence on the type of index used; where the page based approach would require limiting thresholds so prompts don't go beyond the allowed token limit, while on the other hand, paragraph based index has smaller content elements and hence allowing more context to be injected is preferred.
In both cases the threshold should consider both the number of documents (limited when using page based and large with paragraph-based index) as well as the relative score threshold (large would be siding on lower token count, and low would be siding on more content).
The latter would be included based on the tradeoff of quality and prompt size. In this demo we have selected a threshold of 50% of the top-ranking score to be the threshold. Anything below that score is ignored.
2. Including History: The chat history is fundamental to grounding the result on the conversation. Including history enables handling of user's follow up requests. This is done by merging prior dialogues with the current user input to adequately establish context of the current query.
3. Prompt limitation: Despite the effort in thresholding, the prompt size could large enough to go beyond the max token allowance (given that we need to allow for the answer to be returned).
This requires that the size of the input prompt be measured, and the search results injected be reduced accordingly (even if they satisfy the threshold requirements). Working to remove the least relevant search results as well as reducing the amount of history would keep the prompt within limits. It is worth mentioning that the reduction through removing search results would be more effective compared to reducing history elements.
4. Summarizing/aggregation of content: Based on the type of index and the nominal size of the content, either summarizing the individual content (when individual search results are big), or aggregation in case when the individual search results are shorter (paragraph based index for example) could also be considered. Summarization could be done by using semantic search capabilities or through summarization using AOAI. When using semantic search feature of the Azure Cognitive Search, the search results also include summarized content. Another alternative is using key phrase extraction.
On the other hand, aggregation of content could be through expanding content that has more coverage to the topic. This could be through including full section content when more than one result is shared in the same section.
