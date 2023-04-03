# Azure OpenAI API Samples (Microsoft Confidential for authorized users)
Welcome to the Azure OpenAI (AOAI) API samples for DV3!

This repo gives you instructions and code samples to get started with the AOAI API.

While much of the information here is common with the public AOAI API, please treat all parts of this repo as Microsoft Confidential for specific authorized users only.  Only users authorized by their respective teams have access to this repository.  Do not share the contents of this repository with anybody who is not a member of your team's authorized users.

## Getting Access
If you're here we assume that your team's API administrators have authorized you for access to the API.  Here is the list of [team API administrators](team_contacts.md).

## Using the API

You can call the API in the following ways:
1. Directly call the AOAI REST API using your method of choice.  This includes and is not limited to:
    * Python `requests`, JavaScript, C#, etc.
    * `curl` from command line 
    * Postman : Use only local installed versions of programs like Postman, not cloud hosted versions.  You should check status of 3rd party tools carefully so that they are not logging confidential information.
2. Call the AOAI API using the OpenAI Python SDK

To call the API, you need to authenticate with Azure Active Directory (AAD).

## Table of Contents

|Topic| 
|--|
| [Setup to use AAD and test with CLI](setup_aad.md) | 
| [Setup Python virtual environment](setup_python_env.md) | 
| [Sample Python notebook for OpenAI SDK](aad_integration_example_sdk.ipynb) |  
| [Sample Python notebook for REST](aad_integration_example_restapi.ipynb) |


## Azure OpenAI Documentation
The public documentation for the AOAI API is available at [Azure OpenAI Documentation](hhttps://learn.microsoft.com/en-us/azure/cognitive-services/openai/).  Note that not all parts of the public documentation apply for your usage.  Reach out to the AOAI team (below) for any questions.

