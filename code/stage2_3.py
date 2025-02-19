from glob import glob
import pandas as pd
import json
import time
import random
import openai
import sys
import os
import re

system = sys.argv[1]
lp = sys.argv[2]
starting = int(sys.argv[3])
ending = int(sys.argv[4])


judge_system_prompt = "You are a judge for the translation error annotations, given the translation pair and annotations from previous rounds. Your task is to integrate them and remove repeated annotations if any, where if a single error_span contains multiple errors, indicate only the one that is the most severe, and if some errors have the same severity, choose the first matching category listed in the error typology (accuracy, then fluency, then terminology, then style). But please note this rule is only applied when a single error_span contains multiple errors. However, if it is not possible to reliably identify distinct errors because the translation is too badly garbled or is unrelated to the source, then mark a special category, called non-translation, that spans the entire segment. There can be at most one non-translation error per segment, and it should span the entire segment. No other errors should be identified if non-translation is selected."

judge_agent = "Regarding the translation pair \n\n##src_lng## source:\n##source_segment##\n##tgt_lng## translation:\n##target_segment##\n\nFrom previous annotations, we have the accuracy errors detection expert annotations: \n\n##accuracy_annotations##; the fluency errors detection expert annotations: \n\n##fluency_annotations##; the terminology errors detection expert annotations: \n\n##term_annotations##; and the style errors detection expert annotations: \n\n##style_annotations##.\n\nBased on the above information, output your analyses and the final annotations in JSON format as follows: {\"analysis\":(first, judge if it is non-translation error, if yes, explain responsibly why it is; if no, explain how do you use the rule when a single error_span contains multiple errors to output final annotations), \"annotations\":[{\"error_span\":(if non-translation error is selected, provide 'all'; otherwise, the error_span must be chosen from within the translated segment), \"category\":\"({category}/{subcategory} or non-translation)\", \"severity\":\"(minor or major)\", \"is_source_error\":\"(yes or no)\"},...]}"

# judge_agent = "Regarding the translation pair, from previous annotations, we have the accuracy errors detection expert annotations: \n\n##accuracy_annotations##; the fluency errors detection expert annotations: \n\n##fluency_annotations##; the terminology errors detection expert annotations: \n\n##term_annotations##; and the style errors detection expert annotations: \n\n##style_annotations##.\n\nBased on the above information, output your analyses and the final annotations in JSON format as follows: {\"analysis\":(first, judge if it is non-translation error, if yes, explain responsibly why it is; if no, explain how do you use the rule when a single error_span contains multiple errors to output final annotations), \"annotations\":[{\"error_span\":(if non-translation error is selected, provide 'all'; otherwise, the error_span must be chosen from within the translated segment), \"category\":\"({category}/{subcategory} or non-translation)\", \"severity\":\"(minor or major)\", \"is_source_error\":\"(yes or no)\"},...]}"

def set_meta_prompt(meta_prompt: str):
    return {"role": "system", "content": f"{meta_prompt}"}

def add_event(event: str):
    return {"role": "user", "content": f"{event}"}

def construct_message(agents, idx):
    prefix_string = "These are the annotations from the other agent:"

    for agent in agents:
        agent_response = agent[idx]["content"]
        response = "\n\n ```{}```".format(agent_response)

        prefix_string = prefix_string + response
    # When the severity is hard to decide, please lean toward "minor." Only assign "major" if it significantly impacts the meaning. 
    prefix_string = prefix_string + """\n\n Given two different answers, think about it again. Examine your annotations and the other agent's annotations step by step. When the severity is hard to decide, please lean toward "minor." Only assign "major" if it significantly impacts the meaning. Avoid assigning 'non-translation' unless absolutely necessary. Provide your answer in the following JSON format at the end of your response: ```json\n{\"annotations\":[{\"error_span\": {error span in translated segment}, \"category\":\"{category}/{subcategory}\", \"severity\":\"{minor or major}\", \"is_source_error\":\"{yes or no}\"},...]}\n. If no errors are annotated, use the json format: ```json\n{"annotations": []}\n"""

    return {"role": "user", "content": prefix_string}

def ask_prompt(content):
    return [{"role": "user", "content": content}]

def construct_assistant_message(completion):
    content = completion["choices"][0]["message"]["content"]
    return {"role": "assistant", "content": content}


def generate_answer(answer_context):
    # try:
    completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=answer_context,
                n=1)
    return completion

def isnull(content):
    if content == '{"annotations": []}' or content == '{"annotations":[]}' or content == "{'annotations': []}" or content == "{'annotations':[]}":
        return True
    return False

def is_only_double_quotes(text):
    double_quote_forms = {'"', '“', '”'}
    return all(char in double_quote_forms for char in text)

def load_json_files(folder_path):
    json_data = []
    
    files = os.listdir(folder_path)
    
    json_files = sorted(
        [f for f in files if f.endswith('_v1.json') and f.split('_v1.json')[0].isdigit()],
        key=lambda x: int(x.split('_v1.json')[0])
)

    for json_file in json_files:
        try:
            file_path = os.path.join(folder_path, json_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                json_data.append(data)
        except:
            json_data.append(None)
    return json_data

def extract_annotations(content):
    print("content: ", content)

    # pattern = r'\{\s*"annotations"\s*:\s*\[(.*?)\]\s*\}'
    # pattern = r'"annotations"\s*:\s*\[(.*?)\]'
    # pattern = r'"annotations"\s*:\s*\[(.+?)\]'
    pattern = r'"annotations"\s*:\s*\[(.*)\]'


    matches = re.findall(pattern, content, re.DOTALL)

    if matches:
        last_match = matches[-1]
        json_string = f'{{"annotations":[{last_match}]}}'
        print("json_string: ", json_string)
        try:
            json_data = json.loads(json_string)  # 将字符串解析为字典
            return json_data
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return json.loads('{"annotations":[]}')
    else:
        print("No matching JSON found.")


system_prompts = [
    "You are an expert in detecting accuracy errors in translations. Accuracy errors occur when the target content does not accurately reflect the propositional content of the source text. Review the provided translation and identify any errors in the following subcategories: addition, mistranslation, omission, and untranslated text. If no errors are found, return {\"annotations\": []}. If errors are found, list each error with the following details: the exact error span, the subcategory, and the severity (major or minor). Major errors significantly impact meaning and may confuse or mislead the reader. Minor errors have a slight impact, but do not cause loss of meaning or confusion. In case when it is not possible to reliably identify distinct errors because the translation is too badly garbled or is unrelated to the source, then mark a special category, called non-translation. No other errors should be identified if non-translation is selected.", 
    
    "You are an expert in detecting fluency errors in translations. Fluency errors are related to the linguistic well-formedness of the text. Review the provided translation and identify any errors in the following subcategories: character encoding, grammar, inconsistency, punctuation, register, and spelling. If no errors are found, return {\"annotations\": []}. If errors are found, list each error with the following details: the exact error span, the subcategory, and the severity (major or minor). Major errors significantly impact meaning and may confuse or mislead the reader. Minor errors have a slight impact, but do not cause loss of meaning or confusion. In case when it is not possible to reliably identify distinct errors because the translation is too badly garbled or is unrelated to the source, then mark a special category, called non-translation. No other errors should be identified if non-translation is selected.",
    
    "You are an expert in detecting terminology errors in translations. Terminology errors occur when a term deviates from standard subject field or organizational terminology, or when the target term is not the correct equivalent of the source term. Review the provided translation and identify any errors in the following subcategories: inappropriate for context, and inconsistent use. If no errors are found, return {\"annotations\": []}. If errors are found, list each error with the following details: the exact error span, the subcategory, and the severity (major or minor). Major errors significantly impact meaning and may confuse or mislead the reader. Minor errors have a slight impact, but do not cause loss of meaning or confusion. In case when it is not possible to reliably identify distinct errors because the translation is too badly garbled or is unrelated to the source, then mark a special category, called non-translation. No other errors should be identified if non-translation is selected.",
    
    "You are an expert in detecting style errors in translations. Style errors occur when the text is grammatically correct but deviates from organizational style guides or uses inappropriate language. Review the provided translation and identify any style errors. If no errors are found, return {\"annotations\": []}. If errors are found, list each error with the following details: the exact error span, the subcategory (which is always 'awkward' in the style category), and the severity (major or minor). Major errors significantly impact meaning and may confuse or mislead the reader. Minor errors have a slight impact, but do not cause loss of meaning or confusion. In case when it is not possible to reliably identify distinct errors because the translation is too badly garbled or is unrelated to the source, then mark a special category, called non-translation. No other errors should be identified if non-translation is selected."
]

user_prompt = """
{src_lng} source:\n{source_segment}\n{tgt_lng} translation:\n{target_segment}
"""

judge_prompt = "Compare the error annotations provided by two agents for the same machine-translated segment. Determine if the annotations are essentially consistent. The first agent annotations are: {first_annotations}; the other agent annotations are: {second_annotations}. Return \"yes\" if they are consistent, or \"no\" if they are inconsistent. Provide no additional output."


source_lang = "Chinese"
target_lang = "English"


if __name__ == "__main__":
    agents = 2
    max_rounds = 4
    mqm_agents = ["Accuracy", "Fluency", "Terminology", "Style"]

    folder_path = f"M-MAD/data/output_{lp}_{system}_v1"
    all_json_data = load_json_files(folder_path)
    n = len(all_json_data)

    random.seed(0)
    response_dict = {}

    folder_path = f"stage2_3_{lp}_{system}"
    os.makedirs(folder_path, exist_ok=True)
    if ending == 2000:
        ending = n
    for i in range(starting, ending):
        print(f"-------------------The {i}th sample:---------------------")
        if os.path.exists(f"{folder_path}/{i}_v1.json") and os.path.getsize(f"{folder_path}/{i}_v1.json") > 0:
            continue
        with open(f"{folder_path}/{i}_v1.json", "w", encoding='utf-8') as f:
            if all_json_data[i] == "None":
                continue
            source_seg = all_json_data[i]["source_segment"]
            target_seg = all_json_data[i]["target_segment"]
            print("source: ", source_seg)
            print("target: ", target_seg)
            response_dict["source"] = source_seg
            response_dict["target"] = target_seg
            agent_contexts = []
            for mqm_agent_index in range(len(mqm_agents)):
                annotation = all_json_data[i]["players"][mqm_agents[mqm_agent_index]+" Agent"][-1]["content"]

                if "non-translation" in annotation:
                    other_annotation = "I do not think it meets the criteria of being too badly garbled or entirely unrelated to the source, so it cannot be counted as a non-translation error."
                else:
                    other_annotation = annotation.replace("major", "minor")
                content = [annotation, other_annotation]
                
                if annotation == other_annotation:
                    response_dict[mqm_agents[mqm_agent_index]] = annotation
                    continue

                agent_contexts = [[{"role": "system", "content": system_prompts[mqm_agent_index]}, 
                                {"role": "user", "content": user_prompt.format(src_lng=source_lang, tgt_lng=target_lang, source_segment=source_seg, target_segment=target_seg)}]
                                for agent in range(agents)]

                for round in range(max_rounds):
                    for j, agent_context in enumerate(agent_contexts):
                        
                        if round == 0:
                            assistant_message = {"role": "assistant", "content": content[j]}
                            agent_context.append(assistant_message)
                        else:
                            agent_contexts_other = agent_contexts[:j] + agent_contexts[j+1:]
                            message = construct_message(agent_contexts_other, 2 * round)
                            agent_context.append(message)
                            try:
                                completion = generate_answer(agent_context)
                            except:
                                completion = generate_answer(agent_context)
                            assistant_message = construct_assistant_message(completion)
                            agent_context.append(assistant_message)

                    if round != 0:
                        print(agent_contexts[0][-1]['content'])
                        print(agent_contexts[1][-1]['content'])
                        annotation1 = extract_annotations(agent_contexts[0][-1]['content'])
                        annotation2 = extract_annotations(agent_contexts[1][-1]['content'])
                        print("annotation1: ", agent_contexts[0][-1]['content'], "\n", annotation1)
                        print("annotation2: ", agent_contexts[1][-1]['content'], "\n",annotation2)

                        try:
                            judge_response = generate_answer(ask_prompt(judge_prompt.format(first_annotations = annotation1, second_annotations = annotation2)))
                        except:
                            judge_response = generate_answer(ask_prompt(judge_prompt.format(first_annotations = annotation1, second_annotations = annotation2)))
                        judge_ans = judge_response["choices"][0]["message"]["content"]

                        if "yes" in judge_ans:
                            response_dict[mqm_agents[mqm_agent_index]] = extract_annotations(agent_contexts[0][-1]['content'])
                            break
                            
                if "no" in judge_ans:
                    response_dict[mqm_agents[mqm_agent_index]] = extract_annotations(agent_contexts[0][-1]['content'])


            system_prompt = set_meta_prompt(judge_system_prompt)
            use_prompt = add_event(judge_agent.replace("##src_lng##", source_lang).replace("##tgt_lng##", target_lang).replace("##source_segment##", source_seg).replace("##target_segment##", target_seg).replace('##accuracy_annotations##', str(response_dict[mqm_agents[0]])).replace('##fluency_annotations##', str(response_dict[mqm_agents[1]])).replace('##term_annotations##', str(response_dict[mqm_agents[2]])).replace('##style_annotations##', str(response_dict[mqm_agents[3]])))

            print("judge user prompt\n", use_prompt)

            if isnull(response_dict[mqm_agents[0]]) and isnull(response_dict[mqm_agents[1]]) and isnull(response_dict[mqm_agents[2]]) and isnull(response_dict[mqm_agents[3]]):
                response = '{"annotations":[]}'
            elif is_only_double_quotes(source_seg) and is_only_double_quotes(target_seg):
                response = '{"annotations":[]}'
            else:
                try:
                    response = generate_answer([system_prompt, use_prompt])["choices"][0]["message"]["content"]
                except:
                    response = generate_answer([system_prompt, use_prompt])["choices"][0]["message"]["content"]
            print("response", response)
            response = extract_annotations(response)
            response_dict["judge"] = response


            json.dump(response_dict, f, ensure_ascii=False, indent=4)
