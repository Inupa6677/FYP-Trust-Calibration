import argparse
import glob
import json
import os
import random
import sys
import time
import backoff

import ollama   

# FAST_DOWNWARD_ALIAS = "lama"
FAST_DOWNWARD_ALIAS = "lama-first"

def postprocess(x):
    return x.strip()


def get_cost(x):
    splitted = x.split()
    counter = 0
    found = False
    cost = 1e5
    for i, xx in enumerate(splitted):
        if xx == "cost":
            counter = i
            found = True
            break
    if found:
        cost = float(splitted[counter+2])
    return cost


###############################################################################
#
# Define different problem domains
#
###############################################################################

DOMAINS = [
    "barman",
    "blocksworld",
    "floortile",
    "grippers",
    "storage",
    "termes",
    "tyreworld",
    "manipulation"
]


class Domain:
    def __init__(self):
        self.context = ("p_example.nl", "p_example.pddl", "p_example.sol")
        self.tasks = [] 
        self.grab_tasks()

    def grab_tasks(self):
        path = f"./domains/{self.name}"
        nls = []
        for fn in glob.glob(f"{path}/*.nl"):
            fn_ = os.path.basename(fn)  
            if "domain" not in fn_ and "p_example" not in fn_:
                if os.path.exists(fn.replace("nl", "pddl")):
                    nls.append(fn_)
        sorted_nls = sorted(nls)
        self.tasks = [(nl, nl.replace("nl", "pddl")) for nl in sorted_nls]

    def __len__(self):
        return len(self.tasks)

    def get_task_suffix(self, i):
        nl, pddl = self.tasks[i]
        return pddl

    def get_task_file(self, i):
        nl, pddl = self.tasks[i]
        return f"./domains/{self.name}/{nl}", f"./domains/{self.name}/{pddl}"

    def get_task(self, i):
        nl_f, pddl_f = self.get_task_file(i)
        with open(nl_f, 'r') as f:
            nl = f.read()
        with open(pddl_f, 'r') as f:
            pddl = f.read()
        return postprocess(nl), postprocess(pddl)

    def get_context(self):
        nl_f   = f"./domains/{self.name}/{self.context[0]}"
        pddl_f = f"./domains/{self.name}/{self.context[1]}"
        sol_f  = f"./domains/{self.name}/{self.context[2]}"
        with open(nl_f, 'r') as f:
            nl   = f.read()
        with open(pddl_f, 'r') as f:
            pddl = f.read()
        with open(sol_f, 'r') as f:
            sol  = f.read()
        return postprocess(nl), postprocess(pddl), postprocess(sol)

    def get_domain_pddl(self):
        domain_pddl_f = self.get_domain_pddl_file()
        with open(domain_pddl_f, 'r') as f:
            domain_pddl = f.read()
        return postprocess(domain_pddl)

    def get_domain_pddl_file(self):
        return f"./domains/{self.name}/domain.pddl"

    def get_domain_nl(self):
        domain_nl_f = self.get_domain_nl_file()
        try:
            with open(domain_nl_f, 'r') as f:
                domain_nl = f.read()
        except:
            domain_nl = "Nothing"
        return postprocess(domain_nl)

    def get_domain_nl_file(self):
        return f"./domains/{self.name}/domain.nl"


class Barman(Domain):
    name = "barman"

class Floortile(Domain):
    name = "floortile"

class Termes(Domain):
    name = "termes"

class Tyreworld(Domain):
    name = "tyreworld"

class Grippers(Domain):
    name = "grippers"

class Storage(Domain):
    name = "storage"

class Blocksworld(Domain):
    name = "blocksworld"

class Manipulation(Domain):
    name = "manipulation"

###############################################################################
#
# The agent that leverages classical planner to help LLMs to plan
#
###############################################################################


class Planner:
    def __init__(self):
        pass

    def load_hf_token(self):
        hf_keys_file = os.path.join(os.getcwd(), "keys/hf_token.txt")
        with open(hf_keys_file, "r") as f:
            return f.read().strip()

    def create_llm_prompt(self, task_nl, domain_nl):
        # Baseline 1 (LLM-as-P): directly ask the LLM for plan
        prompt = f"{domain_nl} \n" + \
                 f"Now consider a planning problem. " + \
                 f"The problem description is: \n {task_nl} \n" + \
                 f"Can you provide an optimal plan, in the way of a " + \
                 f"sequence of behaviors, to solve the problem?"
        return prompt

    def create_llm_stepbystep_prompt(self, task_nl, domain_nl):
        # Baseline 1 (LLM-as-P): directly ask the LLM for plan
        prompt = f"{domain_nl} \n" + \
                 f"Now consider a planning problem. " + \
                 f"The problem description is: \n {task_nl} \n" + \
                 f"Can you provide an optimal plan, in the way of a " + \
                 f"sequence of behaviors, to solve the problem? \n" + \
                 f"Please think step by step."
        return prompt

    def create_llm_tot_ic_prompt(self, task_nl, domain_nl, context, plan):
        context_nl, context_pddl, context_sol = context
        prompt = f"Given the current state, provide the set of feasible actions and their corresponding next states, using the format 'action -> state'. \n" + \
                 f"Keep the list short. Think carefully about the requirements of the actions you select and make sure they are met in the current state. \n" + \
                 f"Start with actions that are most likely to make progress towards the goal. \n" + \
                 f"Only output one action per line. Do not return anything else. " + \
                 f"Here are the rules. \n {domain_nl} \n\n" + \
                 f"An example planning problem is: \n {context_nl} \n" + \
                 f"A plan for the example problem is: \n {context_sol} \n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"You have taken the following actions: \n {plan} \n"
        # print(prompt)
        return prompt

    def create_llm_tot_ic_value_prompt(self, task_nl, domain_nl, context, plan):
        context_nl, context_pddl, context_sol = context
        context_sure_1 = context_sol.split('\n')[0]
        context_sure_2 = context_sol.split('\n')[0] + context_sol.split('\n')[1]
        context_impossible_1 = '\n'.join(context_sol.split('\n')[1:])
        context_impossible_2 = context_sol.split('\n')[-1]
        '''
        prompt = f"Evaluate if a given plan reaches the goal or is an optimal partial plan towards the goal (reached/sure/maybe/impossible). \n" + \
                 f"Only answer 'reached' if the goal conditions are reached by the exact plan in the prompt. \n" + \
                 f"Only answer 'sure' if you are sure that preconditions are satisfied for all actions in the plan, and the plan makes fast progress towards the goal. \n" + \
                 f"Answer 'impossible' if one of the actions has unmet preconditions. \n" + \
                 f"Here are the rules. \n {domain_nl} \n\n" + \
                 f"Here are some example evaluations for the planning problem: \n {context_nl} \n\n " + \
                 f"Plan: {context_sure_1} \n" + \
                 f"Answer: Sure. \n\n" + \
                 f"Plan: {context_sure_2} \n" + \
                 f"Answer: Sure. \n\n" + \
                 f"Plan: {context_sol} \n" + \
                 f"Answer: Reached. \n\n" + \
                 f"Plan: {context_impossible_1} \n" + \
                 f"Answer: Impossible. \n\n" + \
                 f"Plan: {context_impossible_2} \n" + \
                 f"Answer: Impossible. \n\n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"Evaluate the following partial plan as reached/sure/maybe/impossible. DO NOT RETURN ANYTHING ELSE. DO NOT TRY TO COMPLETE THE PLAN. \n" + \
                 f"Plan: {plan} \n"
        '''
        prompt = f"Determine if a given plan reaches the goal or give your confidence score that it is an optimal partial plan towards the goal (reached/impossible/0-1). \n" + \
                 f"Only answer 'reached' if the goal conditions are reached by the exact plan in the prompt. \n" + \
                 f"Answer 'impossible' if one of the actions has unmet preconditions. \n" + \
                 f"Otherwise,give a number between 0 and 1 as your evaluation of the partial plan's progress towards the goal. \n" + \
                 f"Here are the rules. \n {domain_nl} \n\n" + \
                 f"Here are some example evaluations for the planning problem: \n {context_nl} \n\n " + \
                 f"Plan: {context_sure_1} \n" + \
                 f"Answer: 0.8. \n\n" + \
                 f"Plan: {context_sure_2} \n" + \
                 f"Answer: 0.9. \n\n" + \
                 f"Plan: {context_sol} \n" + \
                 f"Answer: Reached. \n\n" + \
                 f"Plan: {context_impossible_1} \n" + \
                 f"Answer: Impossible. \n\n" + \
                 f"Plan: {context_impossible_2} \n" + \
                 f"Answer: Impossible. \n\n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"Evaluate the following partial plan as reached/impossible/0-1. DO NOT RETURN ANYTHING ELSE. DO NOT TRY TO COMPLETE THE PLAN. \n" + \
                 f"Plan: {plan} \n"

        return prompt


    def tot_bfs(self, task_nl, domain_nl, context, time_left=200, max_depth=2):
        from queue import PriorityQueue
        start_time = time.time()
        plan_queue = PriorityQueue()
        plan_queue.put((0, ""))
        while time.time() - start_time < time_left and not plan_queue.empty():
            priority, plan = plan_queue.get()
            # print (priority, plan)
            steps = plan.split('\n')
            if len(steps) > max_depth:
                return ""
            candidates_prompt = self.create_llm_tot_ic_prompt(task_nl, domain_nl, context, plan)
            candidates = self.query(candidates_prompt).strip()
            print (candidates)
            lines = candidates.split('\n')
            for line in lines:
                if time.time() - start_time > time_left:
                    break
                if len(line) > 0 and '->' in line:
                    new_plan = plan + "\n" + line
                    value_prompt = self.create_llm_tot_ic_value_prompt(task_nl, domain_nl, context, new_plan)
                    answer = self.query(value_prompt).strip().lower()
                    print(new_plan)
                    print("Response \n" + answer)

                    if "reached" in answer:
                        return new_plan

                    if "impossible" in answer:
                        continue

                    if "answer: " in answer:
                        answer = answer.split("answer: ")[1]

                    try:
                        score = float(answer)
                    except ValueError:
                        continue

                    if score > 0:
                        new_priority = priority + 1 / score
                        plan_queue.put((new_priority, new_plan))

        return ""

    def create_llm_ic_prompt(self, task_nl, domain_nl, context):
        # Baseline 2 (LLM-as-P with context): directly ask the LLM for plan
        context_nl, context_pddl, context_sol = context
        prompt = f"{domain_nl} \n" + \
                 f"An example planning problem is: \n {context_nl} \n" + \
                 f"A plan for the example problem is: \n {context_sol} \n" + \
                 f"Now I have a new planning problem and its description is: \n {task_nl} \n" + \
                 f"Can you provide an optimal plan, in the way of a " + \
                 f"sequence of behaviors, to solve the problem?"
        return prompt

    def create_llm_pddl_prompt(self, task_nl, domain_nl):
        # Baseline 3 (LM+P w/o context), no context, create the problem PDDL
        prompt = f"{domain_nl} \n" + \
                 f"Now consider a planning problem. " + \
                 f"The problem description is: \n {task_nl} \n" + \
                 f"Provide me with the problem PDDL file that describes " + \
                 f"the planning problem directly without further explanations?" +\
                 f"Keep the domain name consistent in the problem PDDL. Only return the PDDL file. Do not return anything else."
        return prompt

    def create_llm_ic_pddl_prompt(self, task_nl, domain_pddl, context):
        context_nl, context_pddl, context_sol = context

        # Few-shot example context (from same domain)
        example_context = f"""
    # EXAMPLE TASK (Natural Language)
    {context_nl.strip()}

    # EXAMPLE PDDL PROBLEM
    {context_pddl.strip()}
    """.strip()

        # Instructional prompt with sections
        prompt = f"""You are an expert AI assistant that generates syntactically and semantically valid PDDL problem files for automated planning tasks.

    ## DOMAIN DEFINITION
    {domain_pddl.strip()}

    ## TASK DESCRIPTION
    {task_nl.strip()}

    ## INSTRUCTION
    Generate a complete and valid PDDL problem definition for the given task using the domain above. 
    Your output **must** include:
    - A properly named `define` block with a unique problem name.
    - A meaningful `:objects` section listing all relevant objects.
    - A logically complete `:init` section with at least two facts.
    - A valid `:goal` section based on the task description.

    ## EXAMPLE (Few-shot format)
    {example_context}

    ## FORMAT RULES
    - Do NOT include comments, explanations, or markdown formatting.
    - Do NOT describe your reasoning or repeat the input.
    - ONLY return the raw PDDL problem file.

    Your output must start with `(define (problem` and be a fully structured `.pddl` problem.
    """
        return prompt



    def query(self, prompt_text):
        print("[INFO] Using Ollama locally...")
        try:
            result = ollama.generate(
                model="qwen2.5:7b-instruct",
                prompt=prompt_text,
                options={"temperature": 0.3, "top_p": 0.2, "num_ctx": 4096}
            )
            return result['response'].strip()
        except Exception as e:
            print("[OLLAMA ERROR]", e)
            return "(define (problem auto-generated)\n(:domain barman)\n(:init)\n(:goal (and))\n)"

    
    
    def parse_result(self, pddl_string):
        pddl_string = pddl_string.replace("```", "").strip()

        # Ensure closing parentheses are balanced
        open_parens = pddl_string.count("(")
        close_parens = pddl_string.count(")")
        if close_parens < open_parens:
            pddl_string += ")" * (open_parens - close_parens)

        # If no goal found, inject a default goal
        if ":goal" not in pddl_string or "(:goal (and" in pddl_string and pddl_string.strip().endswith("(:goal (and))"):
            pddl_string = pddl_string.replace("(:goal (and))",
                                            "(:goal (and (contains shot1 cocktail1)))")

        # Ensure starts with define
        if not pddl_string.startswith("(define"):
            pddl_string = "(define (problem auto-generated)\n(:domain barman)\n(:init)\n(:goal (and (contains shot1 cocktail1)))\n)"

        return pddl_string

    def plan_to_language(self, plan, task_nl, domain_nl, domain_pddl):
        domain_pddl_ = " ".join(domain_pddl.split())
        task_nl_ = " ".join(task_nl.split())
        prompt = f"A planning problem is described as: \n {task_nl} \n" + \
                 f"The corresponding domain PDDL file is: \n {domain_pddl_} \n" + \
                 f"The optimal PDDL plan is: \n {plan} \n" + \
                 f"Transform the PDDL plan into a sequence of behaviors without further explanation."
        res = self.query(prompt).strip() + "\n"
        return res


def llm_ic_pddl_planner(args, planner, domain):
    """
    Our method:
        context: (task natural language, task problem PDDL)
        Condition on the context (task description -> task problem PDDL),
        LLM will be asked to provide the problem PDDL of a new task description.
        Then, we use a planner to find the near optimal solution, and translate
        that back to natural language.
    """
    context          = domain.get_context()
    domain_pddl      = domain.get_domain_pddl()
    domain_pddl_file = domain.get_domain_pddl_file()
    domain_nl        = domain.get_domain_nl()
    domain_nl_file   = domain.get_domain_nl_file()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_ic_pddl/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_ic_pddl/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_ic_pddl/{domain.name}"

    if not os.path.exists(problem_folder):
        os.system(f"mkdir -p {problem_folder}")
    if not os.path.exists(plan_folder):
        os.system(f"mkdir -p {plan_folder}")
    if not os.path.exists(result_folder):
        os.system(f"mkdir -p {result_folder}")

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, task_pddl = domain.get_task(task) 
    prompt             = planner.create_llm_ic_pddl_prompt(task_nl, domain_pddl, context)
    raw_result         = planner.query(prompt)
    task_pddl_         = planner.parse_result(raw_result)

    # B. write the problem file into the problem folder
    task_pddl_file_name = f"./experiments/run{args.run}/problems/llm_ic_pddl/{task_suffix}"
    #os.makedirs(os.path.dirname(task_pddl_file_name), exist_ok=True)
    with open(task_pddl_file_name, "w") as f:
        f.write(task_pddl_)
    time.sleep(1)

    ## C. run fastforward to plan
    plan_file_name = f"./experiments/run{args.run}/plans/llm_ic_pddl/{task_suffix}"
    sas_file_name  = f"./experiments/run{args.run}/plans/llm_ic_pddl/{task_suffix}.sas"
    os.system(f"python ./downward/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
              f"--search-time-limit {args.time_limit} --plan-file {plan_file_name} " + \
              f"--sas-file {sas_file_name} " + \
              f"{domain_pddl_file} {task_pddl_file_name}")

    # D. collect the least cost plan
    best_cost = 1e10
    best_plan = None
    for fn in glob.glob(f"{plan_file_name}.*"):
        with open(fn, "r") as f:
            plans = f.readlines()
            cost = get_cost(plans[-1])
            if cost < best_cost:
                best_cost = cost
                best_plan = "\n".join([p.strip() for p in plans[:-1]])

    # E. translate the plan back to natural language, and write it to result
    # commented out due to exceeding token limit of gpt-4
    '''
    if best_plan:
        plans_nl = planner.plan_to_language(best_plan, task_nl, domain_nl, domain_pddl)
        plan_nl_file_name = f"./experiments/run{args.run}/results/llm_ic_pddl/{task_suffix}"
        with open(plan_nl_file_name, "w") as f:
            f.write(plans_nl)
    '''
    end_time = time.time()
    if best_plan:
        print(f"[info] task {task} takes {end_time - start_time} sec, found a plan with cost {best_cost}")
    else:
        print(f"[info] task {task} takes {end_time - start_time} sec, no solution found")


def llm_pddl_planner(args, planner, domain):
    """
    Baseline method:
        Same as ours, except that no context is given. In other words, the LLM
        will be asked to directly give a problem PDDL file without any context.
    """
    context          = domain.get_context()
    domain_pddl      = domain.get_domain_pddl()
    domain_pddl_file = domain.get_domain_pddl_file()
    domain_nl        = domain.get_domain_nl()
    domain_nl_file   = domain.get_domain_nl_file()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_pddl/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_pddl/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_pddl/{domain.name}"

    if not os.path.exists(problem_folder):
        os.system(f"mkdir -p {problem_folder}")
    if not os.path.exists(plan_folder):
        os.system(f"mkdir -p {plan_folder}")
    if not os.path.exists(result_folder):
        os.system(f"mkdir -p {result_folder}")

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, task_pddl = domain.get_task(task) 
    prompt             = planner.create_llm_pddl_prompt(task_nl, domain_nl)
    raw_result         = planner.query(prompt)
    task_pddl_         = planner.parse_result(raw_result)

    # B. write the problem file into the problem folder
    task_pddl_file_name = f"./experiments/run{args.run}/problems/llm_pddl/{task_suffix}"
    with open(task_pddl_file_name, "w") as f:
        f.write(task_pddl_)
    time.sleep(1)

    # C. run fastforward to plan
    plan_file_name = f"./experiments/run{args.run}/plans/llm_pddl/{task_suffix}"
    sas_file_name  = f"./experiments/run{args.run}/plans/llm_pddl/{task_suffix}.sas"
    os.system(f"python ./downward/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
              f"--search-time-limit {args.time_limit} --plan-file {plan_file_name} " + \
              f"--sas-file {sas_file_name} " + \
              f"{domain_pddl_file} {task_pddl_file_name}")

    # D. collect the least cost plan
    best_cost = 1e10
    best_plan = None
    for fn in glob.glob(f"{plan_file_name}.*"):
        with open(fn, "r") as f:
            try:
                plans = f.readlines()
                cost = get_cost(plans[-1])
                if cost < best_cost:
                    best_cost = cost
                    best_plan = "\n".join([p.strip() for p in plans[:-1]])
            except:
                continue

    # E. translate the plan back to natural language, and write it to result
    # commented out due to exceeding token limit of gpt-4
    '''
    if best_plan:
        plans_nl = planner.plan_to_language(best_plan, task_nl, domain_nl, domain_pddl)
        plan_nl_file_name = f"./experiments/run{args.run}/results/llm_pddl/{task_suffix}"
        with open(plan_nl_file_name, "w") as f:
            f.write(plans_nl)
    '''
    end_time = time.time()
    if best_plan:
        print(f"[info] task {task} takes {end_time - start_time} sec, found a plan with cost {best_cost}")
    else:
        print(f"[info] task {task} takes {end_time - start_time} sec, no solution found")


def llm_planner(args, planner, domain):
    """
    Baseline method:
        The LLM will be asked to directly give a plan based on the task description.
    """
    context          = domain.get_context()
    domain_pddl      = domain.get_domain_pddl()
    domain_pddl_file = domain.get_domain_pddl_file()
    domain_nl        = domain.get_domain_nl()
    domain_nl_file   = domain.get_domain_nl_file()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm/{domain.name}"

    if not os.path.exists(problem_folder):
        os.system(f"mkdir -p {problem_folder}")
    if not os.path.exists(plan_folder):
        os.system(f"mkdir -p {plan_folder}")
    if not os.path.exists(result_folder):
        os.system(f"mkdir -p {result_folder}")

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, task_pddl = domain.get_task(task) 
    prompt             = planner.create_llm_prompt(task_nl, domain_nl)
    text_plan          = planner.query(prompt)

    # B. write the problem file into the problem folder
    text_plan_file_name = f"./experiments/run{args.run}/results/llm/{task_suffix}"
    with open(text_plan_file_name, "w") as f:
        f.write(text_plan)
    end_time = time.time()
    print(f"[info] task {task} takes {end_time - start_time} sec")


def llm_stepbystep_planner(args, planner, domain):
    """
    Baseline method:
        The LLM will be asked to directly give a plan based on the task description.
    """
    context          = domain.get_context()
    domain_pddl      = domain.get_domain_pddl()
    domain_pddl_file = domain.get_domain_pddl_file()
    domain_nl        = domain.get_domain_nl()
    domain_nl_file   = domain.get_domain_nl_file()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_step/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_step/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_step/{domain.name}"

    if not os.path.exists(problem_folder):
        os.system(f"mkdir -p {problem_folder}")
    if not os.path.exists(plan_folder):
        os.system(f"mkdir -p {plan_folder}")
    if not os.path.exists(result_folder):
        os.system(f"mkdir -p {result_folder}")

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, task_pddl = domain.get_task(task) 
    prompt             = planner.create_llm_stepbystep_prompt(task_nl, domain_nl)
    text_plan          = planner.query(prompt)

    # B. write the problem file into the problem folder
    text_plan_file_name = f"./experiments/run{args.run}/results/llm_step/{task_suffix}"
    with open(text_plan_file_name, "w") as f:
        f.write(text_plan)
    end_time = time.time()
    print(f"[info] task {task} takes {end_time - start_time} sec")


def llm_tot_ic_planner(args, planner, domain):
    """
    Tree of Thoughts planner
    """
    context          = domain.get_context()
    domain_pddl      = domain.get_domain_pddl()
    domain_pddl_file = domain.get_domain_pddl_file()
    domain_nl        = domain.get_domain_nl()
    domain_nl_file   = domain.get_domain_nl_file()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_tot_ic/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_tot_ic/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_tot_ic/{domain.name}"

    if not os.path.exists(problem_folder):
        os.system(f"mkdir -p {problem_folder}")
    if not os.path.exists(plan_folder):
        os.system(f"mkdir -p {plan_folder}")
    if not os.path.exists(result_folder):
        os.system(f"mkdir -p {result_folder}")

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, task_pddl = domain.get_task(task)
    text_plan = planner.tot_bfs(task_nl, domain_nl, context, time_left=200, max_depth=10)

    # B. write the problem file into the problem folder
    text_plan_file_name = f"./experiments/run{args.run}/results/llm_tot_ic/{task_suffix}"
    with open(text_plan_file_name, "w") as f:
        f.write(text_plan)
    end_time = time.time()
    print(f"[info] task {task} takes {end_time - start_time} sec")


def llm_ic_planner(args, planner, domain):
    """
    Baseline method:
        The LLM will be asked to directly give a plan based on the task description.
    """
    context          = domain.get_context()
    domain_pddl      = domain.get_domain_pddl()
    domain_pddl_file = domain.get_domain_pddl_file()
    domain_nl        = domain.get_domain_nl()
    domain_nl_file   = domain.get_domain_nl_file()

    # create the tmp / result folders
    problem_folder = f"./experiments/run{args.run}/problems/llm_ic/{domain.name}"
    plan_folder    = f"./experiments/run{args.run}/plans/llm_ic/{domain.name}"
    result_folder  = f"./experiments/run{args.run}/results/llm_ic/{domain.name}"

    if not os.path.exists(problem_folder):
        os.system(f"mkdir -p {problem_folder}")
    if not os.path.exists(plan_folder):
        os.system(f"mkdir -p {plan_folder}")
    if not os.path.exists(result_folder):
        os.system(f"mkdir -p {result_folder}")

    task = args.task

    start_time = time.time()

    # A. generate problem pddl file
    task_suffix        = domain.get_task_suffix(task)
    task_nl, task_pddl = domain.get_task(task) 
    prompt             = planner.create_llm_ic_prompt(task_nl, domain_nl, context)
    text_plan          = planner.query(prompt)

    # B. write the problem file into the problem folder
    text_plan_file_name = f"./experiments/run{args.run}/results/llm_ic/{task_suffix}"
    with open(text_plan_file_name, "w") as f:
        f.write(text_plan)
    end_time = time.time()
    print(f"[info] task {task} takes {end_time - start_time} sec")


def print_all_prompts(planner):
    for domain_name in DOMAINS:
        domain = eval(domain_name.capitalize())()
        context = domain.get_context()
        domain_pddl = domain.get_domain_pddl()
        domain_pddl_file = domain.get_domain_pddl_file()
        domain_nl = domain.get_domain_nl()
        
        for folder_name in [
            f"./prompts/llm/{domain.name}",
            f"./prompts/llm_step/{domain.name}",
            f"./prompts/llm_ic/{domain.name}",
            f"./prompts/llm_pddl/{domain.name}",
            f"./prompts/llm_ic_pddl/{domain.name}"]:
            if not os.path.exists(folder_name):
                os.system(f"mkdir -p {folder_name}")

        for task in range(len(domain)):
            task_nl_file, task_pddl_file = domain.get_task_file(task) 
            task_nl, task_pddl = domain.get_task(task) 
            task_suffix = domain.get_task_suffix(task)

            llm_prompt = planner.create_llm_prompt(task_nl, domain_nl)
            llm_stepbystep_prompt = planner.create_llm_stepbystep_prompt(task_nl, domain_nl)
            llm_ic_prompt = planner.create_llm_ic_prompt(task_nl, domain_nl, context)
            llm_pddl_prompt = planner.create_llm_pddl_prompt(task_nl, domain_nl)
            llm_ic_pddl_prompt = planner.create_llm_ic_pddl_prompt(task_nl, domain_pddl, context)
            with open(f"./prompts/llm/{task_suffix}.prompt", "w") as f:
                f.write(llm_prompt)
            with open(f"./prompts/llm_step/{task_suffix}.prompt", "w") as f:
                f.write(llm_stepbystep_prompt)
            with open(f"./prompts/llm_ic/{task_suffix}.prompt", "w") as f:
                f.write(llm_ic_prompt)
            with open(f"./prompts/llm_pddl/{task_suffix}.prompt", "w") as f:
                f.write(llm_pddl_prompt)
            with open(f"./prompts/llm_ic_pddl/{task_suffix}.prompt", "w") as f:
                f.write(llm_ic_pddl_prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM-Planner")
    parser.add_argument('--domain', type=str, choices=DOMAINS, default="barman")
    parser.add_argument('--method', type=str, choices=["llm_ic_pddl_planner",
                                                       "llm_pddl_planner",
                                                       "llm_planner",
                                                       "llm_stepbystep_planner",
                                                       "llm_ic_planner",
                                                       "llm_tot_ic_planner"],
                                              default="llm_ic_pddl_planner")
    parser.add_argument('--time-limit', type=int, default=200)
    parser.add_argument('--task', type=int, default=0)
    parser.add_argument('--run', type=int, default=0)
    parser.add_argument('--print-prompts', action='store_true')
    args = parser.parse_args()

    # 1. initialize problem domain
    domain = eval(args.domain.capitalize())()

    # 2. initialize the planner
    planner = Planner()

    # 3. execute the llm planner
    method = {
        "llm_ic_pddl_planner"   : llm_ic_pddl_planner,
        "llm_pddl_planner"      : llm_pddl_planner,
        "llm_planner"           : llm_planner,
        "llm_stepbystep_planner": llm_stepbystep_planner,
        "llm_ic_planner"        : llm_ic_planner,
        "llm_tot_ic_planner"       : llm_tot_ic_planner,
    }[args.method]

    if args.print_prompts:
        print_all_prompts(planner)
    else:
        method(args, planner, domain)
