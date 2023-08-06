import pydantic
import logging
import json
import pprint
import openai
import time
import cloudlanguagetools.chatapi
import cloudlanguagetools.options

logger = logging.getLogger(__name__)

class IsNewSentenceQuery(pydantic.BaseModel):
    is_new_sentence: bool = pydantic.Field(description="true if the last user message is a new input sentence for translation, transliteration, pronuncation or dictionary lookup," 
                                           "false if it is a question regarding the meaning, grammar, or vocabulary of the previous sentence")


"""
holds an instance of a conversation
"""
class ChatModel():
    FUNCTION_NAME_TRANSLATE = 'translate'
    FUNCTION_NAME_TRANSLITERATE = 'transliterate'
    FUNCTION_NAME_DICTIONARY_LOOKUP = 'dictionary_lookup'
    FUNCTION_NAME_BREAKDOWN = 'breakdown'
    FUNCTION_NAME_PRONOUNCE = 'pronounce'

    def __init__(self, manager, audio_format=cloudlanguagetools.options.AudioFormat.mp3):
        self.manager = manager
        self.chatapi = cloudlanguagetools.chatapi.ChatAPI(self.manager)
        self.instruction = None
        self.message_history = []
        self.last_call_messages = None
        self.total_tokens = 0
        self.latest_token_usage = 0
        self.last_input_sentence = None
        self.audio_format = audio_format
    
    def set_instruction(self, instruction):
        self.instruction = instruction

    def get_instruction(self):
        return self.instruction

    def get_last_call_messages(self):
        return self.last_call_messages

    def set_send_message_callback(self, send_message_fn, send_audio_fn, send_error_fn):
        self.send_message_fn = send_message_fn
        self.send_audio_fn = send_audio_fn
        self.send_error_fn = send_error_fn

    def send_message(self, message):
        self.send_message_fn(message)

    def send_audio(self, audio_tempfile):
        self.send_audio_fn(audio_tempfile)

    def send_error(self, error: str):
        self.send_error_fn(error)        

    def get_system_messages(self):
        # do we have any instructions ?
        instruction_message_list = []
        if self.instruction != None:
            instruction_message_list = [{"role": "system", "content": self.instruction}]

        messages = [
            {"role": "system", "content": "You are a helpful assistant specialized in translation and language learning."}
        ] + instruction_message_list

        return messages

    def call_openai(self):

        messages = self.get_system_messages()
        messages.extend(self.message_history)

        self.last_call_messages = messages

        logger.debug(f"sending messages to openai: {pprint.pformat(messages)}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            # require larger context
            # model="gpt-3.5-turbo-16k",
            messages=messages,
            functions=self.get_openai_functions(),
            function_call= "auto",
            temperature=0.0
        )

        self.latest_token_usage = response['usage']['total_tokens']
        self.latest_prompt_usage = response['usage']['prompt_tokens']
        self.latest_completion_usage = response['usage']['completion_tokens']
        self.total_tokens += self.latest_token_usage

        return response

    def status(self):
        return f'total_tokens: {self.total_tokens}, latest_token_usage: {self.latest_token_usage} (prompt: {self.latest_prompt_usage} completion: {self.latest_completion_usage})'

    def is_new_sentence(self, input_sentence) -> bool:
        """return true if input is a new sentence. we'll use this to clear history"""

        messages = [
            {"role": "system", "content": "You are a helpful assistant specialized in translation and language learning."},
            {"role": "user", "content": self.last_input_sentence},
            {"role": "user", "content": input_sentence}
        ]

        new_sentence_function_name = 'is_new_sentence'

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=[{
                'name': new_sentence_function_name,
                'description': "Determine whether the last user message is a new sentence or a question regarding the meaning, grammar, or vocabulary of the previous sentence",
                'parameters': IsNewSentenceQuery.model_json_schema(),
            }],
            function_call={'name': new_sentence_function_name},
            temperature=0.0
        )

        message = response['choices'][0]['message']
        function_name = message['function_call']['name']
        assert function_name == new_sentence_function_name
        arguments = json.loads(message["function_call"]["arguments"])
        is_new_sentence_arg = IsNewSentenceQuery(**arguments)
        
        logger.info(f'input sentence: [{input_sentence}] is new sentence: {is_new_sentence_arg.is_new_sentence}')
        return is_new_sentence_arg.is_new_sentence



    def process_message(self, input_message):
    
        # do we need to clear history ?
        if len(self.message_history) > 0 and self.is_new_sentence(input_message):
            self.message_history = []

        max_calls = 10
        continue_processing = True

        # message_history contains the most recent request
        self.message_history.append({"role": "user", "content": input_message})


        function_call_cache = {}
        at_least_one_message_to_user = False

        try:
            while continue_processing and max_calls > 0:
                max_calls -= 1
                response = self.call_openai()
                logger.debug(pprint.pformat(response))
                message = response['choices'][0]['message']
                message_content = message.get('content', None)
                if 'function_call' in message:
                    function_name = message['function_call']['name']
                    logger.info(f'function_call: function_name: {function_name}')
                    try:
                        arguments = json.loads(message["function_call"]["arguments"])
                    except json.decoder.JSONDecodeError as e:
                        logger.exception(f'error decoding json: {message}')
                    arguments_str = json.dumps(arguments, indent=4)
                    # check whether we've called that function with exact same arguments before
                    if arguments_str not in function_call_cache.get(function_name, {}):
                        # haven't called it with these arguments before
                        function_call_result, sent_message_to_user = self.process_function_call(function_name, arguments)
                        at_least_one_message_to_user = at_least_one_message_to_user or sent_message_to_user
                        self.message_history.append({"role": "function", "name": function_name, "content": function_call_result})
                        # cache function call results
                        if function_name not in function_call_cache:
                            function_call_cache[function_name] = {}
                        function_call_cache[function_name][arguments_str] = function_call_result
                    else:
                        # we've called that function already with same arguments, we won't call again, but
                        # add to history again, so that chatgpt doesn't call the function again
                        self.message_history.append({"role": "function", "name": function_name, "content": function_call_result})
                else:
                    continue_processing = False
                    if at_least_one_message_to_user == False:
                        # or nothing has been shown to the user yet, so we should show the final message. maybe chatgpt is trying to explain something
                        self.send_message(message['content'])
                
                # if there was a message, append it to the history
                if message_content != None:
                    self.message_history.append({"role": "assistant", "content": message_content})
        except Exception as e:
            logger.exception(f'error processing function call')
            self.send_error(str(e))                

        # clear history after processing one input sentence
        # self.message_history = []
        self.last_input_sentence = input_message

    def process_function_call(self, function_name, arguments):
        # by default, don't send output to user
        send_message_to_user = False
        if function_name == self.FUNCTION_NAME_PRONOUNCE:
            query = cloudlanguagetools.chatapi.AudioQuery(**arguments)
            audio_tempfile = self.chatapi.audio(query, self.audio_format)
            result = query.input_text
            self.send_audio(audio_tempfile)
            send_message_to_user = True
        else:
            # text-based functions
            try:
                if function_name == self.FUNCTION_NAME_TRANSLATE:
                    translate_query = cloudlanguagetools.chatapi.TranslateQuery(**arguments)
                    result = self.chatapi.translate(translate_query)
                    send_message_to_user = True
                elif function_name == self.FUNCTION_NAME_TRANSLITERATE:
                    query = cloudlanguagetools.chatapi.TransliterateQuery(**arguments)
                    result = self.chatapi.transliterate(query)
                    send_message_to_user = True
                elif function_name == self.FUNCTION_NAME_DICTIONARY_LOOKUP:
                    query = cloudlanguagetools.chatapi.DictionaryLookup(**arguments)
                    result = self.chatapi.dictionary_lookup(query)
                    send_message_to_user = True
                elif function_name == self.FUNCTION_NAME_BREAKDOWN:
                    query = cloudlanguagetools.chatapi.BreakdownQuery(**arguments)
                    result = self.chatapi.breakdown(query)
                    send_message_to_user = True
                else:
                    # report unknown function
                    result = f'unknown function: {function_name}'
            except cloudlanguagetools.chatapi.NoDataFoundException as e:
                result = str(e)
            logger.info(f'function: {function_name} result: {result}')
            if send_message_to_user:
                self.send_message(result)
        # need to echo the result back to chatgpt
        return result, send_message_to_user    

    def get_openai_functions(self):
        return [
            {
                'name': self.FUNCTION_NAME_TRANSLATE,
                'description': "Translate input text from source language to target language",
                'parameters': cloudlanguagetools.chatapi.TranslateQuery.model_json_schema(),
            },
            {
                'name': self.FUNCTION_NAME_TRANSLITERATE,
                'description': "Transliterate the input text in the given language",
                'parameters': cloudlanguagetools.chatapi.TransliterateQuery.model_json_schema(),
            },
            {
                'name': self.FUNCTION_NAME_DICTIONARY_LOOKUP,
                'description': "Lookup the input word in the given language",
                'parameters': cloudlanguagetools.chatapi.DictionaryLookup.model_json_schema(),
            },
            {
                'name': self.FUNCTION_NAME_BREAKDOWN,
                'description': "Breakdown the given sentence into words",
                'parameters': cloudlanguagetools.chatapi.BreakdownQuery.model_json_schema(),
            },            
            {
                'name': self.FUNCTION_NAME_PRONOUNCE,
                'description': "Pronounce input text in the given language (generate text to speech audio)",
                'parameters': cloudlanguagetools.chatapi.AudioQuery.model_json_schema(),
            },
        ]
