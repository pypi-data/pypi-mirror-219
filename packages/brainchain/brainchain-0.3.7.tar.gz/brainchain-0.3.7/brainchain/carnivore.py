import json, os, requests
from urllib.parse import quote
import promptlayer
from promptlayer import openai
from modal import Image, Stub, web_endpoint, Secret

try:
    stub = Stub(f"carnivore-client-{os.environ['USER']}")
except:
    stub = Stub(f"carnivore-client-guest")

class Carnivore:
    def __init__(self, env: str = "prod"):
        if env == "prod":
            self.service_url = "https://brainchain--carnivore.modal.run/"
        elif env == "dev":
            self.service_url = "https://brainchain--carnivore-dev.modal.run/"

    def scrape(self, link, tags, tag_delimiter=" "):
        payload = {"base_url": link, "tags": tags, "tag_delimiter": tag_delimiter}
        response = requests.post(
            self.service_url, params=payload, headers={"accept": "application/json"}
        )
        return response.json()

    def content(self, link, tags="p", tag_delimiter=" ", return_string=True):
        extracted = []
        print("Processing: ", end="")
        for tag in tags.split(tag_delimiter):
            print(f"[<{tag}>...</{tag}>, ...], ", end="\n")
            content = self.scrape(link, tag)["content"]
            if tag in content:
                for item in content[tag]:
                    print(f"{item}")
                    extracted.append(item)
        if return_string:
            return ''.join(extracted)
        else:
            extracted

    def condense(self, page):
        content = ''.join(self.content(page, return_string=True))
        system_prompt = "Condense the following information taken from a page scrape. Do not omit any details. Just synthesize the information appropriately."
        agg = []
        text_splitter = TokenTextSplitter(
            chunk_size=10000, chunk_overlap=0
        )
        chunks = text_splitter.split_text(content)

        for text in chunks:
            print("TEXT! ", text)
            agg.append(gpt(system_prompt="Summarize this text, retaining all important information", user_prompt=text,history=[])[-1]["content"])
            
        return gpt(system_prompt="Coaslesce all this information into a nice summary that preserves all useful facts.", user_prompt=" ".join(agg), history=[])[-1]["content"]

    def analyze_content(self, link, tags="*", tag_delimiter=" "):
        contents_metadata = {}
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo-16k-0613")
        content_store = []
        running_length = 0
        extracted = []

        loader = UnstructuredURLLoader([link])
        d = loader.load()
        print(d)
        for i, doc in enumerate(d):
            print(f"running_length: {running_length}")
            tokens_in_doc = len(enc.encode(doc.page_content))
            if tokens_in_doc + running_length <= 16384-50:
                content_store.append(doc.page_content)
                print(content_store[-1])
                running_length += tokens_in_doc
            else:
                for text_item in split_text(content):
                    extracted_text = gpt(f"{prompt}: {text_item}", model="gpt-3.5-turbo-16k-0613", history=[])
                    print(extracted_text)
                    extracted.append(extracted_text)

        content = ' ]|[ '.join(content_store)
        if len(content) <= 16050:
                # Call the ChatCompletion API to fact-check
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are unstructured web soup content summarizer. Clean up and extract all relevant info from this unstructured mess.",
                        },
                        {"role": "user", "content": content},
                    ],
                )
                return chat
        else:
            agg = []
            for text in split_text(content, chunk_size=8500, chunk_overlap=128):
                agg.append(gpt(system_prompt="Summarize this text, retaining all important information", user_prompt=text,history=[]))
            
        return gpt(system_prompt="Coaslesce all this information into a nice summary that preserves all useful facts.", user_prompt=" ".join(agg), history=[])[-1]
                
    def links(self, link):
        page = self.scrape(link, "a")
        links = page["external_links"] + page["links"]
        return list(filter(lambda x: x.startswith("http"), links))

    def slurp(self, link):
        return self.scrape(link, "*")

def gpt(
    user_prompt=None,
    system_prompt="You're an AI research assistant, here to help.",
    model="gpt-3.5-turbo-16k-0613",
    temperature=1.0,
    frequency_penalty=1.0,
    presence_penalty=1.0,
    history=[],
    max_tokens=2048,
    n=1,
):
    if len(history) == 0:
        history.append({"role": "system", "content": system_prompt})
    else:
        history.append({"role": "user", "content": prompt})
    
    try:
        import promptlayer
        from promptlayer import openai
        promptlayer.api_key = os.environ["PROMPTLAYER_API_KEY"]
        openai.api_key = os.environ["OPENAI_API_KEY"]
        response = openai.ChatCompletion.create(
        model=model, messages=history, n=n, max_tokens=max_tokens
        )
        history.append(
            {
                "role": "assistant",
                "content": " ".join(
                    [msg["message"]["content"] for msg in response["choices"]]
                ),
            }
        )
        return history
    except:
        return []

