# Character Generator
#### Video Demo:  <https://youtu.be/NqHjRHFUs10>

## Preface
This project was created as a capstone to CS50. It utilizes python, SQL, Django, Javascript and html. The app allows you to easily create characters for Dungeons and Dragons 5e using generative AI at its core. I used OpenAI's API to generate the characters and ClipDrop's API to create character portraits using information generated prior. The project has 2 py files, html templates, and a static folder that contains images, stylesheet, and the database that stores the generated characters.

The app will not work due to requiring API keys (which aren't free). I'm not made of money so no API keys here.
Additionally, to run the app properly, you will need to install openai and langchain libraries using "pip install openai" and "pip install langchain".

## Files
The main app.py file contains all the routes and functions to generate and store characters. Multiple dependencies are used, the most important of which are openai and langchain which make character generation possible. API keys are imported from a seperate file to be used later (though when submitting the keys will be placeholders). The app uses Flask as a web interface and SQLite3 to create a database file with the proper tables for character storage if one does not exist.

#### Functions
## Image Generation
The image generation function takes in the character description as input and returns an image file. It sends a text-to-image request to ClipDrop to create a stylized visual representation of the character being generated. The style being requested is an ink painting with muted colours. After numerous tests, this specific style was most fitting for the D&D setting.

## Character Database
The character add function handles storing character information after generation. The character information presented in the section below is saved to a local database file with the character image information being saved as a path only to save on space.

The character info function retrieves and sorts the characters by alphabetical order for neater presentantion.

#### Flask Routes
## Generate
When the user accesses the "/generate" route, they are presented with a form where they can input the character name and level. Upon form submission, the application generates a D&D character based on the input and presents the following components:

Character Title: The generated title includes the character's stats and class, adhering to D&D 5th edition standards. The stats are represented by abbreviations like STR for Strength.

Character Script: The character script is an engaging fantasy backstory for the character, ending with an unresolved event that requires resolution.

Character Description: The character description provides details about the character's gender, race, class, and physical characteristics, excluding the character's name.

Character Image: An image is generated based on the character description and saved as a PNG file in a local static/Image folder. The underlying image generation used by ClipDrop is Stable Diffusion (not XL).

The application uses OpenAI's language models (LLMs) to generate the character details, with different models for each part of the character profile (title, script, and description). The LLMs are based on prompt templates, allowing for flexible character generation.

## Home
When the user accesses the default "/" route, the home html page is rendered to greet the user.

## Characters
When the user accesses the "/characters" route, the character info function is called and all of the characters generated up to the current point are returned for use when the corresponding html page is rendered.

#### HTML
## Layout
This is a simple page that utilizes Bootstrap and W3 to create a basic structure for use in other pages. As this page is always rendered, it features a navigation bar at the top to navigate between the "HOME," "GENERATE," and "CHARACTERS" pages. It also includes a "main" content block where specific content for each page is added.

## Home
The home page provides a short description of what the app is for and a splash image as a preview of what generated characters could look like.

## Generate
When accessed from the navigation bar, the page presents two required input fields of Name and Level, the latter of which only accepts numbers between 1 and 20 inclusive as they are the minimum and maximum levels possible in Dungeons and Dragons respectively. A generate button sits below that is used to submit the information provided in the fields. When submitted, the given information is combined with a premade prompt template to generate the base stats, skills, race, and class(es) of a character altogether called "title". The "title" from the first generation is used partly to generated a biography of the character called "script". The last piece of information is "description" which is generated using the previous two outputs. A character image is created based on the "description" and is presented below all text. The page is rerendered with all of the newly generated content.

During content generation, as it is a time consuming process, the generate button calls forth a fullscreen locked modal with an animated spinning element and text to indicate to the user that their submission was recieved and a character is being generated. When the page is rendered again with the generated content, the modal naturally disappears. The modal is displayed using a Javascript function to make sure it appears only when both form fields are filled and character generation has started.

## Characters
The characters page utilizes the output from the character info function and displays a character library in a drop down accordion list. Using a for loop, the character info is split up into individual characters that are each presented as a seperate accordion item. The drop down accordion is an aesthetically pleasing and visually economic way to present a large amount of information without overwhelming the user. Expanding and collapsing items is the user's prerogative and so they can control the amount of information they are presented with at any given moment.

#### Credits
Special thanks to Stackoverflow for providing examples and explanations that helped me smooth over the many issues I came across bringing this to fruition.
Credits to W3 and Bootstrap for providing visually pleasing elements with which I could display my project and Flask for the easy framework.
I fully acknowledge this project uses OpenAI's language models and ClipDrop's image generation.
As AI was used to create the characters, all generations are free for use by anyone.