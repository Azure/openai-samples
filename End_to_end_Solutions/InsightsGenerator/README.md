# Insights Generator

## Overview
Insights Generator (IG) is a GPT powered tool to extract summarized insights from a natural language corpus.
IG comes in two flavours:
a) IG for product reviews
b) IG for group chats
IG extracts high level summaries and dominant topics from the text corpus.
Various detailed insights are accompanied with supporting references, action items and statistics.
The tool scales to large number of documents, and will handle more documents than can fit in a prompt.

Insights generator is a proof of concept code sample. A list of limitations is included.
The helper functions and intermediate outputs are exposed and the notebooks can be extended beyond the current use cases easily.

## Requirements
Python 3.5.2+

## Usage
Install the insights\_generator package by following the following commands.
From within the root directory:

```
pip install -r requirements.txt
pip install .
```

Then run:
1. Insights Generator Notebook.ipynb (product reviews use case)
2. InsightsGeneratorMinecraftSynthetic.ipynb (group chat use case)

## Data Format

For InsightsGeneratorMinecraft.ipynb, please use the file sample_reviews/minecraft_massage.py
to create data for use by the notebook.

## Limitations

The chief errors are due to hallucinations by GPT.
This can be controlled by a human-in-the-loop approach,
eg checking the topic summaries against the references in InsightsGeneratorMinecraft.ipynb

The second mode of errors is due to omissions of topics / content in the insights.
This can be controlled by examining the intermediate outputs eg the batchwise summaries in InsightsGeneratorMinecraft.ipynb

In the Insights Generator Notebook.ipynb, only aspects that are signficantly positive or significantly negative
are summarized. Aspects that are mixed are not summarized.
