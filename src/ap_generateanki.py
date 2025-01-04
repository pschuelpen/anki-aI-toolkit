##########################################################
# Anki AI Toolkit - Create Anki Cards from Q&A Pairs
# (c)pschuelpen.tec
#
# www.tec.pschuelpen.com/anki_ai_toolkit/
#
# Generate Anki Deck
#
# Optimized for:
# Python3 - Running on any computer - Docker
#
##########################################################
# Import Libraries
##########################################################


import genanki
import random
import html


#####################################
#            Class Def. 
#####################################


class AnkiDeckGenerator:
    def __init__(self, deck_name):
        """
        Initialize the AnkiDeckGenerator with a deck name.
        """
        self.deck_name = deck_name
        self.deck_id = random.randrange(1 << 30, 1 << 31)
        self.model_id = random.randrange(1 << 30, 1 << 31)
        self.model = genanki.Model(
            self.model_id,
            f"{deck_name} Model",
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ],
        )
        self.deck = genanki.Deck(
            self.deck_id,
            self.deck_name,
        )
        self.media_files = []
    
    def set_name(self, deck_name):
        self.deck_name = deck_name

    def add_card(self, question, answer, media_file=None):
        """
        Add a card to the deck.
        :param question: Front side of the card.
        :param answer: Back side of the card.
        :param media_file: Optional, path to an image or audio file to include.
        """
        sanitized_question = html.escape(question)
        sanitized_answer = html.escape(answer)
        note = genanki.Note(
            model=self.model,
            fields=[sanitized_question, sanitized_answer],
        )
        self.deck.add_note(note)
        if media_file:
            self.media_files.append(media_file)

    def generate_package(self, output_file):
        """
        Generate an Anki package (.apkg).
        :param output_file: Path to save the .apkg file.
        """
        package = genanki.Package(self.deck)
        package.media_files = self.media_files
        package.write_to_file(output_file)
        print(f"Anki package created: {output_file}")



#####################################
#          Example Usage 
#####################################

if __name__ == "__main__":
    generator = AnkiDeckGenerator("Geography Facts")
    generator.add_card("What is the capital of France?", "Paris")
    generator.add_card("What is the highest mountain in the world?", "Mount Everest", "mount_everest.jpg")
    generator.generate_package("geography_facts.apkg")
