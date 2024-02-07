import os
import openai
from openai import OpenAI
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from intro_to_flask import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .create_speech_form import CreateSpeechForm
from pathlib import Path

create_speech_blueprint = Blueprint('create_speech', __name__)

@create_speech_blueprint.route('/create_speech',methods=['GET', 'POST'])
@app.route('/create_speech',methods=['GET', 'POST'])
def create_speech():
  form = CreateSpeechForm(request.form)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('create_speech.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/api-reference/images
        client = OpenAI()

        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="Today is a wonderful day to build something people love!"
            )
        speech = response.stream_to_file(speech_file_path)
        return render_template('create_speech.html', speech_prompt=form.prompt.data, speech_response=speech, success=True)
      
  elif request.method == 'GET':
      return render_template('create_speech.html', form=form)