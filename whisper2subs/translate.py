import deepl

from whisper2subs.transcribe import TranscribeResult


def deepl_translate(
    transcribed_audio: TranscribeResult, output_language: str, api_key: str
) -> TranscribeResult:
    dialogues = [x["text"] for x in transcribed_audio["segments"]]  # type: ignore

    try:
        translator = deepl.Translator(api_key, send_platform_info=False)
        result = translator.translate_text(
            dialogues, source_lang="EN", target_lang=output_language.upper()
        )
    except deepl.DeepLException as err:
        raise err

    if not isinstance(result, list):
        result = [result]
    for index, line in enumerate(result, 0):
        transcribed_audio["segments"][index]["text"] = line.text  # type: ignore
    return transcribed_audio
