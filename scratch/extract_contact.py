from html.parser import HTMLParser

class ContactExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_target = False
        self.target_html = []
        self.depth = 0
        self.saved_html = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')
        if 'contact-form' in cls:
            self.in_target = True
            self.depth = 0
            self.target_html = []
            print(f"Found contact form container start: tag={tag}, class={cls}")
        
        if self.in_target:
            self.depth += 1
            attr_str = " ".join([f'{k}="{v}"' for k, v in attrs])
            self.target_html.append(f"<{tag} {attr_str}>" if attr_str else f"<{tag}>")

    def handle_endtag(self, tag):
        if self.in_target:
            self.target_html.append(f"</{tag}>")
            self.depth -= 1
            if self.depth == 0:
                self.in_target = False
                self.saved_html = "".join(self.target_html)
                print("Finished contact extraction.")

    def handle_data(self, data):
        if self.in_target:
            self.target_html.append(data)

with open("pages/contact.html", "r", encoding="utf-8") as f:
    content = f.read()

parser = ContactExtractor()
parser.feed(content)

if parser.saved_html:
    with open("C:/Users/ravik/.gemini/antigravity-ide/brain/70a26aa0-84b9-41a4-bb6e-06a64a180c35/scratch/extracted_contact_form.html", "w", encoding="utf-8") as out:
        out.write(parser.saved_html)
    print("Contact form section written successfully.")
else:
    print("Could not find contact form.")
