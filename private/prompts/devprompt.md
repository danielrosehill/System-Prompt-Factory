Your objective is to generate a Streamless application. In order to create system prompts. The idea for this demo application is to create general purpose system prompts by combining a few different elements. 

In the repository is a folder called library. This is a Github submodule and it's a separate repository I created in order to bring together some ideas I had for different system prompts. 

As I was writing this repository, I had a few different ideas for how general system prompts could be put together. These would depend upon where the user was based, the user's political views, the type of personality the user wished to engage with in the AI tool. 

But I'd like to attempt in this repository is to explore the idea that we could actually create one overarching system prompt by putting these different building blocks together. 

The user would need to be presented with blocks as I describe them. The blocks are the elements as laid out in the repository. The interface in this streamed application would be pretty simple. The user would select a block from each item and then they would add them together and the UI would put out a system prompt. 

You might need to rewrite the library a little bit in order for it to work at this purpose. It would be better to keep the original system prompts from the sub module on touch. So I've created another folder called repo library with the idea that you could write. More programmatic versions of the prompts that could be easily combined in that folder. 

The objective is that the blocks would fit together to create one system prompt that It felt really natural and logical. Perhaps a large language model would actually be required to put these building blocks together, in which case you could put an API key holder in the repository that can be stored in the browser and the user can use a tool like Open AI in order to do that work. But that's just an idea of the ultimate implementation it's up to you