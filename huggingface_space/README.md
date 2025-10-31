# Hugging Face Space Deployment

To deploy this project on Hugging Face Spaces:

1. Create a new Space and choose the **Gradio** SDK.
2. Upload the contents of this repository, or configure GitHub integration.
3. Add the following secrets as needed for LLM access:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `AZURE_OPENAI_API_KEY`
4. Ensure `huggingface_space/requirements.txt` is referenced by the Space (default when copying this folder).
5. Set the entrypoint to `huggingface_space/app.py`.
6. Launch the Space; it will boot the Gradio interface defined in `demos/gradio_interface.py`.

The interface defaults to the deterministic mock LLM for reproducible demos. Supplying API keys enables live LLM calls without code changes.
