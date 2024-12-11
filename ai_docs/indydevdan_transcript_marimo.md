Here's the corrected transcript for the YouTube video about Marimo:

## Introduction

What's up engineers? IndyDevDan here. Today I have something incredible to share with you. I want to introduce you to Marimo, a next-generation Python notebook. I've got a three-course special for you today. These three pieces of value will help you win in the age of generative AI.

## Overview

First, we're going to break down the Marimo reactive notebooks and talk about why it's so important to have a rapid prototyping tool like this. We'll then see how we can use Marimo to quickly run individual prompts and run a single prompt against every state-of-the-art large language model by clicking a single checkbox. Lastly, I want to share the early stages of what my prompt library looks like to give you ideas on how you can build, maintain, and grow your own agentic library.

## Marimo Introduction

So first things first, we have to talk about Marimo. This is a brand new tool that aims to replace Jupyter notebooks. Python notebooks in general are places where engineers can rapidly build out ideas and features. It's often used in AI and ML engineering to pull in data, to experiment on data, to get insights, build artifacts, test out ideas, and so on and so forth.

Marimo has a couple of really interesting killer features. First, they're importing, then creating a markdown item, and you can see here the markdown H1 gets rendered directly above the block. They created a variable in items. Let me go and zoom in on this a little bit. They created a variable in items. As soon as they changed it, the cells that reference that variable - you can see here there are n items - it automatically gets updated.

Now they've changed it to a slider, and the slider automatically updates that value and every other cell that has a reference. Now they're pulling in a chart, and this chart then, of course, is getting fully rendered and is reactively updating based on this slider. They're then going to hop into some data exploration, and honestly, things are moving so quickly here, it's better if we just jump into this ourselves and really see how these notebooks can help you build and rapidly prototype software in the age of AI.

## Marimo Demo

Here we have a codebase that we're going to slowly build up on. So we have three notebooks here. We're going to start with this. After you run the installation instructions, you'll be able to kick off this command here. We're just going to go ahead and fire this off.

So right away, a notebook gets opened up for us, and the first thing I'm going to do here is get out of dev mode and go into what I like to call user mode. I'm going to hit Command+. and now we're presented with this simple UI.

Now, a key part about Marimo that differentiates it from other notebooks is that it is reactive. So if I look at the slider here and I slide this, you can see we have a value just below getting updated. Let me go and bump the size a little bit. So if I scroll here, you can see that value is getting updated. If I click this checkbox, again we have state getting updated. So we have UI automatically updating state.

Let's type in this input field: "Hello, Marimo is awesome" and if I blur or hit enter, we're going to get the text field value. I want you to hold onto that key idea while we move through this.

## Data Visualization

What else can we do with Marimo? We have reactive data visualization. So we have this plot here. It's a simple dataframe with some random data. Right now it's a scatter plot. If we want to, we can change its form. We want to see a line chart? Perfect. If we want to see the bar version, we can go ahead and do that as well. Nice and clean, nice and simple. So you can already kind of see this being useful for data exploration.

If we scroll down, we do have conditional output and control flow. If I hit this checkbox, of course based on a boolean, we can render different content. If we check that off, it'll change. Turn it on, it'll change again.

If we drag and drop a CSV file, we can automatically get a breakdown of the data. So this basically just converted a pandas dataframe and gave us a really clean layout of a bunch of fields. You can see here all the columns. We can do some sorting. Let's descend on location. Let's ascend on age. So you can see this mock user dataset getting broken down.

And then we have some advanced UI components. We have classic accordion, we have nested slider in here, and then we have a dataframe display. We have things like tabs, we have forms, images, videos, layouts, and full-on interactive data exploration with just a few lines of code.

## Developer Mode

So this is incredible. What we're going to do now is hop out of user mode. So I like to call this user mode, and then if we hit Command+., we'll hop into builder mode or engineering mode. So basically, these notebooks are now showing the code surrounding them.

So we have all of our imports here. You can see we have all the markdown getting displayed in these sections, and then we can see what exactly these components look like. So super clean, super declarative. If you've used SwiftUI or any framework where you define your elements inline, you'll be very familiar and you'll be very accustomed to how Marimo creates components.

So we have slider, checkbox, input field, and then we're just rendering them in a vstack. If we want to, we can just switch this. Right now, hstack. Command+Enter, and all of a sudden we're floating left to right, and we just really quickly updated the UI of our elements. So I'll revert that back, and we can do the same thing in developer mode.

I'm checking this, I'm changing this, I'm typing, you know, "test input input value" hitting enter, and you can see that all gets updated there. If we want to, we can hop in here and do something kind of fun. We can paste this and say slider.val and multiply it by the text input value, and of course this is going to render that value multiple times.

So let's go ahead and do something else. Let's change text input to like just an emoji or something. So if we do something like this, place a star here, rerender, we can now change this value and reactively... One of the highlights of Marimo is that this is fully reactive. So as the slider goes up, our stars go up and down.

## Prompt Engineering with Marimo

Let's talk about how we can use this wonderful, reusable, very visual, interactive notebook to get an edge in the age of AI. Let's look at a concrete use case of using this tool for prompt engineering, for prompt management, and ultimately to build your own prompt library.

All right, so if we hop back to the readme and copy this, paste this, and run it, you can see here that we have an ad hoc prompt notebook. And again, Command+., we're now in user mode. So before we were in kind of deep engineering mode, you can see all the code, you can see all the details, you can quickly tweak and modify. You hit Command+., and now you're just focused on consuming the tool, consuming the use case. And you can imagine this is super useful for yourself looking back at products, for you and I on the channel sharing ideas, sharing tools, but also for other engineers on your team and for your product managers and your product team.

So you can see here we have a couple input fields. We have prompt, we have temperature, we have a model, and if we click the model dropdown, you can see we have all the state-of-the-art models at our disposal. And then we can hit "run on all models". So let's just do a test prompt. We'll just say "ping". We'll run on ChatGPT 3.5, and we'll hit submit.

So you can see two new blocks have appeared. We have the form values, which are just the values of our form from above, and we also have the prompt output. So let's go ahead and run something else. We'll say "count to 10, then implement in Python, then in TypeScript", okay? And then we'll just hit submit. So just running another random prompt here on ChatGPT 3.5. You can see they got kicked off and we got a nice response there. We have markdown, we have code, and this is just a simple reusable ad hoc prompt tool.

Again, if we just hit Command+., we can switch into engineering mode, and we can see exactly how this works. So we have imports, we're pulling in our models, we're creating a map between the name and the value of our model. We have our inputs. So you can see here, you know, we're literally just creating m.text_area, m.slider, dropdown, and then we have a checkbox.

And so remember I said in the beginning, you know, one checkbox is going to run this prompt against every single one of our models. So you know what? While we're looking at this, we can go ahead and just kick this off. So I'll say "run on all models" and let's make it do something more interesting. Let's say, "Create a pros and cons of TypeScript versus Python. Explain when to use both." And then we'll hit submit here.

So that's just going to be kicking off in the background, and you can see here... we're taking Marimo components and we're throwing them in a form. You know, that's how we got our text rendered. That's how we got our temp, our model, and our run all. So really kind of simple, declarative UI. It's easy to reason about, it's easy to consume and think about.

You can see here we just have ad hoc prompt, and then we just in text we place our four components. We then run this batch to kind of insert our data into the MD, and then we call form on this. So the form is what creates the submit button. We can then click that and get our submitted output. We can see our form values just as before, and this is a simple, you know, looping through our form and just grabbing the values based on the key. And then we use the mo.ui component, and then we just throw that inside of a markdown block. So that's how we get that.

If we scroll down here, you can see this is our loader for our single prompt execution. Takes the form value, form prompt, and the form temperature. If we're running the Anthropic or Gemini prompts, the temperature just gets set to one inside of this llm module prompt with temperature function.

So if we scroll down some more, you can see we have our multi-model prompt completed. We have an H1. You can see we have a nice clean table. Model ID and then the output. We have the ChatGPT 3.5 answer to our pros and cons table comparing TypeScript and Python. We also have our Claude 2, Claude 3, you know, you can already kind of tell that the reasoning model outputs are much richer. And then we have GPT-4, latest Claude, Gemini 1.5, and Anthropic's latest model.

And if we scroll down to see what that looks like, it's really, really simple. We're taking our list of objects, placing that in the table, and then we're just throwing that in a vstack. Since I'm not running any computations in the cell, it just reruns no problem. All the data in the previous cells that it's used inside of this cell doesn't need to change or update.

So this is really, really powerful. I hope you can see the value in this. We're in engineering mode. We can come in here, we can add models, we can update our list, we can add new UI items very, very quickly. If we haven't clicked submit, you know, our form won't have any values to display, so this block just won't show up. Same thing with the values down here.

And in just two cells, we're able to build a multi-model execution prompt that runs the same prompt against several models. In just eight cells or so, we've replaced a ton of tools. You've probably seen or use a tool that does basically just this. It's a simple ChatGPT replacement with a couple extra nice features and tweaks.

So this is just a minimal example of how you can build a simple reusable prompt notebook that you can hop into, run prompts, test your prompts against different models, and just kind of get an idea for prompts and easily see and read the output. If we want to, we can uncheck, we can fire off a Claude mini, and then we can just get that response. So if we hit submit, all of our reactive cells that are dependent on the form are now recomputing and giving us a concise result. So you can see there the Claude mini is giving us a really great breakdown of when to use TypeScript versus Python.

## Additional Marimo Features

Before we move onto the prompt library, I want to call out another incredible Marimo feature. Inside of the display user mode, we can come over to this dropdown and display as a grid and as slides. Great engineering really comes down to two things: build great software and then communicate the great software that you've built. This tool allows you to do both of those things.

So let's switch over to grid mode here, and as you can imagine, we can now drag and drop the cells that we've been building up. So we now have this cell here. Let's just say I wanted this view and I wanted my prompt output view. I just want to keep it really simple here when I'm in this mode. Widen this a little bit. Okay, so let's just go ahead and run another prompt. So let's just drop down to GPT-4 and let's just rerun. You can see we got the loading state, and now we're just looking at these two cells left to right. Super concise, super simple. It's rendering our prompts, and we can pull in any cell that we want.

For instance, if we wanted to, we can pull in our form values component and move that over here, make this a little wider so we can see everything that's actually getting computed from this. And again, it's all reactive. So if I, you know, maximize this, if I switch to 1.5 Pro, resubmit, both of these items, because they depend and have state referenced in this original cell, all of those states will get updated. So now we have our new model, temperature, and so on and so forth.

Marimo notebooks are incredible. We have rapid prototyping, we have reactive notebooks, we have data visualization which we haven't tapped into too much yet, and we have easy interactivity. Let's go ahead and keep pushing. You know, this is just another fantastic way to view the work you've done. There's also a mode where you can run it in slides.

For our latest, let's make it super specific, and then we can hit submit. And then in our, you know, future items here, you know, while this is loading, it's going to run in this slide mode. Really interesting way to kind of view, manage, and update your code.

So let's go ahead and switch back to vertical view so that you have a good idea of how this works. Go ahead and hit the like, hit the sub, and let's hop into how we can use Marimo next-generation Python notebooks to build a reusable prompt library.

## Building a Prompt Library

So let's dive into our third notebook. I'm going to copy this UV run command, and this is going to kick off our prompt library notebook. Right away, I'm going to collapse all the code, and we're just going to talk about this from a high level. We don't need to see all the nitty-gritty details. We're reviewing the product, we're reviewing the tool, and we're just talking high level.

So you can see here we have a similar UI. We have a nice H1 header, we have a form with a submit button, and here we can select an LLM. So let's go ahead and just select, um, let's go and use Claude mini, and now we're going to select a prompt. So you can see here I have four prompts. Three of these you'll recognize from the previous Claude reasoning model video. We're going to use the bullet knowledge compression prompt and hit submit.

So we've now locked in our prompt. If I hit "click to show", you can see we can view this prompt right here. And if we want to, we can go ahead and change our prompt, hit submit again, and you can see we've now selected that other prompt. So this is a YouTube video chapter prompt that automatically generates YouTube chapters based on timestamps and SEO keywords. Let's go ahead and hop back. Let's keep this simple for this example.

Here's the amazing part that makes this prompt library and that makes Marimo notebooks really powerful. We have this block that we want to update. You want to reuse your prompts. You don't want to spend a bunch of time and then throw your prompt away. There's massive value in reusing your prompts and, most importantly, adding variables to your prompts.

So you can see here we have a variable content, and this Marimo notebook takes that content and finds this pattern. It takes the variable within it and creates a text area. So now we can fill in this text area here, and what I'll do here is I'll pull... I'll pull the legendary "How to Succeed in Mr. Beast Production" PDF. This PDF went viral a couple weeks ago. I think there are some seriously valuable nuggets of information in here.

So let's go ahead and just grab a piece of content. One of my favorite sections was...

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/39473573/8f5704a1-be9d-4a43-991a-496e0f578d8b/English-auto-generated-Engineer-your-Prompt-Library_-Marimo-Notebooks-with-o1-mini-Claude-Gemini-DownSub.com.txt
[2] https://www.youtube.com/watch?v=PcLkBkQujMI
[3] https://docs.marimo.io
[4] https://www.youtube.com/watch?v=PcLkBkQujMI
