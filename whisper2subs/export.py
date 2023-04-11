from pathlib import Path

from whisper.utils import get_writer

from whisper2subs.transcribe import TranscribeResult


def export_subtitles(
    output_filename: Path,
    transcribed_audio: TranscribeResult,
    output_format: str = "all",
) -> None:
    writer = get_writer(output_format, str(output_filename.parent))
    writer(transcribed_audio, str(output_filename.name))
