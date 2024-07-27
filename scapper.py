import requests
import base64
import sys
def scrape_leetcode(question_number):
    sys.stdout.reconfigure(encoding='utf-8')
    repo_owner = "doocs"
    repo_name = "leetcode"
    readme_path = "README_EN.md"
    question_number="0001"

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/solution/{readme_path}"
    response = requests.get(api_url)

    if response.status_code == 200:
        readme_content = response.json()["content"]
        decoded_content = base64.b64decode(readme_content).decode("utf-8")
        #print(decoded_content)
    else:
        print("Failed to retrieve README file")
    lines = decoded_content.split("\n")
    formatted_lines = []
    for line in lines:
      formatted_lines.append(line)
    with open("leetcode.txt", "w",encoding="utf-8") as f:
            f.writelines(formatted_lines)
    import re
    def extract_info_from_file(question_number, file_path):
    with open(file_path, 'r',encoding="utf-8") as f:
      for line in f:
        if len(line)>70:
          if(line[3:7]==question_number):
            return line
    return None
    file_path=r'C:\Users\CHANAKYA\Documents\iitisoc\leetcode.txt'
    line=extract_info_from_file(question_number,file_path)
    columns = line.strip().split("|")
    solution_link = columns[2].strip().split("]")[1].split("(")[1].split(")")[0]
    solution_link_str = solution_link
    link_contents=solution_link_str.strip().split("/")
    range = link_contents[2]
    location= link_contents[3]
    repo_owner = "doocs"
    repo_name = "leetcode"
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/solution/{range}/{location}/README_EN.md"
    response = requests.get(url)
    #print(response.text)
    with open('solution_readme.txt', 'w',encoding="utf-8") as f:
        f.write(response.text)
    with open('solution_readme.txt', 'r',encoding="utf-8") as f:
        content = response.text

    description = re.search(r'## Description(.*?)##', content, re.DOTALL).group(1).strip()
    description = re.sub(r'<!-- description:start -->\n\n', '', description)
    description = re.sub(r'\n\n<!-- description:end -->', '', description)
    description = re.sub(r'<p>', '', description)
    description = re.sub(r'</p>', '', description)
    description = re.sub(r'<strong class="example">', '', description)
    description = re.sub(r'</strong>', '', description)
    description = re.sub(r'<code>', '', description)
    description = re.sub(r'</code>', '', description)
    description = re.sub(r'<li>', '\n- ', description)
    description = re.sub(r'<ul>', '', description)
    description = re.sub(r'</ul>', '', description)

    description = re.sub(r'<strong>', '', description)
    description = re.sub(r'</strong>', '', description)
    description = re.sub(r'&quot;', '"', description)
    description = re.sub(r'&#39;', "'", description)
    description = re.sub(r'<sup>', '^', description)
    description = re.sub(r'</sup>', '', description)
    description = re.sub(r'<em>', '', description)
    description = re.sub(r'</em>', '', description)
    description = re.sub(r'&nbsp;', ' ', description)
    description = re.sub(r'<pre>', '', description)
    description = re.sub(r'</pre>', '', description)
    description = re.sub(r'<li>', '- ', description)
    description = re.sub(r'</li>', '', description)
    description = re.sub(r'&lt;', '<', description)
    description=description.strip()
    description = re.sub(r'  ', ' ', description)
    return description

import requests
from bs4 import BeautifulSoup
import re
def scrapecf(input_str):
    def separate_numbers_and_letter(s):
        # Use regular expression to find numbers and letters
        match = re.match(r"(\d+)([a-zA-Z])", s)
        if match:
            numbers = match.group(1)
            letter = match.group(2)
            return numbers, letter
        else:
            raise ValueError("The input string does not match the expected format.")

    numbers, letter = separate_numbers_and_letter(input_str)
    def scrape(url):
      vocab = {"<p>":" ", "</p>":" ", "$$$":'', "\\leq":" <= ", "\\le":" <= ", r'\xa0':" ", "\\cdot":" x ", "\\ldots":"...","\\dots":"...",
            '</span>':' ' , '<span class="tex-font-style-it">':' ', '<span class="tex-font-style-bf">':' ','<span class="tex-font-style-tt">':' ' ,
            '\\ne': '≠', r'\xa0':'', '\\oplus':' xor ', '\\,':'', '&lt':'<', '&gt':'>', "^\\dagger":'', '\\ge':' >= ', '\\operatorname':'',
            "\'":''}

      r = requests.get(url)

      # Parsing the HTML
      soup = BeautifulSoup(r.content, 'html.parser')

      s = soup.find('div', class_='entry-content')
      ques = soup.find('div',{"class":"problem-statement"}).get_text()
      tags = soup.find_all('span', {"class": "tag-box"})
      # print(tags, type(tags))
      tag_lst=[]
      for tag in tags:
        lst = tag.get_text().split('\n')
        tag_lst.append(lst[1].strip())

      Rating = list(map(lambda x: x[1:].isnumeric(), tag_lst))
      Rating = int(list(tag_lst[i] for i in range(len(tag_lst)) if Rating[i])[0][1:])
      # print(Rating)
      # Rating  = int(input("Enter your current rating:"))
    #   sim = []
    #   for Tag in tag_lst:
    #     url = f"https://codeforces.com/problemset?tags={Tag},{Rating+100}-{Rating+200}"
    #     r = requests.get(url)
    #     soup = bs(r.content, 'html.parser')
    #     elems = soup.find_all('div',style="float: left;")
    #     i = 0
    #     for elem in elems:
    #       anchor_tag = elem.find('a')
    #       href_value = anchor_tag.get('href')
    #       sim.append(f"https://codeforces.com{href_value}")
    #       i += 1
    #       if i == 5:
    #         break
      
    #   ques = ques.split("Note")[0]
    #   ques = "".join(map(str, ques))
    #   ques = ques.split("standard output")[1]
    #   ques = "".join(map(str, ques))
    #   ques = ques.split("ExamplesInput")[0]
    #   ques = "".join(map(str, ques))
    #   ques = ques.split("ExampleInput")[0]

      for word in vocab:
        lst = []
        for i in ques.split(word):
          if i!='':
            lst.append(i)
        # lst
        ques = vocab[word].join(map(str, lst))
      return ques, tag_lst, Rating

def scrapeL(question_number):
  def get_leetcode_question(question_number):
      url = "https://leetcode.com/graphql"
      query = """
          query getQuestion($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                  content
                  stats
                  codeDefinition
                  sampleTestCase
              }
          }
      """
      # First, we need to get the title slug of the question
      title_slug_url = "https://leetcode.com/api/problems/all/"
      response = requests.get(title_slug_url)
      data = response.json()

      title_slug = None
      for question in data["stat_status_pairs"]:
          if question["stat"]["question_id"] == question_number:
              title_slug = question["stat"]["question__title_slug"]
              break

      if title_slug is None:
          return None

      # Now we can fetch the question content
      response = requests.post(url, json={"query": query, "variables": {"titleSlug": title_slug}})
      data = response.json()

      return data["data"]["question"]

  question = get_leetcode_question(question_number)
  print(question)
  import json
  import re

  def convert_to_readable(text):
      # Remove any leading or trailing whitespace
      text = text.strip()

      # Use regular expressions to extract the problem statement, examples, and constraints
      problem_statement = re.search(r'{"content": "(.*?)",', text, re.DOTALL)
      examples = re.findall(r'"example": "(.*?)",', text, re.DOTALL)
      constraints = re.search(r'"Constraints": "(.*?)",', text, re.DOTALL)

      # Extract the problem statement
      problem_statement = problem_statement.group(1) if problem_statement else ""
      problem_statement = problem_statement.replace("\\n", "\n")
      problem_statement = problem_statement.replace("\\t", "\t")

      # Extract the examples
      examples = [example.replace("\\n", "\n").replace("\\t", "\t") for example in examples]

      # Extract the constraints
      constraints = constraints.group(1) if constraints else ""
      constraints = constraints.replace("\\n", "\n")
      constraints = constraints.replace("\\t", "\t")

      # Use regular expressions to extract the input and output from the examples
      example_inputs = []
      example_outputs = []
      for example in examples:
          input_match = re.search(r"Input: (.*?)\n", example)
          output_match = re.search(r"Output: (.*?)\n", example)
          if input_match and output_match:
              example_inputs.append(input_match.group(1))
              example_outputs.append(output_match.group(1))

      # Create a dictionary to store the extracted data
      data = {
          "problem_statement": problem_statement,
          "examples": list(zip(example_inputs, example_outputs)),
          "constraints": constraints
      }

      # Convert the dictionary to a readable English format
      readable_text = ""
      readable_text += "Problem Statement:\n"
      readable_text += data["problem_statement"] + "\n\n"
      readable_text += "Examples:\n"
      for i, (example_input, example_output) in enumerate(data["examples"]):
          readable_text += f"Example {i+1}:\n"
          readable_text += f"Input: {example_input}\n"
          readable_text += f"Output: {example_output}\n\n"
      readable_text += "Constraints:\n"
      readable_text += data["constraints"]

      return readable_text
  return output  

    