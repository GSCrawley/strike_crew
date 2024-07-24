# langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer

*class* langchain\_experimental.graph\_transformers.diffbot.**DiffbotGraphTransformer**(*diffbot\_api\_key: \~typing.Optional\[str\] \= None, fact\_confidence\_threshold: float \= 0.7, include\_qualifiers: bool \= True, include\_evidence: bool \= True, simplified\_schema: bool \= True, extract\_types: \~typing.List\[\~langchain\_experimental.graph\_transformers.diffbot.TypeOption\] \= \[\<TypeOption.FACTS: 'facts'\>\], \*, include\_confidence: bool \= False*)[\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_experimental/graph\_transformers/diffbot.html\#DiffbotGraphTransformer)  
Transform documents into graph documents using Diffbot NLP API.

A graph document transformation system takes a sequence of Documents and returns a sequence of Graph Documents.

**Example**

Initialize the graph transformer with various options.

**Parameters**

* **diffbot\_api\_key** (*str*) – The API key for Diffbot’s NLP services.  
* **fact\_confidence\_threshold** (*float*) – Minimum confidence level for facts to be included.  
* **include\_qualifiers** (*bool*) – Whether to include qualifiers in the relationships.  
* **include\_evidence** (*bool*) – Whether to include evidence for the relationships.  
* **simplified\_schema** (*bool*) – Whether to use a simplified schema for relationships.  
* **extract\_types** (*List\[[TypeOption](https://api.python.langchain.com/en/latest/graph\_transformers/langchain\_experimental.graph\_transformers.diffbot.TypeOption.html\#langchain\_experimental.graph\_transformers.diffbot.TypeOption)\]*) – A list of data types to extract. Facts, entities, and sentiment are supported. By default, the option is set to facts. A fact represents a combination of source and target nodes with a relationship type.  
* **include\_confidence** (*bool*) – Whether to include confidence scores on nodes and rels

**Methods**

| [\_\_init\_\_](https://api.python.langchain.com/en/latest/graph\_transformers/langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.html\#langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.\_\_init\_\_)(\[diffbot\_api\_key, ...\]) | Initialize the graph transformer with various options. |
| :---- | :---- |
| [**convert\_to\_graph\_documents**](https://api.python.langchain.com/en/latest/graph\_transformers/langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.html\#langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.convert\_to\_graph\_documents)(documents) | Convert a sequence of documents into graph documents. |
| [**nlp\_request**](https://api.python.langchain.com/en/latest/graph\_transformers/langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.html\#langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.nlp\_request)(text) | Make an API request to the Diffbot NLP endpoint. |
| [**process\_response**](https://api.python.langchain.com/en/latest/graph\_transformers/langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.html\#langchain\_experimental.graph\_transformers.diffbot.DiffbotGraphTransformer.process\_response)(payload, document) | Transform the Diffbot NLP response into a GraphDocument. |

**\_\_init\_\_**(*diffbot\_api\_key: \~typing.Optional\[str\] \= None, fact\_confidence\_threshold: float \= 0.7, include\_qualifiers: bool \= True, include\_evidence: bool \= True, simplified\_schema: bool \= True, extract\_types: \~typing.List\[\~langchain\_experimental.graph\_transformers.diffbot.TypeOption\] \= \[\<TypeOption.FACTS: 'facts'\>\], \*, include\_confidence: bool \= False*) → None[\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_experimental/graph\_transformers/diffbot.html\#DiffbotGraphTransformer.\_\_init\_\_)  
Initialize the graph transformer with various options.

**Parameters**

* **diffbot\_api\_key** (*str*) – The API key for Diffbot’s NLP services.  
* **fact\_confidence\_threshold** (*float*) – Minimum confidence level for facts to be included.  
* **include\_qualifiers** (*bool*) – Whether to include qualifiers in the relationships.  
* **include\_evidence** (*bool*) – Whether to include evidence for the relationships.  
* **simplified\_schema** (*bool*) – Whether to use a simplified schema for relationships.  
* **extract\_types** (*List\[[TypeOption](https://api.python.langchain.com/en/latest/graph\_transformers/langchain\_experimental.graph\_transformers.diffbot.TypeOption.html\#langchain\_experimental.graph\_transformers.diffbot.TypeOption)\]*) – A list of data types to extract. Facts, entities, and sentiment are supported. By default, the option is set to facts. A fact represents a combination of source and target nodes with a relationship type.  
* **include\_confidence** (*bool*) – Whether to include confidence scores on nodes and rels

**Return type**  
None

**convert\_to\_graph\_documents**(*documents: Sequence\[[Document](https://api.python.langchain.com/en/latest/documents/langchain\_core.documents.base.Document.html\#langchain\_core.documents.base.Document)\]*) → List\[[GraphDocument](https://api.python.langchain.com/en/latest/graphs/langchain\_community.graphs.graph\_document.GraphDocument.html\#langchain\_community.graphs.graph\_document.GraphDocument)\][\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_experimental/graph\_transformers/diffbot.html\#DiffbotGraphTransformer.convert\_to\_graph\_documents)  
Convert a sequence of documents into graph documents.

**Parameters**

* **documents** (*Sequence\[[Document](https://api.python.langchain.com/en/latest/documents/langchain\_core.documents.base.Document.html\#langchain\_core.documents.base.Document)\]*) – The original documents.  
* **\*\*kwargs** – Additional keyword arguments.

**Returns**  
The transformed documents as graphs.

**Return type**  
Sequence\[[GraphDocument](https://api.python.langchain.com/en/latest/graphs/langchain\_community.graphs.graph\_document.GraphDocument.html\#langchain\_community.graphs.graph\_document.GraphDocument)\]

**nlp\_request**(*text: str*) → Dict\[str, Any\][\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_experimental/graph\_transformers/diffbot.html\#DiffbotGraphTransformer.nlp\_request)  
Make an API request to the Diffbot NLP endpoint.

**Parameters**  
**text** (*str*) – The text to be processed.

**Returns**  
The JSON response from the API.

**Return type**  
Dict\[str, Any\]

**process\_response**(*payload: Dict\[str, Any\]*, *document: [Document](https://api.python.langchain.com/en/latest/documents/langchain\_core.documents.base.Document.html\#langchain\_core.documents.base.Document)*) → [GraphDocument](https://api.python.langchain.com/en/latest/graphs/langchain\_community.graphs.graph\_document.GraphDocument.html\#langchain\_community.graphs.graph\_document.GraphDocument)[\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_experimental/graph\_transformers/diffbot.html\#DiffbotGraphTransformer.process\_response)  
Transform the Diffbot NLP response into a GraphDocument.

**Parameters**

* **payload** (*Dict\[str, Any\]*) – The JSON response from Diffbot’s NLP API.  
* **document** ([*Document*](https://api.python.langchain.com/en/latest/documents/langchain\_core.documents.base.Document.html\#langchain\_core.documents.base.Document)) – The original document.

**Returns**  
The transformed document as a graph.

**Return type**  
[GraphDocument](https://api.python.langchain.com/en/latest/graphs/langchain\_community.graphs.graph\_document.GraphDocument.html\#langchain\_community.graphs.graph\_document.GraphDocument)

# langchain\_community.chains.graph\_qa.cypher.GraphCypherQAChain

**Note** GraphCypherQAChain implements the standard [**Runnable Interface**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable). 🏃  
The [**Runnable Interface**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable) has additional methods that are available on runnables, such as [**with\_types**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.with\_types), [**with\_retry**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.with\_retry), [**assign**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.assign), [**bind**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.bind), [**get\_graph**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.get\_graph), and more.  
*class* langchain\_community.chains.graph\_qa.cypher.**GraphCypherQAChain[\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_community/chains/graph\_qa/cypher.html\#GraphCypherQAChain)  
Bases: [**Chain**](https://api.python.langchain.com/en/latest/chains/langchain.chains.base.Chain.html\#langchain.chains.base.Chain)

Chain for question-answering against a graph by generating Cypher statements.

***Security note*****: Make sure that the database connection uses credentials**  
that are narrowly-scoped to only include necessary permissions. Failure to do so may result in data corruption or loss, since the calling code may attempt commands that would result in deletion, mutation of data if appropriately prompted or reading sensitive data if such data is present in the database. The best way to guard against such negative outcomes is to (as appropriate) limit the permissions granted to the credentials used with this tool.

See [https://python.langchain.com/docs/security](https://python.langchain.com/docs/security) for more information.

Create a new model by parsing and validating input data from keyword arguments.

Raises ValidationError if the input data cannot be parsed to form a valid model.

*param* **callback\_manager*: Optional\[[BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\] \= None*  
\[DEPRECATED\] Use callbacks instead.

*param* **callbacks*: Callbacks \= None*  
Optional list of callback handlers (or callback manager). Defaults to None. Callback handlers are called throughout the lifecycle of a call to a chain, starting with on\_chain\_start, ending with on\_chain\_end or on\_chain\_error. Each custom chain can optionally call additional callback methods, see Callback docs for full details.

*param* **cypher\_generation\_chain*: [LLMChain](https://api.python.langchain.com/en/latest/chains/langchain.chains.llm.LLMChain.html\#langchain.chains.llm.LLMChain) \[Required\]*  
*param* **cypher\_query\_corrector*: Optional\[[CypherQueryCorrector](https://api.python.langchain.com/en/latest/chains/langchain\_community.chains.graph\_qa.cypher\_utils.CypherQueryCorrector.html\#langchain\_community.chains.graph\_qa.cypher\_utils.CypherQueryCorrector)\] \= None*  
Optional cypher validation tool

*param* **graph*: [GraphStore](https://api.python.langchain.com/en/latest/graphs/langchain\_community.graphs.graph\_store.GraphStore.html\#langchain\_community.graphs.graph\_store.GraphStore) \[Required\]*  
*param* **graph\_schema*: str \[Required\]*  
*param* **memory*: Optional\[[BaseMemory](https://api.python.langchain.com/en/latest/memory/langchain\_core.memory.BaseMemory.html\#langchain\_core.memory.BaseMemory)\] \= None*  
Optional memory object. Defaults to None. Memory is a class that gets called at the start and at the end of every chain. At the start, memory loads variables and passes them along in the chain. At the end, it saves any returned variables. There are many different types of memory \- please see memory docs for the full catalog.

*param* **metadata*: Optional\[Dict\[str, Any\]\] \= None*  
Optional metadata associated with the chain. Defaults to None. This metadata will be associated with each call to this chain, and passed as arguments to the handlers defined in callbacks. You can use these to eg identify a specific instance of a chain with its use case.

*param* **qa\_chain*: Union\[[LLMChain](https://api.python.langchain.com/en/latest/chains/langchain.chains.llm.LLMChain.html\#langchain.chains.llm.LLMChain), [Runnable](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable)\] \[Required\]*  
*param* **return\_direct*: bool \= False*  
Whether or not to return the result of querying the graph directly.

*param* **return\_intermediate\_steps*: bool \= False*  
Whether or not to return the intermediate steps along with the final answer.

*param* **tags*: Optional\[List\[str\]\] \= None*  
Optional list of tags associated with the chain. Defaults to None. These tags will be associated with each call to this chain, and passed as arguments to the handlers defined in callbacks. You can use these to eg identify a specific instance of a chain with its use case.

*param* **top\_k*: int \= 10*  
Number of results to return from the query

*param* **use\_function\_response*: bool \= False*  
Whether to wrap the database context as tool/function response

*param* **verbose*: bool \[Optional\]*  
Whether or not run in verbose mode. In verbose mode, some intermediate logs will be printed to the console. Defaults to the global verbose value, accessible via langchain.globals.get\_verbose().

**\_\_call\_\_**(*inputs: Union\[Dict\[str, Any\], Any\]*, *return\_only\_outputs: bool \= False*, *callbacks: Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\] \= None*, *\**, *tags: Optional\[List\[str\]\] \= None*, *metadata: Optional\[Dict\[str, Any\]\] \= None*, *run\_name: Optional\[str*  
*async* **abatch**(*inputs: List\[Input\]*, *config: Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), List\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\] \= None*, *\**, *return\_exceptions: bool \= False*, *\*\*kwargs: Optional\[Any\]*) → List\[Output\]  
Default implementation runs ainvoke in parallel using asyncio.gather.

The default implementation of batch works well for IO bound runnables.

Subclasses should override this method if they can batch more efficiently; e.g., if the underlying Runnable uses an API which supports a batch mode.

**Parameters**

* **inputs** (*List\[Input\]*) – A list of inputs to the Runnable.  
* **config** (*Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), List\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\]*) – A config to use when invoking the Runnable. The config supports standard keys like ‘tags’, ‘metadata’ for tracing purposes, ‘max\_concurrency’ for controlling how much work to do in parallel, and other keys. Please refer to the RunnableConfig for more details. Defaults to None.  
* **return\_exceptions** (*bool*) – Whether to return exceptions instead of raising them. Defaults to False.  
* **\*\*kwargs** (*Optional\[Any\]*) – Additional keyword arguments to pass to the Runnable.

**Returns**  
A list of outputs from the Runnable.

**Return type**  
*List*\[*Output*\]

*async* **abatch\_as\_completed**(*inputs: Sequence\[Input\]*, *config: Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), Sequence\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\] \= None*, *\**, *return\_exceptions: bool \= False*, *\*\*kwargs: Optional\[Any\]*) → AsyncIterator\[Tuple\[int, Union\[Output, Exception\]\]\]  
Run ainvoke in parallel on a list of inputs, yielding results as they complete.

**Parameters**

* **inputs** (*Sequence\[Input\]*) – A list of inputs to the Runnable.  
* **config** (*Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), Sequence\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\]*) – A config to use when invoking the Runnable. The config supports standard keys like ‘tags’, ‘metadata’ for tracing purposes, ‘max\_concurrency’ for controlling how much work to do in parallel, and other keys. Please refer to the RunnableConfig for more details. Defaults to None. Defaults to None.  
* **return\_exceptions** (*bool*) – Whether to return exceptions instead of raising them. Defaults to False.  
* **\*\*kwargs** (*Optional\[Any\]*) – Additional keyword arguments to pass to the Runnable.

**Yields**  
A tuple of the index of the input and the output from the Runnable.

**Return type**  
*AsyncIterator*\[*Tuple*\[int, *Union*\[*Output*, Exception\]\]\]

*async* **ainvoke**(*input: Dict\[str, Any\]*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *\*\*kwargs: Any*) → Dict\[str, Any\]  
Default implementation of ainvoke, calls invoke from a thread.

The default implementation allows usage of async code even if the Runnable did not implement a native async version of invoke.

Subclasses should override this method if they can run asynchronously.

**Parameters**

* **input** (*Dict\[str, Any\]*) –  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) –  
* **kwargs** (*Any*) –

**Return type**  
*Dict*\[str, *Any*\]

*async* **aprep\_inputs**(*inputs: Union\[Dict\[str, Any\], Any\]*) → Dict\[str, str\]  
Prepare chain inputs, including adding inputs from memory.

**Parameters**  
**inputs** (*Union\[Dict\[str, Any\], Any\]*) – Dictionary of raw inputs, or single input if chain expects only one param. Should contain all inputs specified in Chain.input\_keys except for inputs that will be set by the chain’s memory.

**Returns**  
A dictionary of all inputs, including those added by the chain’s memory.

**Return type**  
*Dict*\[str, str\]

*async* **aprep\_outputs**(*inputs: Dict\[str, str\]*, *outputs: Dict\[str, str\]*, *return\_only\_outputs: bool \= False*) → Dict\[str, str\]  
Validate and prepare chain outputs, and save info about this run to memory.

**Parameters**

* **inputs** (*Dict\[str, str\]*) – Dictionary of chain inputs, including any inputs added by chain memory.  
* **outputs** (*Dict\[str, str\]*) – Dictionary of initial chain outputs.  
* **return\_only\_outputs** (*bool*) – Whether to only return the chain outputs. If False, inputs are also added to the final outputs.

**Returns**  
A dict of the final chain outputs.

**Return type**  
*Dict*\[str, str\]

*async* **arun**(*\*args: Any*, *callbacks: Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\] \= None*, *tags: Optional\[List\[str\]\] \= None*, *metadata: Optional\[Dict\[str, Any\]\] \= None*, *\*\*kwargs: Any*) → Any  
\[*Deprecated*\] Convenience method for executing chain.

The main difference between this method and Chain.\_\_call\_\_ is that this method expects inputs to be passed directly in as positional arguments or keyword arguments, whereas Chain.\_\_call\_\_ expects a single input dictionary with all the inputs

**Parameters**

* **\*args** (*Any*) – If the chain expects a single input, it can be passed in as the sole positional argument.  
* **callbacks** (*Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\]*) – Callbacks to use for this chain run. These will be called in addition to callbacks passed to the chain during construction, but only these runtime callbacks will propagate to calls to other objects.  
* **tags** (*Optional\[List\[str\]\]*) – List of string tags to pass to all callbacks. These will be passed in addition to tags passed to the chain during construction, but only these runtime tags will propagate to calls to other objects.  
* **\*\*kwargs** (*Any*) – If the chain expects multiple inputs, they can be passed in directly as keyword arguments.  
* **metadata** (*Optional\[Dict\[str, Any\]\]*) –  
* **\*\*kwargs** –

**Returns**  
The chain output.

**Return type**  
*Any*

**Example**

*\# Suppose we have a single-input chain that takes a 'question' string:*  
**await** chain.arun("What's the temperature in Boise, Idaho?")  
*\# \-\> "The temperature in Boise is..."*

*\# Suppose we have a multi-input chain that takes a 'question' string*  
*\# and 'context' string:*  
question \= "What's the temperature in Boise, Idaho?"  
context \= "Weather report for Boise, Idaho on 07/03/23..."  
**await** chain.arun(question\=question, context\=context)  
*\# \-\> "The temperature in Boise is..."*

# langchain\_community.tools.bing\_search.tool.BingSearchResults[¶](https://api.python.langchain.com/en/latest/tools/langchain\_community.tools.bing\_search.tool.BingSearchResults.html\#langchain-community-tools-bing-search-tool-bingsearchresults)

**Note** BingSearchResults implements the standard [**Runnable Interface**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable). 🏃  
The [**Runnable Interface**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable) has additional methods that are available on runnables, such as [**with\_types**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.with\_types), [**with\_retry**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.with\_retry), [**assign**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.assign), [**bind**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.bind), [**get\_graph**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.get\_graph), and more.  
*class* langchain\_community.tools.bing\_search.tool.**BingSearchResults[\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_community/tools/bing\_search/tool.html\#BingSearchResults)  
Bases: [**BaseTool**](https://api.python.langchain.com/en/latest/tools/langchain\_core.tools.BaseTool.html\#langchain\_core.tools.BaseTool)

Tool that queries the Bing Search API and gets back json.

Initialize the tool.

*param* **api\_wrapper*: [BingSearchAPIWrapper](https://api.python.langchain.com/en/latest/utilities/langchain\_community.utilities.bing\_search.BingSearchAPIWrapper.html\#langchain\_community.utilities.bing\_search.BingSearchAPIWrapper) \[Required\]*  
*param* **args\_schema*: Optional\[TypeBaseModel\] \= None*  
Pydantic model class to validate and parse the tool’s input arguments.

Args schema should be either:

* A subclass of pydantic.BaseModel.

or \- A subclass of pydantic.v1.BaseModel if accessing v1 namespace in pydantic 2

*param* **callback\_manager*: Optional\[[BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\] \= None*  
Deprecated. Please use callbacks instead.

*param* **callbacks*: Callbacks \= None*  
Callbacks to be called during tool execution.

*param* **description*: str \= 'A wrapper around Bing Search. Useful for when you need to answer questions about current events. Input should be a search query. Output is a JSON array of the query results'*  
Used to tell the model how/when/why to use the tool.

You can provide few-shot examples as a part of the description.

*param* **handle\_tool\_error*: Optional\[Union\[bool, str, Callable\[\[[ToolException](https://api.python.langchain.com/en/latest/tools/langchain\_core.tools.ToolException.html\#langchain\_core.tools.ToolException)\], str\]\]\] \= False*  
Handle the content of the ToolException thrown.

*param* **handle\_validation\_error*: Optional\[Union\[bool, str, Callable\[\[ValidationError\], str\]\]\] \= False*  
Handle the content of the ValidationError thrown.

*param* **metadata*: Optional\[Dict\[str, Any\]\] \= None*  
Optional metadata associated with the tool. Defaults to None. This metadata will be associated with each call to this tool, and passed as arguments to the handlers defined in callbacks. You can use these to eg identify a specific instance of a tool with its use case.

*param* **num\_results*: int \= 4*  
*param* **response\_format*: Literal\['content', 'content\_and\_artifact'\] \= 'content'*  
The tool response format. Defaults to ‘content’.

If “content” then the output of the tool is interpreted as the contents of a ToolMessage. If “content\_and\_artifact” then the output is expected to be a two-tuple corresponding to the (content, artifact) of a ToolMessage.

*param* **return\_direct*: bool \= False*  
Whether to return the tool’s output directly.

Setting this to True means that after the tool is called, the AgentExecutor will stop looping.

*param* **tags*: Optional\[List\[str\]\] \= None*  
Optional list of tags associated with the tool. Defaults to None. These tags will be associated with each call to this tool, and passed as arguments to the handlers defined in callbacks. You can use these to eg identify a specific instance of a tool with its use case.

*param* **verbose*: bool \= False*  
Whether to log the tool’s progress.

**\_\_call\_\_**(*tool\_input: str*, *callbacks: Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\] \= None*) → str  
