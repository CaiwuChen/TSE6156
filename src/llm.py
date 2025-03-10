from google import genai
import google.genai.errors as genai_errors
from openai import OpenAI
import time
import textwrap

def llm_init():
    global client, prompt_system, prompt_history, query_count

    client = genai.Client(api_key="AIzaSyBCzRutWIyKtOHU7U9o0kSecLynt-8wLm0")
    '''
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    '''
    prompt_system = '''
    You are the controller of a quadrupedal robot (A1 robot) with 70 Hz.
    Please inference the output.
    
    The robot's state is represented by a 33-dimensional input space.
    The first 3 dimensions correspond to the robot's linear velocity.
    The next 3 dimensions denote the robot's angular velocity.
    The following 3 dimensions represent the gravity vector.
    The subsequent 12 dimensions represent the joint positions.
    The final 12 dimensions indicate the velocity of each joint.

    The output space is 12-dimension, which is the joint position. 
    The order of the joints is [FRH, FRT, FRC, FLH, FLT, FLC, RRH, RRT, RRC, RLH, RLT, RLC].

    After we have the output, we will use 200 Hz PD controller to track it.

    The following are past and consecutive inputs and outputs.
    All numbers are normalized to non-negative integers by our special rule. 
    The output would be impacted by the previous inputs.
    The trend of the outputs should be smooth.

    Your output is only one line and starts with "Output:", please do not output other redundant words.
    ''' 
    prompt_system = textwrap.dedent(prompt_system)
    prompt_system = prompt_system.split('\n', 1)[1]
    prompt_history = ''
    query_count = 0


def llm_query(msg, call_api=True, retries=3, delay=10):
    global prompt_system, prompt_history, query_count, client

    prompt_history += msg + '\n'
    res=""
    if call_api:
        
        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt_history
                )
               
                res = response.text.split('\n', 1)[0]

                break  # Success, exit retry loop
            except genai_errors.ClientError as e:
                error_message = str(e)  # Convert exception to string for checking
                if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
                    print(f"Rate limit exceeded. Retrying in {delay} sec (Attempt {attempt + 1}/{retries})...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    raise  # Raise other errors that are not rate limit related'
        '''
        completion = client.chat.completions.create( 
            extra_body={},
            model="qwen/qwq-32b:free", 
            messages=[  
                {"role": "user", "content": prompt_history} ],
                temperature=0.0 )
        print("send")
        res = completion.choices[0].message.content
        print(res)
        res = res.split('\n', 1)[0]
        '''
    query_count += 1
    
    if query_count > 50:
        prompt_history = prompt_history.split('\n', 1)[1]
        prompt_history = prompt_history.split('\n', 1)[1]

    if call_api:
        return res
    else:
        return None
    '''
    # Prevent `prompt_history` from growing too long
    if query_count > 50:
        prompt_history = '\n'.join(prompt_history.split('\n')[2:])

    return res if call_api else None'''