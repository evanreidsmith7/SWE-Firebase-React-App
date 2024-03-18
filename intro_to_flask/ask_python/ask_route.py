import os
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint, flash
from .ask_form import AskmeForm

ask_blueprint = Blueprint('askme', __name__)

@ask_blueprint.route('/askme',methods=['GET', 'POST'])
@app.route('/askme',methods=['GET', 'POST'])
def askme():
    form = AskmeForm(request.form)

    if request.method == 'POST':
        if not form.validate():
            return render_template('askme.html', form=form)
        else:
            client = openai.OpenAI()

            # Moderation step
            moderation_response = client.moderations.create(
                input=form.prompt.data
            )
            if moderation_response.results[0].flagged:
                # Handle flagged prompts
                display_text = 'Your prompt contains inappropriate content. Please try again with a different prompt.'
                return render_template('askme.html',form=form, ask_me_prompt=form.prompt.data, ask_me_response=display_text, success=True)
            else:
                # Safe to proceed
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You're using an application that interacts with users."},
                        {"role": "user", "content": form.prompt.data}
                    ],
                    max_tokens=150
                )

                display_text = response.choices[0].message.content
                return render_template('askme.html', ask_me_prompt=form.prompt.data, ask_me_response=display_text, success=True)

    elif request.method == 'GET':
        return render_template('askme.html', form=form)