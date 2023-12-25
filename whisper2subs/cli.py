from pathlib import Path

import click
import deepl
from whisper import available_models

from whisper2subs import __version__
from whisper2subs.export import export_subtitles
from whisper2subs.transcribe import Transcriber, TranscribeResult
from whisper2subs.translate import deepl_translate


def _check_deepl_apikey(ctx: click.Context, param: click.Option, value: str) -> str:
    if ctx.params["translate_to"] and not value:
        if ctx.params["translate_to"].lower() == "en":
            return value
        click.echo(
            "To perform translations, provide a DeepL API key using the option "
            "'--deepl-apikey' or the environment variable 'DEEPL_APIKEY'.",
            err=True,
        )
        ctx.exit()
    return value


def _translate(
    translate_to: str,
    deepl_apikey: str,
    transcribed_audio: TranscribeResult,
    context: str,
) -> TranscribeResult:
    click.echo(f"Translating transcribed audio to {translate_to}")
    try:
        translated_audio = deepl_translate(
            transcribed_audio, translate_to, deepl_apikey, context
        )
    except deepl.exceptions.AuthorizationException as err:
        raise click.exceptions.ClickException(
            "Authentication failure, check the API key of DeepL."
        ) from err
    except deepl.exceptions.QuotaExceededException as err:
        raise click.exceptions.ClickException(
            "You have exceeded your DeepL API quota."
        ) from err
    return translated_audio


@click.command(context_settings={"show_default": True})
@click.argument(
    "input_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.argument(
    "output_directory",
    type=click.Path(exists=True, file_okay=False, writable=True, path_type=Path),
)
@click.option(
    "-m",
    "--whisper-model",
    type=click.Choice(available_models()),
    default="medium",
    help="Model to generate the transcript.",
)
@click.option(
    "-l",
    "--language",
    help="""Main language of the input file. If not specified Whisper will try to
    detect it.""",
)
@click.option(
    "-t",
    "--translate-to",
    default="",
    help="Language into which the transcript is translated. ISO-639-1 format.",
)
@click.option(
    "--deepl-apikey",
    envvar="DEEPL_APIKEY",
    callback=_check_deepl_apikey,
    help="API key from DeepL to perform translations.",
)
@click.option(
    "--output-format",
    type=click.Choice(["all", "txt", "vtt", "srt", "tsv", "json"]),
    default="all",
    help="Format in which the transcript will be exported.",
)
@click.option("--initial-prompt", help="An initial prompt to provide context.")
@click.version_option(__version__)
def whisper2subs(
    input_file: Path,
    output_directory: Path,
    whisper_model: str,
    language: str,
    translate_to: str,
    deepl_apikey: str,
    output_format: str,
    initial_prompt: str,
) -> None:
    """Transcribes audio using Whisper and translates it using DeepL.

    Examples:\n
        Transcribe a file:\n
        $ whisper2subs input.mp4 subs/

        Transcribe an input file using large-v2 model and translate it to Spanish:\n
        $ whisper2subs input.mp4 -l japanese -t es -m large-v2 input.mp4 ./

    Notes:\n
        - The models are stored in ~/.cache/whisper
    """
    task = "translate" if translate_to else "transcribe"
    translate_to = translate_to.upper()

    click.echo(f"Loading model: {whisper_model}. This will take some time...")
    transcriber = Transcriber(whisper_model)

    if translate_to == "EN":
        click.echo("The English translation is done with Whisper instead of DeepL.")

    click.echo(f"Performing {task} task.")
    transcribed_audio: TranscribeResult = transcriber.transcribe(
        input_file,
        task,
        language,
        initial_prompt,
    )

    click.echo(f"Exporting files with audio transcription to {output_directory}.")
    export_subtitles(
        output_directory.joinpath(input_file.name), transcribed_audio, output_format
    )

    if translate_to and deepl_apikey and translate_to != "EN":
        translated_audio = _translate(
            translate_to, deepl_apikey, transcribed_audio, initial_prompt
        )

        click.echo(f"Exporting translated files to {output_directory}")

        export_subtitles(
            output_directory.joinpath(f"{translate_to}_{input_file.name}"),
            translated_audio,
            output_format,
        )
