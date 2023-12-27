from pathlib import Path
from typing import Any, Dict, List, Union

import whisper

TranscribeResult = Dict[str, Union[str, List[Any]]]


class Transcriber:
    def __init__(self, model: str = "medium") -> None:
        self.model = self._load_model(model)

    def _load_model(self, model_name: str) -> whisper.Whisper:
        return whisper.load_model(model_name)

    def transcribe(
        self,
        input_file: Path,
        task: str = "transcribe",
        language: Union[str, None] = None,
        initial_prompt: Union[str, None] = None,
        word_timestamps: bool = False,
    ) -> Any:
        args = {
            "audio": str(input_file),
            "verbose": False,  # only display progress bar
            "condition_on_previous_text": True,
            "language": language,
            "task": task,
            "initial_prompt": initial_prompt,
            "word_timestamps": word_timestamps,
        }

        return self.model.transcribe(**args)
