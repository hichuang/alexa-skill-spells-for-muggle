# coding=utf-8
"""
Spells for Muggle is built with the Amazon Alexa Skills Kit.
"""

from __future__ import print_function
import random

pause_ssml_tag = '<break time="300ms"/>'

# --------------- Spell class ------------------
class Spell:
    'class for spell'
    __all_spells__ = {}

    def __init__(self, name, desc, actions, ipa):
        self.name = name.lower()
        self.desc = desc
        self.actions = actions
        self.ipa = ipa
        Spell.__all_spells__[self.name] = self

    @staticmethod
    def getSpell(name):
        if name.lower() in Spell.__all_spells__:
            return Spell.__all_spells__[name.lower()]
        return None

    @staticmethod
    def pickSpell():
        return Spell.__all_spells__[random.choice(Spell.__all_spells__.keys())]

    @staticmethod
    def actionToSpell(action):
        for spell in Spell.__all_spells__.values():
            if action.lower() in spell.actions:
                return spell
        return None

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(card_title, card_content, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': wrap_within_speak_tags(output)
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': card_content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': wrap_within_speak_tags(reprompt_text)
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def initialize_spells():
    """ Initialize all the spells
    """
    Spell("Accio", "A charm that allows the caster to summon an object", ["summon", "summoned"], "ˈæksioʊ")
    Spell("Alohomora", "A spell to open locks", ["open", "unlock", "opened", "unlocked"], "əˌloʊhəˈmɔərə")
    Spell("Expelliarmus", "A spell that removes an object (often a wand) from the recipient's hand", ["remove", "removed"], "ɛksˌpɛliˈɑːrməs")
    Spell("Impedimenta", "A spell to stop or slow down any person or creature by temporarily immobilising them", ["stop", "slow down", "immobilize"], "ɪmˌpɛdᵻˈmɛntə")
    Spell("Lumos", "A spell that lights up dark places at the flick of a wand", ["brighten", "bright", "light up", "illuminate"], "ˈljuːmɒs")
    Spell("Nox", "Counter charm to the Lumos spell. This spell causes the light at the end of the caster's wand to be extinguished", ["extinguish", "dark"], "ˈnɒks")
    Spell("Obliviate", "A charm that hides a memory of a particular event", ["hide"], "oʊˈblɪvieɪt")
    Spell("Petrificus Totalus", "Also known as The Full Body-Bind, this spell paralyses the victim", ["paralyze"], "pɛˈtrɪfᵻkəs toʊˈtæləs")
    Spell("Reparo", "This spell repairs broken or damaged objects", ["repair", "repaired", "fix", "fixed"], "rɛˈpɑːroʊ")
    Spell("Silencio", "This spell silences something immediately", ["silence", "quite", "shut up", "silent"], "sɪˈlɛnsioʊ")
    Spell("Wingardium Leviosa", "This spell leviates an object off the ground and moved according to the caster", ["leviate", "fly", "float"], "wɪŋˈɡɑːrdiəm ˌlɛviˈoʊsə")

def wrap_within_speak_tags(ssml_text):
    if ssml_text:
        return "<speak>{}</speak>".format(ssml_text)
    else:
        return None

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    should_end_session = False
    session_attributes = {}
    card_title = "Welcome to Spells for Muggle"
    card_content = "Try ask me, teach me a spell."
    speech_output = "Welcome to Spells for Muggle. " \
                    "Try ask me, teach me a spell or something like, how to light up a room."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = speech_output
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    speech_output = "Thank you for trying Spells for Muggle. " + \
                    "Have a nice day! "
    card_title = "See you next time"
    card_content = speech_output
    # Setting this to true ends the session and exits the skill.
    should_end_session = True

    return build_response({}, build_speechlet_response(
        card_title, card_content, speech_output, None, should_end_session))

def spell_by_name(intent, session):
    """ Gets the spell from the name in the intent or pick a random one if not specified
    """
    should_end_session = True
    spell_not_exists = False

    # Get spell by name if there is value in Spell slot
    if 'Spell' in intent['slots'] and 'value' in intent['slots']['Spell']:
        spell_name = intent['slots']['Spell']['value']
        spell = Spell.getSpell(spell_name)
        if spell is None:
            # If spell name did not exist, pick a random spell to teach
            spell_not_exists = True
            spell = Spell.pickSpell()
    else:
        spell = Spell.pickSpell()

    session_attributes = {"Spell": spell.name}
    spell_phoneme = '<phoneme alphabet="ipa" ph="{}">{}</phoneme>'.format(spell.ipa, spell.name.title())
    speech_output = '{},{} {}. Repeat after me. {} {}'.format(spell_phoneme, pause_ssml_tag, spell.desc, pause_ssml_tag, spell_phoneme)
    if spell_not_exists:
        speech_output = "We can't find the spell, {}, you inquired. Here is a spell we pick for you. {}".format(spell_name, speech_output)
    reprompt_text = None
    card_title = spell.name.title()
    card_content = spell.desc

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def spell_by_action(intent, session):
    """ Gets the spell by the action
    """
    card_title = "Spell Not Found"
    card_content = "Please try again."
    session_attributes = {}
    should_end_session = False

    if 'Action' in intent['slots'] and 'value' in intent['slots']['Action']:
        action = intent['slots']['Action']['value']
        spell = Spell.actionToSpell(action)
        if spell:
            # action map to a spell
            session_attributes = {"Spell": spell.name}
            spell_phoneme = '<phoneme alphabet="ipa" ph="{}">{}</phoneme>'.format(spell.ipa, spell.name.title())
            speech_output = 'The spell you should use is, {} {}. {} {}. Repeat after me. {} {}'.format(
                pause_ssml_tag, spell_phoneme, pause_ssml_tag, spell.desc, pause_ssml_tag, spell_phoneme)
            reprompt_text = None
            card_title = spell.name.title()
            card_content = spell.desc
            should_end_session = True
        else:
            speech_output = "I can't find the spell for {}. Please try something else.".format(action)
            reprompt_text = speech_output
    else:
        speech_output = "Try ask me how to perform an action on something or just ask, Teach me a spell."
        reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def cast_spell(intent, session):
    """ Cast a spell: See if there is a quiz need to answer. Otherwise, just explains the spell.
    """
    card_title = "Wrong Answer"
    card_content = "Please try again."
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    if 'Spell' in intent['slots'] and session.get('attributes', {}) and "spellToCast" in session.get('attributes', {}):
        spell_casted_name = intent['slots']['Spell']['value']
        spell_to_cast_name = session['attributes']['spellToCast']
        # get casted spell object
        spell = Spell.getSpell(spell_casted_name)
        if spell:
            spell_phoneme = '<phoneme alphabet="ipa" ph="{}">{}</phoneme>'.format(spell.ipa, spell.name)
        else:
            spell_phoneme = spell_casted_name

        if spell_casted_name.lower() == spell_to_cast_name.lower():
            # spell casted match the answer
            speech_output = "You are right. The spell to cast is {}. Good job!".format(spell_phoneme)
            card_title = "Correct Answer!"
            card_content = "{} is the right answer.".format(spell.name.title())
            should_end_session = True
        else:
            question = session['attributes']['spellQuizSpeech']
            speech_output = "Sorry, {} is not the right answer. Please try another answer. {}".format(spell_phoneme, question)
            reprompt_text = speech_output
            session_attributes = session.get('attributes', {})
    else:
        return spell_by_name(intent, session)

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))
    

def start_spell_quiz(intent, session):
    """ Start spell quiz
    """
    should_end_session = False

    spell = Spell.pickSpell()
    reprompt_text = "Answer the following description with a spell. {} {}. {} Which spell will you use?".format(
        pause_ssml_tag, spell.desc, pause_ssml_tag)
    speech_output = "let's start a quiz. " + reprompt_text

    card_title = "Let's start a quiz"
    card_content = "Answer the following description with a spell. {}. Which spell will you use?".format(spell.desc)
    session_attributes = {"spellToCast": spell.name, "spellQuizSpeech": reprompt_text}

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TeachSpell":
        return spell_by_name(intent, session)
    elif intent_name == "CastSpell":
        return cast_spell(intent, session)
    elif intent_name == "WhichSpell":
        return spell_by_action(intent, session)
    elif intent_name == "SpellQuiz":
        return start_spell_quiz(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    initialize_spells()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
