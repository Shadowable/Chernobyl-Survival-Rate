import math
import os
from typing import Any

import requests
import streamlit as st


DEFAULT_API_BASE_URL = os.environ.get(
    "API_BASE_URL", "http://127.0.0.1:5002"
).rstrip("/")

DEMO_NOTICE = (
    "This is a fictional interface demo. Its score is made up and is not a "
    "survival probability, medical assessment, risk estimate, or safety guidance."
)


def request_demo_index(api_base_url: str, inputs: dict[str, Any]) -> float:
    response = requests.post(
        f"{api_base_url.rstrip('/')}/predict",
        json=inputs,
        timeout=(3, 30),
    )
    response.raise_for_status()

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise ValueError("The API returned an invalid JSON response.") from error

    demo_index = result.get("demo_index") if isinstance(result, dict) else None
    if (
        isinstance(demo_index, bool)
        or not isinstance(demo_index, (int, float))
        or not math.isfinite(float(demo_index))
    ):
        raise ValueError("The API response did not contain a valid demo index.")
    return float(demo_index)


def main() -> None:
    st.set_page_config(
        page_title="Chernobyl Scenario Lab",
        page_icon="☢️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(ellipse at 12% 0%, #243d35 0%, transparent 36%),
                linear-gradient(160deg, #101916 0%, #151d1a 52%, #202721 100%);
            color: #edf2e8;
        }
        [data-testid="stHeader"] { background: transparent; }
        .block-container { max-width: 1080px; padding-top: 2rem; }
        .hero {
            padding: 2.2rem 2.4rem;
            border: 1px solid #536345;
            border-radius: 22px;
            background: linear-gradient(115deg, #202e27, #30362a);
            margin-bottom: 1.4rem;
        }
        .eyebrow {
            color: #c5d58a;
            text-transform: uppercase;
            letter-spacing: .16em;
            font-size: .75rem;
            font-weight: 700;
        }
        .hero h1 {
            color: #f3f4e8;
            font-size: clamp(2rem, 5vw, 3.2rem);
            line-height: 1.08;
            margin: .55rem 0;
        }
        .hero p { color: #c8d0c3; font-size: 1.05rem; margin-bottom: 0; }
        .notice {
            border: 1px solid #d5a840;
            border-left: 5px solid #e4b54e;
            border-radius: 12px;
            background: #302b1d;
            color: #f3e7c7;
            padding: 1rem 1.2rem;
            margin: 1rem 0 1.5rem;
        }
        div[data-testid="stForm"] {
            border: 1px solid #465148;
            border-radius: 18px;
            background: rgba(31, 41, 35, .9);
            padding: 1.2rem 1.5rem;
        }
        div[data-testid="stFormSubmitButton"] button {
            border: 0;
            border-radius: 10px;
            background: #c7d879;
            color: #172019;
            font-weight: 700;
            min-height: 3rem;
        }
        .result-card {
            border: 1px solid #687455;
            border-radius: 16px;
            background: #263129;
            padding: 1.25rem 1.5rem;
            margin-top: 1rem;
        }
        .result-label {
            color: #c5d58a;
            font-size: .8rem;
            letter-spacing: .12em;
            text-transform: uppercase;
        }
        .result-value {
            color: #f3f4e8;
            font-size: 2.7rem;
            font-weight: 750;
            margin: .25rem 0;
        }
        div[data-testid="stCaptionContainer"] { color: #b6c0b5; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <section class="hero">
          <div class="eyebrow">Historical scenario · interface demo</div>
          <h1>Chernobyl Scenario Lab</h1>
          <p>Explore how a few scenario inputs change a fictional demo index.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="notice"><strong>Important:</strong> {DEMO_NOTICE} '
        "Radiation readings and distance alone cannot determine a person's safety."
        "</div>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("API connection")
        api_base_url = st.text_input(
            "Flask API base URL",
            value=DEFAULT_API_BASE_URL,
            help="The Flask API must be running and reachable from this machine.",
        ).strip().rstrip("/")

    with st.form("scenario_inputs"):
        st.subheader("Scenario inputs")
        first_row = st.columns(2)
        with first_row[0]:
            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=35,
                step=1,
                help="Age in years. This demo input is not a clinical factor assessment.",
            )
        with first_row[1]:
            distance_km = st.number_input(
                "Distance from reactor (km)",
                min_value=0.0,
                max_value=1000.0,
                value=10.0,
                step=1.0,
                help="Straight-line distance entered for the fictional scenario.",
            )

        second_row = st.columns(2)
        with second_row[0]:
            physical_ability = st.slider(
                "Physical ability",
                min_value=1,
                max_value=10,
                value=5,
                help="An arbitrary interface-demo setting, not a medical measure.",
            )
            st.caption("1 = Low · 10 = High")
        with second_row[1]:
            dose_rate_usv_h = st.number_input(
                "Ambient dose rate (µSv/h)",
                min_value=0.0,
                max_value=1_000_000.0,
                value=0.0,
                step=1.0,
                help=(
                    "Enter a measured dose rate in microsieverts per hour. "
                    "This demo does not interpret measurements."
                ),
            )

        submitted = st.form_submit_button(
            "Generate fictional demo index", type="primary", use_container_width=True
        )

    if submitted:
        if not api_base_url:
            st.error("Enter the Flask API base URL in the sidebar.")
            return

        scenario = {
            "age": age,
            "distance_km": distance_km,
            "physical_ability": physical_ability,
            "dose_rate_usv_h": dose_rate_usv_h,
        }
        try:
            demo_index = request_demo_index(api_base_url, scenario)
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to Flask. Start the API and check its URL.")
        except requests.exceptions.Timeout:
            st.error("The Flask API did not respond in time. Please try again.")
        except requests.exceptions.HTTPError as error:
            if error.response is not None and error.response.status_code == 400:
                st.error(
                    "The API rejected the new input format. Stop the old Flask "
                    "server and restart it with `python app.py`."
                )
            else:
                st.error(f"The Flask API returned an error: {error}")
        except requests.exceptions.RequestException as error:
            st.error(f"Could not complete the request: {error}")
        except ValueError as error:
            st.error(f"Could not read the API response: {error}")
        else:
            st.markdown(
                f"""
                <section class="result-card">
                  <div class="result-label">Fictional demo index · not a probability</div>
                  <div class="result-value">{demo_index:.1f} <span style="font-size:1.2rem">/ 100</span></div>
                  <div>{DEMO_NOTICE}</div>
                </section>
                """,
                unsafe_allow_html=True,
            )

    st.divider()
    with st.expander("How is this demo index calculated?"):
        st.write(
            "It is an invented arithmetic average of four inputs scaled to "
            "arbitrary ranges. The formula has no scientific or historical "
            "validation, does not model radiation exposure or survival, and "
            "has no meaningful interpretation. It exists only to demonstrate "
            "a form-to-API workflow."
        )
    st.caption(
        "Historical context only. For a real radiation emergency, follow "
        "official emergency-management and public-health instructions."
    )


if __name__ == "__main__":
    main()
