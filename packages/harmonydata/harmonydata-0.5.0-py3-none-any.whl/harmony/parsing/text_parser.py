import re
import traceback
from typing import List

from langdetect import detect

from harmony.parsing.text_extraction.ensemble_named_entity_recogniser import extract_questions
from harmony.schemas.enums.file_types import FileType
from harmony.schemas.requests.text import RawFile, Instrument, Question


def convert_text_to_instruments(file: RawFile) -> List[Instrument]:
    if file.file_type == FileType.txt:
        page_text = file.content
    else:
        page_text = file.text_content

    if file.file_id is None:
        file.file_id = str(hash(page_text))

    try:
        language = detect(page_text)
    except:
        language = "en"
        print(f"Error identifying language in {file.file_type} file")
        traceback.print_exc()
        traceback.print_stack()

    # TODO: replace this with smarter logic
    if file.file_type == FileType.txt:
        questions = []
        for line in page_text.split("\n"):
            if line.strip() == "":
                continue
            line = re.sub(r'\s+', ' ', line)
            question = Question(question_no=len(questions) + 1, question_intro="", question_text=line.strip(),
                                options=[])
            questions.append(question)
    else:
        questions, _, _ = extract_questions(page_text, file.tables)

    instrument = Instrument(
        file_id=file.file_id,
        instrument_id=file.file_id + "_0",
        instrument_name=file.file_name,
        file_name=file.file_name,
        file_type=file.file_type,
        file_section="",
        language=language,
        questions=questions
    )

    instruments = [instrument]

    return instruments
