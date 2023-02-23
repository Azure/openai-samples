
# OpenAI Samples

This repository contains samples demonstrating how to use GPT and ChatGpt via python SDK or REST API.

<br>

## Installation
Install all of the Python modules and packages listed in the requirements.txt file using the below command.

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

Learn more about Azure OpenAI Service REST API here:
https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference

## Example code
Sample codes for various use case scenario using GPT/ChatGPT can be found in respective 'Python SDK' & 'RestAPI' folders. 


## Requirements
Python 3.7.1+


<br>
<br>


# Project
> This repo has been populated by an initial template to help get you started. Please
> make sure to update the content to build a great experience for community-building.

As the maintainer of this project, please make a few updates:

- Improving this README.MD file to provide a great experience
- Updating SUPPORT.MD with content about this project's support experience
- Understanding the security reporting process in SECURITY.MD
- Remove this section from the README

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


