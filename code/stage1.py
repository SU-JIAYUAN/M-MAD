import os
import json
import random
# random.seed(0)
import argparse
from langcodes import Language
from utils.agent import Agent
from datetime import datetime
from tqdm import tqdm
import openai
from few_shot_demos import accuracy_user_shot, accuracy_mem_shot, fluency_user_shot, fluency_mem_shot, term_user_shot, term_mem_shot, style_user_shot, style_mem_shot, nontran_user_shot, nontran_mem_shot


NAME_LIST=[
    "Accuracy Agent",
    "Fluency Agent",
    "Terminology Agent",
    "Style Agent",
    "Judge"
]

def extract_json(text):
    brace_open = text.find("{")
    brace_close = text.rfind("}")
    return text[brace_open:brace_close+1]


class DebatePlayer(Agent):
    def __init__(self, model_name: str, name: str, temperature:float, openai_api_key: str, sleep_time: float) -> None:
        super(DebatePlayer, self).__init__(model_name, name, temperature, sleep_time)
        self.openai_api_key = openai_api_key


class Debate:
    def __init__(self,
            model_name: str='gpt-4o-mini',
            temperature: float=0,
            num_players: int=5,
            save_file_dir: str=None,
            openai_api_key: str=None,
            prompts_path: str=None,
            max_round: int=3,
            sleep_time: float=0
        ) -> None:

        self.model_name = model_name
        self.temperature = temperature
        self.num_players = num_players
        self.save_file_dir = save_file_dir
        self.openai_api_key = openai_api_key
        self.max_round = max_round
        self.sleep_time = sleep_time

        # init save file
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H:%M:%S")
        self.save_file = {
            'start_time': current_time,
            'end_time': '',
            'model_name': model_name,
            'temperature': temperature,
            'num_players': num_players,
            'success': False,
            "src_lng": "",
            "tgt_lng": "",
            'source_segment': '',
            'target_segment': '',
            'accuracy_annotations': '',
            'fluency_annotations': '',
            'term_annotations': '',
            'style_annotations': '',
            'final_annotations': '',
            'players': {},
        }
        prompts = json.load(open(prompts_path))
        self.save_file.update(prompts)
        self.init_prompt()

        if self.save_file['accuracy_annotations'] == "":
            self.create_base()

        self.creat_agents()
        self.init_agents()


    def init_prompt(self):
        def prompt_replace(key):
            self.save_file[key] = self.save_file[key].replace("##src_lng##", self.save_file["src_lng"]).replace("##tgt_lng##", self.save_file["tgt_lng"]).replace("##source_segment##", self.save_file["source_segment"]).replace("##target_segment##", self.save_file["target_segment"])
        prompt_replace("accuracy_agent")
        prompt_replace("fluency_agent")
        prompt_replace("term_agent")
        prompt_replace("style_agent")
        prompt_replace("judge_agent")

    def create_base(self):
        print(f"\n===== Translation Eval Task =====\n")

    def creat_agents(self):
        self.players = [
            DebatePlayer(model_name=self.model_name, name=name, temperature=self.temperature, openai_api_key=self.openai_api_key, sleep_time=self.sleep_time) for name in NAME_LIST
        ]
        self.accuracy_agent = self.players[0]
        self.fluency_agent = self.players[1]
        self.term_agent = self.players[2]
        self.style_agent = self.players[3]
        self.judge = self.players[4]

    def init_agents(self):
        self.accuracy_agent.set_meta_prompt(self.save_file['base_system_prompt'])
        self.fluency_agent.set_meta_prompt(self.save_file['base_system_prompt'])
        self.term_agent.set_meta_prompt(self.save_file['base_system_prompt'])
        self.style_agent.set_meta_prompt(self.save_file['base_system_prompt'])
        self.judge.set_meta_prompt(self.save_file['judge_system_prompt'])
        

        self.accuracy_agent.add_event(accuracy_user_shot[0])
        self.accuracy_agent.add_memory(accuracy_mem_shot[0])
        self.accuracy_agent.add_event(accuracy_user_shot[1])
        self.accuracy_agent.add_memory(accuracy_mem_shot[1])
        self.accuracy_agent.add_event(accuracy_user_shot[2])
        self.accuracy_agent.add_memory(accuracy_mem_shot[2])
        self.accuracy_agent.add_event(nontran_user_shot[0])
        self.accuracy_agent.add_memory(nontran_mem_shot[0])

        self.accuracy_agent.add_event(self.save_file['accuracy_agent'])
        count = 0
        retry = True
        while retry and count < 10:
            try:
                self.accuracy_annotations = self.accuracy_agent.ask()
                retry = False
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
            count += 1

        self.accuracy_agent.add_memory(self.accuracy_annotations)



        self.fluency_agent.add_event(fluency_user_shot[0])
        self.fluency_agent.add_memory(fluency_mem_shot[0])
        self.fluency_agent.add_event(fluency_user_shot[1])
        self.fluency_agent.add_memory(fluency_mem_shot[1])
        self.fluency_agent.add_event(fluency_user_shot[2])
        self.fluency_agent.add_memory(fluency_mem_shot[2])
        self.fluency_agent.add_event(nontran_user_shot[1])
        self.fluency_agent.add_memory(nontran_mem_shot[1])

        self.fluency_agent.add_event(self.save_file['fluency_agent'])
        
        retry = True
        count = 0
        while retry and count < 10:
            try:
                self.fluency_annotations = self.fluency_agent.ask()
                retry = False
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
            count += 1

        self.fluency_agent.add_memory(self.fluency_annotations)


        self.term_agent.add_event(term_user_shot[0])
        self.term_agent.add_memory(term_mem_shot[0])
        self.term_agent.add_event(term_user_shot[1])
        self.term_agent.add_memory(term_mem_shot[1])
        self.term_agent.add_event(term_user_shot[2])
        self.term_agent.add_memory(term_mem_shot[2])
        self.term_agent.add_event(nontran_user_shot[2])
        self.term_agent.add_memory(nontran_mem_shot[2])

        self.term_agent.add_event(self.save_file['term_agent'])
        
        retry = True
        count = 0
        while retry:
            try:
                self.term_annotations = self.term_agent.ask()
                retry = False
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
            count += 1

        self.term_agent.add_memory(self.term_annotations)

        self.style_agent.add_event(style_user_shot[0])
        self.style_agent.add_memory(style_mem_shot[0])
        self.style_agent.add_event(style_user_shot[1])
        self.style_agent.add_memory(style_mem_shot[1])
        self.style_agent.add_event(style_user_shot[2])
        self.style_agent.add_memory(style_mem_shot[2])
        self.style_agent.add_event(nontran_user_shot[3])
        self.style_agent.add_memory(nontran_mem_shot[3])

        self.style_agent.add_event(self.save_file['style_agent'])
        

        retry = True
        count = 0
        while retry:
            try:
                self.style_annotations = self.style_agent.ask()
                retry = False
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
            count += 1

        self.style_agent.add_memory(self.style_annotations)

        self.judge.add_event(self.save_file['judge_agent'].replace('##accuracy_annotations##', self.accuracy_annotations).replace('##fluency_annotations##', self.fluency_annotations).replace('##term_annotations##', self.term_annotations).replace('##style_annotations##', self.style_annotations))
        count = 0
        while True and count < 10:
            try:
                self.judge_ans = self.judge.ask()
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
            
            count += 1
            match = extract_json(self.judge_ans)
            if match:
                try:
                    self.judge_ans = eval(match)
                    self.judge.add_memory(self.judge_ans)
                    break
                except Exception as e:
                    print(f"Error in eval: {e}. Retrying...")

            if count >= 10:
                self.judge_ans = {'annotations': [{'error span': 'all', 'category': 'non-translation', 'severity': 'major', 'is_source_error': 'no'}]}
                self.judge.add_memory(self.judge_ans)

    def round_dct(self, num: int):
        dct = {
            1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth'
        }
        return dct[num]
            
    def save_file_to_json(self, id):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H:%M:%S")
        save_file_path = os.path.join(self.save_file_dir, f"{id}_v1.json")
        
        self.save_file['end_time'] = current_time
        json_str = json.dumps(self.save_file, ensure_ascii=False, indent=4)
        with open(save_file_path, 'w') as f:
            f.write(json_str)
    
    def save_file_to_json_without_annoatation(self, id):
        save_file_path = os.path.join(self.save_file_dir, f"{id}_v1.json")
        json_str = json.dumps("None")
        with open(save_file_path, 'w') as f:
            f.write(json_str)



    def run(self):
        self.save_file.update(self.judge_ans)
        self.save_file['success'] = True

        for player in self.players:
            self.save_file['players'][player.name] = player.memory_lst


def parse_args():
    parser = argparse.ArgumentParser("", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-i", "--input-file", type=str, required=True, help="Input file path")
    parser.add_argument("-o", "--output-dir", type=str, required=True, help="Output file dir")
    parser.add_argument("-lp", "--lang-pair", type=str, required=True, help="Language pair")
    parser.add_argument("-k", "--api-key", type=str, required=True, help="OpenAI api key")
    parser.add_argument("-m", "--model-name", type=str, default="gpt-3.5-turbo", help="Model name")
    parser.add_argument("-t", "--temperature", type=float, default=0, help="Sampling temperature")
    parser.add_argument("-s", "--start-line", type=int, default=1, help="Dataset starting line")

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    openai_api_key = args.api_key

    current_script_path = os.path.abspath(__file__)
    MAD_path = current_script_path.rsplit("/", 2)[0]

    src_lng, tgt_lng = args.lang_pair.split('-')
    src_full = Language.make(language=src_lng).display_name()
    tgt_full = Language.make(language=tgt_lng).display_name()

    config = json.load(open(f"{MAD_path}/code/utils/stage1.json", "r"))

    start_line = args.start_line
    inputs = open(args.input_file, "r").readlines()
    inputs = [l.strip() for l in inputs[start_line-1:]]

    save_file_dir = args.output_dir
    if not os.path.exists(save_file_dir):
            os.mkdir(save_file_dir)

    for id, input in enumerate(tqdm(inputs)):
        try:
            prompts_path = f"{save_file_dir}/{id+start_line-1}-config_v1.json"

            config['source_segment'] = input.split('\t')[0]
            config['target_segment'] = input.split('\t')[1]
            annotated = input.split('\t')[2]
            config['src_lng'] = src_full
            config['tgt_lng'] = tgt_full

            with open(prompts_path, 'w') as file:
                json.dump(config, file, ensure_ascii=False, indent=4)
                
            debate = Debate(save_file_dir=save_file_dir, num_players=4, openai_api_key=openai_api_key, prompts_path=prompts_path, temperature=0, sleep_time=0)
            if annotated == "no":
                debate.save_file_to_json_without_annoatation(id+start_line-1)
            else:
                debate.run()
                debate.save_file_to_json(id+start_line-1)
        except:
            continue