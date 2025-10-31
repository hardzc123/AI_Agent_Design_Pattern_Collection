from demos.gradio_interface import create_app


demo = create_app()


def main() -> None:
    demo.launch()


if __name__ == "__main__":
    main()
