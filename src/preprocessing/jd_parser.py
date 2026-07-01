from docx import Document
import pickle
import re
from pathlib import Path


class JDParser:

    def __init__(self, jd_path):

        self.jd_path = jd_path

        self.text = self._read_doc()

    def _read_doc(self):

        doc = Document(self.jd_path)

        text = []

        for para in doc.paragraphs:

            if para.text.strip():

                text.append(
                    para.text.strip()
                )

        return "\n".join(text)

    def extract_experience(self):

        patterns = [

            r"(\d+)\+?\s*years",

            r"minimum\s*(\d+)\s*years",

            r"(\d+)\s*-\s*(\d+)\s*years"

        ]

        text = self.text.lower()

        for pattern in patterns:

            matches = re.findall(
                pattern,
                text
            )

            if matches:

                if isinstance(
                        matches[0], tuple):

                    return int(
                        matches[0][0]
                    )

                return int(
                    matches[0]
                )

        return 0

    def load_skill_vocabulary(self):

        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        skill_path = (
            project_root /
            "data" /
            "processed" /
            "skill_vocabulary.pkl"
        )

        with open(
                skill_path,
                "rb"
        ) as f:

            vocabulary = pickle.load(f)

        return vocabulary

    def extract_skills(self):

        vocabulary = (
            self.load_skill_vocabulary()
        )

        jd_text = self.text.lower()

        found_skills = []

        for skill in vocabulary:

            if skill in jd_text:

                found_skills.append(
                    skill
                )

        return sorted(
            list(set(found_skills))
        )

    def extract_negative_keywords(self):

        text = self.text.lower()

        negative_phrases = [

            "not a fit",

            "not suitable",

            "do not want",

            "must not",

            "should not",

            "will not move forward",

            "not interested in",

            "exclude",

            "disqualify"

        ]

        vocabulary = (
            self.load_skill_vocabulary()
        )

        negative_keywords = []

        sentences = re.split(
            r"[.\n]",
            text
        )

        for sentence in sentences:

            if any(
                    phrase in sentence
                    for phrase in
                    negative_phrases
            ):

                for skill in vocabulary:

                    if skill in sentence:

                        negative_keywords.append(
                            skill
                        )

        return sorted(
            list(
                set(
                    negative_keywords
                )
            )
        )

    def parse(self):

        skills = self.extract_skills()

        return {

            "required_skills":
                skills,

            "mandatory_skills":
                skills,

            "negative_keywords":
                self.extract_negative_keywords(),

            "min_experience":
                self.extract_experience(),

            "full_text":
                self.text
        }