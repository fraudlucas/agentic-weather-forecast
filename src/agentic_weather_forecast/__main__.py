from datetime import datetime

from agentic_weather_forecast.graph.workflow import build_graph


def main():
    graph = build_graph()
    today = datetime.today().strftime("%Y-%m-%d")

    inputs = {
        "messages": [
            ("user", f"What is the weather in Recife on {today}?"),
            ("user", f"Would it be warmer in João Pessoa?"),
        ]
    }

    for state in graph.stream(inputs, stream_mode="values"):
        last_message = state["messages"][-1]
        last_message.pretty_print()


if __name__ == "__main__":
    main()
