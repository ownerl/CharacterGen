import os
import io
import sqlite3
from flask import Flask, render_template, request
import openai
import requests
from apikey import apikey, image_key
from PIL import Image
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


openai.api_key = apikey
os.environ['OPENAI_API_KEY'] = apikey


# configure my app
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# path to images
img_path = "static/Image/"


con = sqlite3.connect("static/character.db", check_same_thread=False)

db = con.cursor()


db.execute(
    "CREATE TABLE IF NOT EXISTS character( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, level NUM, stats TEXT, bio TEXT, desc TEXT, image TEXT)"
)


# defining image generation first.
def generate_image(desc):
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
    files = {
        'prompt': (None, 'Ink painting of character. Muted colors, fantasy setting. 4k, high quality, anatomically correct. {}'.format(desc), 'text/plain')
    },
    headers = { 'x-api-key': image_key}
    )

    if (r.ok):
        generated_image = r.content
        return generated_image
    else:
        r.raise_for_status()

# defining adding character into database
def add_character(name, level, stats, bio, desc, image):
    db.execute(
        "INSERT INTO character(name, level, stats, bio, desc, image) VALUES (:name, :level, :stats, :bio, :desc, :image)", {'name': name, 'level': level, 'stats': stats, 'bio': bio, 'desc': desc, 'image': image}
    )
    con.commit()

# fetch all characters to display in library webpage
def character_info():
    db.execute(
        "SELECT * FROM character ORDER BY name ASC"
    )
    info_characters = db.fetchall()
    return info_characters


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/characters")
def characters():
    characters_info = character_info()
    return render_template("characters.html", characters=characters_info)


@app.route("/generate", methods=["POST", "GET"])
def generate():
    if request.method == "POST":
        prompt = request.form.get("generate")
        level = str("Level " + request.form.get("level"))

            # prompt templates - can be chained together
        title_template = PromptTemplate(
            input_variables = ['topic', 'level'],
            template="""Come up with stats, skills, race, and class(es) for this Dungeons and Dragons character: {topic}, {level}. Stats, skills, race, and class(es) MUST be provided.
            The output should be consistent with Dungeons and Dragons 5th edition standards and randomized appropriately to the character level.
            The stats should be capable of filling all fields of a Dungeons and Dragons 5th edition character sheet. Shorten the stats, for example Strength should be STR. All stats should be on a single line.
            Each of the skills should be its own item with a corresponding bonus separated by a colon like this Acrobatics: +2. All skills should be on a single line separate from stats. The stats like STR should not output a bonus.
            """
        )
        script_template = PromptTemplate(
            input_variables = ['topic', 'title'],
            template='{topic} is a dungeons and dragons character with the following stats and class: {title}. Write an engaging fantasy backstory for this character ending with an event that is needs a resolution. Make sure no statements contradict each other and object permanence is observed.'
        )
        desc_template = PromptTemplate(
            input_variables = ['script', 'title'],
            template='Clearly state the gender (male or female), race, class, and describe the phyiscal, facial, and body characteristics of a person based on the following information: {script} {title}. The output should be 1-2 descriptive sentences. Exclude the name of the person.'
        )

        # LLMs
        llm = OpenAI(temperature=0.7, max_tokens=1024)
        llm2 = OpenAI(temperature=0.1, max_tokens=1024)
        # llm chains based on prompt template

        title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title')
        script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script')
        desc_chain = LLMChain(llm=llm2, prompt=desc_template, verbose=True, output_key='desc')

        if prompt:
            title = title_chain.run(topic=prompt, level=level)
            script = script_chain.run(title=title, topic=prompt)
            desc = desc_chain.run(script=script, title=title)

        generated_image = generate_image(desc)
        stream = io.BytesIO(generated_image)
        simage = Image.open(stream)
        simage.save(f"static/Image/{prompt}.png", format="PNG")
        image = img_path + prompt + ".png"

        # save character to database
        add_character(prompt, level, title, script, desc, image)

        return render_template("generate.html", image=image, title=title, script=script, desc=desc)
    else:
        return render_template("generate.html")




