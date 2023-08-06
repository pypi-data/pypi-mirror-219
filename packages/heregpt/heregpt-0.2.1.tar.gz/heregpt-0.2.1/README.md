# hereGPT

Your chatGPT assistant right in the Terminal

## Getting started and OpenAI key

1. Install using `pip install heregpt` (or using any other method you favor).
2. Get yourself an [OpenAI API key](https://platform.openai.com/account/api-keys).
3. Place the key in one of the following places:
   1. ~/config/heregpt with the key `OPENAI_API_KEY`
   2. Set the environment variable `OPENAI_API_KEY`
   3. Use the global option `openai-key`. For example: `heregpt --openai-key "my-great-key-12jd33`
   4. When you're in DEV mode, you can also place the key in a `.env` file. It should be with the key `OPENAI_API_KEY`
