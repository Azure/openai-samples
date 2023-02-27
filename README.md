
# What is the Azure OpenAI service?

Azure OpenAI Service provides REST API access to OpenAI's powerful language models including the GPT-3, Codex and Embeddings model series. These models can be easily adapted to your specific task including but not limited to content generation, summarization, semantic search, and natural language to code translation. Users can access the service through REST APIs, Python SDK, or our web-based interface in the Azure OpenAI Studio.

# Important concepts and terminology
Refer to the following documents for a better understanding of Azure OpenAI concepts and the related terminology:

 - [How to generate or manipulate text](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/completions) 
 - [What are embeddings?](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/concepts/understand-embeddings)
 - [How to generate embeddings?](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/embeddings?tabs=console)

# Responsible AI with Azure OpenAI
At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Generative models such as the ones available in Azure OpenAI have significant potential benefits, but without careful design and thoughtful mitigations, such models have the potential to generate incorrect or even harmful content. Microsoft has made significant investments to help guard against abuse and unintended harm, which includes requiring applicants to show well-defined use cases, incorporating Microsoft’s [principles for responsible AI use](https://www.microsoft.com/ai/responsible-ai?activetab=pivot1:primaryr6), building content filters to support customers, and providing responsible AI implementation guidance to onboarded customers.

More details on the RAI guidelines for the Azure OpenAI service can be found [here](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/transparency-note?context=/azure/cognitive-services/openai/context/context).

# OpenAI Samples

This repository contains samples demonstrating how to use GPT and ChatGPT via Python SDK or REST API.

## Installation
Install all Python modules and packages listed in the requirements.txt file using the below command.

```python
pip install -r requirements.txt
```

### Microsoft Azure Endpoints
In order to use the Open AI library or REST API with Microsoft Azure endpoints, you need to set OPENAI_API_KEY, RESOURCE_NAME & DEPLOYMENT_NAME in _config.json_ file.

```js
{
    "DEPLOYMENT_NAME":"<GPT model name>",
    "RESOURCE_NAME":"<your azure resource name>",
    "OPENAI_API_KEY":"<your_api_key>"
}
``` 

Learn more about Azure OpenAI Service REST API [here](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference).

## Example code
Sample codes for various use case scenario using GPT/ChatGPT can be found in respective 'Python SDK' & 'RestAPI' folders. 


## Requirements
Python 3.7.1+


<br>
<br>


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.


