What was the end of year prediction made in the SCRIPT below?

SCRIPT
Gemma Phi 3, OpenELM, and Llama 3. Open source language models are becoming more viable with every single release. The terminology from Apple's new OpenELM model is spot on. These efficient language models are taking center stage in the LLM ecosystem. Why are ELMs so important? Because they reshape the business model of your agentic tools and products. When you can run a prompt directly on your device, the cost of building goes to zero. The pace of innovation has been incredible, especially with the release of Llama 3. But every time a new model drops, I'm always asking the same question. Are efficient language models truly ready for on-device use? And how do you know your ELM meets your standards? I'm going to give you a couple of examples here. The first one is that you need to know your ELM. Everyone has different standards for their prompts, prompt chains, AI agents, and agentic workflows. How do you know your personal standards are being met by Phi 3, by Llama 3, and whatever's coming next? This is something that we stress on the channel a lot. Always look at where the ball is going, not where it is. If this trend of incredible local models continue, how soon will it be until we can do what GPT-4 does right on our device? With Llama 3, it's looking like this. It's looking like this. It's looking like this. It's looking like this. It's looking like this. It's looking like this. It's looking like this. It's looking like this. It's looking like this. That time is coming very soon. In this video, we're going to answer the question, are efficient language models ready for on-device use? How do you know if they're ready for your specific use cases? Here are all the big ideas. We're going to set some standards for what ELM attributes we actually care about. There are things like RAM consumption, tokens per second, accuracy. We're going to look at some specific attributes of ELMs and talk about where they need to be for them to work on-device for us. We're going to break down the IT V-Benchmark. We'll explain exactly what that is. That's going to help us answer the question, is this model good enough for your specific use cases? And then we're going to actually run the IT V-Benchmark on Gemma 5.3 and Llama 3 for real on-device use. So we're going to look at a concrete example of the IT V-Benchmark running on my M2 MacBook Pro with 64 gigabytes of RAM and really try to answer the question in a concrete way. Is this ready for prime time? Are these ELMs, are these efficient language models ready for prime time? Let's first walk through some standards and then I'll share some of my personal standards for ELMs. So we'll look at it through the lens of how I'm approaching this as I'm building out agentic tools and products. How do we know we're ready for on-device use? First two most important metrics we need to look at, accuracy and speed. Given your test suite that validates that this model works for your use case, what accuracy do you need? Is it okay if it fails a couple of tests giving you 90% or are you okay with, you know, 60, 70 or 80%? I think accuracy is the most important benchmark we should all be paying attention to. Something like speed is also a complete blocker if it's too low. So we'll be measuring speed and TPS, tokens per second. We'll look at a range from one token per second, all the way up to grok levels, right? Of something like 500 plus, you know, 1000 tokens per second level. What else do we need to pay attention to? Memory and context window. So memory coupled with speed are the big two constraints for ELMs right now. Efficient language model, models that can run on your device. They chew up anywhere from four gigabytes of RAM, of GPU, of CPU, all the way up to 128 and beyond. To run Lama 3, 70 billion parameter on my MacBook, it will chew up something like half of all my available RAM. We also have context window. This is a classic one. Then we have JSON response and vision support. We're not gonna focus on these too much. These are more yes, no, do they have it or do they not? Is it multimodal or not? There are a couple other things that we need to pay attention to. First of all, we need to pay attention to these other attributes that we're missing here, but I don't think they matter as much as these six and specifically these four at the top here. So let's go ahead and walk through this through the lens of my personal standards for efficient language models. Let's break it down. So first things first, the accuracy for the ITV benchmark, which we're about to get to must hit 80%. So if a model is not passing about 80% here, I automatically disqualify it. Tokens per second. I require at least 20 tokens per second minimum. If it's below this, it's honestly just not worth it. It's too slow. There's not enough happening. Anything above this, of course we'll accept. So keep in mind when you're setting your personal standards, you're really looking for ranges, right? Anything above 80% for me is golden. Anything above 20 tokens per second at a very minimum is what we're looking for. So let's look at memory. For me, I am only willing to consume up to about 32 gigabytes of RAM, GPU, CPU. However, it ends up getting sliced. On my 64 gigabyte, I have several Docker instances and other applications that are basically running 24 seven that constrain my dev environment. Regardless, I'm looking for ELMs that consume less than 32 gigabytes of memory. Context window, for me, the sweet spot is 32K and above. Lama 3 released with 8K. I said, cool. Benchmarks look great, but it's a little too small. For some of the larger prompts and prompt chains that I'm building up, I'm looking for 32K minimum context. I highly recommend you go through and set your personal standard for each one of these metrics, as they're likely to be the most important for getting your ELM, for getting a model running on your device. So JSON response, vision support. I don't really care about vision support. This is not a high priority for me. Of course, it's a nice to have. There are image models that can run in isolation. That does the trick for me. I'm not super concerned about having local on device multimodal models, at least right now. JSON response support is a must have. For me, this is built into a lot of the model providers, and it's typically not a problem anymore. So these are my personal standards. The most important ones are up here. 80% accuracy on the ITP benchmark, which we'll talk about in just a second. We have the speed. I'm looking for 20 tokens per second at a minimum. I'm looking for a memory consumption maximum of 32. And then of course, the context window. I am simplifying a lot of the details here, especially around the memory usage. I just want to give you a high level of how to think about what your standards are for ELMs. So that when they come around, you're ready to start using it for your personal tools and products. Having this ready to go as soon as these models are ready will save you time and money, especially as you scale up your usage of language models. So let's talk about the ITP benchmark. What is this? It's simple. It's nothing fancy. ITP is just, is this viable? That's what the test is all about. I just want to know, is this ELM viable? Are these efficient language models, AKA on device language models good enough? This code repository we're about to dive into. It's a personalized use case specific benchmark to quickly swap in and out ELMs, AKA on device language models to know if it's ready for your tools and applications. So let's go ahead and take a quick look at this code base. Link for this is going to be in the description. Let's go ahead and crack open VS code and let's just start with the README. So let's preview this and it's simple. This uses Bunn, PromptFu, and Alama for a minimalist cross-platform local LLM prompt testing and benchmarking experience. So before we dive into this anymore, I'm just going to go ahead, open up the terminal. I'm going to type Bunn run ELM, and that's going to kick off the test. So you can see right away, I have four models running, starting with GPT 3.5 as a control model to test against. And then you can see here, we have Alama Chat, Alama 3, we have PHY, and we have Gemma running as well. So while this is running through our 12 test cases, let's go ahead and take a look at what this code base looks like. So all the details that get set up are going to be in the README. Once you're able to get set up with this in less than a minute, this code base was designed specifically for you to help you benchmark local models for your use cases so that when they're ready, you can start saving time and saving money immediately. If we look at the structure, it's very simple. We have some setup, some minor scripts, and then we have the most important thing, bench, underscore, underscore, and then whatever the test suite name is. This one's called Efficient Language Models. So let's go ahead and look at the prompt. So the prompt is just a simple template. This gets filled in with each individual test run. And if we open up our test files, you can see here, let's go ahead and collapse everything. You can see here we have a list of what do we have here, 12 tests. They're sectioned off. You can see we have string manipulation here, command generation, code explanation, text classification. This is a work in progress of my personal ELM accuracy benchmark. By the time you're watching this, there'll likely be a few additional tests here. They'll be generic enough though, so that you can come in, understand them, and tweak them to fit your own specific use case. So let's go ahead and take a look at this. So this is the test file, and we'll look into this in more detail in just a second here. But if you go to the most important file, prompt through configuration, you can see here, let's go ahead and collapse this. We have our control cloud LLM. So I like to have a kind of control and an experimental group. The control group is going to be our cloud LLM that we want to prove our local models are as good as or near the performance of. Right now I'm using dbt 3.5. And then we have our experimental local ELMs. So we're going to go ahead and take a look at this. So in here, you can see we have LLM 3, we have 5.3, and we have Gemma. Again, you can tweak these. This is all built on top of LLM. Let's go ahead and run through our tool set quickly. We're using Bun, which is an all in one JavaScript runtime. Over the past year, the engineers have really matured the ecosystem. This is my go-to tool for all things JavaScript and TypeScript related. They recently just launched Windows support, which means that this code base will work out of the box for Mac, Linux, and Windows users. You can go ahead and click on this, and you'll be able to see the code base. Huge shout out to the Bun developers on all the great work here. We're using Ollama to serve our local language models. I probably don't need to introduce them. And last but not least, we're using PromptFu. I've talked about PromptFu in a few videos in the past, but it's super, super important to bring back up. This is how you can test your individual prompts against expectations. So what does that look like? If we scroll down to the hero here, you can see exactly what a test case looks like. So you have your prompts that you're going to test. So this is what you would normally type in a chat input field. And then you can go ahead and click test. And then you can go ahead and you have your individual models. Let's say you want to test OpenAI, Plod, and Mistral Large. You would put those all here. So for each provider, it's going to run every single prompt. And then at the bottom, you have your test cases. Your test cases can pass in variables to your prompts, as you can see here. And then most importantly, your test cases can assert specific expectations on the output of your LLM. So you can see here where you're running this type contains. We need to make sure that it has this string in it. We're making sure that the cost is below this amount, latency below this, etc. There are many different assertion types. The ITV benchmark repo uses these three key pieces of technology for a really, really simplistic experience. So you have your prompt configuration where you specify what models you want to use. You have your tests, which specify the details. So let's go ahead and look at one of these tests. You can see here, this is a simple bullet summary test. So I'm saying create a summary of the following text in bullet points. And then here's the script to one of our previous videos. So, you know, here's a simple yet powerful idea that can help you take a large step toward useful and valuable agentic workflows. We're asserting case insensitively that all of these items are in the response of the prompt. So let's go ahead and look at our output. Let's see if our prompts completed. Okay, so we have 33 success and 15 failed tests. So LLM3 ran every single one of these test cases here and reported its results. So let's go ahead and take a look at what that looks like. So after you run that was Bon ELM, after you run that you can run Bon View and if we open up package.json, and you can see Bon view just runs prompt foo view Bon view. This is going to kick off a local prompt foo server that shows us exactly what happened in the test runs. So right away, you can see we have a great summary of the results. So we have our control test failing at only one test, right. So it passed 91% accuracy. This and then we have llama 3 so close to my 80 standard we'll dig into where it went wrong in just a second here we then have phi 3 failed half of the 12 test cases and then we have gemma looks like it did one better 7 out of 12 so you can see here this is why it's important to have a control group specifically for testing elms it's really good to compare against a kind of high performing model and you know gpg 3.5 turbo it's not really even high performing anymore but it's a good benchmark for testing against local models because really if we use opus or gpt4 here the local models won't even come close so that's why i like to compare to something like gpg 3.5 you can also use cloud 3 haiku here this right away gives you a great benchmark on how local models are performing let's go ahead and look at one of these tests what happened where did things go wrong let's look at our text classification this is a simple test the prompt is is the following block of text a sql natural language query nlq respond exclusively with yes or no so this test here is going to look at how well the model can both answer correctly and answer precisely right it needs to say yes or no and then the block of text is select 10 users over the age of 21 with a gmail address and then we have the assertion type equals yes so our test case validates this test if it returns exclusively yes and we can look at the prompt test to see exactly what that looks like so if you go to test.yaml we can see we're looking for just yes this is what that test looks like right so this is our one of our text classification tests and and we have this assertion type equals yes so equals is used when you know exactly what you want the response to be a lot of the times you'll want something like a i contains all so case insensitive contains everything or a case insensitive contains any and there are lots of different assertions you can make you can easily dive into that i've linked that in the readme you'll want to look at the assertions documentation in prompt foo they have a whole list here of different assertions you can make to improve and strengthen your prompt test so that's what that test looks like and and you can kind of go through the line over each model to see exactly what went right what went wrong etc so feel free to check out the other test cases the long story short here is that by running the itv benchmark by running your personal benchmarks against local models you can have higher confidence and you can have first movers advantage on getting your hands on these local models and truly utilizing them as you can see here llama 3 is nearly within my standard of what i need an elm to do based on these 12 test cases i'll increase this to add a lot more of the use cases that i use out of these 12 test cases llama 3 is performing really really well and this is the 8b model right so if we look at a llama you can see here the default version that comes in here is the 8 billion parameter model that's the 4b quantization so pretty good stuff here i don't need to talk about how great llama 3 is the rest of the internet is doing that but it is really awesome to see how it performs on your specific use cases the closer you get to the metal here the closer you understand how these models are performing next to each other the better and the faster you're going to be able to take these models and productionize them in your tools and products i also just want to shout out how incredible it is to actually run these tests over and over and over again with the same model without thinking about the cost for a single second. You can see here, we're getting about 12 tokens per second across the board. So not ideal, not super great, but still everything completed fine. You can walk through the examples. A lot of these test cases are passing. This is really great. I'm gonna be keeping a pretty close eye on this stuff. So definitely like and subscribe if you're interested in the best local performing models. I feel like we're gonna have a few different classes of models, right? If we break this down, fastest, cheapest, and then it was best, slowest. And now what I think we need to do is take this and add a nest to it. So we basically say something like this, right? We say cloud, right? And then we say the slowest, most expensive. And then we say local, fastest, lower accuracy, and best, slowest, right? So things kind of change when you're at the local level. Now we're just trading off speed and accuracy, which simplifies things a lot, right? Because basically we were doing this where we had the fastest, cheapest, and we had lower accuracy. And then we had best, slowest, most expensive, right? So this is your Opus, this is your GPT-4, and this is your Haiku, GPT-3. But now we're getting into this interesting place where now we have things like this, right? Now we have PHY-3, we have LAMA-3, LAMA-3 is seven or eight billion. We also have Gemma. And then in the slowest, we have our bigger models, right? So this is where like LAMA-3 was at 70 billion, that's where this goes. And then, you know, whatever other big models that come out that are, you know, going to really trip your RAM, they're going to run slower, but they will give you the best performance that you can possibly have locally. So I'm keeping an eye on this. Hit the like and hit the sub if you want to stay up to date with how cloud versus local models progress. We're going to be covering these on the channel and I'll likely use, you know, this class system to separate them to keep an eye on these, right? First thing that needs to happen is we need anything at all. To run locally, right? So this is kind of, you know, in the future, same with this. Right now we need just anything to run well enough. So, you know, we need decent accuracy, any speed, right? So this is what we're looking for right now. And this stuff is going to come in the future. So that's the way I'm looking at this. The ITV benchmark can help you gain confidence in your prompts. Link for the code is going to be in the description. I built this to be ultra simple. Just follow the README to get started. Thanks to Bunn. Pramphu and Ollama. This should be completely cross-platform and I'll be updating this with some additional test cases. By the time you watch this, I'll likely have added several additional tests. I'm missing some things in here like code generation, context window length testing, and a couple other sections. So look forward to that. I hope all of this makes sense. Up your feeling, the speed of the open source community building toward usable viable ELMs. I think this is something that we've all been really excited about. And it's finally starting to happen. I'm going to predict by the end of the year, we're going to have an on-device Haiku to GPT-4 level model running, consuming less than 8 gigabytes of RAM. As soon as OpenELM hits Ollama, we'll be able to test this as well. And that's one of the highlights of using the ITV benchmark inside of this code base. You'll be able to quickly and seamlessly get that up and running by just updating the model name, adding a new configuration here like this. And then it'll look something like this, OpenELM, and then whatever the size is going to be, say it's the 3B, and that's it. Then you just run the test again, right? So that's the beauty of having a test suite like this set up and ready to go. You can, of course, come in here and customize this. You can add Opus, you can add Haiku, you can add other models, tweak it to your liking. That's what this is all about. I highly recommend you get in here and test this. This was important enough for me to take a break from personal AI assistance, and HSE, and all of that stuff. And I'll see you guys in the next video. Bye-bye. MacBook Pro M4 chip is released. And as the LLM community rolls out permutations of Llama 3, I think very soon, possibly before mid-2024, ELM's efficient language models will be ready for on-device use. Again, this is use case specific, which is really the whole point of me creating this video is to share this code base with you so that you can know exactly what your use case specific standards are. Because after you have standards set and a great prompting framework like PromptFu, you can then answer the question for yourself, for your tools, and for your products, is this efficient language model ready for my device? For me personally, the answer to this question is very soon. If you enjoyed this video, you know what to do. Thanks so much for watching. Stay focused and keep building.