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

# [**langchain\_google\_community.search**](https://api.python.langchain.com/en/latest/google\_community\_api\_reference.html\#module-langchain\_google\_community.search).GoogleSearchResults

**Note** GoogleSearchResults implements the standard [**Runnable Interface**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable). 🏃  
The [**Runnable Interface**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable) has additional methods that are available on runnables, such as [**with\_types**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.with\_types), [**with\_retry**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.with\_retry), [**assign**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.assign), [**bind**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.bind), [**get\_graph**](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable.get\_graph), and more.  
*class* langchain\_google\_community.search.**GoogleSearchResults[\[source\]](https://api.python.langchain.com/en/latest/\_modules/langchain\_google\_community/search.html\#GoogleSearchResults)  
Bases: [**BaseTool**](https://api.python.langchain.com/en/latest/tools/langchain\_core.tools.BaseTool.html\#langchain\_core.tools.BaseTool)

Tool that queries the Google Search API and gets back json.

Initialize the tool.

*param* **api\_wrapper*: [GoogleSearchAPIWrapper](https://api.python.langchain.com/en/latest/search/langchain\_google\_community.search.GoogleSearchAPIWrapper.html\#langchain\_google\_community.search.GoogleSearchAPIWrapper) \[Required\]*  
*param* **args\_schema*: Optional\[TypeBaseModel\] \= None*  
Pydantic model class to validate and parse the tool’s input arguments.

Args schema should be either:

* A subclass of pydantic.BaseModel.

or \- A subclass of pydantic.v1.BaseModel if accessing v1 namespace in pydantic 2

*param* **callback\_manager*: Optional\[[BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\] \= None*  
Deprecated. Please use callbacks instead.

*param* **callbacks*: Callbacks \= None*  
Callbacks to be called during tool execution.

*param* **description*: str \= 'A wrapper around Google Search. Useful for when you need to answer questions about current events. Input should be a search query. Output is a JSON array of the query results'*  
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
\[*Deprecated*\] Make tool callable.

**Notes**

*Deprecated since version langchain-core==0.1.47:* Use invoke instead.  
**Parameters**

* **tool\_input** (*str*) –  
* **callbacks** (*Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\]*) –

**Return type**  
str

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

*async* **ainvoke**(*input: Union\[str, Dict, [ToolCall](https://api.python.langchain.com/en/latest/messages/langchain\_core.messages.tool.ToolCall.html\#langchain\_core.messages.tool.ToolCall)\]*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *\*\*kwargs: Any*) → Any  
Default implementation of ainvoke, calls invoke from a thread.

The default implementation allows usage of async code even if the Runnable did not implement a native async version of invoke.

Subclasses should override this method if they can run asynchronously.

**Parameters**

* **input** (*Union\[str, Dict, [ToolCall](https://api.python.langchain.com/en/latest/messages/langchain\_core.messages.tool.ToolCall.html\#langchain\_core.messages.tool.ToolCall)\]*) –  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) –  
* **kwargs** (*Any*) –

**Return type**  
*Any*

*async* **arun**(*tool\_input: Union\[str, Dict\]*, *verbose: Optional\[bool\] \= None*, *start\_color: Optional\[str\] \= 'green'*, *color: Optional\[str\] \= 'green'*, *callbacks: Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\] \= None*, *\**, *tags: Optional\[List\[str\]\] \= None*, *metadata: Optional\[Dict\[str, Any\]\] \= None*, *run\_name: Optional\[str\] \= None*, *run\_id: Optional\[UUID\] \= None*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *tool\_call\_id: Optional\[str\] \= None*, *\*\*kwargs: Any*) → Any  
Run the tool asynchronously.

**Parameters**

* **tool\_input** (*Union\[str, Dict\]*) – The input to the tool.  
* **verbose** (*Optional\[bool\]*) – Whether to log the tool’s progress. Defaults to None.  
* **start\_color** (*Optional\[str\]*) – The color to use when starting the tool. Defaults to ‘green’.  
* **color** (*Optional\[str\]*) – The color to use when ending the tool. Defaults to ‘green’.  
* **callbacks** (*Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\]*) – Callbacks to be called during tool execution. Defaults to None.  
* **tags** (*Optional\[List\[str\]\]*) – Optional list of tags associated with the tool. Defaults to None.  
* **metadata** (*Optional\[Dict\[str, Any\]\]*) – Optional metadata associated with the tool. Defaults to None.  
* **run\_name** (*Optional\[str\]*) – The name of the run. Defaults to None.  
* **run\_id** (*Optional\[UUID\]*) – The id of the run. Defaults to None.  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) – The configuration for the tool. Defaults to None.  
* **tool\_call\_id** (*Optional\[str\]*) – The id of the tool call. Defaults to None.  
* **kwargs** (*Any*) – Additional arguments to pass to the tool

**Returns**  
The output of the tool.

**Raises**  
[**ToolException**](https://api.python.langchain.com/en/latest/tools/langchain\_core.tools.ToolException.html\#langchain\_core.tools.ToolException) – If an error occurs during tool execution.

**Return type**  
*Any*

**as\_tool**(*args\_schema: Optional\[Type\[[BaseModel](https://api.python.langchain.com/en/latest/video\_captioning/langchain\_experimental.video\_captioning.models.BaseModel.html\#langchain\_experimental.video\_captioning.models.BaseModel)\]\] \= None*, *\**, *name: Optional\[str\] \= None*, *description: Optional\[str\] \= None*, *arg\_types: Optional\[Dict\[str, Type\]\] \= None*) → [BaseTool](https://api.python.langchain.com/en/latest/tools/langchain\_core.tools.BaseTool.html\#langchain\_core.tools.BaseTool)  
\[*Beta*\] Create a BaseTool from a Runnable.

as\_tool will instantiate a BaseTool with a name, description, and args\_schema from a Runnable. Where possible, schemas are inferred from runnable.get\_input\_schema. Alternatively (e.g., if the Runnable takes a dict as input and the specific dict keys are not typed), the schema can be specified directly with args\_schema. You can also pass arg\_types to just specify the required arguments and their types.

**Parameters**

* **args\_schema** (*Optional\[Type\[[BaseModel](https://api.python.langchain.com/en/latest/video\_captioning/langchain\_experimental.video\_captioning.models.BaseModel.html\#langchain\_experimental.video\_captioning.models.BaseModel)\]\]*) – The schema for the tool. Defaults to None.  
* **name** (*Optional\[str\]*) – The name of the tool. Defaults to None.  
* **description** (*Optional\[str\]*) – The description of the tool. Defaults to None.  
* **arg\_types** (*Optional\[Dict\[str, Type\]\]*) – A dictionary of argument names to types. Defaults to None.

**Returns**  
A BaseTool instance.

**Return type**  
[BaseTool](https://api.python.langchain.com/en/latest/tools/langchain\_core.tools.BaseTool.html\#langchain\_core.tools.BaseTool)

Typed dict input:

**from** **typing** **import** List  
**from** **typing\_extensions** **import** TypedDict  
**from** **langchain\_core.runnables** **import** RunnableLambda

**class** **Args**(TypedDict):  
    a: int  
    b: List\[int\]

**def** f(x: Args) \-\> str:  
    **return** str(x\["a"\] \* max(x\["b"\]))

runnable \= RunnableLambda(f)  
as\_tool \= runnable.as\_tool()  
as\_tool.invoke({"a": 3, "b": \[1, 2\]})

dict input, specifying schema via args\_schema:

**from** **typing** **import** Any, Dict, List  
**from** **langchain\_core.pydantic\_v1** **import** BaseModel, Field  
**from** **langchain\_core.runnables** **import** RunnableLambda

**def** f(x: Dict\[str, Any\]) \-\> str:  
    **return** str(x\["a"\] \* max(x\["b"\]))

**class** **FSchema**(BaseModel):  
    *"""Apply a function to an integer and list of integers."""*

    a: int \= Field(..., description\="Integer")  
    b: List\[int\] \= Field(..., description\="List of ints")

runnable \= RunnableLambda(f)  
as\_tool \= runnable.as\_tool(FSchema)  
as\_tool.invoke({"a": 3, "b": \[1, 2\]})

dict input, specifying schema via arg\_types:

**from** **typing** **import** Any, Dict, List  
**from** **langchain\_core.runnables** **import** RunnableLambda

**def** f(x: Dict\[str, Any\]) \-\> str:  
    **return** str(x\["a"\] \* max(x\["b"\]))

runnable \= RunnableLambda(f)  
as\_tool \= runnable.as\_tool(arg\_types\={"a": int, "b": List\[int\]})  
as\_tool.invoke({"a": 3, "b": \[1, 2\]})

String input:

**from** **langchain\_core.runnables** **import** RunnableLambda

**def** f(x: str) \-\> str:  
    **return** x \+ "a"

**def** g(x: str) \-\> str:  
    **return** x \+ "z"

runnable \= RunnableLambda(f) | g  
as\_tool \= runnable.as\_tool()  
as\_tool.invoke("b")

*New in version 0.2.14.*

**Notes**

*async* **astream**(*input: Input*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *\*\*kwargs: Optional\[Any\]*) → AsyncIterator\[Output\]  
Default implementation of astream, which calls ainvoke. Subclasses should override this method if they support streaming output.

**Parameters**

* **input** (*Input*) – The input to the Runnable.  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) – The config to use for the Runnable. Defaults to None.  
* **\*\*kwargs** (*Optional\[Any\]*) – Additional keyword arguments to pass to the Runnable.

**Yields**  
The output of the Runnable.

**Return type**  
*AsyncIterator*\[*Output*\]

**astream\_events**(*input: Any*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *\**, *version: Literal\['v1', 'v2'\]*, *include\_names: Optional\[Sequence\[str\]\] \= None*, *include\_types: Optional\[Sequence\[str\]\] \= None*, *include\_tags: Optional\[Sequence\[str\]\] \= None*, *exclude\_names: Optional\[Sequence\[str\]\] \= None*, *exclude\_types: Optional\[Sequence\[str\]\] \= None*, *exclude\_tags: Optional\[Sequence\[str\]\] \= None*, *\*\*kwargs: Any*) → AsyncIterator\[Union\[[StandardStreamEvent](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.schema.StandardStreamEvent.html\#langchain\_core.runnables.schema.StandardStreamEvent), [CustomStreamEvent](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.schema.CustomStreamEvent.html\#langchain\_core.runnables.schema.CustomStreamEvent)\]\]  
\[*Beta*\] Generate a stream of events.

Use to create an iterator over StreamEvents that provide real-time information about the progress of the Runnable, including StreamEvents from intermediate results.

A StreamEvent is a dictionary with the following schema:

* **event: str \- Event names are of the**  
  format: on\_\[runnable\_type\]\_(start|stream|end).  
* name: **str** \- The name of the Runnable that generated the event.  
* **run\_id: str \- randomly generated ID associated with the given execution of**  
  the Runnable that emitted the event. A child Runnable that gets invoked as part of the execution of a parent Runnable is assigned its own unique ID.  
* **parent\_ids: List\[str\] \- The IDs of the parent runnables that**  
  generated the event. The root Runnable will have an empty list. The order of the parent IDs is from the root to the immediate parent. Only available for v2 version of the API. The v1 version of the API will return an empty list.  
* **tags: Optional\[List\[str\]\] \- The tags of the Runnable that generated**  
  the event.  
* **metadata: Optional\[Dict\[str, Any\]\] \- The metadata of the Runnable**  
  that generated the event.  
* data: **Dict\[str, Any\]**

Below is a table that illustrates some evens that might be emitted by various chains. Metadata fields have been omitted from the table for brevity. Chain definitions have been included after the table.

**ATTENTION** This reference table is for the V2 version of the schema.

| event | name | chunk | input | output |
| ----- | ----- | ----- | ----- | ----- |
| on\_chat\_model\_start | \[model name\] |  | {“messages”: \[\[SystemMessage, HumanMessage\]\]} |  |
| on\_chat\_model\_stream | \[model name\] | AIMessageChunk(content=”hello”) |  |  |
| on\_chat\_model\_end | \[model name\] |  | {“messages”: \[\[SystemMessage, HumanMessage\]\]} | AIMessageChunk(content=”hello world”) |
| on\_llm\_start | \[model name\] |  | {‘input’: ‘hello’} |  |
| on\_llm\_stream | \[model name\] | ‘Hello’ |  |  |
| on\_llm\_end | \[model name\] |  | ‘Hello human\!’ |  |
| on\_chain\_start | format\_docs |  |  |  |
| on\_chain\_stream | format\_docs | “hello world\!, goodbye world\!” |  |  |
| on\_chain\_end | format\_docs |  | \[Document(…)\] | “hello world\!, goodbye world\!” |
| on\_tool\_start | some\_tool |  | {“x”: 1, “y”: “2”} |  |
| on\_tool\_end | some\_tool |  |  | {“x”: 1, “y”: “2”} |
| on\_retriever\_start | \[retriever name\] |  | {“query”: “hello”} |  |
| on\_retriever\_end | \[retriever name\] |  | {“query”: “hello”} | \[Document(…), ..\] |
| on\_prompt\_start | \[template\_name\] |  | {“question”: “hello”} |  |
| on\_prompt\_end | \[template\_name\] |  | {“question”: “hello”} | ChatPromptValue(messages: \[SystemMessage, …\]) |

In addition to the standard events, users can also dispatch custom events (see example below).

Custom events will be only be surfaced with in the v2 version of the API\!

A custom event has following format:

| Attribute | Type | Description |
| ----- | ----- | ----- |
| name | str | A user defined name for the event. |
| data | Any | The data associated with the event. This can be anything, though we suggest making it JSON serializable. |

Here are declarations associated with the standard events shown above:

format\_docs:

**def** format\_docs(docs: List\[Document\]) \-\> str:  
    *'''Format the docs.'''*  
    **return** ", ".join(\[doc.page\_content **for** doc **in** docs\])

format\_docs \= RunnableLambda(format\_docs)

some\_tool:

**@tool**  
**def** some\_tool(x: int, y: str) \-\> dict:  
    *'''Some\_tool.'''*  
    **return** {"x": x, "y": y}

prompt:

template \= ChatPromptTemplate.from\_messages(  
    \[("system", "You are Cat Agent 007"), ("human", "***{question}***")\]  
).with\_config({"run\_name": "my\_template", "tags": \["my\_template"\]})

Example:

**from** **langchain\_core.runnables** **import** RunnableLambda

**async** **def** reverse(s: str) \-\> str:  
    **return** s\[::\-1\]

chain \= RunnableLambda(func\=reverse)

events \= \[  
    event **async** **for** event **in** chain.astream\_events("hello", version\="v2")  
\]

*\# will produce the following events (run\_id, and parent\_ids*  
*\# has been omitted for brevity):*  
\[  
    {  
        "data": {"input": "hello"},  
        "event": "on\_chain\_start",  
        "metadata": {},  
        "name": "reverse",  
        "tags": \[\],  
    },  
    {  
        "data": {"chunk": "olleh"},  
        "event": "on\_chain\_stream",  
        "metadata": {},  
        "name": "reverse",  
        "tags": \[\],  
    },  
    {  
        "data": {"output": "olleh"},  
        "event": "on\_chain\_end",  
        "metadata": {},  
        "name": "reverse",  
        "tags": \[\],  
    },  
\]

Example: Dispatch Custom Event

**from** **langchain\_core.callbacks.manager** **import** (  
    adispatch\_custom\_event,  
)  
**from** **langchain\_core.runnables** **import** RunnableLambda, RunnableConfig  
**import** **asyncio**

**async** **def** slow\_thing(some\_input: str, config: RunnableConfig) \-\> str:  
    *"""Do something that takes a long time."""*  
    **await** asyncio.sleep(1) *\# Placeholder for some slow operation*  
    **await** adispatch\_custom\_event(  
        "progress\_event",  
        {"message": "Finished step 1 of 3"},  
        config\=config *\# Must be included for python \< 3.10*  
    )  
    **await** asyncio.sleep(1) *\# Placeholder for some slow operation*  
    **await** adispatch\_custom\_event(  
        "progress\_event",  
        {"message": "Finished step 2 of 3"},  
        config\=config *\# Must be included for python \< 3.10*  
    )  
    **await** asyncio.sleep(1) *\# Placeholder for some slow operation*  
    **return** "Done"

slow\_thing \= RunnableLambda(slow\_thing)

**async** **for** event **in** slow\_thing.astream\_events("some\_input", version\="v2"):  
    print(event)

**Parameters**

* **input** (*Any*) – The input to the Runnable.  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) – The config to use for the Runnable.  
* **version** (*Literal\['v1', 'v2'\]*) – The version of the schema to use either v2 or v1. Users should use v2. v1 is for backwards compatibility and will be deprecated in 0.4.0. No default will be assigned until the API is stabilized. custom events will only be surfaced in v2.  
* **include\_names** (*Optional\[Sequence\[str\]\]*) – Only include events from runnables with matching names.  
* **include\_types** (*Optional\[Sequence\[str\]\]*) – Only include events from runnables with matching types.  
* **include\_tags** (*Optional\[Sequence\[str\]\]*) – Only include events from runnables with matching tags.  
* **exclude\_names** (*Optional\[Sequence\[str\]\]*) – Exclude events from runnables with matching names.  
* **exclude\_types** (*Optional\[Sequence\[str\]\]*) – Exclude events from runnables with matching types.  
* **exclude\_tags** (*Optional\[Sequence\[str\]\]*) – Exclude events from runnables with matching tags.  
* **kwargs** (*Any*) – Additional keyword arguments to pass to the Runnable. These will be passed to astream\_log as this implementation of astream\_events is built on top of astream\_log.

**Yields**  
An async stream of StreamEvents.

**Raises**  
**NotImplementedError** – If the version is not v1 or v2.

**Return type**  
*AsyncIterator*\[*Union*\[[*StandardStreamEvent*](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.schema.StandardStreamEvent.html\#langchain\_core.runnables.schema.StandardStreamEvent), [*CustomStreamEvent*](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.schema.CustomStreamEvent.html\#langchain\_core.runnables.schema.CustomStreamEvent)\]\]

**Notes**

**batch**(*inputs: List\[Input\]*, *config: Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), List\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\] \= None*, *\**, *return\_exceptions: bool \= False*, *\*\*kwargs: Optional\[Any\]*) → List\[Output\]  
Default implementation runs invoke in parallel using a thread pool executor.

The default implementation of batch works well for IO bound runnables.

Subclasses should override this method if they can batch more efficiently; e.g., if the underlying Runnable uses an API which supports a batch mode.

**Parameters**

* **inputs** (*List\[Input\]*) –  
* **config** (*Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), List\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\]*) –  
* **return\_exceptions** (*bool*) –  
* **kwargs** (*Optional\[Any\]*) –

**Return type**  
*List*\[*Output*\]

**batch\_as\_completed**(*inputs: Sequence\[Input\]*, *config: Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), Sequence\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\] \= None*, *\**, *return\_exceptions: bool \= False*, *\*\*kwargs: Optional\[Any\]*) → Iterator\[Tuple\[int, Union\[Output, Exception\]\]\]  
Run invoke in parallel on a list of inputs, yielding results as they complete.

**Parameters**

* **inputs** (*Sequence\[Input\]*) –  
* **config** (*Optional\[Union\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig), Sequence\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]\]\]*) –  
* **return\_exceptions** (*bool*) –  
* **kwargs** (*Optional\[Any\]*) –

**Return type**  
*Iterator*\[*Tuple*\[int, *Union*\[*Output*, Exception\]\]\]

**configurable\_alternatives**(*which: [ConfigurableField](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableField.html\#langchain\_core.runnables.utils.ConfigurableField)*, *\**, *default\_key: str \= 'default'*, *prefix\_keys: bool \= False*, *\*\*kwargs: Union\[[Runnable](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable)\[Input, Output\], Callable\[\[\], [Runnable](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable)\[Input, Output\]\]\]*) → [RunnableSerializable](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.RunnableSerializable.html\#langchain\_core.runnables.base.RunnableSerializable)\[Input, Output\]  
Configure alternatives for Runnables that can be set at runtime.

**Parameters**

* **which** ([*ConfigurableField*](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableField.html\#langchain\_core.runnables.utils.ConfigurableField)) – The ConfigurableField instance that will be used to select the alternative.  
* **default\_key** (*str*) – The default key to use if no alternative is selected. Defaults to “default”.  
* **prefix\_keys** (*bool*) – Whether to prefix the keys with the ConfigurableField id. Defaults to False.  
* **\*\*kwargs** (*Union\[[Runnable](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable)\[Input, Output\], Callable\[\[\], [Runnable](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.Runnable.html\#langchain\_core.runnables.base.Runnable)\[Input, Output\]\]\]*) – A dictionary of keys to Runnable instances or callables that return Runnable instances.

**Returns**  
A new Runnable with the alternatives configured.

**Return type**  
[*RunnableSerializable*](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.RunnableSerializable.html\#langchain\_core.runnables.base.RunnableSerializable)\[*Input*, *Output*\]

**from** **langchain\_anthropic** **import** ChatAnthropic  
**from** **langchain\_core.runnables.utils** **import** ConfigurableField  
**from** **langchain\_openai** **import** ChatOpenAI

model \= ChatAnthropic(  
    model\_name\="claude-3-sonnet-20240229"  
).configurable\_alternatives(  
    ConfigurableField(id\="llm"),  
    default\_key\="anthropic",  
    openai\=ChatOpenAI()  
)

*\# uses the default model ChatAnthropic*  
print(model.invoke("which organization created you?").content)

*\# uses ChatOpenAI*  
print(  
    model.with\_config(  
        configurable\={"llm": "openai"}  
    ).invoke("which organization created you?").content  
)

**configurable\_fields**(*\*\*kwargs: Union\[[ConfigurableField](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableField.html\#langchain\_core.runnables.utils.ConfigurableField), [ConfigurableFieldSingleOption](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableFieldSingleOption.html\#langchain\_core.runnables.utils.ConfigurableFieldSingleOption), [ConfigurableFieldMultiOption](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableFieldMultiOption.html\#langchain\_core.runnables.utils.ConfigurableFieldMultiOption)\]*) → [RunnableSerializable](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.RunnableSerializable.html\#langchain\_core.runnables.base.RunnableSerializable)\[Input, Output\]  
Configure particular Runnable fields at runtime.

**Parameters**  
**\*\*kwargs** (*Union\[[ConfigurableField](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableField.html\#langchain\_core.runnables.utils.ConfigurableField), [ConfigurableFieldSingleOption](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableFieldSingleOption.html\#langchain\_core.runnables.utils.ConfigurableFieldSingleOption), [ConfigurableFieldMultiOption](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.utils.ConfigurableFieldMultiOption.html\#langchain\_core.runnables.utils.ConfigurableFieldMultiOption)\]*) – A dictionary of ConfigurableField instances to configure.

**Returns**  
A new Runnable with the fields configured.

**Return type**  
[*RunnableSerializable*](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.base.RunnableSerializable.html\#langchain\_core.runnables.base.RunnableSerializable)\[*Input*, *Output*\]

**from** **langchain\_core.runnables** **import** ConfigurableField  
**from** **langchain\_openai** **import** ChatOpenAI

model \= ChatOpenAI(max\_tokens\=20).configurable\_fields(  
    max\_tokens\=ConfigurableField(  
        id\="output\_token\_number",  
        name\="Max tokens in the output",  
        description\="The maximum number of tokens in the output",  
    )  
)

*\# max\_tokens \= 20*  
print(  
    "max\_tokens\_20: ",  
    model.invoke("tell me something about chess").content  
)

*\# max\_tokens \= 200*  
print("max\_tokens\_200: ", model.with\_config(  
    configurable\={"output\_token\_number": 200}  
    ).invoke("tell me something about chess").content  
)

**invoke**(*input: Union\[str, Dict, [ToolCall](https://api.python.langchain.com/en/latest/messages/langchain\_core.messages.tool.ToolCall.html\#langchain\_core.messages.tool.ToolCall)\]*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *\*\*kwargs: Any*) → Any  
Transform a single input into an output. Override to implement.

**Parameters**

* **input** (*Union\[str, Dict, [ToolCall](https://api.python.langchain.com/en/latest/messages/langchain\_core.messages.tool.ToolCall.html\#langchain\_core.messages.tool.ToolCall)\]*) – The input to the Runnable.  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) – A config to use when invoking the Runnable. The config supports standard keys like ‘tags’, ‘metadata’ for tracing purposes, ‘max\_concurrency’ for controlling how much work to do in parallel, and other keys. Please refer to the RunnableConfig for more details.  
* **kwargs** (*Any*) –

**Returns**  
The output of the Runnable.

**Return type**  
*Any*

**run**(*tool\_input: Union\[str, Dict\[str, Any\]\]*, *verbose: Optional\[bool\] \= None*, *start\_color: Optional\[str\] \= 'green'*, *color: Optional\[str\] \= 'green'*, *callbacks: Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\] \= None*, *\**, *tags: Optional\[List\[str\]\] \= None*, *metadata: Optional\[Dict\[str, Any\]\] \= None*, *run\_name: Optional\[str\] \= None*, *run\_id: Optional\[UUID\] \= None*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *tool\_call\_id: Optional\[str\] \= None*, *\*\*kwargs: Any*) → Any  
Run the tool.

**Parameters**

* **tool\_input** (*Union\[str, Dict\[str, Any\]\]*) – The input to the tool.  
* **verbose** (*Optional\[bool\]*) – Whether to log the tool’s progress. Defaults to None.  
* **start\_color** (*Optional\[str\]*) – The color to use when starting the tool. Defaults to ‘green’.  
* **color** (*Optional\[str\]*) – The color to use when ending the tool. Defaults to ‘green’.  
* **callbacks** (*Optional\[Union\[List\[[BaseCallbackHandler](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackHandler.html\#langchain\_core.callbacks.base.BaseCallbackHandler)\], [BaseCallbackManager](https://api.python.langchain.com/en/latest/callbacks/langchain\_core.callbacks.base.BaseCallbackManager.html\#langchain\_core.callbacks.base.BaseCallbackManager)\]\]*) – Callbacks to be called during tool execution. Defaults to None.  
* **tags** (*Optional\[List\[str\]\]*) – Optional list of tags associated with the tool. Defaults to None.  
* **metadata** (*Optional\[Dict\[str, Any\]\]*) – Optional metadata associated with the tool. Defaults to None.  
* **run\_name** (*Optional\[str\]*) – The name of the run. Defaults to None.  
* **run\_id** (*Optional\[UUID\]*) – The id of the run. Defaults to None.  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) – The configuration for the tool. Defaults to None.  
* **tool\_call\_id** (*Optional\[str\]*) – The id of the tool call. Defaults to None.  
* **kwargs** (*Any*) – Additional arguments to pass to the tool

**Returns**  
The output of the tool.

**Raises**  
[**ToolException**](https://api.python.langchain.com/en/latest/tools/langchain\_core.tools.ToolException.html\#langchain\_core.tools.ToolException) – If an error occurs during tool execution.

**Return type**  
*Any*

**stream**(*input: Input*, *config: Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\] \= None*, *\*\*kwargs: Optional\[Any\]*) → Iterator\[Output\]  
Default implementation of stream, which calls invoke. Subclasses should override this method if they support streaming output.

**Parameters**

* **input** (*Input*) – The input to the Runnable.  
* **config** (*Optional\[[RunnableConfig](https://api.python.langchain.com/en/latest/runnables/langchain\_core.runnables.config.RunnableConfig.html\#langchain\_core.runnables.config.RunnableConfig)\]*) – The config to use for the Runnable. Defaults to None.  
* **\*\*kwargs** (*Optional\[Any\]*) – Additional keyword arguments to pass to the Runnable.

**Yields**  
The output of the Runnable.

**Return type**  
*Iterator*\[*Output*\]

**to\_json**() → Union\[[SerializedConstructor](https://api.python.langchain.com/en/latest/load/langchain\_core.load.serializable.SerializedConstructor.html\#langchain\_core.load.serializable.SerializedConstructor), [SerializedNotImplemented](https://api.python.langchain.com/en/latest/load/langchain\_core.load.serializable.SerializedNotImplemented.html\#langchain\_core.load.serializable.SerializedNotImplemented)\]  
Serialize the Runnable to JSON.

**Returns**  
A JSON-serializable representation of the Runnable.

**Return type**  
*Union*\[[*SerializedConstructor*](https://api.python.langchain.com/en/latest/load/langchain\_core.load.serializable.SerializedConstructor.html\#langchain\_core.load.serializable.SerializedConstructor), [*SerializedNotImplemented*](https://api.python.langchain.com/en/latest/load/langchain\_core.load.serializable.SerializedNotImplemented.html\#langchain\_core.load.serializable.SerializedNotImplemented)\]

*property* **args*: dict*  
*property* **is\_single\_input*: bool*  
Whether the tool only accepts a single input.

*property* **tool\_call\_schema*: Type\[BaseModel\]*  
