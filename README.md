[![PyPI](https://img.shields.io/pypi/v/whisper2subs?style=flat-square)](https://pypi.org/project/whisper2subs/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/whisper2subs?style=flat-square)](https://pypi.org/project/whisper2subs/)
[![PyPI - License](https://img.shields.io/pypi/l/whisper2subs?style=flat-square)](https://github.com/LuqueDaniel/whisper2subs/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black?style=flat-square)

# whisper2subs

A CLI tool that transcribes audio using [`openai-whisper`](https://github.com/openai/whisper) and translates it using [DeepL](https://www.deepl.com/docs-api).

## Install

```shell
pip install --user whisper2subs
```

## Usage

```shell
whisper2subs --help
```

### Translate

In order to perform translations into languages **other than English**, it's required to **provide an API key from DeepL**. Using the `--deepl-apikey` option or with the `DEEPL_APIKEY` environment variable. You can [**create a free account**](https://www.deepl.com/en/pro?cta=header-pro-button/) to get an API key.

Transcribe and then translate to Spanish the audio of an mp4 file, using the `large-v2` model.

```shell
whisper2subs -m large-v2 -t es --deepl-apikey "yout-api-key" input.mp4 subs/
```

If the language of the input file is not specified Whisper will try to detect it. To specify the language of the input file, use the `-l` option.

```shell
whisper2subs -l ja -m large-v2 -t es --deepl-apikey "yout-api-key" input.mp4 subs/
```

Change output format to `str` only:

```shell
whisper2subs -l ja -t es --output-format srt --deepl-apikey "yout-api-key" input.mp4 subs/
```

For more information:

```shell
whisper2subs --help
```

### Transcribe

Transcribe audio without translating it:

```shell
whisper2subs input.mp4 text/
```

## References

* [Whisper](https://github.com/openai/whisper)
* [DeepL API reference](https://www.deepl.com/docs-api)
* [`deepl-python`](https://github.com/DeepLcom/deepl-python)
